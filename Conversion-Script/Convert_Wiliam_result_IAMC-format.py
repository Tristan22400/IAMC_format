import numpy as np 
import pandas as pd
import os
import time
import ast




def get_last_added_file(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Filter Excel files
    excel_files = [file for file in files if file.endswith('.xlsx') or file.endswith('.xls') or file.endswith('.csv')]
    
    if not excel_files:
        return None  # No Excel files found
    
    # Sort files by modification time (newest first)
    excel_files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)), reverse=True)
    
    # Return the path to the last added Excel file
    return os.path.join(folder_path, excel_files[0])





def create_folder_if_not_exists(folder_name):
    # Get current folder 
    folder_path = os.getcwd()
    
    try:
        os.makedirs("pip")
        print("DONE")
    except FileExistsError:
        
        pass
    if not os.path.exists(os.path.join(folder_path,folder_name)):
        os.makedirs(folder_name)
        print("Folder '{}' created.".format(folder_name))
    else:
        print("Folder '{}' already exists.".format(folder_name))

def read_dict_txt(filename):
    # Open the text file containing the energy dictionary
    with open(filename, 'r') as f:
        # Read the contents of the file
        dict_str = f.read()

    # Convert the string representation of the dictionary back to a dictionary object
    dict = ast.literal_eval(dict_str)
    return dict

def change_unit(row):
    if not pd.isna(row):
        if 'Year' in row:
            row = row.replace('Year','yr')
    return row

# Aggregate the subscripts at the end of the variable 
def aggregate_variable_name(row, counter, country_dict, energy_dict, rest_dict):
    for k in range(counter):
        subscript=row["Subscript "+str(k)]
    
        if k==0 :
            if country_dict.get(subscript)==1: 
                #Give the name of the region for that variable
                row["Region"]=subscript
                
                row["Subscript 0"]=np.nan
                continue
        
        if not pd.isnull(subscript):
            
            if energy_dict.get(subscript, None) is not None:
                
                subscript = energy_dict[subscript]
            elif rest_dict.get(subscript,None): 
                subscript = rest_dict[subscript]
            
            row["Variable"]=row["Variable"]+"|"+subscript
            
    return row

# Change the format of the string to respect IAMC's format
def transform_string(s,upper_word_list):
    # Split the string into words
    if pd.isnull(s): 
        return s
    words = s.split('|')

    capitalized_words = []
    # Capitalize the first letter of each word
    for word in words: 
        if word not in upper_word_list:
            new_word_list = word.split('_')
            new_word_list = [new_word.capitalize() for new_word in new_word_list] 
            capitalized_words += [' '.join(new_word_list) + '|']
        else: 
            capitalized_words += [word + '|']
    
    # Join the words with spaces
    transformed_string = ''.join(capitalized_words)

    result = ''
    capitalize_next=False
    # Capitalize the letter after each space
    for char in transformed_string[:-1]:
        if char == ' ' or char == '-':
            capitalize_next = True
            result += char
        elif capitalize_next:
            result += char.upper()
            capitalize_next = False
        else:
            result += char
                
    
    return result



# Iterate over the rows to create the name and the unit of emissions correctly. 
# The new list of variables and unit is then updated to the real dataframe.
def emission_correction(emission_rows,GHGs_to_check, HFC_list):

    variable_list = []
    unit_list = []

    for row_index, row in emission_rows[['Variable','Unit']].iterrows():
        specific_word = 'Emissions'
        ghg_bool = False
        for string in GHGs_to_check:
            
            if string in row['Variable']:
                
                index_emission = row['Variable'].find('Emissions') + len(specific_word)
                index_gas = row['Variable'].find(string)
                row['Variable'] = row['Variable'][:index_emission] + '|' + string + row['Variable'][index_emission:index_gas-1] + row['Variable'][index_gas+len(string):]            
                ghg = string
                ghg_bool = True
            
                break
        
        for string in HFC_list:
            if string in row['Variable']:
                
                index_emission = row['Variable'].find('Emissions') + len(specific_word)
                index_gas = row['Variable'].find(string)
                row['Variable'] = row['Variable'][:index_emission] + '|HFC|' + string + row['Variable'][index_emission:index_gas-1] + row['Variable'][index_gas+len(string):]
                
                break
        index_year = row['Unit'].find('/yr')
        if row['Unit'] == 'Mt/yr' or row['Unit'] == 'Gt/yr':
            if ghg_bool: 
                row['Unit'] = row['Unit'][:index_year] + ' ' + ghg + row['Unit'][index_year:]
            else : 
                row['Unit'] = row['Unit'][:index_year] + ' ' + string + row['Unit'][index_year:]
        variable_list.append(row['Variable'])
        unit_list.append(row['Unit'])
    return variable_list, unit_list

