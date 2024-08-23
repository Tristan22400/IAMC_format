# IAMC_format


This repository is used to transform Wiliam's IAM data to the IAMC's format. There are some pending issues to solve and variables to be converted. 


## Add missing values in the program.

The following code enables everyone to transform the data for William to IAMC format in a partial way.
To run correctly the code, you need to :

- Export dataset with the Vensim application in csv or excel. You need to click on : On a separate colum in the export options.
- Extract the github repository on your computer.
- Open a terminal and go the directory of the project to move in the terminal, you can use the command line: cd filename
  To go back the command line is : cd ..
- Run the following command in your terminal to install the required Python packages : conda env create -f environment.yaml

- Go on the Final_script folder by using the cd command. 
- Put the file that you want to translate in the folder File_To_Convert create it if it does not exist.
- Execute the translation.py file to translate your file by writing the following command line in the terminal : python translation.py
If you want to create an automatic report of the scenario. you can run the following command: python translation.py --arguments report. 


The execution of translation.py file will create three files at least: 
- The file of the translated variable with the data called scenario_name_converted.csv
- The variable_name_change_dict.txt which are giving you a dictionary which associated all the variable in Wiliam that are not translated with their translation if they are in the Variable_IAMC.xlsx otherwise it shows the name in Wiliam. It corresponds to only variables not translated and not the subscript added.
- The new_variable_name_dict.txt which are giving you a dictionary which associated all the variables gather with the subscripts to the variable's name of Wiliam gather with the subscripts translated to IAMC_format. The names of Wiliam's variable are not translated. 

If you want to translate the names of variables in Wiliam, you can change it manually or you can change automacally with the variable_name_change_dict.txt by running the following command line. python translation_helpers.py

If you want to convert other file, follow the previous instructions for each file. Add the file to folder File_To_Convert and follow the previous step.


UPDATE and CHECK of the different dictionaries. 

- If you want to update the aggregation dictionary or the translation dict, you need to run the update_dict.py with the argument aggregation or variable according to the dict you want to modify.
The command line is then python update_dict.py --arguments aggregations  or  python update_dict.py --arguments variables.
- If you want to change a variable that is already defined, you can force the update of both dictionaries by running the following command line. 
python update_dict.py --arguments aggregations,forced or python update_dict.py --arguments variables,forced
- If you want to update without overwriting then you need to run the update_dict.py with the following command. 
python update_dict.py --arguments aggregations,check

You should know that the update even forced is only possible if the naming of the variable are correct. 

You can also use the translation_helpers to change only the variable 

The Visualization folder

This folder contains a lot of examples of usual plot that you could want to do. You just need to go on the graph you want to do and select among the type of graph available. 
If the ones, you are searching for is not present in the documentation, you can go to the documentation of pyam. 
https://pyam-iamc.readthedocs.io/en/stable/

The matplotlib documentation can also be consulted if you want to change the esthetic of the plot. https://pyam-iamc.readthedocs.io/en/stable/

Contributions :

If you want to contribute to the repository, please follow the following settings in VS Code settings:
{
"[python]": {
"editor.formatOnSave": true,
"editor.defaultFormatter": "charliermarsh.ruff"
},
"editor.formatOnPaste": true}
