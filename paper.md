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
	- name: Department of Applied Economics, University of Valladolid, Spain
	  index: 4
date: 16 July 2024
bibliography: paper.bib
---

# Summary
The international scientific community assessing on climate change and mitigation scenarios requests standardization and harmonization of results in integrated assessment models to: ensure full transparency about the origin and structure of data; facilitate the comparison across models in both the historical period and future scenarios; and discuss on conceptual ideas about the internal structure of models, so to what extent different models representing the same system present similar results and conclusions.

Results from different measurement procedures for the same measure should be equivalent (harmonized) within stated specifications to measure uncertainty. A task that is already mandatory to contribute on high-level international reports such as those elaborated by the Intergovernmental Pannel of Climate Change (IPCC) while necessary in the daily work of collaborative projects where different tools are applied to solve the same research question. The present `wiliamcformat` library aims to adapt and extend the potential of existing material for users of a novel integrated assessment model, WILIAM. A pending task that has not been documented before although the urgency for improving transparency and responsability of this model to meet open-science principles (FAIR [@Wilkinson2016] and TRUST [@Lin2020]), as well as usability. Furthermore, we hope that these materials will inspire students to engage move deeply with the science of climate change and social transitions.


# Statement of need
Integrated assessment models (IAMs) have been used for a wide range of problems in the climate change field. From generating consensus to identify key parameters and complex feedbacks on future between the world economies and nature [@Sarofim2011]. However, [@Wilson2021] highlight that IAM evaluation should improve interpretability of results to communicate insights, credibility as producers of knowledge under a 'sceptical review', and relevance of modelling analysis for informing scientific understanding to policymakers and stakeholders. A challenge that may be achieved (at least partially) with model inter-comparisons, which are mostly used to compare outputs and insights to explore uncertainties, and diagnostics, which proposes descriptive indicators to explain characteristics of the performance in terms of model structure and assumptions.

The demand from model inter-comparison projects (MIPs) is a fruitful enterprise [@EdNature2015]. Recently, some authors [@Nikas2021] identified several MIPs and inter-comparison studies. An emerging practice in the field of IAMs that will surely place these tools at the same level of reliability than climate and energy models. To overcome the limitations, the IAM Consortium and the International Institute for Applied Systems Analysis (IIASA) started with a common standard, the IAMC format [@IAMCformatIIASA] and a plotting module to play with timeseries called *pyam* [@Huppmann2021]. Some prominent studies using the IAMC format have been recently identified by [@Claudia2024] including IPCC reports and multi-IAM studies.

Additionally, despite the topic of climate change is being introduced in educational curriculum, [@Filho2023] identified *less attention given to systematically assessing the attitude, perceptions, and practices of students and the integration of the climate topic in the higher education institutions’ curricula and co-curricular activities in a way that may guide changes in the curriculum and teaching practices*. Consequently, we also aim to contribute here, inspiring students to engage with climate change problems when they are learning Python lessons. 

WILIAM is a nascent system dynamics policy-simulation model, descendent from the MEDEAS model [@capellan2020], which purpose is to capture the socioeconomic implications of the energy transition(s) accounting for biophysical constraints. Although there are some articles published, standardization and harmonization is yet missing so a potential improvement to better present results and increase the transparency of the overall research activity with it. To do it properly, we have developed `wiliamcformat`, a python package that translates WILIAM outputs to IAMC format timeseries for linking results with the existing aPython library called pyam, supported by IIASA. Standarization, harmonization and visualization in a unique code for WILIAM users.

# Functionality
This section describes the code with a short example to easily follow the whole workflow.

## A brief description

The `wiliamcformat` package is public, available at the domain https://github.com/Tristan22400/IAMC_format. Following the next steps (more detailed in the *README.md* file), the user can obtain the results of WILIAM under the IAMC format criteria and plot results in a general report or customized graphs.

The user can follow the next steps to install a stable version of the code and play with examples:

1. Download the package and unzip it.
2. Open the terminal and go to the folder containing the package.
3. (optional) We recommend the creation of a virtual environment to avoid uncompatible dependencies across Python packages with new updates. To do it, the easiest way is to open the anaconda prompt and run `conda env create -f environment.yaml` to install all the dependencies required automatically. You can check the available environments in your computer by typing `conda env list`, and activate it by typing `conda activate wiliamcformat`.
3. Place the files with the WILIAM results (CSV and Excel formats are allowed) into the folder *File_To_Convert*. *Example.csv* is a real simulation of WILIAM with results with which anyone can play. 
3. Execute the file *translation.py* to translate all the simulations into the same file formatted with IAMC criteria. The output file is named (`Results_Converted`) in folder *File_Converted*.

## Notes about the architecture

The `wiliamcformat` package is built upon a suit of tools and functions provided by the `pyam` project. This project uses well-known libraries such as `pandas` and `plotly` to manage and visualize the data. So, results in WILIAM may be enriched with new updates in the aforementioned packages. `wiliamcformat` is structured in two blocks:
- Translation of WILIAM variables into IAMC standards.
- Notebooks to facilitate the reporting and visualization of data.

The user can download WILIAM in two languages, Python (https://github.com/LOCOMOTION-h2020/pywiliam) and Vensim (https://github.com/LOCOMOTION-h2020/WILIAM_model_VENSIM), and generate the CSV file of a simulation. Both tools were developed during the European H2020 Locomotion project (Grant Agreement number 821105). 

Regarding the translation, the notebook named *translation.ipynb* explains every step easily to learn the code. The translation is supported by dictionaries (folder *Create_Variable_Dict*) to solve the equivalence between the dimensions of WILIAM variables (subscripts in Vensim software) and the specific IAMC format. In the same folder, the file *Variable_name_IAMC.xlsx* facilitates the translation of WILIAM variable names. The code automatically builds the correspoinding name list called *variable_name_dict.txt*. Missing variables during the translation process are tracked in file *list_missing_variable.txt* to correct them in a second translation round. 

Finally, several notebooks are available in the folder *Visualization* to facilitate the learning process, including a general report with principal variables of the model, as well as specific examples of customizable plots.

# Acknowledgements

G.P. and J.P. acknowledge financial support from the European Union's Horizon research program under grant agreement 101056306 (IAM COMPACT project).

# References