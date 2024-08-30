import numpy as np
import pandas as pd
import os
import ast
import pyam
import matplotlib.pyplot as plt
import argparse
import translation_helpers

#################################
# Functions used in this script #
#################################

def create_folder_if_not_exists(folder_name):
    # Get current folder
    folder_path = os.getcwd()

    if not os.path.exists(os.path.join(folder_path, folder_name)):
        os.makedirs(folder_name)
        print("Folder '{}' created.".format(folder_name))
    else:
        print("Folder '{}' already exists.".format(folder_name))

# Get the paths of files to be translated
def get_path_files(folder_path):
    # Get a list of all files in the folder
    filenames = os.listdir(folder_path)

    # Filter Excel and CSV files
    files_path = [
        os.path.join(folder_path, filename)
        for filename in filenames
        if filename.endswith(".xlsx") or filename.endswith(".xls") or filename.endswith(".csv")
    ]

    if not files_path:
        print("No files found in the folder.")
        return None  # No Excel files found
  
    # Return the paths to the Excel files
    return files_path

# Function to open a dictionary
def open_dict(dict_filename):
    # Open the text file containing the dictionary
    try: 
        with open("Create_Variable_Dict/" + dict_filename, "r") as f:
            # Read the contents of the file
            read_dict_str = f.read()

        # Convert the string representation of the dictionary back to a dictionary object
        read_dict = ast.literal_eval(read_dict_str)
    except Exception:
        print("Error during opening the dictionary file:", dict_filename)
        read_dict = dict()
    return read_dict

# Aggregate the subscripts at the end of the variable
def aggregate_subscript_variable_name(row, counter, existing_country_Wiliam_dict, country_dict):
    for k in range(counter):
        subscript = row["Subscript " + str(k)]

        if k == 0:
            if existing_country_Wiliam_dict.get(subscript) == 1:
                # Give the name of the region for that variable
                row["Region"] = country_dict.get(subscript)

                row["Subscript 0"] = np.nan
                continue

        if not pd.isnull(subscript):
            row["Variable"] = row["Variable"] + "|" + subscript

    return row

# Function to replace and track missing values
def replace_and_track(row, variable_name_dict,missing_variable):
    # If it exists, get the name translated to IAMC format. 
    translation_name = variable_name_dict.get(row["Variable"], None)

    if translation_name:
        # Modify the row to provide the IAMC-format name
        row["Variable"] = translation_name
        # Turn to "True" to verify the translation in the dataframe
        row["Translation"] = True
        return row
    else:
        # Add the missing variable to the list of untranslated variable. 
        missing_variable.append(row["Variable"])
        return row

# Function to create the aggregations per row
def aggregate_rows(df, aggregations):
    # List of new rows
    new_rows = []
    # Get the list of all regions
    regions = df['Region'].unique()

    for region in regions:
        # Filter the dataframe on the actual region
        df_region = df[df['Region'] == region]
        for names, new_name in aggregations.items():
            # Check if all the names are present
            if all(name in df_region["Variable"].values for name in names):
                # Filter the dataframe with the names of interest
                df_subset = df_region[df_region["Variable"].isin(names)]

                # Compute the sum of the aggregation of the value
                summed_values = df_subset.drop(columns=["Variable", "Unit", "Model", "Scenario", "Region"]).sum()

                # Create the new aggreagted rows
                new_row = {
                    "Model": df_subset["Model"].iloc[0],
                    "Scenario": df_subset["Scenario"].iloc[0],
                    "Region": region,
                    "Variable": new_name,
                    "Unit": df_subset["Unit"].iloc[0],
                    ** summed_values.to_dict(),
                }
                new_rows.append(new_row)

    # Create a dataframe with the new rows
    new_df = pd.DataFrame(new_rows)

    # Concatenate the two dataframe to get the aggregated rows
    df_final = pd.concat([df, new_df], ignore_index=True)

    return df_final

###############
# Main script #
###############

