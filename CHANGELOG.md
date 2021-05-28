Release History
===============

0.3.0 (2021-05-28)
------------------

**|new|**       created a CHANGELOG.md file to keep track of code changes from now on

**|changed|**   the probability coincident switch-on of several identical appliances owned by a single user is changed to penalise less the probability of maximum coincidence, for both 
off- and on-peak events

**|fixed|**     `s_peak` value is now set by default to 0.5, rather than 1. This fixes an unwanted behaviour in how the `random.gauss` function worked

