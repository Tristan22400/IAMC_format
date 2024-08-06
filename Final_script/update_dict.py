import argparse
import ast

upper_word_list = [
    "CO2",
    "CO2eq",
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
    "HFC4310mee",
    "CO2eq[per capita]",
    "HFC",
    "w/o CCS",
    "w/ CCS",
    "w/",
    "w/o",
    "CCS",
    "PV",
    "CSP",
    "AFOLU",
    "AFOFI",
    "CO2eq",
    "EROI",
    "ESOI",
    "PV",
    "CSP",
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
    "COICOP",
    "CIGS",
    "CdTe",
]

def check_brackets(s):
    """
    Checks that a string contains no hook or has a balanced pair of one open
    and one close hook, with the close hook being the last character if present.
    """
    # Count occurrences of open and close hook
    open_bracket_count = s.count("[")
    close_bracket_count = s.count("]")

    # Check if the string contains no hook
    if open_bracket_count == 0 and close_bracket_count == 0:
        return True

    # Check for exactly one pair of hook and proper placement
    if open_bracket_count == 1 and close_bracket_count == 1:
        # Ensure that the close hook is the last character
        if s.endswith("]") and " [" in s:
            if "[ " not in s and " ]" not in s: 
                return True
            else: 
                print("A space should not be presented after the opening hook and before the closing hook: ", s)
                return False
        else: 
            print("The string does not finished by a closing hook or needs a supplementary space: ", s)
            return False
    print("The number of crochets is greater than the maximum number of crochets or the position of them are not good in the following string: ", s)
    return False

def is_valid_string(s):
    """
    Checks that the string contains only spaces, letters, digits, or pipes.
    """
    valid_string_bool = True
    for char in s:
        if not (char.isalnum() or char in " |[]-/+"): # Need to remove _ for testing only
            print('This character is not authorized in the IAMC Format: ', char, ' in ', s)
            valid_string_bool = False
    # Check for spaces before or after each pipe
    if " |" in s or "| " in s:
        print('There is some unusual space before or after a pipe in the following string: ', s)
        valid_string_bool = False

    # Check double space in the string.
    if "  " in s:
        print("There is some double space: ", s)
        valid_string_bool = False
    
    # Check the bracket conditions
    if not check_brackets(s):
        valid_string_bool = False

    # Check that the string is not finishing by a space. 
    if s.endswith(" "):
        print("The string should not finished by a space: ", s)
        valid_string_bool = False

    return valid_string_bool

def remove_bracketed_parts(s):
    """
    Removes all substrings enclosed in square brackets from the input string.

    This function iterates over the input string and removes any part of the string
    that is enclosed within square brackets, including the brackets themselves.
    """
    result = []
    inside_brackets = False

    for char in s:
        if char == "[":
            inside_brackets = True
        elif char == "]":
            inside_brackets = False
        elif not inside_brackets:
            result.append(char)

    return "".join(result)

def has_number_or_dash(s):
    """
    Check for any digit or dash in the string
    """
    return any(char.isdigit() or char == '-' for char in s)

def check_capitalization(words, conjunctions):
    """
    Checks that each word is capitalized unless it is a conjunction.
    """

    valid_capitalization_bool = True
    for word in words:
        if word.lower() in conjunctions:
            if word != word.lower():
                print("This word should be in lowercase: ", word)
                valid_capitalization_bool = False
        else:
            if has_number_or_dash(word): 
                continue
            elif word in upper_word_list: 
                continue
            elif word != word.capitalize():
                print("This word should be capitalized or added to the upper word list: ", word)
                valid_capitalization_bool = False
    return valid_capitalization_bool


def process_values_dict(data_dict):
    """
    Checks and processes the values in a dictionary.
    """
    # List of conjunctions and words that should not be capitalized
    conjunctions = {"and", "or", "nor", "but", "so", "for", "yet", "of", "w/", "w/o", "on"}
    correct_format_bool = True
    for key, value in data_dict.items():
        if isinstance(value, str):
            # Check if the string contains only valid characters
            if not is_valid_string(value):
                print(
                    f"The value associated with key '{key}' is not following IAMC format rules."
                )
                correct_format_bool = False



            # Split the string into words using spaces and pipes as separators
            value = remove_bracketed_parts(value)
            words = value.split()
            split_words = []
            for word in words:
                split_words.extend(word.split("|"))

            # Check the capitalization of words
            if not check_capitalization(split_words, conjunctions):
                print(
                    f"The value associated with key '{key}' does not have all words written properly."
                )
                correct_format_bool = False
    
    return correct_format_bool


def open_dict(dict_path):
    # Open the text file containing the dictionary
    with open(dict_path, "r") as f:
        # Read the contents of the file
        read_dict_str = f.read()

    # Convert the string representation of the dictionary back to a dictionary object
    read_dict = ast.literal_eval(read_dict_str)
    return read_dict

def check_and_merge_dicts(dict1, dict2, forced_update):
    # Find overlapping keys
    overlapping_keys = set(dict1.keys()) & set(dict2.keys())

    # Check if there are any differences in the overlapping keys
    for key in overlapping_keys:
        if dict1[key] != dict2[key]:

            print(f"Conflict found for key '{key}':")
            print(f" - Dict1 has {dict1[key]}")
            print(f" - Dict2 has {dict2[key]}")

            # Return None if there's a conflict and the update was not forced
            if not forced_update:
                return None

    # Merge the dictionaries if there are no conflicts
    merged_dict = dict1.copy()  # Start with a copy of the first dictionary
    merged_dict.update(dict2)  # Update it with the second dictionary
    return merged_dict

