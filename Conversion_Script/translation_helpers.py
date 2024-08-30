import pandas as pd
import ast
import update_dict

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
def format_string(s, upper_word_list):
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
                new_word.capitalize() + "|"
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

def process_list(
    missing_variable_list,
    dict_list,
    upper_word_list
):
    original_to_transformed = {}

    for variable in missing_variable_list:
        # Split the string by '|' to extract parts
        parts = variable.split("|")
        
        # Replace parts with dictionary values if they are keys in the dictionary
        transformed_parts = []
        for part in parts:
            subscript = part
            for dict_variariables in dict_list:
                if dict_variariables.get(part, None):
                    subscript = dict_variariables[part]
        
            
            transformed_parts.append(subscript)
            

        # Reconstruct the string with transformed parts
        transformed_string = "|".join(transformed_parts)

        # Move the word in the brackets at the end of the word.
        transformed_string = move_crochets(transformed_string)

        # Transform the string to respect the IAMC format
        # transformed_string = format_string(transformed_string, upper_word_list)

        # Map the original string to the transformed string
        original_to_transformed[variable] = transformed_string

    return original_to_transformed

def open_dict(dict_filename):
    # Open the text file containing the dictionary
    with open("../Create_Variable_Dict/" + dict_filename, "r") as f:
        # Read the contents of the file
        read_dict_str = f.read()

    # Convert the string representation of the dictionary back to a dictionary object
    read_dict = ast.literal_eval(read_dict_str)
    return read_dict


def create_automatic_translation(missing_variable_list): 

    # Open the text file containing the age cohort dictionary
    age_cohort_dict = open_dict("age_cohort_dict.txt")

    # Open the text file containing the COICOP dict
    COICOP_dict = open_dict("COICOP_dict.txt")

    # Open the text file containing the economy dashboard dict
    economy_dashboard_dict = open_dict("economy_dashboard_dict.txt")

    # Open the text file containing the ev chargers dict
    ev_chargers_dict = open_dict("ev_chargers_dict.txt")

    # Open the text file containing the final demand dict
    final_demand_dict = open_dict("final_demand_dict.txt")

    # Open the text file containing the GHG dict
    GHG_dict = open_dict("GHG_dict.txt")

    # Open the text file containing the households demography dict
    households_demography_dict = open_dict("households_demography_dict.txt")

    # Open the text file containing the land dict
    land_dict = open_dict("land_dict.txt")

    # Open the text file containing the materials W dict
    materials_W_dict = open_dict("materials_W_dict.txt")

    # Open the text file containing the NRG Commodities dict
    NRG_Commodities_dict = open_dict("NRG_Commodities_dict.txt")

    # Open the text file containing the NRG_Pro_dict
    NRG_Commodities_dict = open_dict("NRG_Commodities_dict.txt")

    # Open the text file containing the ore grade dict
    ore_grade_dict = open_dict("ore_grade_dict.txt")

    # Open the text file containing the pprofile dict
    pprofile_dict = open_dict("pprofile_dict.txt")

    # Open the text file containing the pv subtech dict
    pv_subtech_dict = open_dict("pv_subtech_dict.txt")

    # Open the text file containing the sectors dictionary
    sectors_dict = open_dict("sectors_dict.txt")

    # Open the text file containing the sex dict
    transport_mode_dict = open_dict("transport_mode_dict.txt")

    # Open the text file containing the transport_power_train_dict
    transport_power_train_dict = open_dict("transport_power_train_dict.txt")

    dict_list = [age_cohort_dict, COICOP_dict, economy_dashboard_dict, ev_chargers_dict, final_demand_dict, GHG_dict, households_demography_dict, land_dict, materials_W_dict, NRG_Commodities_dict]

    # List with the words in uppercase which will not be capitalized by the next functions
    upper_word_list = update_dict.upper_word_list
    

    # Process the variables not translated. 
    new_variable_name_dict = process_list(
        missing_variable_list,
        dict_list,
        update_dict.upper_word_list
    )
    
    # Write the dictionary to a text file
    with open('new_variable_name_dict.txt', "w") as file:
        
        # Start with the opening curly brace
        file.write("{\n")
        
        # Write each key-value pair on a new line with single quotes
        for key, value in new_variable_name_dict.items():
            file.write(f"    '{key}': '{value}',\n")
        
        # End with the closing curly brace
        file.write("}\n")

    # Read the CSV file into a pandas DataFrame
    data_name_df = pd.read_excel(
        "../Conversion-Script/Variable_Reference/Variable_name_IAMC.xlsx"
    )
    # Create a dict with Wiliam's name as key, IAMC's name as value
    IAMC_WILIAM_name_dict = data_name_df.set_index("WILIAM_variable")[
        "IAMC_variable"
    ].to_dict()

    # Create the dict of only variable name dictionary
    variable_name_change_dict = dict()

    for key in new_variable_name_dict.keys():
        # Find the index of the first pipe
        pipe_index = key.find("|")

        # Slice the string from the start to the first pipe
        if pipe_index != -1:  # Check if the pipe exists
            variable_Wiliam = key[:pipe_index]
        else:
            variable_Wiliam = key  # No pipe found, use the whole string
        
        # Get the Value in the Wiliam to Iamc format dict and return the key if not found. 
        variable_name_change_dict[variable_Wiliam] = IAMC_WILIAM_name_dict.get(variable_Wiliam, variable_Wiliam)

    # Write the dictionary to a text file
    with open("variable_name_change_dict.txt", "w") as file:
        # Start with the opening curly brace
        file.write("{\n")
        
        # Write each key-value pair on a new line with single quotes
        for key, value in variable_name_change_dict.items():
            file.write(f"    '{key}': '{value}',\n")
        
        # End with the closing curly brace
        file.write("}\n")

        

            