def main():
    # Parse the argument put in the command line. 
    parser = argparse.ArgumentParser()
    parser.add_argument("--arguments", help="insert argg")
    args = parser.parse_args()

    # Folders with input and output files
    folder_name_to_convert = "File_To_Convert"
    folder_name_converted = "File_Converted"

    # Get current folder
    folder_path = os.getcwd()
    
    # Get the path where input files are located
    folder_path_input_files = os.path.join(folder_path, folder_name_to_convert)
    
    # Get the paths of the input files
    files = get_path_files(folder_path_input_files)

    # Print the name of the files to be translated
    print("Files to translate:")
    for f in files:
        print(os.path.basename(f))
    
    # Get the name and extension of the files to be converted
    files_name_extension = [os.path.splitext(os.path.basename(f)) for f in files]

    # Scenarios are the name of original files
    scenarios = [os.path.splitext(os.path.basename(f))[0] for f in files]

    # Read the files
    index = 0
    df_original = {}
    while index < len(files):
        if (
            files_name_extension[index][1] == ".xls"
            or files_name_extension[index][1] == ".xlsx"
        ):
            df_original[scenarios[index]] = pd.read_excel(files[index], low_memory=False)
        elif files_name_extension[index][1] == ".csv":
            df_original[scenarios[index]] = pd.read_csv(files[index], low_memory=False)
        index += 1
    
    # Remove duplicated rows in the file.
    df_duplicates_removed = {}
    for scen in scenarios:
        df_duplicates_removed[scen] = df_original[scen].drop_duplicates().copy()

    # Rename the column of the file
    for scen in scenarios:
        columns = df_duplicates_removed[scen].columns.str.replace("Unnamed:", "Subscript")
        columns = columns.str.replace(".", " ")
        
        # Define the string you want in column names
        search_string = "Subscript"
        counter = 0

        for k in range(len(columns)):
            if search_string in columns[k]:
                columns.values[k] = search_string + " " + str(counter)
                counter += 1

    for scen in scenarios:
        # Rename columns of subscripts ("Unnamed: X" by "Subscipt X")
        my_dict = {k: v for k, v in zip(df_duplicates_removed[scen].columns[2:6], columns[2:6])}
        
        df_duplicates_removed[scen].rename(columns=my_dict, inplace=True)

        # Rename other columns
        df_duplicates_removed[scen].rename(
        columns={"Time": "Variable", "Year": "Unit", "Subscript": "Subscript 0"},
        inplace=True
        )

    # Insert three columns to define the model, scenario and region in the right place for IAMC format
        if "Model" not in df_duplicates_removed[scen].columns:
            df_duplicates_removed[scen].insert(0, "Model", "WILIAM")
        if "Scenario" not in df_duplicates_removed[scen].columns:
            df_duplicates_removed[scen].insert(1, "Scenario", scen)
        if "Region" not in df_duplicates_removed[scen].columns:
            df_duplicates_removed[scen].insert(2, "Region", "World")
        

    # Merge all files into one
    df_merged = pd.concat(df_duplicates_removed.values(), ignore_index=True)

    # Management of regions from WILIAM to IAMC format
    # Dict used to check if the subscripts is a region used in Wiliam. 
    existing_country_Wiliam_dict = {
        "EU27": 1,
        "UK": 1,
        "CHINA": 1,
        "EASOC": 1,
        "INDIA": 1,
        "LATAM": 1,
        "RUSSIA": 1,
        "USMCA": 1,
        "LROW": 1,
        "AUSTRIA": 1,
        "BELGIUM": 1,
        "BULGARIA": 1,
        "CROATIA": 1,
        "CYPRUS": 1,
        "CZECH_REPUBLIC": 1,
        "DENMARK": 1,
        "ESTONIA": 1,
        "FINLAND": 1,
        "FRANCE": 1,
        "GERMANY": 1,
        "GREECE": 1,
        "HUNGARY": 1,
        "IRELAND": 1,
        "ITALY": 1,
        "LATVIA": 1,
        "LITHUANIA": 1,
        "LUXEMBOURG": 1,
        "MALTA": 1,
        "NETHERLANDS": 1,
        "POLAND": 1,
        "PORTUGAL": 1,
        "ROMANIA": 1,
        "SLOVAKIA": 1,
        "SLOVENIA": 1,
        "SPAIN": 1,
        "SWEDEN": 1,
    }

    # Open the text file containing the country dictionary to translate the country name of Wiliam to the IAMC format.
    country_dict = open_dict("country_dict.txt")

    # Order the subscript of each variable and give the right region to each row
    df_subscripts = df_merged.apply(
        aggregate_subscript_variable_name, args=(counter, existing_country_Wiliam_dict, country_dict),axis=1)

    # Remove the subscript columns once they have been alreday added at the end of the variable name
    drop_columns_list = ["Subscript " + str(k) for k in range(counter)]

    df_subscripts.drop(columns=drop_columns_list, inplace=True)

    # Open the text file containing the dictionary to translate each variable name of Wiliam to IAMC format.
    variable_name_dict = open_dict("variable_name_dict.txt")

    # Create a list to save  the variables with a missing translation.
    missing_variable = []

    # Create a new column in the dataframe for selecting translated variables
    df_subscripts['Translation'] = False

    # Apply the translation function of the variable name's column to respect the IAMC format
    df_variables_translated = df_subscripts.apply(
        replace_and_track, args=(variable_name_dict, missing_variable), axis=1
    )

    # Remove the untranslated variable of the dataframe
    df_variables_translated = df_variables_translated.loc[df_variables_translated.Translation,:]

    # Create the aggregations rows in the dataframe
    # Open the text file containing the aggregation dictionary
    aggregation_dict = open_dict("aggregation_dict.txt")

    # Apply the function to sum values of aggregations 
    df_aggregations = aggregate_rows(df_variables_translated, aggregation_dict)

    # Create the path for the file containing the missing variable
    print("The translation of ", len(missing_variable),
        " variables are missing. You can find all the translation in the file called new_variable_name_dict.txt")

    # Process the automatic translation of missing variables. 
    translation_helpers.create_automatic_translation(missing_variable)

    # Write the new excel file in the File_Converted folder
    folder_file_converted = os.path.join(folder_path, folder_name_converted)

    # Create the correct naming and extension (Excel or CSV) for the converted file
    filename_output = ("Results_converted" + files_name_extension[0][1])

    # Check for duplicate rows
    duplicate_rows = df_aggregations[
        df_aggregations.duplicated(subset=["Region", "Scenario", "Variable", "Unit"])
    ]

    # Count the number of duplicate rows. Normally we should find zero duplicates.
    num_duplicated_rows = duplicate_rows.shape[0]
    if num_duplicated_rows > 0:
        print("Number of Duplicate Rows:", num_duplicated_rows)

    # Remove duplicate rows
    df_aggregations.drop_duplicates(subset=["Region", "Scenario", "Variable", "Unit"], inplace=True)
    
    df_final_output = df_aggregations.copy()

    # Create new folder
    create_folder_if_not_exists(folder_file_converted)

    # Write the following dataframe to excel or CSV
    if (
        files_name_extension[0][1] == ".xls"
        or files_name_extension[0][1] == ".xlsx"
    ):
        df_final_output.to_excel(os.path.join(folder_file_converted, filename_output))
    elif files_name_extension[0][1] == ".csv":
        df_final_output.to_csv(
            os.path.join(folder_file_converted, filename_output), index=False
        )

    print("Conversion Done")

    # Structure to check the existance of the file
    try:
        scenario_df = pyam.IamDataFrame(
            os.path.join(folder_file_converted, filename_output)
    )
         # This defines the model and scenario used for the report
        args = dict(model="WILIAM", scenario=scenarios[0])
        
    except Exception:
        print("ERROR opening the file with results in IAMC format")
        exit()



if __name__ == "__main__":
    main()

