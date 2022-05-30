## Description of RAMP algorithm

An input file consists in a list of user type (i.e. Hospital, Low Income Household, School, etc.). There is a certain number of users from each of the user types (minimum is one). To each user type is associated a list of typical appliances.

Almost all the usage parameters (specific power consumption, usage windows during a 24h period) are defined at the appliance level.

A theoretical load profile is computed with the following steps:

1. identify an expected peak time frame to allow differentiating between off- and on-peak switch-on
events of appliances

2. for each type of appliance of each user of each user type, check if the appliance type is used
based on a weekly frequency of use. If not, ignore the appliance type. Otherwise,
compute:
    
   1. the randomised appliance type's total time of use
   
   2. the randomised vector of time frames in which the appliance type is allowed to be switched on
    
   Subsequently, iterate over the following steps until the sum of the durations of all the switch-on events equals the randomised total time of use defined in step 2.i.:

   3. a random switch-on time frame within the allowed time frames defined in step 2.ii

   4. compute the randomised power required by the appliance type for the switch-on time frame defined in step 2.iii

   5. compute the actual power absorbed by the appliances of the type under consideration during the switch-on event considering a random numerosity of appliances

    Repeat then step 2. N times to get a stochastic variation of the appliances' usage

3. Average the N profiles in the total load profile.
