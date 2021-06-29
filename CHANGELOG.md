Release History
===============

0.3.2-dev ()
------------------

**|new|**       added a qualitative testing functionality, accessible via `test/test_run.py`, to check how code changes affect default outputs

**|fixed|**     the way in which the random switch-on time is computed in the `stochastic_process` has been changed so that it is sampled with uniform probability from a concatenated set of functioning windows, rather than for each window separately (which led to short windows having higher concentration of switch-on events and demand peaks)

**|fixed|**     the default value for the `peak_enlarg` parameter has been changed from the mistyped value of 0 to the intended value of 0.15 


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

