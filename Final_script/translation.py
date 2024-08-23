import numpy as np
import pandas as pd
import os
import ast
import pyam
import matplotlib.pyplot as plt
import report_pdf
import argparse
import translation_helpers



def get_last_added_file(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Filter Excel and CSV files
    excel_files = [
        file
        for file in files
        if file.endswith(".xlsx") or file.endswith(".xls") or file.endswith(".csv")
    ]

    if not excel_files:
        return None  # No Excel files found
    print()
    # Sort files by modification time (newest first)
    excel_files.sort(
        key=lambda x: os.path.getctime(os.path.join(folder_path, x)), reverse=True
    )

    # Return the path to the last added Excel file
    return os.path.join(folder_path, excel_files[0])


def create_folder_if_not_exists(folder_name):
    # Get current folder
    folder_path = os.getcwd()

    if not os.path.exists(os.path.join(folder_path, folder_name)):
        os.makedirs(folder_name)
        print("Folder '{}' created.".format(folder_name))
    else:
        print("Folder '{}' already exists.".format(folder_name))


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

# Function to replace values and track missing ones
def replace_and_track(row, variable_name_dict,missing_variable):

    # Get the name translated if it exists. 
    translation_name = variable_name_dict.get(row["Variable"], None)

    if translation_name:
        # Modify the row to give it the correct translation
        row["Variable"] = translation_name
        row["Translation"] = True
        return row
    else:
        # Add the missing variable to the list of untranslated variable. 
        missing_variable.append(row["Variable"])
        return row

# Function to create the aggregations of each row
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

def open_dict(dict_filename):
    # Open the text file containing the dictionary
    try: 
        with open("../Create_Variable_Dict/" + dict_filename, "r") as f:
            # Read the contents of the file
            read_dict_str = f.read()

        # Convert the string representation of the dictionary back to a dictionary object
        read_dict = ast.literal_eval(read_dict_str)
    except Exception:
        read_dict = dict()
    return read_dict

def create_report(scenario_df, args):
    # Create instance of FPDF class
    pdf = report_pdf.PDFReport()

    data = scenario_df.filter(
        model=args["model"], scenario=args["scenario"], variable="Primary Energy|*"
    )

    if len(data.variable) > 0:
        data.plot(color="region", title="Primary Energy")
        data.timeseries()
        plt.legend(loc=1)
        plt.tight_layout()
        plt.savefig("Primary_Energy.png")

        # Add a page
        pdf.add_page()
        pdf.ln(50)
        image_path = "Primary_Energy.png"
        page_width = pdf.w
        image_width = 100  # Width of the image
        space_image_text = 10
        x_position = (page_width - image_width) / 2

        # Insert image
        pdf.image(image_path, x=x_position, y=40, w=image_width)

        # Insert text centered just below the image
        pdf.ln(image_width)  # Move down by the height of the image
        pdf.set_y(space_image_text + image_width)  # Ensure the text is below the image

        # Calculate text width and center
        text = "Figure 1: World Primary Energy Consumption"
        text_width = pdf.get_string_width(text)
        pdf.set_x((page_width - text_width) / 2)  # Center the text

        # Insert text
        pdf.cell(text_width, 10, txt=text, ln=2, border=0, align="C")

        # Center the second image
        second_image_path = "Primary_Energy.png"
        second_image_y = (
            image_width + 4 * space_image_text
        )  # Adjust y to place the second image below the text

        # Insert the second image
        pdf.image(second_image_path, x=x_position, y=second_image_y, w=image_width)

        # Insert text centered just below the image
        pdf.ln(image_width)  # Move down by the height of the image
        pdf.set_y(
            2 * image_width + space_image_text
        )  # Ensure the text is below the image

        # Calculate text width and center
        text = "Figure 1: World Primary Energy Consumption"
        text_width = pdf.get_string_width(text)
        pdf.set_x((page_width - text_width) / 2)  # Center the text

        # Insert text
        pdf.cell(text_width, 10, txt=text, ln=2, border=0, align="C")

        pdf.output(args["scenario"] + "report.pdf", "F")


def main():
    # Parse the argument put in the command line. 
    parser = argparse.ArgumentParser()
    parser.add_argument("--arguments", help="insert argg")
    args = parser.parse_args()

    # Inform the user if a report will be created
    report_creation_bool = False
    if args.arguments == 'report':
        report_creation_bool = True

    # Folder name to create
    folder_name_to_convert = "File_To_Convert"
    folder_name_converted = "File_Converted"

    # Get current folder
    folder_path = os.getcwd()


    # Create new folder
    create_folder_if_not_exists(folder_name_converted)

    # Check the existence of the File_To_Convert folder 
    folder_created_bool = os.path.isdir(os.path.join(folder_path, folder_name_to_convert))
    if not folder_created_bool: 
        print('The path to the File_To_Convert folder', folder_path + folder_name_to_convert, ' is not a directory.' )


    # Get the last upload excel file
    real_folder_path = os.path.join(folder_path, folder_name_to_convert)

    last_file = get_last_added_file(real_folder_path)


    if last_file:
        print("Last added file:", last_file)
    else:
        print("No files found in the folder.")

    # Get the correct naming for the converted file
    filename_with_extension = os.path.basename(last_file)
    splited_filename_with_extension = os.path.splitext(filename_with_extension)
    
    filename = (
        splited_filename_with_extension[0]
        + "converted"
        + splited_filename_with_extension[1]
    )


    
    # The scenario name is the name of the file to translate.
    # Possibility to create a thread to run all the code during the wait for the user answer.
    # scenario = input("Give the name of the scenario")
    scenario = splited_filename_with_extension[0]

    # Read the selected file
    if (
        splited_filename_with_extension[1] == ".xls"
        or splited_filename_with_extension[1] == ".xlsx"
    ):
        scenario_variable_df = pd.read_excel(last_file)
    elif splited_filename_with_extension[1] == ".csv":
        scenario_variable_df = pd.read_csv(last_file)

    # Remove duplicated rows in the file. 
    scenario_variable_df = scenario_variable_df.drop_duplicates()
    
    # Rename the column of the file
    columns = scenario_variable_df.columns.str.replace("Unnamed:", "Subscript")
    columns = columns.str.replace(".", " ")

    # Define the string you want in column names
    search_string = "Subscript"
    counter = 0

    for k in range(len(columns)):
        if search_string in columns[k]:
            columns.values[k] = search_string + " " + str(counter)
            counter += 1


    # Create a dictionary using zip() and dictionary comprehension
    my_dict = {k: v for k, v in zip(scenario_variable_df.columns[2:6], columns[2:6])}
    scenario_variable_df.rename(columns=my_dict, inplace=True)
    scenario_variable_df.rename(
        columns={"Time": "Variable", "Year": "Unit", "Subscript": "Subscript 0"},
        inplace=True,
    )

    # Insert the three columns in the right place for IAMC format
    scenario_variable_df.insert(0, "Model", "WILIAM")
    scenario_variable_df.insert(1, "Scenario", scenario)
    scenario_variable_df.insert(2, "Region", "World")

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
    scenario_variable_df = scenario_variable_df.apply(
        aggregate_subscript_variable_name, args=(counter, existing_country_Wiliam_dict, country_dict),axis=1
    )

    # Remove the subscript columns once they have been added at the end of the variable name
    drop_columns_list = ["Subscript " + str(k) for k in range(counter)]
    scenario_variable_df.drop(columns=drop_columns_list, inplace=True)

    # Open the text file containing the variable dictionary to translate each variable name of Wiliam to the variable name in the IAMC format.
    variable_name_dict = open_dict("variable_name_dict.txt")

    # Convert all the variable name to the IAMC format and get the variables with a missing translation.
    # Create the list of missing variable.
    missing_variable = []

    # Create a new column for the selection of translated variable
    scenario_variable_df['Translation'] = False

    # Apply the translation of the variable name's column to respect the IAMC format

    scenario_variable_df = scenario_variable_df.apply(
        replace_and_track, args=(variable_name_dict, missing_variable,), axis=1
    )

    # Remove the untranslated variable of the dataframe
    scenario_variable_df = scenario_variable_df.loc[scenario_variable_df.Translation,:]

    # Open the text file containing the aggregation dictionary
    aggregation_dict = open_dict("aggregation_dict.txt")

    # Create the aggregations rows in the dataframe
    scenario_variable_df = aggregate_rows(scenario_variable_df, aggregation_dict)

    # Create the path for the file containing the missing variable
    print(
        "The translation of ",
        len(missing_variable),
        " variables are missing. You can find all the translation in the file called new_variable_name_dict.txt")

    # Process the automatic translation of missing variables. 
    translation_helpers.create_automatic_translation(missing_variable)

    # Write the new excel file in the File_Converted folder
    folder_file_converted = os.path.join(folder_path, folder_name_converted)

    # Get the correct naming for the converted file
    filename_with_extension = os.path.basename(last_file)
    filename = (
        splited_filename_with_extension[0]
        + "converted"
        + splited_filename_with_extension[1]
    )

    # Check for duplicate rows
    duplicate_rows = scenario_variable_df[
        scenario_variable_df.duplicated(subset=["Region", "Variable", "Unit"])
    ]

    # Count the number of duplicate rows. Normally we should find zero duplicates.
    num_duplicate_rows = duplicate_rows.shape[0]
    if num_duplicate_rows > 0:
        print("Number of Duplicate Rows:", num_duplicate_rows)

    # Remove duplicate rows
    scenario_variable_df.drop_duplicates(subset=["Region", "Variable", "Unit"], inplace=True)

    # Write the following dataframe to excel or CSV
    if (
        splited_filename_with_extension[1] == ".xls"
        or splited_filename_with_extension[1] == ".xlsx"
    ):
        scenario_variable_df.to_excel(os.path.join(folder_file_converted, filename))
    elif splited_filename_with_extension[1] == ".csv":
        scenario_variable_df.to_csv(
            os.path.join(folder_file_converted, filename), index=False
        )

    print("Conversion Done")

    if not report_creation_bool: 
        exit()

    # Structure to check the existance of the file
    try:
        scenario_df = pyam.IamDataFrame(
            os.path.join(folder_file_converted, filename)
    )
         # This defines the model and scenario used for the report
        args = dict(model="WILIAM", scenario=scenario)

        
        create_report(scenario_df, args)
    except Exception:
        print("ERROR opening the file with results in IAMC format")
        exit()
    
   
    
    print("Report's creation in process")
    




if __name__ == "__main__":
    main()
    
    

