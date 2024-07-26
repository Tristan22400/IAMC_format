import pandas as pd
import ast
import csv
import pprint

# Function to move the matched string after the specific word
def move_crochets(s):
    specific_word_1 = "[per capita]"
    specific_word_2 = "[intensity]"
    specific_word_3 = "[share]"

    if specific_word_1 in s:
        index_emission = s.find(specific_word_1)

        s = (
            s[: index_emission - 1]
            + s[index_emission + len(specific_word_1) :]
            + specific_word_1
        )

    if specific_word_2 in s:
        index_emission = s.find(specific_word_2)

        s = (
            s[: index_emission - 1]
            + s[index_emission + len(specific_word_2) :]
            + "[Intensity]"
        )

    if specific_word_3 in s:
        index_emission = s.find(specific_word_3)

        s = (
            s[: index_emission - 1]
            + s[index_emission + len(specific_word_1) :]
            + "[Share]"
        )

    return s





# Change the format of the string to respect IAMC's format
def format_string(s, upper_word_list, vehicule_list):
    # Split the string into words
    if pd.isnull(s):
        return s
    words = s.split("|")

    capitalized_words = []
    # Capitalize the first letter of each word
    for word in words:
        if word not in upper_word_list:
            new_word_list = word.split("_")
            new_word_list = [new_word.capitalize() for new_word in new_word_list]
            capitalized_words += [" ".join(new_word_list) + "|"]
        else:
            new_word_list = word.split("_")
            capitalized_words += [
                new_word + "|"
                if new_word in vehicule_list
                else new_word.capitalize() + "|"
                for new_word in new_word_list
            ]

    # Join the words with spaces
    transformed_string = "".join(capitalized_words)

    result = ""
    capitalize_next = False
    # Capitalize the letter after each space
    for char in transformed_string[:-1]:
        if char == " " or char == "-":
            capitalize_next = True
            result += char
        elif capitalize_next:
            result += char.upper()
            capitalize_next = False
        else:
            result += char

    return result

def process_csv(
    input_file,
    IAMC_WILIAM_name_dict,
    energy_dict,
    rest_dict,
    sectors_dict,
    economy_dashboard_dict,
    upper_word_list,
    vehicle_list,
):
    original_to_transformed = {}

    # Open the CSV file and read it line by line
    with open(input_file, mode="r") as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            original_string = row[0]  # Get the original string
            # Split the string by '|' to extract parts
            parts = original_string.split("|")

            # Replace parts with dictionary values if they are keys in the dictionary
            transformed_parts = []
            for part in parts:
                if IAMC_WILIAM_name_dict.get(part,None):
                    part = IAMC_WILIAM_name_dict.get(part, None)
                elif energy_dict.get(part, None):
                    part = energy_dict[part]
                elif rest_dict.get(part, None):
                    part = rest_dict[part]
                elif sectors_dict.get(part, None):
                    part = sectors_dict[part]
                elif economy_dashboard_dict.get(part, None):
                    part = economy_dashboard_dict[part]
                
                transformed_parts.append(part)

            # Reconstruct the string with transformed parts
            transformed_string = "|".join(transformed_parts)

            # Move the word in the brackets at the end of the word.
            transformed_string = move_crochets(transformed_string)

            # Transform the string to respect the IAMC format
            transformed_string = format_string(transformed_string, upper_word_list, vehicle_list)

            # Map the original string to the transformed string
            original_to_transformed[original_string] = transformed_string

    return original_to_transformed

def open_dict(dict_filename):
    # Open the text file containing the dictionary
    with open("../Conversion-Script/Create_Variable_Dict/" + dict_filename, "r") as f:
        # Read the contents of the file
        read_dict_str = f.read()

    # Convert the string representation of the dictionary back to a dictionary object
    read_dict = ast.literal_eval(read_dict_str)
    return read_dict


def main(): 

    # File that should be read.
    csv_file_path = "missing_variable.csv" 

    # Open the text file containing the energy dictionary
    energy_dict = open_dict("energy_dict.txt")


    # Open the text file containing the rest dictionary
    rest_dict = open_dict("rest_dict.txt")


    # Open the text file containing the sectors dictionary
    sectors_dict = open_dict("sectors_dict.txt")


    # Open the text file containing the dictionary for the economy dashboard subscript.
    economy_dashboard_dict = open_dict("economy_dashboard.txt")

    # List with the words in uppercase which will not be capitalized by the next functions
    upper_word_list = [
    "CO2",
    "CH4",
    "N2O",
    "PFC",
    "SF6",
    "HFC134a",
    "HFC23",
    "HFC32",
    "HFC125",
    "HFC143a",
    "HFC152a",
    "HFC227ea",
    "HFC245ca",
    "HFC43-10",
    "HFC",
    "w/o CCS",
    "w/ CCS",
    "PV",
    "CSP",
    "AFOLU",
    "CO2eq",
    "EROI",
    "PV",
    "CSP",
    "ICE_gasoline",
    "ICE_diesel",
    "ICE_gas",
    "ICE_LPG",
    "BEV",
    "PHEV",
    "HEV",
    "FCEV",
    "EV",
    "HPV",
    "LMO",
    "NMC622",
    "NMC811",
    "NCA",
    "LFP",
    "LDV",
    "MDV",
    "HDV",
    "NMT",
    "GDP",
    "PPP",
    ]
    vehicle_list = ["gasoline", "gas", "diesel"]

    # Read the CSV file into a pandas DataFrame
    data_name_df = pd.read_excel("../Conversion-Script/Variable_Reference/Variable_name_IAMC.xlsx")
    # Create a dict with Wiliam's name as key, IAMC's name as value
    IAMC_WILIAM_name_dict = data_name_df.set_index('WILIAM_variable')['IAMC_variable'].to_dict()

    translation_dict = process_csv(
        csv_file_path,
        IAMC_WILIAM_name_dict,
        energy_dict,
        rest_dict,
        sectors_dict,
        economy_dashboard_dict,
        upper_word_list,
        vehicle_list,
    )
    
    # Save dictionary with pprint
    with open("new_variable_name_dict.txt", "w") as f:
        pprint.pprint(translation_dict, f)


if __name__ == "__main__":
    main()
