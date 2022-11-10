.. image:: https://img.shields.io/gitter/room/RAMP-project/RAMP
   :target: https://gitter.im/RAMP-project/community

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


.. image:: https://github.com/RAMP-project/RAMP/blob/master/docs/figures/RAMP_logo_basic.png?raw=true
   :width: 300


*An open-source bottom-up stochastic model for generating multi-energy load profiles.*

What is RAMP
-------------
RAMP is a bottom-up stochastic model for the generation
of high-resolution multi-energy profiles, conceived for
application in contexts where only rough information about users'
behaviour are obtainable. Those may range from remote villages to whole countries. RAMP provides an easy and intuitve
API for building up stochastic profiles.

.. image:: https://github.com/RAMP-project/RAMP/blob/master/docs/figures/Example_output.jpg?raw=true
   :width: 600

Recommended installation method
-------------------------------

The easiest way to make RAMP software working is to use the free
conda package manager which can install the current and future RAMP
depencies in an easy and user friendly way.

To get conda, `download and install "Anaconda Distribution" <https://www.anaconda.com/products/individual>`_.
You can install RAMP using pip, conda or from source code.

Installing through pip
=======================
1. For installing RAMP software, it is suggested to create a new environment by running the following command in the anaconda prompt:

.. code-block:: python

   conda create -n ramp python=3.8

2. If you create a new environment for mario, to use it, you need to activate the ramp environment each time by writing
the following line in *Anaconda Prompt*

.. code-block:: python

   conda activate ramp

3. Now you can use pip to install ramp on your environment as follow:

.. code-block:: python

  pip install ramp

Installing through conda
==========================


Installing throguh source code
================================
You can also install from the source code!


Requirements
------------
RAMP has been tested on macOS and Windows.

For running RAMP, a couple of things are needed:

#. The Python programming language, version 3.6 or higher
#. A number of Python adds-on packages
#. RAMP software itself


Quick start
------------

How to create a user category?

.. code-block:: python

   from ramp import User

   # Create a user category
   low_income_households = User(
    user_name = "low_income_household", # an optional feature for the User class
    num_users = 10, # Specifying the number of specific user category in the community
   )

You can add appliances to a user category by:

.. code-block:: python

   # adding some appliances for the household
   radio = low_income_household.Appliance(
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
   low_income_household.generate_aggregated_load_profiles(

   )




.. _RST pckgs:

Python module requirements
--------------------------
Some of the key packages that RAMP relies on are:

* `Pandas  <https://pandas.pydata.org/>`_
* `Numpy  <https://numpy.org/>`_
* `Matplotlib  <https://matplotlib.org/>`_
* `Openpyxl  <https://openpyxl.readthedocs.io/en/stable/>`_


How to cite
------------
Please cite the original Journal publication if you use RAMP in your research:

*F. Lombardi, S. Balderrama, S. Quoilin, E. Colombo, Generating high-resolution multi-energy load profiles for remote areas with an open-source stochastic model, Energy, 2019,*
`https://doi.org/10.1016/j.energy.2019.04.097 <https://doi.org/10.1016/j.energy.2019.04.097>`_

List of publications
---------------------
This is an up-to-date list of publications featuring RAMP:

`[1] <https://doi.org/10.3390/en14144232>`_ *William Clements, Surendra Pandit, Prashanna Bajracharya, Joe Butchers, Sam Williamson, Biraj Gautam, and Paul Harper. Techno-Economic Modelling of Micro-Hydropower Mini-Grids in Nepal to Improve Financial Sustainability and Enable Electric Cooking, Energies (2020), 14, no. 14: 4232.*

`[2] <https://doi.org/10.1088/1748-9326/ac0cab>`_ *Giacomo Falchetta, Nicolò Stevanato, Magda Moner-Girona, Davide Mazzoni, Emanuela Colombo, Manfred Hafner, The M-LED platform: advancing electricity demand assessment for communities living in energy poverty, Environmental Reasearch Letters (2021)*

`[3] <https://doi.org/10.3390/app10217445>`_ *Nicolò Stevanato, Lorenzo Rinaldi, Stefano Pistolese, Sergio Balderrama, Sylvain Quoilin, Emanuela Colombo, Modeling of a Village-Scale Multi-Energy System for the Integrated Supply of Electric and Thermal Energy, Applied Sciences (2020)*

`[4] <http://hdl.handle.net/11311/1143671>`_ *Francesco Lombardi, Sylvain Quoilin, Emanuela Colombo, Modelling distributed Power-to-Heat technologies as a flexibility option for smart heat-electricity integration, Proceedings of ECOS 2020, pp. 2369-2380*

`[5] <http://hdl.handle.net/11311/1139750>`_ *Sergio Balderrama, Gabriela Peña Balderrama, Francesco Lombardi, Nicolò Stevanato, Andreas Sahlberg, Mark Howells, Emanuela Colombo and Sylvain Quoilin, Model-Base cost evaluation of Microgrids systems for rural Electrification and energy planning purposes, Proceedings of ISES Solar World Congress 2019*

`[6] <https://doi.org/10.1016/j.esd.2020.07.002>`_ *Nicolò Stevanato, Francesco Lombardi, Giulia Guidicini, Lorenzo Rinaldi, Sergio Balderrama, Matija Pavičević, Sylvain Quoilin, Emanuela Colombo, Long-term sizing of rural microgrids: Accounting for load evolution through multi-step investment plan and stochastic optimization, Energy for Sustainable Development (2020), 58, pp. 16-29*

`[7] <https://doi.org/10.1109/ICCEP.2019.8890129>`_ *Claudio Del Pero, Fabrizio Leonforte, Francesco Lombardi, Nicolò Stevanato, Jacopo Barbieri, Nicolò Aste, Harold Huerto, Emanuela Colombo,
Modelling of an integrated multi-energy system for a nearly Zero Energy Smart District,
Proceedings of ICCEP 2019*

`[8] <http://hdl.handle.net/11311/1121368>`_ *Sergio Balderrama, Francesco Lombardi, Nicolò Stevanato, Gabriela Peña, Emanuela Colombo, Sylvain Quoilin,
Automated evaluation of levelized cost of energy of isolated micro-grids for energy planning purposes in developing countries,
Proceedings of ECOS 2019*

`[9] <https://doi.org/10.1109/PTC.2019.8810571>`_ *Nicolò Stevanato, Francesco Lombardi, Emanuela Colombo, Sergio Balderrama, Sylvain Quoilin,
Two-Stage Stochastic Sizing of a Rural Micro-Grid Based on Stochastic Load Generation,
2019 IEEE Milan PowerTech, Milan, Italy, 2019, pp. 1-6.*

`[10] <https://doi.org/10.1016/j.energy.2019.01.004>`_ *Francesco Lombardi, Matteo Vincenzo Rocco, Emanuela Colombo,
A multi-layer energy modelling methodology to assess the impact of heat-electricity integration strategies: the case of the residential cooking sector in Italy,
Energy (2019)*


License
--------
Copyright 2019 RAMP, contributors listed in **Authors**

Licensed under the European Union Public Licence (EUPL), Version 1.2-or-later; you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an **"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND**, either express or implied. See the License for the specific language governing permissions and limitations under the License.
