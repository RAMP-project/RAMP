# RAMP Continuous Time Simulation Mode

## Overview

The continuous time simulation mode eliminates day-boundary discontinuities in RAMP load profiles. In the legacy mode, each day is generated independently with a fresh `np.zeros(1440)` array, causing unrealistic power drops at midnight. The continuous mode writes all days into a single shared array and allows switch-on events to naturally cross day boundaries.

## Quick Start

The only user-facing change is a single parameter:

```python
from ramp.core.core import UseCase

uc = UseCase(users=User_list, parallel_processing=False)
uc.initialize(peak_enlarge=0.15, num_days=10)

# Legacy mode (default, unchanged behavior)
profiles = uc.generate_daily_load_profiles(flat=True)

# Continuous mode — add continuous=True
profiles = uc.generate_daily_load_profiles(flat=True, continuous=True)
```

Both modes return identical output formats:
- `flat=True` → 1D array of shape `(num_days × 1440,)`
- `flat=False` → 2D array of shape `(num_days, 1440)`

All existing appliance definitions, windows, duty cycles, and post-processing code work without modification.

---

## How It Works

### The Problem

In legacy mode, each day's load profile is generated in isolation:

```
Day 0: [0 ──────── appliance events ────────── 0]  ← np.zeros(1440)
Day 1: [0 ──────── appliance events ────────── 0]  ← np.zeros(1440)
         ↑ gap                              gap ↑
```

Switch-on events cannot extend past minute 1440, and no events can start before minute 0. This creates exclusion zones near midnight where the probability of any appliance being active drops to zero.

### The Solution: Per-Day with Spillover

Continuous mode creates one global array of `num_days × 1440` minutes. Each day is still processed independently (preserving per-day randomization, duty cycles, and power values), but:

1. **Windows are projected** onto the global timeline via `day_offset = day_idx × 1440`
2. **Windows are extended** by `func_cycle` minutes past midnight (`spillover`)
3. **Events write into the global array** using `np.add.at()`, so switch-on events near midnight naturally extend into the next day

```
Global array: [0 ──── day 0 events ──→ spillover ──── day 1 events ──→ spillover ──── ...]
                                    ↑ no gap
```

### Midnight-Crossing Window Merge

Appliances with windows split across midnight (a common RAMP pattern) are automatically detected and merged:

```python
# User defines:
app.windows([1080, 1440], [0, 360])  # 6pm-midnight + midnight-6am

# Internally merged to:
# [1080, 1800]  (6pm to 6am as one continuous window)
```

This is handled by `Appliance._merge_midnight_crossing_windows()`.

### Duty Cycle Compatibility

Duty cycle windows (e.g., `cycle_behaviour([480, 1200], ...)`) are defined in daily-relative minutes `[0, 1440]`. Since switch-on events in continuous mode use global indexes (e.g., minute 7764), the duty cycle matching converts indexes to daily-local minutes via `% 1440` before comparison.

---

## Changes to `core.py`

### Modified Methods

| Method | Change |
|--------|--------|
| `UseCase.generate_daily_load_profiles()` | Added `continuous=False` parameter. When `True`, delegates to `_generate_continuous_profiles()` |
| `Appliance.rand_switch_on_window()` | Duty cycle window matching now uses `indexes % 1440` for compatibility with global indexes |

### New Methods

| Method | Purpose |
|--------|---------|
| `UseCase._generate_continuous_profiles()` | Creates the global `num_days × 1440` array and iterates users → user instances → appliances |
| `Appliance.generate_continuous_load_profile()` | Processes all days for one appliance, projecting windows with spillover and writing to the global array |
| `Appliance._merge_midnight_crossing_windows()` | Detects and merges legacy split-window patterns like `[1080, 1440] + [0, 360]` → `[1080, 1800]` |
| `Appliance._update_continuous_use()` | Writes switch-on event power values to the global array (mirrors `update_daily_use`) |

### Architecture Difference

```
Legacy:  days → users → user instances → appliances (per-day arrays)
Continuous:  users → user instances → appliances → days (shared global array)
```

In continuous mode, the outer loop is over users/appliances (not days), so each appliance can process all its days with awareness of the global timeline.

---

## Simulation Example

```python
from ramp.core.core import User, UseCase
from ramp.post_process import post_process as pp

# Define users and appliances (unchanged)
User_list = []
HI = User(user_name="high income", num_users=10, user_preference=3)
User_list.append(HI)

HI_indoor_bulb = HI.add_appliance(
    number=5.5, power=7, num_windows=2,
    func_time=600, time_fraction_random_variability=0.2,
    func_cycle=270, name="indoor_bulb",
)
HI_indoor_bulb.windows([1170, 1440], [0, 360], 0)

HI_Freezer = HI.add_appliance(1, 200, 1, 1440, 0, 30, "yes", 3, name="freezer")
HI_Freezer.windows([0, 1440], [0, 0])
HI_Freezer.specific_cycle_1(200, 20, 5, 10)
HI_Freezer.specific_cycle_2(200, 15, 5, 15)
HI_Freezer.specific_cycle_3(200, 10, 5, 20)
HI_Freezer.cycle_behaviour([480, 1200], [0, 0], [300, 479], [0, 0], [0, 299], [1201, 1440])

# Run simulation
uc = UseCase(users=User_list, parallel_processing=False)
uc.initialize(peak_enlarge=0.15, num_days=10)

# Generate continuous profiles
Profiles_list = uc.generate_daily_load_profiles(flat=False, continuous=True)

# Post-processing works identically
Profiles_avg, Profiles_list_kW, Profiles_series = pp.Profile_formatting(Profiles_list)
pp.Profile_series_plot(Profiles_series)
pp.Profile_cloud_plot(Profiles_list, Profiles_avg)
```

---

## Backward Compatibility

- **Default behavior is unchanged**: `continuous=False` is the default
- **No changes to appliance definition APIs**: All `add_appliance()`, `windows()`, `specific_cycle_*()`, and `cycle_behaviour()` calls work identically
- **Output format is identical**: Same shapes, same post-processing compatibility
- **Parallel processing**: Currently only available in legacy mode (`continuous=True` requires `parallel_processing=False`)

## Known Limitations

- **`parallel_processing=True`** is not supported with `continuous=True` — set `parallel_processing=False`
- **Spillover is one `func_cycle`**: Events can extend at most one duty cycle past midnight. For very long `func_cycle` values, this is adequate; for very short ones, the smoothing effect at boundaries is proportionally smaller
- The duty cycle `% 1440` conversion assumes duty cycle windows do not themselves cross midnight
