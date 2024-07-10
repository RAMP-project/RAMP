import pytest

from ramp import UseCase, User, Appliance
from ramp.example.input_file_1 import User_list
from copy import deepcopy


@pytest.fixture
def test_user():
    # Create a User instance (you may need to provide the required arguments for User)
    user = User(user_name="Test User", num_users=1)
    return user


@pytest.mark.usefixtures("test_user")
def test_add_several_appliances_to_user(test_user):
    assert len(test_user.App_list) == 0
    appliance1 = Appliance(
        test_user,
        name="test_appliance1",
        func_time=4 * 60,  # runs for 4 hours per day
    )
    appliance2 = Appliance(
        test_user,
        name="test_appliance2",
        func_time=4 * 60,  # runs for 4 hours per day
    )
    test_user.add_appliance(appliance1, appliance2)
    assert len(test_user.App_list) == 2


@pytest.mark.usefixtures("test_user")
def test_skip_add_existing_appliances_to_user(test_user):
    assert len(test_user.App_list) == 0
    appliance1 = Appliance(
        test_user,
        name="test_appliance1",
        func_time=4 * 60,  # runs for 4 hours per day
    )
    test_user.add_appliance(appliance1)

    assert len(test_user.App_list) == 1

    test_user.add_appliance(appliance1)

    assert len(test_user.App_list) == 1


def test_random_seed_initialization():
    # Build use case 2 and fixed random seed
    uc_1 = UseCase(
        users=deepcopy(User_list),
        random_seed=1,
        date_start="2020-01-01",
        date_end="2020-01-01",
    )
    # Initialize and generate load profile
    uc_1.initialize(peak_enlarge=0.15, num_days=1)
    uc_1_lp = uc_1.generate_daily_load_profiles()

    # Build use case 2 and same fixed random seed as uc_1
    uc_2 = UseCase(users=deepcopy(User_list), random_seed=1)

    # Initialize and generate load profile
    uc_2.initialize(peak_enlarge=0.15, num_days=1)
    uc_2_lp = uc_2.generate_daily_load_profiles()

    assert (uc_1_lp - uc_1_lp == 0).all()
