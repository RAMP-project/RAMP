Model Parameters
================

Excel input file parameter description
--------------------------------------

The table below displays the input parameters of RAMP. If **NA** is displayed in the table below, it means that the corresponding column is not applicable to the parameter.

When filling an .xlsx input file, you can simply leave the cell empty if the parameter is not mandatory. In this case, the default value will be automatically used.

The **"allowed values"** column provide information about the format one should provide. For example:

- {1,2,3} is a set and the allowed value are either 1, 2 or 3;
- in [0-1440] is a range and the allowed value must lie between 0 and 1440. 0 and 1440 are also possible values.

.. list-table:: Parameters
   :widths: 20 15 20 150 10 10 10
   :header-rows: 1

   * - Name
     - Unit
     - Allowed values
     - Description
     - Coding type
     - Is this value mandatory?
     - Default value
   * - user_name
     - NA
     - NA
     - Name of user type
     - string
     - yes
     - NA
   * - num_users
     - NA
     - >=0
     - Number of users within the resprective user-type
     - integer
     - yes
     - 0
   * - user_preference
     - NA
     - {0,1,2,3}
     - Related to cooking behaviour, how many types of meal a user wants a day (number of user preferences has to be defined here and will be further specified with pref_index parameter)
     - integer
     - no
     - 0
   * - name
     - NA
     - NA
     - Appliance name
     - string
     - yes
     - NA
   * - number
     - NA
     - >=0
     - Number of appliances
     - integer
     - yes
     - 0
   * - power
     - Watt
     - >=0
     - Power rating of appliance (average)
     - Float or array
     - yes
     - 0
   * - num_windows
     - NA
     - {1,2,3}
     - Number of distinct time windows, e.g. if an appliance is running 24 h the num_windows is 1. If num_windows is set to x then you have to fill in the window_x_start, window_x_end and random_var_w parameters)
     - integer
     - yes
     - 1
   * - func_time
     - minutes
     - in [0,1440]
     - Total time an appliance is running in a day (not dependant on windows)
     - integer
     - yes
     - 0
   * - time_fraction_random_variability
     - %
     - in [0,1]
     - For time (not for windows), randomizes the total time the appliance is on
     - float
     - no
     - 0
   * - func_cycle
     - minutes
     - in [0,1440]
     - Running time: time the appliance is on (after switching it on)
     - float
     - yes
     - 1
   * - fixed
     - NA
     - {yes,no}
     - All appliances of the same kind (e.g. street lights) are switched on at the same time (if fixed=yes)
     - boolean
     - no
     - 1
   * - fixed_cycle
     - NA
     - {0,1,2,3}
     - Number of duty cycle, 0 means continuous power, if not 0 you have to fill the cw (cycle window) parameter (you may define up to 3 cws)
     - integer
     - no
     - 0
  * - continuous_use_duty_cycle
     - NA
     - {0,1}
     - Duty cycle mode, 0 triggers once per switch-on event, 1 let the duty cycle repeat during the entire switch-on event
     - integer
     - no
     - 1
   * - occasional_use
     - %
     - in [0,1]
     - Defines how often the appliance is used, e.g. every second day will be 0.5
     - float
     - no
     - 1
   * - flat
     - NA
     - {yes,no}
     - No variability in the time of usage, similar to fixed, and no variability in the power consumption
     - boolean
     - no
     - no
   * - thermal_p_var
     - %
     - in [0,1]
     - Range of change of the power of the appliance (e.g. shower not taken at same temparature) or for the power of duty cycles (e.g. for a cooker, AC, heater if external temperature is different…)
     - float
     - no
     - 0
   * - pref_index
     - NA
     - {0,1,2,3}
     - This number must be smaller or equal to the value input in user_preference
     - integer
     - no
     - 0
   * - wd_we_type
     - NA
     - {0,1,2}
     - Specify whether the appliance is used only on weekdays (0), weekend (1) or the whole week (2)
     - integer
     - no
     - 2
   * - p_i1
     - Watt
     - >=0
     - Power rating for first part of ith duty cycle. Only necessary if fixed_cycle is set to 1 or greater
     - float
     - no
     - 0
   * - t_i1
     - minutes
     - in [0,1440]
     - Duration of first part of ith duty cycle. Only necessary if fixed_cycle is set to 1 or greater
     - float
     - no
     - 0
   * - cwi1_start
     - minutes
     - in [0,1440]
     - Window start time for the first part of ith specific duty cycle number (not neccessarily linked to the overall time window)
     - float
     - no
     - 0
   * - cwi1_end
     - minutes
     - in [0,1440]
     - Window end time for the first part of ith specific duty cycle number (not neccessarily linked to the overall time window)
     - float
     - no
     - 0
   * - p_i2
     - Watt
     - >=0
     - Power rating for second part of ith duty cycle number. Only necessary if fixed_cycle is set to i or greater
     - float
     - no
     - 0
   * - t_i2
     - minutes
     - in [0,1440]
     - Duration second part of ith duty cycle number. Only necessary if fixed_cycle is set to I or greater
     - float
     - no
     - 0
   * - cwi2_start
     - minutes
     - in [0,1440]
     - Window start time for the second part of ith duty cycle number (not neccessarily linked to the overall time window)
     - float
     - no
     - 0
   * - cwi2_end
     - minutes
     - in [0,1440]
     - Window end time for the second part of ith duty cycle number (not neccessarily linked to the overall time window)
     - float
     - no
     - 0
   * - r_ci
     - %
     - in [0,1]
     - Randomization of the duty cycle parts’ duration. There will be a uniform random variation around t_i1 and t_i2. If this parameter is set to 0.1, then t_i1 and t_i2 will be randomly reassigned between 90% and 110% of their initial value; 0 means no randomisation
     - float
     - no
     - 0
   * - window_j_start
     - minutes
     - in [0,1440]
     - Start time of time-window j. Only necessary if num_windows is set to j or greater
     - integer
     - yes
     - 0
   * - window_j_end
     - minutes
     - in [0,1440]
     - End time of time-window j. Only necessary if num_windows is set to j or greater
     - integer
     - yes
     - 0
   * - random_var_w
     - %
     - in [0,1]
     - Variability of the windows in percentage, the same for all windows
     - float
     - no
     - 0

