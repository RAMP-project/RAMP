---
title: 'RAMP: stochastic simulation of user-driven energy demand time series'
tags:
  - Python
  - energy demand
  - stochastic
  - time series
  - synthetic data
authors:
  - name: Francesco Lombardi
    orcid: 0000-0002-7624-5886
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: 1
  - name: Pierre-François Duc
    orcid: 
    affiliation: 2
  - name: Mohammad Amin Tahavori
    orcid: 0000-0002-7753-0523
    affiliation: 3
  - name: Claudia Sanchez-Solis
    orcid: 0000-0003-2385-7392
    affiliation: "4,7"
  - name: Sarah Eckhoff
    orcid: 0000-0002-6168-4835
    affiliation: 5  
  - name: Maria C.G. Hart
    orcid: 0000-0002-1031-9782
    affiliation: 5  
  - name: Francesco Sanvito
    orcid: 0000-0002-9152-9684
    affiliation: 1
  - name: Gregory Ireland
    orcid: 
    affiliation: "2,6"
  - name: Sergio Balderrama
    orcid: 
    affiliation: 7
  - name: Sylvain Quoilin
    orcid: 
    affiliation: 4
affiliations:
 - name: TU Delft, Faculty of Technology, Policy and Management, Delft, The Netherlands
   index: 1
 - name: Reiner Lemoine Institut, Berlin, Germany
   index: 2
 - name: VITO, Mol, Belgium
   index: 3
 - name: University of Liège, Integrated and Sustainable Energy Systems, Thermodynamics Laboratory, Liège, Belgium
   index: 4
 - name: Leibniz Universität Hannover, Information Systems Institute, Hannover, Germany
   index: 5
 - name: University of Cape Town, Cape Town, South Africa
   index: 6
 - name: Universidad Mayor de San Simon, Centro Universitario de Investigacion en Energias, Cochabamba, Bolivia
   index: 7
date: 6 December 2023
bibliography: paper.bib

---

# Summary

The urgency of the energy transition is leading to a rapid evolution of energy system design worldwide. In areas with widespread energy infrastructure, existing electricity, heat and mobility networks are being re-designed for carbon neutrality and are increasingly interconnected. In areas where energy infrastructure is limited, instead, networks and systems are being rapidly expanded to ensure access to energy for all. And yet, re-designing and expanding energy systems in these directions requires information on future user behaviour and associated energy demand, which is often unavailable. In fact, historical data are either entirely missing or poorly representative of future behaviour within transitioning systems. This results in the reliance on inadequate demand data, which affect system design and its resilience to rapid behaviour evolution.

# Statement of need

RAMP is an open-source, Python-based software suite that enables the stochastic simulation of any user-driven energy demand time series based on few simple inputs. In fact, the software is designed to require only a basic understanding of the expected user activity patterns and owned appliances as inputs, to be provided in tabular (`.xlsx`) format. Then, it leverages stochasticity (using the `random` package) to make up for the lack of more detailed information and to account for the unpredictability of human behaviour (see Figure \ref{fig:example}). This way, RAMP allows generating and visualising synthetic data wherever metered data does not exist, such as when designing systems in remote areas [@lombardi_generating:2019] or when looking at future electric-vehicle fleets [@mangipinto_impact:2022]. Moreover, it features several degrees of customisations, allowing users to explicitly simulate radically different but equally plausible behaviour scenarios as a key ingredient to robust system design.

RAMP has already been used in many scientific publications, for instance, for the simulation of electricity [@dimovski_holistic:2023], heating [@stevanato_modeling:2020], cooking [@stevanato_long-term:2020] and electric mobility [@secchi_smart:2023] demand time series at scales ranging from districts [@pasqui_new:2023] or villages [@villarroel-schneider_open-source:2023] to continents [@pickering_diversity:2022]. It has dozens of users globally and has recently become a multi-institution software development effort, actively contributed by TU Delft, VITO, Sympheny, the Reiner Lemoine Institut, the University of Liège and the Leibniz University Hannover. The joint development process has brought major improvements to the code structure, syntax and efficiency, more extensive documentation, and a web-based graphical user interface for users with no Python experience [@hart_gui:2023].

RAMP is developed openly on GitHub [@ramp_github] and each new release is archived on Zenodo [@ramp_zenodo:2023].

![Example output (normalised by peak demand) for the simulation of the electricity load of three households in a small village over five days. The thick blue line represents the five-day average, while individual days are plotted in a lighter colour. \label{fig:example}](example_output.png)

# References