def write_dict(dict_path, name_dict): 
    
    # Write the dictionary to a text file
    with open(dict_path, "w") as file:
        
        # Start with the opening curly brace
        file.write("{\n")
        
        # Write each key-value pair on a new line with single quotes
        for key, value in name_dict.items():
            file.write(f"    '{key}': '{value}',\n")
        
        # End with the closing curly brace
        file.write("}\n")
        

def update_variable_dict(forced_update):
    # Read the dict file that contain the update of the translation dict
    new_variable_dict = open_dict('new_variable_name_dict.txt')

    # Check the format of the new variable to translate
    correct_values_format_bool = process_values_dict(new_variable_dict)
    if not correct_values_format_bool:
        exit()
    
    current_variable_translation_dict_path = (
        "../Create_Variable_Dict/variable_name_dict.txt"
    )
    # Read the current dictionary of translation variable
    current_variable_translation_dict = open_dict(current_variable_translation_dict_path)

    # Check that the submitted dict respect the IAMC format constraints and merge the dict
    updated_variable_translation_dict = check_and_merge_dicts(new_variable_dict, current_variable_translation_dict, forced_update)

    # Write the new dictionary if updated. 
    if updated_variable_translation_dict:
        write_dict(
            current_variable_translation_dict_path, updated_variable_translation_dict
        )
        print("Update of the translation dictionary done.")


def process_keys_dict(data_dict):
    # List of conjunctions and words that should not be capitalized
    conjunctions = {"and", "or", "nor", "but", "so", "for", "yet", "of", "w/", "w/o"}
    correct_format_bool = True
    for key_list, value in data_dict.items():
        for key in key_list: 
            if isinstance(key, str):
                # Check if the string contains only valid characters
                if not is_valid_string(key):
                    print(
                        f"The key '{key}' associated with value '{value}' is not following IAMC format rules."
                    )
                    correct_format_bool = False

                # Split the string into words using spaces and pipes as separators
                key = remove_bracketed_parts(key)
                words = value.split()
                split_words = []
                for word in words:
                    split_words.extend(word.split("|"))

                # Check the capitalization of words
                if not check_capitalization(split_words, conjunctions):
                    print(
                        f"The key '{key}' associated with value '{value}' does not have all words written properly."
                    )
                    correct_format_bool = False
    return correct_format_bool


def check_existing_variables_aggregations():
    current_aggregation_dict_path = (
        "../Create_Variable_Dict/aggregation_dict.txt"
    )

    # Read the current dictionary of aggregations of variable.
    current_aggregation_dict = open_dict(current_aggregation_dict_path)

    current_variable_translation_dict_path = (
        "../Create_Variable_Dict/variable_name_dict.txt"
    )
    # Read the current dictionary of translation variable
    current_variable_translation_dict = open_dict(
        current_variable_translation_dict_path
    )


    # Create the dictionary values into a set for fast membership checking
    all_variables_translation_set = set(
        val for val in current_variable_translation_dict.values()  
    )
    
    all_variables_aggregation_set = set(
        val for sublist in current_aggregation_dict.keys() for val in sublist
    )

    # Find elements not present using set difference
    not_present_elements = (
        all_variables_aggregation_set - all_variables_translation_set
    )

    if not_present_elements:
        print(f"These elements are not present in the dictionary values: {not_present_elements}")
    else:
        print("All elements are present in the dictionary values.")


def update_aggregation_dict(forced_update): 
    # Read the dict file that contain the update of the translation dict
    new_aggregation_dict = open_dict("new_aggregation_dict.txt")

    # Check the format of the key and value of this new aggregation dict. 
    correct_values_format_bool = process_values_dict(new_aggregation_dict)
    correct_keys_format_bool = process_keys_dict(new_aggregation_dict)
    print(correct_keys_format_bool, correct_values_format_bool)
    # Stop the run if the IAMC format is not respected. 
    if not correct_values_format_bool or not correct_keys_format_bool:
        exit()


    current_aggregation_dict_path = (
        "../Create_Variable_Dict/aggregation_dict.txt"
    )
    
    # Read the current dictionary of translation variable
    current_aggregation_dict = open_dict(
        current_aggregation_dict_path
    )
    
    # Check that the submitted dict respect the IAMC format constraints and merge the dict
    updated_variable_translation_dict = check_and_merge_dicts(
        new_aggregation_dict, current_aggregation_dict, forced_update
    )

    # Write the new dictionary if updated.
    if updated_variable_translation_dict:
        write_dict(
            current_aggregation_dict_path, updated_variable_translation_dict
        )
        print("Update of the translation dictionary done.")


if __name__ == "__main__":
    # Parse the argument put in the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("--arguments", help="insert argg")
    args = parser.parse_args()
    print(args.arguments)
    if args.arguments == 'variables,forced':
        update_variable_dict(True)
    elif args.arguments == "variables":
        update_variable_dict(False)
    elif args.arguments == "aggregations,forced":
        update_aggregation_dict(True)
    elif args.arguments == "aggregations":
        update_aggregation_dict(False)
    elif args.arguments == "aggregations,check":
        check_existing_variables_aggregations()
    else: 
        print("You need to put a correct argument to execute the update. See the ReadMe.")
