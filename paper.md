---
title: 'wiliamcformat: A Python tool to process and standardize WILIAM outputs'
tags:
    - Python
	- WILIAM
	- Report
	- IAMC format
authors:
    - name: Gonzalo Parrado-Hernando
	  corresponding: true
	  orcid: 0000-0001-9835-4680
	  equal-contrib: true
	  affiliation: "1, 2" 
	- name: Tristan Martin
	  orcid:
	  equal-contrib: true
	  affiliation: 3
	- name: Juan Pérez-Marcos
	  equal-contrib: true
	  affiliation: "1, 4"
affiliations:
    - name: Group of Energy, Economy, and System Dynamics, University of Valladolid, Spain
	  index: 1
	- name: Department of System Engineering and Automation, School of Industrial Engineering, University of Valladolid, Spain
	  index: 2
	- name: Ecole des Ponts ParisTech, Paris, France
	  index: 3
	- Department of Applied Economics, University of Valladolid, Spain
	  index: 4
date: 16 July 2024
bibliography: paper.bib
---

# Summary
The international scientific community assessing on climate change and mitigation scenarios requests standardization and 
harmonization of results in integrated assessment models to:
    - ensure full transparency about the origin and structure of data.
	- facilitate the comparison across models in both the historical period and future scenarios.
	- discuss on conceptual ideas about the internal structure of models, so to what extent different models representing 
	  the same system deliver different results. 

Results from different measurement procedures for the same measure should be equivalent (harmonized) within stated specifications 
to measure uncertainty. A task that is already mandatory to contribute on high-level international reports such as those elaborated 
by the Intergovernmental Pannel of Climate Change (IPCC) while necessary in the daily work of collaborative projects where different 
tools are applied to solve the same research question. The present work aims to adapt and extend the potential of existing material 
for users of a novel integrated assessment model, WILIAM. A pending task that has not been documented before although the urgency 
for improving transparency and responsability of this model to meet open-science principles (FAIR [@Wilkinson2016] and TRUST 
[@Lin2020]), as well as usability. Furthermore, we hope the contents will help to move students closer to climate change science.


# Statement of need
Integrated assessment models (IAMs) have been used for a wide range of problems in the climate change field. From generating 
consensus to identify key parameters and complex feedbacks on future between the world economies and nature [@Sarofim2011]. 
However, [@Wilson2021] highlight that IAM evaluation should improve interpretability of results to communicate insights, credibility 
as producers of knowledge under a 'sceptical review', and relevance of modelling analysis for informing scientific understanding 
to policymakers and stakeholders. A challenge that may be achieved (at least partially) with model inter-comparisons, which are 
mostly used to compare outputs and insights to explore uncertainties, and diagnostics, which proposes descriptive indicators 
to explain characteristics of the performance in terms of model structure and assumptions.

The demand from model inter-comparison projects (MIPs) is a fruitful enterprise [@EdNature2015]. Recently, [@Nikas2021] identified 
several MIPs and inter-comparison studies. An emerging practice in the field of IAMs that will surely place these tools at the same 
level of reliability than climate and energy models. To overcome the limitations, the IAM Consortium and the International Institute 
for Applied Systems Analysis (IIASA) started with a common standard, the IAMC format [@IAMCformatIIASA] and a plotting module to 
play with timeseries called *pyam* [@Huppmann2021]. Some prominent studies using the IAMC format have been recently mentioned by 
[@Claudia2024] including IPCC reports and milti-IAM studies.

Additionally, despite the importance of climate change education[^1] in responding to the impacts of climate change, [@Filho2023] 
identified *less attention given to systematically assessing the attitude, perceptions, and practices of students and the integration *
*of the climate topic in the higher education institutions’ curricula and co-curricular activities in a way that may guide changes *
*in the curriculum and teaching practices*. Consequently, we also aim to contribute to education, bring students closer to the climate 
change problems through playing with the present code in Python lessons. For example, the University of Valladolid currently has Python 
as mandatory subject in the official courses of sciences and engineering. 

[^1] Climate change education refers to curricular contents deployed to increase awareness on climate change [@Filho2023].

We have replicated the structure proposed by [@Claudia2024] for explaining the contents because of proximity of GCAM and WILIAM (both 
are IAMs) and shared inter-comparison experience in the project called IAM COMPACT (see acknowledgements). It is helpful to also 
compare and develop similarities of both tools.

WILIAM is a nascent system dynamics policy-simulation model, descendent from the MEDEAS model [@capellan2020], which purpose is to 
capture the socioeconomic implications of the energy transition(s) accounting for biophysical constraints. Although there are some 
articles published, standardization and harmonization is yet missing so a potential improvement to better present results and increase 
the transparency of the overall research activity with it. To do it properly, we have developed *wiliamcformat*, a python package that 
translates WILIAM outputs to IAMC format timeseries for linking results with the existing aPython library called pyam, supported by 
IIASA. Standarization, harmonization and visualization in a unique code for WILIAM users.

# Functionality
This section describes the code with a short example to easily follow the whole workflow.

## A brief description

## Notes about the architecture

# Acknowledgements

G.P. and J.P. acknowledge financial support from the European Union's Horizon research program under grant agreement 101056306 (IAM COMPACT project).

# References