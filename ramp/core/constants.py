def switch_on_parameters():
    """
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probability of coincident switch-on within the peak window

    mu_peak corresponds to \mu_{%} in [1], p.8
    s_peak corresponds to \sigma_{%} in [1], p.8

    Notes
    -----
    [1] F. Lombardi, S. Balderrama, S. Quoilin, E. Colombo,
        Generating high-resolution multi-energy load profiles for remote areas with an open-source stochastic model,
        Energy, 2019, https://doi.org/10.1016/j.energy.2019.04.097.
    """

    mu_peak = 0.5  # median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 0.5  # standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned
    op_factor = 0.5  # off-peak coincidence calculation parameter

    return mu_peak, s_peak, op_factor


OLD_TO_NEW_MAPPING = {
    "name": "user_name",
    "n_users": "num_users",
    "us_pref": "user_preference",
    "P": "power",
    "P_11": "p_11",
    "P_12": "p_12",
    "P_21": "p_21",
    "P_22": "p_22",
    "P_31": "p_31",
    "P_32": "p_32",
    "pref_index": "pref_index",
    "P_series": "p_series",
    "Thermal_P_var": "thermal_p_var",
    "w": "num_windows",
    "cw11": "cw11",
    "cw12": "cw12",
    "cw21": "cw21",
    "cw22": "cw22",
    "cw31": "cw31",
    "cw32": "cw32",
    "fixed": "fixed",
    "flat": "flat",
    "c": "func_cycle",
    "t": "func_time",
    "n": "number",
    "occasional_use": "occasional_use",
    "r_c1": "r_c1",
    "r_c2": "r_c2",
    "r_c3": "r_c3",
    "r_t": "time_fraction_random_variability",
    "random_var_w": "random_var_w",
    "t_11": "t_11",
    "t_12": "t_12",
    "wd_we_type": "wd_we_type",
    "window_1": "window_1",
    "window_2": "window_2",
    "window_3": "window_3",
}

NEW_TO_OLD_MAPPING = {value: key for (key, value) in OLD_TO_NEW_MAPPING.items()}


APPLIANCE_ATTRIBUTES = (
    "name",
    "number",
    "power",
    "num_windows",
    "func_time",
    "time_fraction_random_variability",
    "func_cycle",
    "fixed",
    "fixed_cycle",
    "continuous_duty_cycle",
    "occasional_use",
    "flat",
    "thermal_p_var",
    "pref_index",
    "wd_we_type",
    "p_11",
    "t_11",
    "cw11",
    "p_12",
    "t_12",
    "cw12",
    "r_c1",
    "p_21",
    "t_21",
    "cw21",
    "p_22",
    "t_22",
    "cw22",
    "r_c2",
    "p_31",
    "t_31",
    "cw31",
    "p_32",
    "t_32",
    "cw32",
    "r_c3",
    "window_1",
    "window_2",
    "window_3",
    "random_var_w",
)

APPLIANCE_ARGS = (
    "number",
    "power",
    # "p_series",
    "num_windows",
    "func_time",
    "time_fraction_random_variability",
    "func_cycle",
    "fixed",
    "fixed_cycle",
    "continuous_duty_cycle",
    "occasional_use",
    "flat",
    "thermal_p_var",
    "pref_index",
    "wd_we_type",
    "name",
)

MAX_WINDOWS = 3
WINDOWS_PARAMETERS = ("window_1", "window_2", "window_3", "random_var_w")
DUTY_CYCLE_PARAMETERS = (
    ("p_11", "t_11", "cw11", "p_12", "t_12", "cw12", "r_c1"),
    ("p_21", "t_21", "cw21", "p_22", "t_22", "cw22", "r_c2"),
    ("p_31", "t_31", "cw31", "p_32", "t_32", "cw32", "r_c3"),
)
