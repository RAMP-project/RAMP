# -*- coding: utf-8 -*-

#%% Import required libraries
import numpy as np
import numpy.ma as ma
import pandas as pd
import warnings
from ramp.core.constants import NEW_TO_OLD_MAPPING, APPLIANCE_ATTRIBUTES, APPLIANCE_ARGS, WINDOWS_PARAMETERS, MAX_WINDOWS, DUTY_CYCLE_PARAMETERS
from ramp.core.utils import read_input_file

#%% Definition of Python classes that constitute the model architecture
"""
The code is based on UseCase, User and Appliance classes.
A UseCase instance consists of a list of User instances which own Appliance instances
Within the Appliance class, some other functions are created to define windows of use and, 
if needed, specific duty cycles
"""


class UseCase:
    def __init__(self, name="", users=None):
        self.name = name
        if users is None:
            users = []
        self.users = users

    def add_user(self, user):
        if isinstance(user, User):
            self.users.append(user)

    def save(self, filename=None):
        answer = pd.concat([user.save() for user in self.users], ignore_index=True)
        if filename is not None:
            answer.to_excel(f"{filename}.xlsx", index=False, engine="openpyxl")
        else:
            return answer

    def export_to_dataframe(self):
        return self.save()

    def load(self, filename):
        """Open an .xlsx file which was produces via the save method and create instances of Users and Appliances"""

        df = read_input_file(filename=filename)
        for user_name in df.user_name.unique():
            user_df = df.loc[df.user_name == user_name]
            num_users = user_df.num_users.unique()
            if len(num_users) == 1:
                num_users = num_users[0]
            else:
                raise ValueError(
                    "'num_users' should be the same for a given user profile"
                )
            user_preference = user_df.user_preference.unique()
            if len(user_preference) == 1:
                user_preference = user_preference[0]
            else:
                raise ValueError(
                    "'user_preference' should be the same for a given user profile"
                )

            # create user and add it to usecase
            user = User(user_name, num_users, user_preference)
            self.add_user(user)
            # itereate through the lines of the DataFrame, each line representing one Appliance instance
            for row in user_df.loc[
                :, ~user_df.columns.isin(["user_name", "num_users", "user_preference"])
            ].to_dict(orient="records"):
                # assign Appliance arguments
                appliance_parameters = {k: row[k] for k in APPLIANCE_ARGS}

                # assign windows arguments
                for k in WINDOWS_PARAMETERS:
                    if "window" in k:
                        w_start = row.get(k + "_start", np.NaN)
                        w_end = row.get(k + "_end", np.NaN)
                        if not np.isnan(w_start) and not np.isnan(w_end):
                            appliance_parameters[k] = np.array(
                                [w_start, w_end], dtype=np.intc
                            )
                    else:
                        val = row.get(k, np.NaN)
                        if not np.isnan(val):
                            appliance_parameters[k] = val

                # assign duty cycles arguments
                for duty_cycle_params in DUTY_CYCLE_PARAMETERS:
                    for k in duty_cycle_params:
                        if "cw" in k:
                            cw_start = row.get(k + "_start", np.NaN)
                            cw_end = row.get(k + "_end", np.NaN)
                            if not np.isnan(cw_start) and not np.isnan(cw_end):
                                appliance_parameters[k] = np.array(
                                    [cw_start, cw_end], dtype=np.intc
                                )
                        else:
                            val = row.get(k, np.NaN)
                            if not np.isnan(val):
                                appliance_parameters[k] = val

                user.add_appliance(**appliance_parameters)



