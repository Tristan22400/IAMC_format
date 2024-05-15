# IAMC_format

This repository is used to transform Wiliam's IAM data to the correct IAMC's format. A lot of work is still needed to convert all the variable in a correct way. 

## Add missing values in the programm. 

The following code enables everyone to transform the data for William to IAMC format in a partial way. 
To run correctly the code, you need to : 
- Export dataset with the Vensim application in csv or excel. You need to click on : On a separate colum in the export options. 
- Create the File_To_Convert folder 
- Put the file to convert inside. 
- Install the numpy and pandas dependencies if the running of the cell above is not working. 
- Run the following command line pip3 install pandas and pip3 install numpy 
- Extract the github repository on your computer. 
- Use the following command line to execute the notebook by replacing my mynotebook by the name of the file. jupyter nbconvert --to notebook --inplace --execute mynotebook.ipynb
- Run the variable_dict jupiter notebook to create the dictionaries used in the main file. 
- Put the file that you want to translate in the folder File_To_Convert
- Execute the Convert_Wiliam_result_IAMC to translate your file. 
- If you want to convert other file, follow the instructions for each file. Add the file to folder File_To_Convert and execute the Convert_Wiliam's file. 
- Once, you have translated on the file you want, you can run the merge_csv file with the same command line to merge all files in the Folder File_Converted.


