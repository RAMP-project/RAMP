Release History
===============

0.3.0 (2021-05-28)
------------------

**|new|**       created a CHANGELOG.md file to keep track of code changes from now on

**|changed|**   the repository structure has been modified for better clarity, replicating the structure of the sister-project RAMP-mobility

**|changed|**   changed the way in which the probability of coincident switch-on of several identical appliances owned by a single user is computed. Now, it penalisse less the probability of maximum coincidence for off-peak events

**|fixed|**     `s_peak` value is now set by default to 0.5, rather than 1. This fixes an unwanted behaviour in how the `random.gauss` function worked

