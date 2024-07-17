# IAMC_format


This repository is used to transform Wiliam's IAM data to the IAMC's format. There are some pending issues to solve and variables to be converted. 


## Add missing values in the program.

The following code enables everyone to transform the data for William to IAMC format in a partial way.
To run correctly the code, you need to :

- Export dataset with the Vensim application in csv or excel. You need to click on : On a separate colum in the export options.
- Extract the github repository on your computer.
- Open a terminal and go the Conversion-Script directory to move in the terminal, you can use the command line: cd filename
  To go back the command line is : cd ..
- Run the following command in your terminal : pip install -r requirements.txt
  If this is not working, you need to download Python on your computer and relaunch the command.
- Put the file that you want to translate in the folder File_To_Convert.
- Execute the Convert_Wiliam_result_IAMC to translate your file by writing the following command line in the terminal : python Convert_Wiliam_result_IAMC-format.py
  You need to be in the Conversion-Script directory to run the file.
- If you want to convert other file, follow the previous instructions for each file. Add the file to folder File_To_Convert and execute the Convert_Wiliam's file.
- Once, you have translated on the file you want, you can run the merge_csv file with the same command line to merge all files that are in the Folder File_Converted with the command line:
  python Merge_csv.py

Contributions :

If you want to contribute to the repository, please follow the following settings in VS Code settings:
{ "editor.defaultFormatter": "esbenp.prettier-vscode",

"[python]": {
"editor.formatOnSave": true,
"editor.defaultFormatter": "charliermarsh.ruff"
},
"editor.formatOnPaste": true,
"editor.formatOnSave": true}
