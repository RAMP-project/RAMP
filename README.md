<img src="/docs/figures/RAMP_logo_basic.png" width="300">

*An open-source bottom-up stochastic model for generating multi-energy load profiles.*

---

## Overview
RAMP is a bottom-up stochastic model for the generation of high-resolution multi-energy profiles, conceived for application in contexts where only rough information about users' behaviour are obtainable. Those may range from remote villages to whole countries.

<img src="/docs/figures/Example_output.jpg" width="700">

The source-code is currently released as v0.3.1. It is not yeat accompained by a detailed documentation, but the Python code is fully commented in each line to allow a complete understanding of it. Further details about the conceptual and mathematical model formulation are provided in the related Journal publication (https://doi.org/10.1016/j.energy.2019.04.097). Check out also the [release history](CHANGELOG.md) to see how the code evolved over time.

Furthermore, you can join our **[Gitter chat](https://gitter.im/RAMP-project/community)** to discuss doubts and make questions about the code!

The repository also hosts all the input files used to generate the profiles appearing in the abovementioned study, which may be also used as a reference example. To access the code version used for the Journal publication, select the tag "v.0.1-pre".
An up-to-date list of publications featuring RAMP, for a variety of applications, is available [here](/docs/pubs_list.md).

## Requirements
The model is developed in Python 3.6, and requires the following libraries:
* numpy
* matplotlib
* math
* random

## Quick start
To get started, download the repository and simply run the "ramp_run.py" script. The console will ask how many profiles (i.e. independent days) need to be simulated, and will provide the results based on the default inputs defined in `input_file_x`.py. To change the inputs, just modify the latter files. Some guidance about the meaning of each input parameter is available in the `core.py` file, where the *User* and *Appliance* Python classes are defined and fully commented. 

### Example input files
Three different input files are provided as example representing three different categories of appliancces that can be modelled with RAMP.

- `input_file_1.py`: represents the most basic electric appliances, is an example of how to model lightbulbs, radios, TVs, fridges, and other electric appliances. This input file is based on the ones used for [this publication](https://doi.org/10.1016/j.energy.2019.04.097).

- `input_file_2.py`: shows how to model thermal loads, with the example of a "shower" appliance. The peculiarity of thermal appiances is that the nominal power can be provided as external input as a "csv" file (in this case, `shower_P.csv`). For the example "shower" appliance, the varying nominal power accounts for the effect of groundwater temperature variation throughout the year. This input file is based on that used for [this publication](https://doi.org/10.3390/app10217445).

- `input_file_3.py`: represents an example of how to model electric cooking appliances. In this input file two different kind of meals are modelled: 1) short and repetitive meals (e.g. breakfast); and 2) main meals (e.g. lunch, dinner). 
Repetitive meals do not vary across days, whilst main meals do so. In particular, every household can randomly choose between 3 different types of main meal every day. Such variability in meal preferences is modelled by means of two parameters: the `user preference` and the `preference index`. 
The `user preference` defines how many types of meal are available for each user to choose every day (e.g. 3). Then, each of the available meal options is modelled separately, with a different `preference index` attached. The stochastic process randomly varies the meal preference of each user every day, deciding whether they want a "type 1" meal, or a "type 2", etc. on a given day.
This input file is used in [this publication](https://doi.org/10.1109/PTC.2019.8810571)

## Citing
Please cite the original Journal publication if you use RAMP in your research:
*F. Lombardi, S. Balderrama, S. Quoilin, E. Colombo, Generating high-resolution multi-energy load profiles for remote areas with an open-source stochastic model, Energy, 2019, https://doi.org/10.1016/j.energy.2019.04.097.*

## Contribute
This project is open-source. Interested users are therefore invited to test, comment or contribute to the tool. Submitting issues is the best way to get in touch with the development team, which will address your comment, question, or development request in the best possible way. We are also looking for contributors to the main code, willing to contibute to its capabilities, computational-efficiency, formulation, etc. 

To contribute changes:
- Fork the project on GitHub
- Create a feature branch (e.g. named "add-this-new-feature") to work on in your fork
- Add your name to the [AUTHORS](AUTHORS) file
- Commit your changes to the feature branch
- Push the branch to GitHub
- On GitHub, create a new pull request from the feature branch

When committing new changes, please also take care of checking code stability by means of the [qualitative testing](CONTRIBUTING.md) functionality.

## License
Copyright 2019 RAMP, contributors listed in **Authors**

Licensed under the European Union Public Licence (EUPL), Version 1.2-or-later; you may not use this file except in compliance with the License. 

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License
