Release History
===============

0.3.1 (2021-06-23)
------------------

**|new|**       added "input_file_3" as an example of e-cooking loads

**|changed|**   the readme.md has been updated to describe the purpose of the 3 provided input files, 1: basic electric appliances, 2: DHW, 3: cooking

**|changed|**   the pubs_list.md has been updated with two new publications

0.3.0 (2021-05-28)
------------------

**|new|**       created a CHANGELOG.md file to keep track of code changes from now on

**|changed|**   the repository structure has been modified for better clarity, replicating the structure of the sister-project RAMP-mobility

**|changed|**   changed the way in which the probability of coincident switch-on of several identical appliances owned by a single user is computed. Now, it penalisse less the probability of maximum coincidence for off-peak events

**|fixed|**     `s_peak` value is now set by default to 0.5, rather than 1. This fixes an unwanted behaviour in how the `random.gauss` function worked

