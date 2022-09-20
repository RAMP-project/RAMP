import os
import pytest
import numpy as np

from ramp.core.core import User, Appliance
from ramp.core.initialise import initialise_inputs
e
from ramp.ramp_convert_old_input_files import convert_old_user_input_file


def load_usecase(j=None, fname=None):
    peak_enlarge, year_behaviour, user_list, num_profiles = initialise_inputs(
        j, fname, num_profiles=1
    )
    return user_list


class TestConversion:
    def setup_method(self):
        self.input_files_to_run = [1, 2, 3]
        self.file_suffix = "_test"
        os.chdir(
            "ramp"
        )  # for legacy code to work the loading of the input file has to happen from the ramp folder
        self.py_fnames = [
            os.path.join("input_files", f"input_file_{i}.py")
            for i in self.input_files_to_run
        ]
        self.xlsx_fnames = [
            os.path.join("test", f"input_file_{i}{self.file_suffix}.xlsx")
            for i in self.input_files_to_run
        ]
        for fname in self.xlsx_fnames:
            if os.path.exists(fname):
                os.remove(fname)

    def teardown_method(self):
        auto_code_proof = (
            "# Code automatically added by ramp_convert_old_input_files.py\n"
        )
        # remove created files
        for fname in self.xlsx_fnames:
            if os.path.exists(fname):
                os.remove(fname)
        # remove additional code in legacy input files to get the appliance name from python variable names
        for fname in self.py_fnames:
            with open(fname, "r") as fp:
                lines = fp.readlines()
                if auto_code_proof in lines:
                    idx = lines.index(auto_code_proof)
            with open(fname, "w") as fp:
                fp.writelines(lines[: idx - 1])

    def test_convert_py_to_xlsx(self):
        """Convert the 3 example .py input files to xlsx and compare each appliance of each user"""
        for i, j in enumerate(self.input_files_to_run):
            old_user_list = load_usecase(j=j)
            convert_old_user_input_file(
                self.py_fnames[i], output_path="test", suffix=self.file_suffix
            )
            new_user_list = load_usecase(fname=self.xlsx_fnames[i])
            for old_user, new_user in zip(old_user_list, new_user_list):
                if old_user != new_user:
                    pytest.fail()


def test_define_appliance_window_directly_equivalent_to_use_windows_method():
    user = User("test user", 1)

    params = dict(number=1, power=200, num_windows=1, func_time=0)
    win_start = 390
    win_stop = 540
    appliance1 = user.add_appliance(**params)
    appliance1.windows(window_1=[win_start, win_stop])

    params.update({"window_1": np.array([win_start, win_stop])})
    appliance2 = user.add_appliance(**params)

    assert appliance1 == appliance2


def test_define_appliance_duty_cycle_directly_equivalent_to_use_specific_cycle_method():
    user = User("test user", 1)

    params = dict(
        number=1,
        power=200,
        num_windows=1,
        func_time=0,
        window_1=[390, 540],
        fixed_cycle=1,
    )

    appliance1 = user.add_appliance(**params)
    cycle_params = {"p_11": 20, "t_11": 10, "cw11": np.array([400, 500])}
    appliance1.specific_cycle_1(**cycle_params)

    params.update(cycle_params)
    appliance2 = user.add_appliance(**params)

    assert appliance1 == appliance2


def test_provide_only_one_appliance_window_when_declaring_two():
    user = User("test user", 1)

    params = dict(number=1, power=200, num_windows=2, func_time=0)
    win_start = 390
    win_stop = 540
    with pytest.raises(ValueError):
        appliance1 = user.add_appliance(**params)
        appliance1.windows(window_1=[win_start, win_stop])
    with pytest.raises(ValueError):
        params.update({"window_1": np.array([win_start, win_stop])})
        user.add_appliance(**params)


def test_provide_no_appliance_window_when_declaring_one():
    user = User("test user", 1)

    params = dict(number=1, power=200, num_windows=1, func_time=0)
    with pytest.warns(UserWarning):
        appliance1 = user.add_appliance(**params)
        appliance1.windows()
    with pytest.warns(UserWarning):
        params.update({"window_1": None})
        user.add_appliance(**params)


def test_A():
    user = User("test user", 1)

    old_params = dict(n=1, P=200, w=1, t=0)
    win_start = 390
    win_stop = 540
    appliance1 = user.Appliance(user, **old_params)
    appliance1.windows(window_1=[win_start, win_stop])

    params = dict(number=1, power=200, num_windows=1, func_time=0, window_1=np.array([win_start, win_stop]))
    appliance2 = user.add_appliance(**params)

    assert appliance1 == appliance2

def test_B():
    user = User("test user", 1)

    params = dict(
        number=1,
        power=200,
        num_windows=1,
        func_time=0,
        window_1=[390, 540],
        fixed_cycle=1,
    )

    appliance1 = user.add_appliance(**params)
    cycle_params = {"p_11": 20, "t_11": 10, "cw11": np.array([400, 500])}
    appliance1.specific_cycle_1(**cycle_params)

    params.update(cycle_params)
    appliance2 = user.add_appliance(**params)

    assert appliance1 == appliance2