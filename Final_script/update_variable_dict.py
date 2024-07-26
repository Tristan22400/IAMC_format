import pprint
import ast

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
        if not (char.isalnum() or char in " |[]"):
            print('This character is not authorized in the IAMC Format: ', char)
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
            if word != word.capitalize():
                print("This word should be capitalized: ", word)
                valid_capitalization_bool = False
    return valid_capitalization_bool


def process_dictionary(data_dict):
    """
    Checks and processes the values in a dictionary.
    """
    # List of conjunctions and words that should not be capitalized
    conjunctions = {"and", "or", "nor", "but", "so", "for", "yet", "of", "w/", "w/o"}
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

def check_and_merge_dicts(dict1, dict2):
    # Find overlapping keys
    overlapping_keys = set(dict1.keys()) & set(dict2.keys())

    # Check if there are any differences in the overlapping keys
    for key in overlapping_keys:
        if dict1[key] != dict2[key]:
            print(f"Conflict found for key '{key}':")
            print(f" - Dict1 has {dict1[key]}")
            print(f" - Dict2 has {dict2[key]}")
            return None  # Return None if there's a conflict

    # Merge the dictionaries if there are no conflicts
    merged_dict = dict1.copy()  # Start with a copy of the first dictionary
    merged_dict.update(dict2)  # Update it with the second dictionary
    return merged_dict

def write_dict(dict_path, name_dict): 
    # Save dictionary with pprint
    with open(dict_path, 'w') as f:
        pprint.pprint( name_dict, f)

def main():
    # Read the dict file that contain the update of the translation dict
    new_variable_dict = open_dict('new_variable_name_dict.txt')

    # Check the format of the new variable to translate
    correct_foramt_bool = process_dictionary(new_variable_dict)
    if not correct_foramt_bool:
        exit()
    
    current_variable_translation_dict_path = (
        "../Conversion-Script/Create_Variable_Dict/variable_name_dict.txt"
    )
    # Read the current dictionary of translation variable
    current_variable_translation_dict = open_dict(current_variable_translation_dict_path)

    updated_variable_translation_dict = check_and_merge_dicts(new_variable_dict, current_variable_translation_dict)

    if updated_variable_translation_dict:
        write_dict(
            current_variable_translation_dict_path, updated_variable_translation_dict
        )
        print("Update of the translation dictionary done.")

if __name__ == "__main__":
    main()
