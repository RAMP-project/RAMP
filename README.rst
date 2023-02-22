.. image:: https://img.shields.io/gitter/room/RAMP-project/RAMP
   :target: https://gitter.im/RAMP-project/community

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://badge.fury.io/py/rampdemand.svg
    :target: https://badge.fury.io/py/rampdemand

.. image:: https://readthedocs.org/projects/rampdemand/badge/?version=latest
    :target: https://rampdemand.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://github.com/RAMP-project/RAMP/blob/documentation/docs/source/_static/RAMP_logo_basic.png?raw=true
   :width: 300


*An open-source bottom-up stochastic model for generating multi-energy load profiles* (`RAMP Website <https://rampdemand.org>`_ , `RAMP Documentation <https://rampdemand.readthedocs.io/en/latest/?badge=latest>`_)


What is RAMP
============
RAMP is an open-source software suite for the stochastic simulation of any user-driven energy demand time series based on few simple inputs.

The project aims to provide synthetic data wherever metered data does not exist, such as when designing systems in remote areas. Check out the `documentation <https://rampdemand.readthedocs.io/en/latest/?badge=latest>`_ and learn more on the RAMP world from our `website <https://rampdemand.org>`_! 

.. image:: https://github.com/RAMP-project/RAMP/blob/master/docs/figures/Example_output.jpg?raw=true
   :width: 600

Recommended installation method
===============================

The easiest way to make RAMP software working is to use the free conda package manager which can install the current and future RAMP
depencies in an easy and user friendly way.

To get conda, `download and install "Anaconda Distribution" <https://www.anaconda.com/products/individual>`_, or `"miniconda" <https://docs.conda.io/en/latest/miniconda.html>`_ which is lighter.
You can install RAMP using pip, conda or from source code.

Installing through pip
----------------------
1. To install the RAMP software, we suggest to create a new environment by running the following command in the anaconda prompt:

.. code-block:: python

   conda create -n ramp python=3.8

2. If you create a new environment for RAMP, you'll need to activate it each time before using it, by writing
the following line in the *Anaconda Prompt*

.. code-block:: python

   conda activate ramp

3. Now you can use pip to install `rampdemand` on your environment as follow:

.. code-block:: python

  pip install rampdemand


Installing through source code
------------------------------
You can also install RAMP from the source code! To do so, you first need to download the source code first:

1. you can use git to clone the repository using:

.. code-block:: bash

   git clone https://github.com/RAMP-project/RAMP.git

2. you may download the source code directly from:

`"RAMP GitHub Repository" <https://github.com/RAMP-project/RAMP/tree/development>`_.

In this case, the source code will be downloaded as a zip file, so you need the extract the files.

After downloading the source code using any of abovementioned ways, you need to use your **anaconda prompt** to install the code.
You can follow the first two steps mentioned in **Installing throguh pip**. Then you need to change the directory of the promt to the folder where the source code is saved (where you can find the *setup.py* file). To install the RAMP software use:

.. code-block:: bash

Alternatively, you may use:

.. code-block:: bash

   conda env create -f requirements.yml

Requirements
============
RAMP has been tested on macOS, Windows and Linux.

For running RAMP, you'll need a few packages:

#. The Python programming language, version 3.6 or higher
#. A number of Python adds-on packages:

   * `Pandas  <https://pandas.pydata.org/>`_
   * `Numpy  <https://numpy.org/>`_
   * `Matplotlib  <https://matplotlib.org/>`_
   * `Openpyxl  <https://openpyxl.readthedocs.io/en/stable/>`_

The requirements are specified in the `requirements.txt` file.

Quick start
===========
There are different ways to build a model using RAMP! Here, we provide a first example but you can find more information in our `documentation  <https://rampdemand.readthedocs.io/en/latest/?badge=latest>`_.

Example python input files
--------------------------
Three different input files are provided as example representing three different categories of appliances that can be modelled with RAMP.
To have a look to the python files, you can download them using the "download_example" function:

.. code-block:: python

   from ramp import download_example

   download_example("the specfic folder directory to save the files")