class User:
    def __init__(self, user_name="", num_users=1, user_preference=0):
        self.user_name = user_name
        self.num_users = num_users  # specifies the number of users within the class
        self.user_preference = user_preference  # allows to check if random number coincides with user preference, to distinguish between various appliance_use options (e.g. different cooking options)
        self.App_list = (
            []
        )  # each instance of User (i.e. each user class) has its own list of Appliances

    def add_appliance(self, *args, **kwargs):

        # parse the args into the kwargs
        if len(args) > 0:
            for a_name, a_val in zip(APPLIANCE_ARGS, args):
                kwargs[a_name] = a_val

        # collects windows arguments
        windows_args = {}
        for k in WINDOWS_PARAMETERS:
            if k in kwargs:
                windows_args[k] = kwargs.pop(k)

        # collects duty cycles arguments
        duty_cycle_parameters = {}
        for i, duty_cycle_params in enumerate(DUTY_CYCLE_PARAMETERS):
            cycle_parameters = {}
            for k in duty_cycle_params:
                if k in kwargs:
                    cycle_parameters[k] = kwargs.pop(k)
            if cycle_parameters:
                duty_cycle_parameters[i+1] = cycle_parameters

        app = Appliance(self, **kwargs)

        if windows_args:
            app.windows(**windows_args)
        for i in duty_cycle_parameters:
            app.specific_cycle(i, **duty_cycle_parameters[i])

        return app

    def save(self, filename=None):
        answer = pd.concat([app.save() for app in self.App_list], ignore_index=True)
        if filename is not None:
            answer.to_excel(f"{filename}.xlsx", engine="openpyxl")
        else:
            return answer

    def __eq__(self, other_user):
        """Compare two users

        ensure they have the same properties
        ensure they have the same appliances
        """
        answer = np.array([])
        for attribute in ("user_name", "num_users", "user_preference"):
            if hasattr(self, attribute) and hasattr(other_user, attribute):
                np.append(
                    answer, [getattr(self, attribute) == getattr(other_user, attribute)]
                )
            else:
                print(f"Problem with {attribute} of user")
                np.append(answer, False)
        answer = answer.all()

        if answer is True:
            # user attributes match, continue to compare each appliance
            if len(self.App_list) == len(other_user.App_list):
                answer = np.array([])
                for my_appliance, their_appliance in zip(
                    self.App_list, other_user.App_list
                ):
                    temp = my_appliance == their_appliance
                    answer = np.append(answer, temp)
                if len(answer) > 0:
                    answer = answer.all()
                else:

                    if len(self.App_list) > 0:
                        answer = False
                    else:
                        # both users have no appliances
                        answer = True
            else:
                print(
                    f"The user {self.user_name} and {other_user.user_name} do not have the same number of appliances"
                )
                answer = False
        return answer

    def export_to_dataframe(self):
        return self.save()

    def Appliance(
        self,
        user,
        n=1,
        P=0,
        w=1,
        t=0,
        r_t=0,
        c=1,
        fixed="no",
        fixed_cycle=0,
        occasional_use=1,
        flat="no",
        thermal_P_var=0,
        pref_index=0,
        wd_we_type=2,
        P_series=False,
        name="",
    ):
        """Back-compatibility with legacy code"""
        return self.add_appliance(
            number=n,
            power=P,
            num_windows=w,
            func_time=t,
            time_fraction_random_variability=r_t,
            func_cycle=c,
            fixed=fixed,
            fixed_cycle=fixed_cycle,
            occasional_use=occasional_use,
            flat=flat,
            thermal_p_var=thermal_P_var,
            pref_index=pref_index,
            wd_we_type=wd_we_type,
            p_series=P_series,
            name=name,
        )


