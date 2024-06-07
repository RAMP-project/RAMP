import pytest

from ramp import User, Appliance


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
