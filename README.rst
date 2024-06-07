.. image:: https://img.shields.io/gitter/room/RAMP-project/RAMP
   :target: https://gitter.im/RAMP-project/community

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://badge.fury.io/py/rampdemand.svg
    :target: https://badge.fury.io/py/rampdemand

.. image:: https://readthedocs.org/projects/rampdemand/badge/?version=latest
    :target: https://rampdemand.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/RAMP-project/RAMP/badge.svg?branch=main
   :target: https://coveralls.io/github/RAMP-project/RAMP?branch=main

.. image:: https://github.com/RAMP-project/RAMP/blob/main/docs/source/_static/RAMP_logo_basic.png?raw=true
   :width: 300


*An open-source bottom-up stochastic model for generating multi-energy load profiles* (`RAMP Website <https://rampdemand.org>`_ , `RAMP Documentation <https://rampdemand.readthedocs.io/en/latest/?badge=latest>`_)


What is RAMP
============
RAMP is an open-source software suite for the stochastic simulation of any user-driven energy demand time series based on few simple inputs.

The project aims to provide synthetic data wherever metered data does not exist, such as when designing systems in remote areas. Check out the `documentation <https://rampdemand.readthedocs.io/en/latest/?badge=latest>`_ and learn more on the RAMP world from our `website <https://rampdemand.org>`_!

.. image:: https://github.com/RAMP-project/RAMP/blob/main/docs/figures/Example_output.jpg?raw=true
   :width: 600

Recommended installation method
===============================

RAMP has been successfully installed and used on macOS, Windows and Linux.

The easiest way to make RAMP software working is to use the free conda package manager which can install the current and future RAMP
dependencies in an easy and user friendly way.

To get conda, `download and install "Anaconda Distribution" <https://www.anaconda.com/products/individual>`_, or `"miniconda" <https://docs.conda.io/en/latest/miniconda.html>`_ which is lighter.
You can install RAMP using pip, conda or from source code.

Installing through pip
----------------------
1. To install the RAMP software, we suggest to create a new environment by running the following command in the *Anaconda prompt*:

.. code-block:: python

   conda create -n ramp python=3.10


2. If you create a new environment for RAMP, you'll need to activate it each time before using it, by writing
the following line in the *Anaconda Prompt*:

.. code-block:: python

   conda activate ramp

3. Now you can use pip to install `rampdemand` on your environment as follow:

.. code-block:: python

  pip install rampdemand


Installing through the source code
----------------------------------
You can also install RAMP from the source code! To do so, you first need to download the source code, which can be done in two ways:

* You can use git to clone the repository via:

.. code-block:: bash

   git clone https://github.com/RAMP-project/RAMP.git

* Or, you may download the source code directly from:

`"RAMP GitHub Repository" <https://github.com/RAMP-project/RAMP>`_.

In this second case, the source code will be downloaded as a zip file, so you'll need to extract the files.

After downloading the source code using any of abovementioned methods, you'll need to use your **anaconda prompt** to install it. There are two options again:

* You may follow the first two steps mentioned in **Installing through pip**. Then, change the directory in the prompt to the folder where the source code is saved (where you can find the *setup.py* file). To install the RAMP software, you may then use:

.. code-block:: bash

   python setup.py install

* Alternatively, without taking any prior action, simply change the directory in the prompt to the folder where the source code is saved and then use:

.. code-block:: bash

   conda env create -f environment.yml

Quick start
===========
There are different ways to build a model using RAMP! Here, we provide a first example but you can find more information in our `documentation  <https://rampdemand.readthedocs.io/en/latest/?badge=latest>`_.

Example python input files
--------------------------
Three different input files are provided as example representing three different categories of appliances that can be modelled with RAMP.
To have a look to the python files, you can download them using the `download_example` function:

.. code-block:: python

   from ramp import download_example

   download_example("the specfic folder directory to save the files")

-  ``input_file_1.py``: represents the most basic electric appliances; it is
   an example of how to model lightbulbs, radios, TVs, fridges, and
   other electric appliances. This input file is based on the ones used
   for `the first RAMP publication <https://doi.org/10.1016/j.energy.2019.04.097>`__.

-  ``input_file_2.py``: shows how to model user-driven thermal loads, with the
   example of a “shower” appliance. The peculiarity of thermal appliances
   is that the nominal power can be provided as external input as a
   “.csv” file (in this case, ``shower_P.csv``). For the example “shower”
   appliance, the varying nominal power accounts for the effect of
   groundwater temperature variation throughout the year. This input
   file is based on that used for `this
   publication <https://doi.org/10.3390/app10217445>`__.

-  ``input_file_3.py``: represents an example of how to model electric
   cooking appliances. In this input file two different kind of meals
   are modelled: 1) short and repetitive meals (e.g. breakfast); and 2)
   main meals (e.g. lunch, dinner). Repetitive meals do not vary across
   days, whilst main meals do so. In particular, every household can
   randomly choose between 3 different types of main meal every day.
   Such variability in meal preferences is modelled by means of two
   parameters: the ``user preference`` and the ``preference index``. The
   ``user preference`` defines how many types of meal are available for
   each user to choose every day (e.g. 3). Then, each of the available
   meal options is modelled separately, with a different
   ``preference index`` attached. The stochastic process randomly varies
   the meal preference of each user every day, deciding whether they
   want a “type 1” meal, or a “type 2”, etc. on a given day. This input
   file is used in `this
   publication <https://doi.org/10.1109/PTC.2019.8810571>`__

You can execute python input files within an IDE, in your terminal with python command

.. code-block:: bash

   python <path to .py input file>

or in your terminal with the ``ramp`` command, see `Command line options <cmd_option_>`_ below for more information.

