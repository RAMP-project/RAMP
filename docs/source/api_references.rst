API Reference
==============

.. currentmodule:: ramp

**********************
Use Case class
**********************

.. autosummary::
    :toctree: api_document/

    UseCase.__init__
    UseCase.add_user
    UseCase.save
    UseCase.export_to_dataframe
    UseCase.load


**********************
User class
**********************

.. autosummary::
    :toctree: api_document/

    User.__init__
    User.add_appliance
    User.save
    User.export_to_dataframe
    User.Appliance
    User.generate_single_load_profile
    User.generate_aggregated_load_profile
    User.maximum_profile



******************
Appliance class
******************

.. autosummary::
    :toctree: api_document/

    Appliance.__init__
    Appliance.save
    Appliance.export_to_dataframe
    Appliance.windows
    Appliance.specific_cycle
    Appliance.specific_cycle_1
    Appliance.specific_cycle_2
    Appliance.specific_cycle_3
    Appliance.cycle_behaviour
    Appliance.maximum_profile
    Appliance.__eq__


****

******************
Utilities
******************

.. autosummary::
    :toctree: api_document/

    yearly_pattern
    calc_peak_time_range