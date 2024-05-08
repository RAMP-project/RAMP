Using tabular inputs to build a model
=====================================

When the number of users or appliances is high, it can be difficult to
create a model using Python scripts. Therefore, RAMP allows you to
create inputs in tabular format (``.xlsx``). On the other hand, it is
still possible to use Python to generate a large tabular file with
default parameter values, which can then be more easily customised. In
this example, we show a possible utilisation of this functionality.

.. code:: ipython3

    from ramp import User, Appliance, UseCase, get_day_type
    import pandas as pd

As a first step, one must create ``User`` classes and assign
``Appliances`` to the user class without assigning detailed appliance
characteristics. Hence, users and their appliances are added to a
``UseCase``.

Building a tabular file populated with default data
---------------------------------------------------

.. code:: ipython3

    # Defining a dict of users with their appliances
    
    user_app = {"household": ["light", "tv"], "school": ["light", "computer"]}

.. code:: ipython3

    # creating a UseCase class to create the database
    use_case = UseCase()

.. code:: ipython3

    # assinging the appliances to users
    for user, apps in user_app.items():
        user_instance = User(user_name=user)
    
        for app in apps:
            app_instance = user_instance.add_appliance(name=app)
            app_instance.windows()
    
        use_case.add_user(user_instance)


.. parsed-literal::

    /home/fl/GitHub-repos/RAMP/ramp/core/core.py:1198: UserWarning: No windows is declared, default window of 24 hours is selected
      warnings.warn(


Once the ``Users`` and ``Appliances`` are added to the ``use_case``
instance, the model user can get a ``pd.DataFrame`` or an ``.xlsx`` file
of all the data with the default values.

Exporting the database
~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    # getting the dataframe
    use_case.export_to_dataframe()




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>user_name</th>
          <th>num_users</th>
          <th>user_preference</th>
          <th>name</th>
          <th>number</th>
          <th>power</th>
          <th>num_windows</th>
          <th>func_time</th>
          <th>time_fraction_random_variability</th>
          <th>func_cycle</th>
          <th>...</th>
          <th>cw32_start</th>
          <th>cw32_end</th>
          <th>r_c3</th>
          <th>window_1_start</th>
          <th>window_1_end</th>
          <th>window_2_start</th>
          <th>window_2_end</th>
          <th>window_3_start</th>
          <th>window_3_end</th>
          <th>random_var_w</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>household</td>
          <td>1</td>
          <td>0</td>
          <td>light</td>
          <td>1</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>...</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1440</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>household</td>
          <td>1</td>
          <td>0</td>
          <td>tv</td>
          <td>1</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>...</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1440</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>2</th>
          <td>school</td>
          <td>1</td>
          <td>0</td>
          <td>light</td>
          <td>1</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>...</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1440</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>school</td>
          <td>1</td>
          <td>0</td>
          <td>computer</td>
          <td>1</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>...</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1440</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
        </tr>
      </tbody>
    </table>
    <p>4 rows × 51 columns</p>
    </div>



.. code:: ipython3

    # Printing out the database to an .xlsx file
    use_case.save("example_excel_usecase")

Once the function is used, an ``.xlsx`` file will be created in the
given path. Now, you can easily fill out the information in the
``.xlsx`` file and load the data into the model database as detailed
below.

Loading the database
~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    # loading data
    
    use_case = UseCase()  # creating a new UseCase instance
    use_case.load("example_excel_usecase_filled.xlsx")

Generating load profiles
------------------------

Once the database is loaded, the user can continue with the normal
analysis, for instance, generating aggregated profiles

.. code:: ipython3

    n_days = 30
    date_start = "2020-01-01"
    use_case.date_start = date_start
    use_case.initialize(num_days=n_days, force=True)
    use_case.generate_daily_load_profiles()


.. parsed-literal::

    You will simulate 30 day(s) from 2020-01-01 00:00:00 until 2020-01-31 00:00:00




.. parsed-literal::

    array([0.   , 0.   , 0.   , ..., 0.002, 0.002, 0.002])



.. code:: ipython3

    profiles = pd.DataFrame(
        data=use_case.generate_daily_load_profiles(flat=True),
        index=pd.date_range(start=date_start, periods=1440 * n_days, freq="T"),
    )
    
    profiles.plot(title="Usecase")




.. parsed-literal::

    <Axes: title={'center': 'Usecase'}>




.. image:: output_17_1.png


Generating load profiles for the single users of the usecase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    for user in use_case.users:
        user_profiles = []
        for day_idx, day in enumerate(use_case.days):
            profile = user.generate_aggregated_load_profile(
                prof_i=day_idx,
                peak_time_range=use_case.peak_time_range,
                day_type=get_day_type(day),
            )
    
            user_profiles.extend(profile)
    
        profiles = pd.DataFrame(
            data=user_profiles,
            index=pd.date_range(start=date_start, periods=1440 * n_days, freq="T"),
        )
    
        profiles.plot(title=user.user_name)



.. image:: output_19_0.png



.. image:: output_19_1.png



:download:`Link to the jupyter notebook file </../notebooks/using_excel.ipynb>`.