Spreadsheet input files
-----------------------

It is also possible to use spreadsheets as input files. To do so, you
need to run the ``ramp`` command with the option ``-i``:

.. code-block:: bash

   ramp -i <path to .xlsx input file>


.. note:: You can input several files, separated from each others by a single blank space you can also input python files

.. _cmd_option:

Command line options
--------------------

In the command line you can also run .py input files
If you already know how many daily profiles you want to simulate you can indicate it with the ``-n`` option:

.. code-block:: bash

   ramp -i <path to .xlsx or .py input file> -n 10

will simulate 10 daily profiles. Note that if you do not provide this option you will being prompted for the
number of daily profiles within the console.


If you want to save ramp results to a custom file, you can provide it with the option `-o`

.. code-block:: bash

   ramp -i <path to .xlsx input file> -o <path where to save RAMP outputs>

.. note:: You can provide a number of output files, separated from each others by a single blank space, matching the number of input files.

Other options are documented in the help of `ramp`, which you access with the ``-h`` option

.. code-block:: bash

   ramp -h


If you have existing python input files from RAMP version prior to 0.5, you can convert them to
spreadsheets input files. Simply run

.. code-block:: bash

   ramp_convert -i <path to the .py input file you wish to convert>

If you want to save a RAMP model you created with a .py file into a spreadsheet refer to
this `example <https://rampdemand.readthedocs.io/en/latest/examples/using_excel/using_excel.html#exporting-the-database>`_

For other examples of command lines options, such as setting date ranges, please visit `the dedicated section  <https://rampdemand.readthedocs.io/en/latest/examples/year_simulation/year_simulation.html#setting-date-range>`_ of the documentation.

Building a model with a python script
-------------------------------------

.. code-block:: python

   # importing functions
   from ramp import UseCase, User

   # Create a user category
   household_1 = User(
    user_name = "Household type 1", # an optional feature for the User class
    num_users = 10, # Specifying the number of specific user category in the community
   )

You can add appliances to a user category by:

.. code-block:: python

   # adding some appliances for the household
   radio = household_1.add_appliance(
    name = "Small Radio", # optional feature for the appliance class
    number = 1, # how many radio each household type 1 has
    power = 10, # RAMP does not take care of units of measure (e.g., Watts), you must be consistent
    func_time = 120, # Total functioning time of appliance in minutes
    num_windows = 2, # how many time-windows the appliance is used in
   )


The use time frames can be specified using the 'window' method for each appliance of the user category:

.. code-block:: python

   # Specifying the functioning windows
   radio.windows(
    window_1 = [480,540], # from 8 AM to 9 AM
    window_2 = [1320,1380], # from 10 PM to 11 PM
   )

You can also add another, different user to the simulation. In this case,
we use a more compact formulation:

.. code-block:: python

   # Create a second user category
   household_2 = User(
    user_name = "Household type 2", # an optional feature for the User class
    num_users = 13, # Specifying the number of specific user category in the community
    )

   # adding some appliances for the new household type in compact form, with windows specified directly and random variability
   light_bulbs = household_2.add_appliance(
    name = "Light bulbs", # optional feature for the appliance class
    number = 5, # how many light bulbs each household type 2 has
    power = 7, # RAMP does not take care of units of measure (e.g., Watts), you must be consistent
    func_time = 120, # total functioning time of appliance in minutes
    time_fraction_random_variability=0.2, # 20% random variability associated to the total functioning time
    num_windows = 2, # how many time-windows the appliance is used in
    window_1 = [390,480], # from 6.30 AM to 8 AM
    window_2 = [1020,1440], # from 5 PM to 12 PM
    random_var_w=0.35 # 35% randomness assigned to the size of the functioning windows
    )

At this point, we can group our different users into a "use case" and run the simulation,
for instance for a whole year.

.. code-block:: python

   use_case = UseCase(users=[household_1,household_2], date_start="2020-01-01", date_end="2020-12-31")
   whole_year_profile = use_case.generate_daily_load_profiles()

Here is your first load for a community including two types of housholds,
for a total of 23 individual users. Of course, more variations and many more
features are possible! For instance, you can simulate loads even for
an individual appliance or user. In addition, you can use in-built plotting
functionalities to explore your results. Check out the documentation
for all the possibilities.

Contributing
============
This project is open-source. Interested users are therefore invited to test, comment or contribute to the tool. Submitting issues is the best way to get in touch with the development team, which will address your comment, question, or development request in the best possible way. We are also looking for contributors to the main code, willing to contribute to its capabilities, computational-efficiency, formulation, etc.

To contribute changes please consult our `Contribution guidelines <https://github.com/RAMP-project/RAMP/blob/main/CONTRIBUTING.md>`_


How to cite
===========
Please cite the original Journal publication if you use RAMP in your research:

*F. Lombardi, S. Balderrama, S. Quoilin, E. Colombo, Generating high-resolution multi-energy load profiles for remote areas with an open-source stochastic model, Energy, 2019,*
`https://doi.org/10.1016/j.energy.2019.04.097 <https://doi.org/10.1016/j.energy.2019.04.097>`_

More information
================
Want to know more about the possible applications of RAMP, the studies that relied on it and much more? Then take a look at the `RAMP Website <https://rampdemand.org>`_!

License
=======
Copyright 2019-2023 RAMP, contributors listed in **Authors**

Licensed under the European Union Public Licence (EUPL), Version 1.2-or-later; you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an **"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND**, either express or implied. See the License for the specific language governing permissions and limitations under the License.


.. note::
   This project is actively maintained and developed. This means that while we provide stable and reliable software releases, we keep developing new features and improvements for upcoming, upgraded versions    of the software.