Python input file parameter description
---------------------------------------

A new instance of class ``User`` requires the parameters ``user_name``,
``num_users``, ``user_preference`` from the table above. To add an
appliance, use the method ``add_appliance`` with at least the mandatory
parameters listed in the table above (except the first three parameters
which belong to the user class and are already assigned in this case)
and with any of the non-mandatory ones.

If no window parameter (``window_j_start``, ``window_j_end``) is
provided to the ``add_appliance`` method of the user, then one must 
call the ``windows`` method of the appliance to provide up to 3 windows
: ``window_1``, ``window_2``, ``window_3`` as well as ``random_var_w``
The parameters to describe a window of time should directly be
provided as a numpy array ( for example
``window_j = np.array([window_j_start, window_j_end])``) (where j is an
integer smaller or equal to the provided value of ``num_windows``).

If no duty cycle parameter is provided to the ``add_appliance`` method
of the user, then one can enable up to 3 different duty cycles by calling 
the method ``specific_cycle_i`` of the appliance (where i is an integer
smaller or equal to the provided value of ``fixed_cycle``) The
parameters to describe the ith duty cycle are the following: ``p_i1``,
``t_i1``, ``p_i2``, ``t_i2``, ``r_ci``, ``cwi1`` and ``cwi2``. It is also
possible to provide the parameters ``cwi1`` and ``cwi2`` using the
method ``cycle_behaviour`` of the appliance.

The legacy way to create an appliance instance is by using the
``Appliance`` method of the user (note that the names of input
parameters are the old ones). This way of creating an appliance is to
keep the backward compatibility of legacy input files: using the
``add_appliance`` method of the user should be preferred. Note that with
the legacy method, one must then call the ``windows`` method of the
appliance to provide at least one windows. And one can add duty cycles
only via the method ``specific_cycle_i`` of the appliance.