# Change the naming of the Wiliam variable with the correct naming for the 
def improve_translation_variable_missing_name():

    # Read the file content
    with open('variable_name_change_dict.txt', 'r') as file:
        translation_dict_str = file.read()

    # Use ast.literal_eval to safely evaluate the string to a dictionary
    translation_dict = ast.literal_eval(translation_dict_str)

    
    # Save dictionary with pprint
    with open("new_variable_name_dict.txt", "r") as f:
        # Read the contents of the file
        variable_name_dict_str = f.read()

    # Convert the string representation of the dictionary back to a dictionary object
    variable_name_dict = ast.literal_eval(variable_name_dict_str)
    new_variable_name_dict = dict()

    for key, value in variable_name_dict.items():
        # Find the index of the first pipe
        pipe_index = value.find("|")

        # Slice the string from the start to the first pipe
        if pipe_index != -1:  # Check if the pipe exists
            result = value[:pipe_index]
        else:
            result = value  # No pipe found, use the whole string
        
        # Replace the old variable name by the new ones.
        if translation_dict.get(result):
            if pipe_index != -1:
                value = translation_dict.get(result) + value[pipe_index:]
            else: 
                value = translation_dict.get(result)
        else: 
            print(result, 'is not translated in the file or has already been translated from the Wiliam IAMC format dict. It is coming from', key)

        # Check that the key is not already existing.
        if key in new_variable_name_dict.keys():
            print('You are trying to update the dict to 2 different values for the same key.')
            exit()
        
        # Write the new dictionary.
        new_variable_name_dict[key] = value

    # Write the dictionary to a text file
    with open("new_variable_name_dict.txt", "w") as file:
        # Start with the opening curly brace
        file.write("{\n")

        # Write each key-value pair on a new line with single quotes
        for key, value in new_variable_name_dict.items():
            file.write(f"    '{key}': '{value}',\n")

        # End with the closing curly brace
        file.write("}\n")
    print("Variable's name translation done.")


if __name__ == "__main__":
    improve_translation_variable_missing_name()