-  ``input_file_1.py``: represents the most basic electric appliances,
   is an example of how to model lightbulbs, radios, TVs, fridges, and
   other electric appliances. This input file is based on the ones used
   for `this
   publication <https://doi.org/10.1016/j.energy.2019.04.097>`__.

-  ``input_file_2.py``: shows how to model thermal loads, with the
   example of a “shower” appliance. The peculiarity of thermal appiances
   is that the nominal power can be provided as external input as a
   “csv” file (in this case, ``shower_P.csv``). For the example “shower”
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

Spreadsheet input files
-----------------------

It is also possible to use spreadsheets as input files. To do so you
need to run the ``ramp`` command with the option ``-i``:

.. code-block:: bash

   ramp -i <path to .xlsx input file>

If you already know
how many profile you want to simulate you can indicate it with the
``-n`` option:

.. code-block:: bash

   ramp -i <path to .xlsx input file> -n 10

will simulate 10 profiles. Note that you can use this option without
providing a ``.xlsx`` input file with the ``-i`` option, this will then
be equivalent to running ``python ramp_run.py`` from the ``ramp`` folder
without being prompted for the number of profile within the console.

Other options are documented in the help of `ramp`, which you access with the ``-h`` option

.. code-block:: bash

   ramp -h


If you have existing python input files, you can convert them to
spreadsheet. To do so, go to ``ramp`` folder and run

.. code-block:: bash

   python ramp_convert_old_input_files.py -i <path to the input file you wish to convert>

For other example of command lines options, such as setting date ranges, please visit `the dedicated section  <https://rampdemand.readthedocs.io/en/latest/examples/year_simulation/year_simulation.html#setting-date-range>`_ of the documentation.

Building a model with a python script
-------------------------------------

.. code-block:: python

   # importing functions
   from ramp import User,calc_peak_time_range,yearly_pattern

   # Create a user category
   low_income_households = User(
    user_name = "low_income_household", # an optional feature for the User class
    num_users = 10, # Specifying the number of specific user category in the community
   )

You can add appliances to a user category by:

.. code-block:: python

   # adding some appliances for the household
   radio = low_income_household.add_appliance(
    name = "Small Radio", # optional feature for the appliance class
    number = 1, # how many radio each low income household holds
    power = 10, # RAMP does not take care of unit of measures , watt
    func_time = 120, # Total functioning time of appliance in minutes
    num_windows = 2, # in how many time-windows the appliance is used
   )

The use time frames can be specified using the 'window' method for each appliance of the user category:

.. code-block:: python

   # Specifying the functioning windows
   radio.windows(
    window_1 = [480,540], # from 8 AM to 9 AM
    window_2 = [1320,1380], # from 10 PM to 11 PM
   )

Now you can generate your **stochastic Profiles**:

.. code-block:: python

   # generating load_curves
   load = low_income_household.generate_aggregated_load_profiles(
      prof_i = 1, # the ith day profile
      peak_time_range = calc_peak_time_range(), # the peak time range
      Year_behaviour = yearly_pattern(), # defining the yearly pattern (like weekdays/weekends)
   )

Contributing
============
This project is open-source. Interested users are therefore invited to test, comment or contribute to the tool. Submitting issues is the best way to get in touch with the development team, which will address your comment, question, or development request in the best possible way. We are also looking for contributors to the main code, willing to contibute to its capabilities, computational-efficiency, formulation, etc.

To contribute changes:

#. Fork the project on GitHub
#. Create a feature branch (e.g. named "add-this-new-feature") to work on in your fork
#. Add your name to the `AUTHORS <https://github.com/RAMP-project/RAMP/blob/development/AUTHORS>`_ file
#. Commit your changes to the feature branch
#. Push the branch to GitHub
#. On GitHub, create a new pull request from the feature branch

When committing new changes, please also take care of checking code stability by means of the `qualitativte testing <https://github.com/RAMP-project/RAMP/blob/development/CONTRIBUTING.md>`_ functionality.


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

   This project is under active development!
