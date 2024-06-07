Release History
===============

0.5.2 (dev)
-----------

**|new|**       Addition of the 'coveralls' badge to the README

**|new|**       Addition of a random-seed functionality to ensure reproducible results if needed

**|new|**       If a `User` instance doesn't have any appliance, its `repr` method prints the user name, and number of users with a message to mention no appliances are assigned to the instance yet. Before it raised a `ValueError`.

**|new|**       Documentation template was changed to sphinx wagtail theme to improve the navigation through the documentation sections

**|new|**       Add issue templates for issue creation on github

**|new|**       Automatic testing of the jupyter notebooks of the documentation, to make sure the examples are always running through

**|new|**       Adding depreciation warning to back-compatibility `Appliance` method in `User` class to let users know they should use the `add_appliance` method instead.

**|new|**       Introduction of an Appliance parameter to model productive use duty cycles: `continuous_use_duty_cycle`

**|changed|**   Expanded and revised documentation, with a particular focus on more and clearer usage examples

**|changed|**   Updated requirements for contributing, including pip dependencies specific to developers

**|changed|**   Expanded test coverage

**|changed|**   Updated .py example input files to match the latest formalism of the RAMP code

**|changed|**   Python version was bumped from 3.8 to 3.10

**|changed|**   Improved the way to run the quantitative tests and the instructions to do so

**|fixed|**     Windows compatibility of path to convert .py to .xlsx

**|fixed|**     `rand_peak_enlarge` is rounded to be at least 1 so that the `peak_time_range` is never empty

**|fixed|**     Running .xlsx files form the command line

**|fixed|**     Ignore profile of appliances if any of their functional time or randomly allocated time of use are 0

0.5.1 (2024-02-08)
------------------

**|fixed|**     Plotting a cloud of profiles from the command line is fixed

0.5.0 (2023-12-06)
------------------

**|fixed|**     jupyter notebooks are up to date with the UseCase class

**|fixed|**     UseCase class usage is now documented

**|changed|**   num_profile variable was changed to num_days

**|changed|**   User class get assigned automatically to a default UseCase instance if not provided

**|changed|**   Delete ramp.core.initialize and ramp.core.stochastic_process, move calc_peak_time_range inside UseCase method

**|fixed|**     conversion of .py files into .xlsx is fixed

**|fixed|**     using .py files is now possible in the command line as well as from IDE

**|new|**       tests for example jupyter notebook (smoke test to see if the notebooks run through)

**|new|**       continuous integration setup

**|new|**       first automated tests

**|fixed|**     installation options have been debugged and the documentation updated accordingly

**|fixed|**     automated download of example applications via the `download_example` functions now includes previously missing .csv files

0.4.1 (2023-10-XX)
------------------

**|hotfix|**    added option `-o` to the terminal command line interface to enable the user to provide output path to save ramp results. This option is also accessible to python users using `ofname` argument of the `ramp/ramp_run.py::run_usecase` or the `ramp/post_process/post_process.py::export_series` functions.

0.4.0 (2023-02-17)
------------------

**|new|**       added full software documentation

**|fixed|**     refactored the code in order to improve execution time, use of masks were dismissed

**|new|**       added a way to compute ramp profiles for a usecase using parallel processes via the `generate_daily_load_profiles_parallel` method of the `UseCase` class  (option `-p` for command line input)

**|new|**       added a way to run a whole year with different input files for each month for seasonality of parameters (only for the command line, type `ramp -h` in terminal for more help)

**|new|**       added a way to define date ranges for ramp simulation to get the weekdays automatically and avoid always starting on a monday (only for the command line, type `ramp -h` in terminal for more help)

**|new|**       added a qualitative testing functionality, accessible via `test/test_run.py`, to check how code changes affect default outputs

**|fixed|**     the way in which the random switch-on time is computed in the `stochastic_process` has been changed so that it is sampled with uniform probability from a concatenated set of functioning windows, rather than for each window separately (which led to short windows having higher concentration of switch-on events and demand peaks)

**|fixed|**     the default value for the `peak_enlarg` parameter has been changed from the mistyped value of 0 to the intended value of 0.15

**|new|**       added a paragraph describing the algorithm of RAMP

**|new|**       refactored the code by moving many of the code from `stochastic_process.py` into the `User` class in `core.py`, used function where code was duplicated

**|fixed|**     the user now gets a warning if the allocated window time is shorter than the provided `func_time`

**|new|**       add a way to run from `.xlsx` input files, keeping the back compatibility with `.py` files (there is possibility to convert `.py` input files to `.xslx`)

**|new|**       defined a new class in `core.py`: `UseCase` which contains a list of `User` instances

**|fixed|**     variable names are now PEP8 compatible

0.3.1 (2021-06-23)
------------------

**|new|**       added `input_file_3` as an example of e-cooking loads

**|changed|**   the way in which input files are called in the ramp_run script has been changed to be more explicit and user-friendly

**|changed|**   the `readme.md` has been updated to describe the purpose of the 3 provided input files, 1: basic electric appliances, 2: DHW, 3: cooking

**|changed|**   the `pubs_list.md` has been updated with two new publications


0.3.0 (2021-05-28)
------------------

**|new|**       created a `CHANGELOG.md` file to keep track of code changes from now on

**|changed|**   the repository structure has been modified for better clarity, replicating the structure of the sister-project RAMP-mobility

**|changed|**   changed the way in which the probability of coincident switch-on of several identical appliances owned by a single user is computed. Now, it penalisse less the probability of maximum coincidence for off-peak events

**|fixed|**     `s_peak` value is now set by default to 0.5, rather than 1. This fixes an unwanted behaviour in how the `random.gauss` function worked
