.. _date_range_input_section:
Using real calendar days to generate profiles
=============================================

Setting date range
~~~~~~~~~~~~~~~~~~

With the command line interface it is possible to generate a given number of profiles (one is always prompt for it if not provided)

.. code-block::

   ramp -i path-to-input-file -n 10

will generate 10 profiles which will be appended one after the other. The first profile will then always be a monday and weekdays and weekends follow from there

It is possible to provide a date range by using ``--start-date`` and ``--end-date`` options. Simply provide the date of in ``YYYY-MM-DD`` ISO 8601 format

.. code-block:: bash

   ramp -i path-to-input-file --start-date 2022-01-01 --end-date 2022-01-31

Will generate a daily profile for each day of January 2022. The type of day (weekday or weekend) is automatically assigned.

.. note::
    order of inputs does not matter

Here are various configurations

.. code-block:: bash

   ramp -i path-to-input-file --start-date 2022-01-03 -n 10

will generate a daily profile for 10 days of starting on 3rd January 2022

.. code-block:: bash

   ramp -i path-to-input-file --end-date 2022-02-09 -n 10

will generate a daily profile for 10 days ending on 9th Febuary 2022


.. code-block:: bash

   ramp -i path-to-input-file --start-date 2022-03-01

will generate a daily profile for all days between March 1st 2022 and December 31st 2022


.. code-block:: bash

   ramp -i path-to-input-file --end-date 2022-04-25


will generate a daily profile for all days from January 1st 2022 and April 25th 2022



.. code-block:: bash

   ramp -i path-to-input-file --start-date 2022-01-01 --end-date 2022-01-31 -n 3

generates 3 daily profiles and average them to one for each of the days of January.
In the future it should lead to either an error or a warning that -n is ignored

Simulation for the whole year
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is also possible to simulate whole years with the ``-y``option

.. code-block:: bash

   ramp -i path-to-input-file -y 2021 -n 1

will generate a daily profile for all days of 2022

.. note::
    Here the `-n` option is used so that the user is not prompted to choose how many profile need to be generated and
    averaged for each single day profile. This might not be needed in the future if we decide that averaging daily profiles is not a good thing.

To chain two or more years you simply provide them, separated by a single space

.. code-block:: bash

   ramp -i path-to-input-file -y 2021 2022 -n 1

will generate a daily profile for all days of 2022 and 2023


Year simulation with different input parameters per month
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to get a daily profile for each day of a whole year 
having different parameters for appliances throughout the 12 months
of the year. The daily profiles are then concatenated in a long timeseries 
for the year with 1-minute resolution. This functionality expects 12 
independent .xlsx input files located in a folder and sorted numerically 
by month number (the sorted order is printed out at the execution of 
the function for the user to check).

For example:

.. code-block:: bash

   ramp -i path-to-folder -y 2022 -n 1

.. note::
    (for windows user use ``\`` instead of ``/`` for path separation)

will simulate 1 daily profile for each day of the whole year 2022.
The results will be saved in the files ``'yearly_profile_min_resolution.csv'`` 
and ``'yearly_profile_hour_resolution.csv'`` for further data analysis.