# Function to move the matched string after the specific word
def move_per_capita(s):
    specific_word = 'Per Capita'
    
    if specific_word in s:
        index_emission = s.find(specific_word) 
        
        s = s[:index_emission-1] + s[index_emission+len(specific_word):] + '|' + specific_word

    return s

def remove_characters_between_indices(input_string, start_index, end_index):
    """
    Remove characters between two given indices of a string.

    Args:
    - input_string (str): The original string.
    - start_index (int): The index of the first character to remove (inclusive).
    - end_index (int): The index of the last character to remove (inclusive).

    Returns:
    - str: The modified string with characters removed between the specified indices.
    """
    if start_index >= end_index:
        return input_string  # Return the original string if start index is greater than or equal to end index
    
    # Ensure indices are within the range of the string
    start_index = max(start_index, 0)
    end_index = min(end_index, len(input_string) - 1)
    
    # Construct the new string by concatenating substrings before and after the characters to be removed
    return input_string[:start_index] + input_string[end_index + 1:]

def remove_string_between_pipe(input_string):
    """
    Remove the string between the second and third '|' characters in the input string.

    Args:
    - input_string (str): The original string.

    Returns:
    - str: The modified string with the content between '|' characters removed.
    """
    second_occurrence = input_string.find('|', input_string.find('|') + 1)
    third_occurrence = input_string.find('|', second_occurrence + 1)-1
    
    # Remove characters between the '|' characters using the previous function
    result = remove_characters_between_indices(input_string, second_occurrence, third_occurrence)

    # Remove CCS extension because it is not relevant 
    result = result.replace('|w/ CCS', '').replace('|w/o CCS', '')
    
    return result


