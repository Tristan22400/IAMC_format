# IAMC_format

This repository is used to transform Wiliam's IAM data to the correct IAMC's format. A lot of work is still needed to convert all the variable in a correct way. 

## Add missing values in the programm. 

The following code enables everyone to transform the data for William to IAMC format in a partial way. 
To run correctly the code, you need to : 
-Exort dataset with the Vensim application in csv or excel. You need to click on : On a separate colum in the export options. 
- Create the File_To_Convert folder 
- Put the file to convert inside. 
- Install the numpy and pandas dependencies if the running of the cell above is not working. 
 - Run the following command line pip3 install pandas and pip3 install numpy 
- Put the scenario name as input after running the third cell. 
- Create a folder named Variable_Reference with two files, one called reference.xlsx which correspond to the variable used in IPCC work and another called Variable_name_IAMC.xlsx which corresponds to the translation  of William's name to IAMC's format. It is still under review and needs to be thought again. Only certain variable are translated to IAMC's format. 