class Appliance:
    def __init__(
        self,
        user,
        number=1,
        power=0,
        num_windows=1,
        func_time=0,
        time_fraction_random_variability=0,
        func_cycle=1,
        fixed="no",
        fixed_cycle=0,
        occasional_use=1,
        flat="no",
        thermal_p_var=0,
        pref_index=0,
        wd_we_type=2,
        p_series=False,
        name="",
    ):
        self.user = user  #user to which the appliance is bounded
        self.name = name
        self.number = number  #number of appliances of the specified kind
        self.num_windows = num_windows  #number of functioning windows to be considered
        self.func_time = func_time  #total time the appliance is on during the day
        self.time_fraction_random_variability = time_fraction_random_variability  #percentage of total time of use that is subject to random variability
        self.func_cycle = (
            func_cycle  #minimum time the appliance is kept on after switch-on event
        )
        self.fixed = fixed  #if 'yes', all the 'n' appliances of this kind are always switched-on together
        self.fixed_cycle = fixed_cycle  #if equal to 1,2 or 3, respectively 1,2 or 3 duty cycles can be modelled, for different periods of the day
        self.occasional_use = occasional_use  #probability that the appliance is always (i.e. everyday) included in the mix of appliances that the user actually switches-on during the day
        self.flat = flat  #allows to model appliances that are not subject to any kind of random variability, such as public lighting
        self.thermal_p_var = (
            thermal_p_var  #allows to randomly variate the App power within a range
        )
        self.pref_index = pref_index  #defines preference index for association with random User daily preference behaviour
        self.wd_we_type = wd_we_type  #defines if the App is associated with weekdays or weekends | 0 is wd 1 is we 2 is all week
        if p_series is True:
            if isinstance(power, str):
                power = pd.read_json(power)
            if not isinstance(power, pd.DataFrame):
                raise(ValueError("The input power is excepted to be a series but it is not recognized as such"))
            self.power = power.values[:, 0]  #if a timeseries is given the power is treated as so
        else:
            self.power = power * np.ones(365)  # treat the power as single value for the entire year

        # attributes initialized by self.windows
        self.random_var_w = 0
        self.window_1 = np.array([0, 0])
        self.window_2 = np.array([0, 0])
        self.window_3 = np.array([0, 0])
        self.random_var_1 = 0
        self.random_var_2 = 0
        self.random_var_3 = 0
        self.daily_use = None
        self.daily_use_masked = None

        # attributes used for specific fixed and random cycles
        self.p_11 = 0
        self.p_12 = 0
        self.t_11 = 0
        self.t_12 = 0
        self.r_c1 = 0
        self.p_21 = 0
        self.p_22 = 0
        self.t_21 = 0
        self.t_22 = 0
        self.r_c2 = 0
        self.p_31 = 0
        self.p_32 = 0
        self.t_31 = 0
        self.t_32 = 0
        self.r_c3 = 0

        # attribute used for cycle_behaviour
        self.cw11 = np.array([0, 0])
        self.cw12 = np.array([0, 0])
        self.cw21 = np.array([0, 0])
        self.cw22 = np.array([0, 0])
        self.cw31 = np.array([0, 0])
        self.cw32 = np.array([0, 0])

        self.random_cycle1 = np.array([])
        self.random_cycle2 = np.array([])
        self.random_cycle3 = np.array([])

    def save(self):
        dm = {}
        for user_attribute in ("user_name", "num_users", "user_preference"):
            dm[user_attribute] = getattr(self.user, user_attribute)
        for attribute in APPLIANCE_ATTRIBUTES:

            if hasattr(self, attribute):
                if "window_" in attribute or "cw" in attribute:
                    window_value = getattr(self, attribute)
                    dm[attribute + "_start"] = window_value[0]
                    dm[attribute + "_end"] = window_value[1]
                elif attribute == "power":
                    power_values = getattr(self, attribute)
                    if np.diff(power_values).sum() == 0:
                        power_values = power_values[0]
                    else:
                        power_values = power_values.tolist()
                    dm[attribute] = power_values
                else:
                    dm[attribute] = getattr(self, attribute)
            else:
                # this is for legacy purpose, so that people can export their old models to new format
                old_attribute = NEW_TO_OLD_MAPPING.get(attribute,attribute)
                if hasattr(self, old_attribute):
                    if "window_" in attribute or "cw" in attribute:
                        window_value = getattr(self, old_attribute)
                        dm[attribute + "_start"] = window_value[0]
                        dm[attribute + "_end"] = window_value[1]
                    elif old_attribute == "POWER":
                        power_values = getattr(self, old_attribute)
                        if np.diff(power_values).sum() == 0:
                            power_values = power_values[0]
                        else:
                            power_values = power_values.tolist()
                        dm[attribute] = power_values
                    else:
                        dm[attribute] = getattr(self, old_attribute)
                else:
                    if "cw" in old_attribute:
                        dm[attribute + "_start"] = None
                        dm[attribute + "_end"] = None
                    else:
                        dm[attribute] = None
        return pd.DataFrame.from_records([dm])

    def export_to_dataframe(self):
        return self.save()

    def __eq__(self, other_appliance):
        """Compare two appliances

        ensure they have the same attributes
        ensure all their attributes have the same value
        """
        answer = np.array([])
        for attribute in APPLIANCE_ATTRIBUTES:
            if hasattr(self, attribute) and hasattr(other_appliance, attribute):
                np.append(
                    answer,
                    [getattr(self, attribute) == getattr(other_appliance, attribute)],
                )
            elif (
                hasattr(self, attribute) is False
                and hasattr(other_appliance, attribute) is False
            ):
                np.append(answer, True)
            else:
                if hasattr(self, attribute) is False:
                    print(f"{attribute} of appliance {self.name} is not assigned")
                else:
                    print(
                        f"{attribute} of appliance {other_appliance.name} is not assigned"
                    )
                np.append(answer, False)
        return answer.all()

    def windows(self, window_1=None, window_2=None, random_var_w=0, window_3=None):
        if window_1 is None:
            warnings.warn(UserWarning("No windows is declared, default window of 24 hours is selected"))
            self.window_1 = np.array([0, 1440])
        else:
            self.window_1 = window_1

        if window_2 is None:
            if self.num_windows >= 2:
                raise ValueError("Windows 2 is not provided although 2 windows were declared")
        else:
            self.window_2 = window_2

        if window_3 is None:
            if self.num_windows == 3:
                raise ValueError("Windows 3 is not provided although 3 windows were declared")
        else:
            self.window_3 = window_3

        # check that the time allocated by the windows is larger or equal to the func_time of the appliance
        window_time = 0
        for i in range(1, self.num_windows + 1, 1):
            window_time = window_time + np.diff(getattr(self, f"window_{i}"))[0]
        if window_time < self.func_time:
            raise ValueError(f"The sum of all windows time intervals for the appliance '{self.name}' of user '{self.user.user_name}' is smaller than the time the appliance is supposed to be on ({window_time} < {self.func_time}). Please check your input file for typos.")

        self.random_var_w = random_var_w #percentage of variability in the start and ending times of the windows
        self.daily_use = np.zeros(1440) #create an empty daily use profile
        self.daily_use[self.window_1[0]:(self.window_1[1])] = np.full(np.diff(self.window_1),0.001) #fills the daily use profile with infinitesimal values that are just used to identify the functioning windows
        self.daily_use[self.window_2[0]:(self.window_2[1])] = np.full(np.diff(self.window_2),0.001) #same as above for window2
        self.daily_use[self.window_3[0]:(self.window_3[1])] = np.full(np.diff(self.window_3),0.001) #same as above for window3
        self.daily_use_masked = np.zeros_like(ma.masked_not_equal(self.daily_use,0.001)) #apply a python mask to the daily_use array to make only functioning windows 'visibile'
        self.random_var_1 = int(random_var_w*np.diff(self.window_1)) #calculate the random variability of window1, i.e. the maximum range of time they can be enlarged or shortened
        self.random_var_2 = int(random_var_w*np.diff(self.window_2)) #same as above
        self.random_var_3 = int(random_var_w*np.diff(self.window_3)) #same as above
        self.user.App_list.append(self) #automatically appends the appliance to the user's appliance list

        if self.fixed_cycle == 1:
            self.cw11 = self.window_1
            self.cw12 = self.window_2

    def specific_cycle(self, cycle_num, **kwargs):
        if cycle_num == 1:
            self.specific_cycle_1(**kwargs)
        elif cycle_num == 2:
            self.specific_cycle_2(**kwargs)
        elif cycle_num == 3:
            self.specific_cycle_3(**kwargs)

        #if needed, specific duty cycles can be defined for each Appliance, for a maximum of three different ones
    def specific_cycle_1(self, p_11 = 0, t_11 = 0, p_12 = 0, t_12 = 0, r_c1 = 0, cw11=None, cw12=None):
        self.p_11 = p_11 #power absorbed during first part of the duty cycle
        self.t_11 = int(t_11) #duration of first part of the duty cycle
        self.p_12 = p_12 #power absorbed during second part of the duty cycle
        self.t_12 = int(t_12) #duration of second part of the duty cycle
        self.r_c1 = r_c1 #random variability of duty cycle segments duration
        if cw11 is not None:
            self.cw11 = cw11
        if cw12 is not None:
            self.cw12 = cw12
        # Below is not used
        self.fixed_cycle1 = np.concatenate(((np.ones(self.t_11)*p_11),(np.ones(self.t_12)*p_12))) #create numpy array representing the duty cycle

    def specific_cycle_2(self, p_21 = 0, t_21 = 0, p_22 = 0, t_22 = 0, r_c2 = 0, cw21=None, cw22=None):
        self.p_21 = p_21 #same as for cycle1
        self.t_21 = int(t_21)
        self.p_22 = p_22
        self.t_22 = int(t_22)
        self.r_c2 = r_c2
        if cw21 is not None:
            self.cw21 = cw21
        if cw22 is not None:
            self.cw22 = cw22
        # Below is not used
        self.fixed_cycle2 = np.concatenate(((np.ones(self.t_21)*p_21),(np.ones(self.t_22)*p_22)))

    def specific_cycle_3(self, p_31 = 0, t_31 = 0, p_32 = 0, t_32 = 0, r_c3 = 0, cw31=None, cw32=None):
        self.p_31 = p_31 #same as for cycle1
        self.t_31 = int(t_31)
        self.p_32 = p_32
        self.t_32 = int(t_32)
        self.r_c3 = r_c3
        if cw31 is not None:
            self.cw31 = cw31
        if cw32 is not None:
            self.cw32 = cw32
        # Below is not used
        self.fixed_cycle3 = np.concatenate(((np.ones(self.t_31)*p_31),(np.ones(self.t_32)*p_32)))

    #different time windows can be associated with different specific duty cycles
    def cycle_behaviour(self, cw11 = np.array([0,0]), cw12 = np.array([0,0]), cw21 = np.array([0,0]), cw22 = np.array([0,0]), cw31 = np.array([0,0]), cw32 = np.array([0,0])):

        # only used around line 223
        self.cw11 = cw11 #first window associated with cycle1
        self.cw12 = cw12 #second window associated with cycle1
        self.cw21 = cw21 #same for cycle2
        self.cw22 = cw22
        self.cw31 = cw31 #same for cycle 3
        self.cw32 = cw32