def main():
    # ### Treat all the variables for csv and excel file

    time0= time.time()

    # Folder name to create 
    folder_name_to_convert = 'File_To_Convert'
    folder_name_converted = 'File_Converted'

    # Get current folder 
    folder_path = os.getcwd()


    # Create new folder 
    create_folder_if_not_exists(folder_name_converted)
    create_folder_if_not_exists(folder_name_to_convert)



    # Get the last upload excel file
    real_folder_path= os.path.join(folder_path , folder_name_to_convert)

    last_file = get_last_added_file(real_folder_path)


    if last_file:
        print("Last added file that will be converted :", last_file)
    else:
        print("No files found in the folder.")

    # Get the correct naming for the converted file 
    filename_with_extension = os.path.basename(last_file)
    splited_filename_with_extension = os.path.splitext(filename_with_extension)

    filename = splited_filename_with_extension[0] + 'converted' + splited_filename_with_extension[1]

    # Possibility to create a thread to run all the code during the wait for the user answer. 
    # scenario = input("Give the name of the scenario")
    scenario = splited_filename_with_extension[0]

    # Read the selected file 
    if splited_filename_with_extension[1] == '.xls' or splited_filename_with_extension[1] == '.xlsx':
        scenario_variable_df = pd.read_excel(last_file)
    elif  splited_filename_with_extension[1] == '.csv': 
        scenario_variable_df = pd.read_csv(last_file)


    #Rename the column of the file 
    columns = scenario_variable_df.columns.str.replace('Unnamed:', 'Subscript')
    columns = columns.str.replace('.', ' ')

    # Define the string you want in column names
    search_string = 'Subscript'
    counter=0 

    for k in range(len(columns)): 
        if search_string in columns[k]: 
            columns.values[k]= search_string + ' ' + str(counter)
            counter+=1



    # Create a dictionary using zip() and dictionary comprehension
    my_dict = {k: v for k, v in zip(scenario_variable_df.columns[2:6], columns[2:6])}
    scenario_variable_df.rename(columns=my_dict, inplace=True)
    scenario_variable_df.rename(columns={"Time": "Variable", "Year": "Unit", "Subscript":"Subscript 0"}, inplace=True)

    # Insert the three columns in the right place for IAMC format
    scenario_variable_df.insert(0, 'Model', "WILIAM")
    scenario_variable_df.insert(1, 'Scenario', scenario)
    scenario_variable_df.insert(2,"Region","World")


    # ### Read the Excel File to change the name of the variable


    # Read the CSV file into a pandas DataFrame
    data_name_df = pd.read_excel('Variable_Reference/Variable_name_IAMC.xlsx')
    # Remplacer les tirets du bas par des espaces dans la colonne
    # data_name_df['WILIAM_variable'] = data_name_df['WILIAM_variable'].str.replace('_', ' ')
    # Drop rows with NaN values which corresponds to values not conserv for the final upload of data in IAMC format
    data_name_df.dropna(subset=['IAMC_variable'],inplace=True)
    data_name_df

    # Create a dict with Wiliam's name as key, IAMC's name as value
    IAMC_WILIAM_name_dict = data_name_df.set_index('WILIAM_variable')['IAMC_variable'].to_dict()
    print(IAMC_WILIAM_name_dict)
    # Replace the variable name used in William to the ones used for IAMC format. 
    scenario_variable_df['Variable']= scenario_variable_df['Variable'].replace(IAMC_WILIAM_name_dict)

    # Keep only the rows where the value in column 'Variable' belongs to the list of wanted values 
    variable_required_list = data_name_df['IAMC_variable'].to_list()
    scenario_variable_df = scenario_variable_df[scenario_variable_df['Variable'].isin(variable_required_list)]


    # ### Check of the variable included in the file


    variables_used_list = scenario_variable_df['Variable'].to_list()
    variables_required_not_in = list(set(variable_required_list) - set(variables_used_list))
    print('The missing variable in the export dataset are the following:', variables_required_not_in)
    print('The number of missing varibles is ', len(variables_required_not_in))


    # ### Change the naming of Subcript in William

    # Open the dictionnary used to change the name of Subcript in Wiliam.
    energy_dict = read_dict_txt('Create_Variable_Dict/energy_dict.txt')
    rest_dict = read_dict_txt('Create_Variable_Dict/rest_dict.txt')

    # ### Change Unit nomenclature for the Year
    scenario_variable_df['Unit'] = scenario_variable_df['Unit'].apply(change_unit)


    # ### Order Dataframe to the required Format by adding subscript at the end of the variable


    # Dict used to check if the subscripts are a country
    country_dict= {'EU27':1, 'UK':1,'CHINA':1,'EASOC':1,'INDIA':1,'LATAM':1,'RUSSIA':1,'USMCA':1,'LROW':1,'AUSTRIA':1,'BELGIUM':1,'BULGARIA':1,'CROATIA':1,'CYPRUS':1,'CZECH_REPUBLIC':1,'DENMARK':1,'ESTONIA':1,'FINLAND':1,'FRANCE':1,'GERMANY':1,'GREECE':1,'HUNGARY':1,'IRELAND':1,'ITALY':1,'LATVIA':1,'LITHUANIA':1,'LUXEMBOURG':1,'MALTA':1,'NETHERLANDS':1,'POLAND':1,'PORTUGAL':1,'ROMANIA':1,'SLOVAKIA':1,'SLOVENIA':1,'SPAIN':1,'SWEDEN':1}


    # Apply the previous function on all the lines
    scenario_variable_df= scenario_variable_df.apply(aggregate_variable_name, args=(counter,country_dict,energy_dict,rest_dict),axis=1)

    # Remove the subscript columns once they have been added at the end of the variable name
    drop_columns_list=["Subscript " + str(k) for k in range(counter)]
    scenario_variable_df.drop(columns=drop_columns_list, inplace=True)

    scenario_variable_df

    # List with the words in uppercase which will not be capitalized by the next functions
    upper_word_list = ['CO2', 'CH4', 'N2O', 'PFC', 'SF6', 'HFC134a', 'HFC23', 'HFC32', 'HFC125', 'HFC143a', 'HFC152a', 'HFC227ea', 'HFC245ca', 'HFC43-10', 'HFC', 'w/o CCS' ,'w/ CCS', 'PV', 'CSP', 'AFOLU', 'CO2eq', 'EROI']


    # Capitalize each variable's name
    scenario_variable_df['Variable'] = scenario_variable_df['Variable'].apply(transform_string, args=(upper_word_list,))
    scenario_variable_df


    # Country Traduction between IAMC country and Wiliam


    # Country Wiliam dictionnary 
    country_Wiliam_dict = read_dict_txt('Create_Variable_Dict/country_dict.txt')

    # Replace the region name by the ones adapted for Wiliam. 
    scenario_variable_df['Region'] = scenario_variable_df['Region'].replace(country_Wiliam_dict)
    scenario_variable_df


    # ### Correct Naming Emissions Intensity, Primary Energy, Secondary Energy


    # Select rows with the name 'Emission'
    emission_rows = scenario_variable_df[scenario_variable_df['Variable'].str.contains('Emission')]
    emission_name_old = emission_rows['Variable'].to_list()

    # List of Greenhouses Gases used in Wiliam 
    # We differentiate the treatment of HFC and others GHGs because they are handle differently in IAMC Format. 
    GHGs_to_check = ['CH4', 'N2O', 'PFC', 'SF6','CO2']
    HFC_list = ['HFC134a', 'HFC23', 'HFC32', 'HFC125', 'HFC143a', 'HFC152a', 'HFC227ea', 'HFC245ca', 'HFC43-10']

    variable_list,unit_list= emission_correction(emission_rows,GHGs_to_check,HFC_list)
    
    indexes = emission_rows.index

    # Assign new values to specific rows in the column for the Variable and Unit 
    scenario_variable_df.loc[indexes, 'Variable'] = variable_list
    scenario_variable_df.loc[indexes, 'Unit'] = unit_list


    # Change Primary Energy Naming
    # Select the rows where the primary energy word 
    energy_rows = scenario_variable_df[scenario_variable_df['Variable'].str.contains('Per Capita')]


    energy_name_old = energy_rows['Variable'].to_list()

    

    # Apply the function to the 'Variable' column
    energy_rows['Variable'] = energy_rows['Variable'].apply(move_per_capita)
    energy_name_new = energy_rows['Variable'].to_list()

    energy_per_capita_dict = dict(zip(energy_name_old, energy_name_new))

    scenario_variable_df['Variable']= scenario_variable_df['Variable'].replace(energy_per_capita_dict)


    # Change Secondary Energy Naming 
    secondary_energy_rows = scenario_variable_df[scenario_variable_df['Variable'].str.contains('Secondary Energy')]
    secondary_energy_rows['Variable'].iloc[0]


    # Change Secondary Energy Naming 
    # Select the rows for Primary Energy Price 
    price_energy_rows = scenario_variable_df[scenario_variable_df['Variable'].str.contains('Price')]
    price_energy_rows = price_energy_rows[price_energy_rows['Variable'].str.contains('Primary Energy')]
    

    price_energy_rows['Variable'] = price_energy_rows['Variable'].apply(remove_string_between_pipe)
    indexes = price_energy_rows.index

    # Assign new values to specific rows in the column for the Variable and Unit 
    scenario_variable_df.loc[indexes, 'Variable'] = price_energy_rows['Variable']

    # Check for duplicate rows
    duplicate_rows = scenario_variable_df[scenario_variable_df.duplicated()]

    # Display duplicate rows
    print("Duplicate Rows:")
    print(duplicate_rows)

    # Count the number of duplicate rows
    num_duplicate_rows = duplicate_rows.shape[0]
    print("Number of Duplicate Rows:", num_duplicate_rows)


    # Write the new excel file in the File_Converted folder
    folder_file_converted=os.path.join(folder_path,folder_name_converted)

    # Get the correct naming for the converted file 
    filename_with_extension = os.path.basename(last_file)
    filename = splited_filename_with_extension[0] + 'converted' + splited_filename_with_extension[1]

    # Remove duplicate rows
    # scenario_variable_df.drop_duplicates(subset=['Region', 'Variable'],inplace=True)
    scenario_variable_df.drop_duplicates(subset=['Region','Variable','Unit'],inplace=True)

    # Write the following dataframe to excel
    if splited_filename_with_extension[1] == '.xls' or splited_filename_with_extension[1] == '.xlsx':
        scenario_variable_df.to_excel(os.path.join(folder_file_converted,filename))
    elif  splited_filename_with_extension[1] == '.csv': 
        scenario_variable_df.to_csv(os.path.join(folder_file_converted,filename),index=False)

    print("Conversion Done")
    print(time.time()-time0, "Seconds to run the code.")

if __name__ == "__main__":
    main()