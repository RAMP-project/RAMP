import pandas as pd
from copy import deepcopy

from ramp.core.core import UseCase

# Import users list of example file 1
from ramp.example.input_file_1 import User_list

# Build use case 1 with non-fixed seed
uc_1 = UseCase(
    users=deepcopy(User_list),
    random_seed=None
)
# Initialize and generate load profile
uc_1.initialize(peak_enlarge=0.15, num_days=3)
uc_1_lp = uc_1.generate_daily_load_profiles()

# Build use case 2 and fixed random seed
uc_2 = UseCase(
    users=deepcopy(User_list),
    random_seed=1
)
# Initialize and generate load profile
uc_2.initialize(peak_enlarge=0.15, num_days=3)
uc_2_lp = uc_2.generate_daily_load_profiles()

# Build use case 3 and same fixed random seed as uc_2
uc_3 = UseCase(
    users=deepcopy(User_list),
    random_seed=1
)

# Initialize and generate load profile
uc_3.initialize(peak_enlarge=0.15, num_days=3)
uc_3_lp = uc_3.generate_daily_load_profiles()


#%% Plot results
import matplotlib.pyplot as plt

lp_df = pd.DataFrame({'uc_1_non_fixed_seed': uc_1_lp,
                      'uc_2_fixed_seed': uc_2_lp,
                      'uc_3_fixed_seed': uc_3_lp,
                      'diff uc_2 - uc-1': uc_2_lp - uc_1_lp,  # difference between uc_1 and uc_2 is not zero
                      'diff uc_2 - uc_3': uc_2_lp - uc_3_lp  # difference between uc_2 and uc_3 is zero
                      })
lp_df.plot()
plt.show()