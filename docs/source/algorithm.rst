****************
RAMP algorithm
****************

An input file consists in a list of user types (i.e. Hospital, Low Income Household, School, etc.). There is a certain number of users from each of the user types (minimum is one). To each user type is associated a list of typical appliances.
Almost all the usage parameters (specific power consumption, usage windows during a 24h period) are defined at the appliance level.
A theoretical load profile is computed with the following steps:

#. identify an expected peak time frame to allow differentiating between off- and on-peak switch-on events of appliances.
#. for each type of appliance of each user of each user type, check if the appliance type is used based on a weekly frequency of use. If not, ignore the appliance type. Otherwise,compute:

   #. the randomised appliance type's total time of use
   #. the randomised vector of time frames in which the appliance type is allowed to be switched on. Subsequently, iterate over the following steps until the sum of the durations of all the switch-on events equals the randomised total time of use defined in step 2.1.
   #. a random switch-on time frame within the allowed time frames defined in step 2.2
   #. compute the randomised power required by the appliance type for the switch-on time frame defined in step 2.3
   #. compute the actual power absorbed by the appliances of the type under consideration during the switch-on event considering a random numerosity of appliances. Repeat then step 2 for N times to get a stochastic variation of the appliances' usage

#. Average the N profiles in the total load profile.
