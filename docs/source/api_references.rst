API Reference
=============

.. currentmodule:: ramp

**************
Use Case class
**************

.. autosummary::
    :toctree: api_document/

    UseCase.__init__
    UseCase.add_user
    UseCase.save
    UseCase.export_to_dataframe
    UseCase.load
    UseCase.collect_appliances_from_users
    UseCase.initialize
    UseCase.calc_peak_time_range
    UseCase.generate_daily_load_profiles
    UseCase.generate_daily_load_profiles_parallel
    UseCase.date_start
    UseCase.date_end
    UseCase.peak_enlarge
    UseCase.num_days
    UseCase.datetimeindex


**********
User class
**********

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



***************
Appliance class
***************

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




*********
Utilities
*********

.. autosummary::
    :toctree: api_document/

    load_data
    download_example
    ramp_py2xlsx


*************
Visualization
*************

.. autosummary::
    :toctree: api_document/

    Plot.__init__
    Plot.from_file
    Plot.freq
    Plot.columns
    Plot.index
    Plot.resample
    Plot.line
    Plot.shadow
    Plot.area
    Plot.load_duration_curve
    Plot.error
    Plot.peak
    Plot.DataFrame
    Plot.add_column
    Plot.loc
    Plot.head
    Plot.plot
    Plot.to_excel
    Plot.to_csv
    Plot.mean
    Plot.sum