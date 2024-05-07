import pytest
from ramp import User, Appliance


@pytest.fixture
def test_user():
    # Create a User instance (you may need to provide the required arguments for User)
    user = User(user_name="Test User", num_users=1)
    return user


@pytest.mark.usefixtures("test_user")
def test_compare_two_appliances(test_user):
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

    appliance3 = Appliance(
        test_user,
        name="test_appliance1",
        func_time=4 * 60,  # runs for 4 hours per day
    )

    assert appliance1 != appliance2
    assert appliance1 == appliance3
