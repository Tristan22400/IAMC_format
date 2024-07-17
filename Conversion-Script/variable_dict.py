#!/usr/bin/env python
# coding: utf-8

import pandas as pd 
import pprint

def rename_country(country_Wiliam_list): 
    # Put the country in lowercase except for the first letter (format used by IPCC for the Countries)
    new_country_Wiliam_list=[]
    for country in country_Wiliam_list: 
        country = country.lower()
        country = country.title()
        country = country.replace('_',' ')
        new_country_Wiliam_list.append(country)
    return new_country_Wiliam_list

# Fonction pour appliquer un changement aux éléments successifs similaires
def apply_change_if_similar(lst):
    new_lst = [lst[k] for k in range(len(lst))]
    for i in range(len(lst)-1):
        
        if 'bio' in new_lst[i+1]: 
            new_lst[i+1] = new_lst[i+1].replace('bio','biomass')
        if 'oceanic' in new_lst[i]: 
            new_lst[i] = new_lst[i].replace('oceanic','ocean')
        if 'hydropower' in new_lst[i]: 
            new_lst[i] = new_lst[i].replace('hydropower','hydro')
        if new_lst[i] == new_lst[i+1][:-4]:
            new_lst[i],new_lst[i+1] = modify_element(new_lst[i],new_lst[i+1])
        
        new_lst[i] = remove_underscore_before_word(new_lst[i],'fuels')
        new_lst[i] = remove_underscore_before_word(new_lst[i],'of_')
        new_lst[i] = remove_underscore_before_word(new_lst[i],'river')
        new_lst[i] = remove_underscore_before_word(new_lst[i],'space')
        
            
    return new_lst


def remove_underscore_before_word(string, word):
    index = string.find(word)
    if index != -1:
        string = string[:index-1] + string[index-1:index].replace("_", " ") + string[index:]
    return string


# Modify the writing for the CCS acronym. 
def modify_element(element, element1):
    element = element + '_w/o CCS'
    element1 = element1[:-3] + 'w/ ' +element1[-3:]
    return element, element1

# Replace the underscores by some spaces and put the adequat separator.
def change_nomnclature_element(element):
    return "|".join([word for word in element.split("_")])

def process_name_change(energy_processes_transformed):

        energy_processes_new = []
        for elem in energy_processes_transformed:
            new_elem = ''
            elem = elem[7:]
            if elem[0:2] == 'PP':
                new_elem = 'Electricity'
                if elem[-6:] == 'w/ CCS': 
                    new_elem = new_elem + '|' + change_nomnclature_element(elem[3:-6]) + elem[-6:]
                elif elem[-7:] == 'w/o CCS': 
                    new_elem = new_elem + '|' + change_nomnclature_element(elem[3:-7]) + elem[-7:]
                else : 
                    new_elem = new_elem + '|' + change_nomnclature_element(elem[3:])
            elif elem[0:2] == 'HP': 
                new_elem = 'Heat'
                if elem[-6:] == 'w/ CCS': 
                    new_elem = new_elem + '|' + change_nomnclature_element(elem[3:-6]) + elem[-6:]
                elif elem[-7:] == 'w/o CCS': 
                    new_elem = new_elem + '|' + change_nomnclature_element(elem[3:-7]) + elem[-7:]
                else: 
                    new_elem = new_elem + '|' + change_nomnclature_element(elem[3:])
            elif elem[0:3] == 'CHP':
                new_elem = 'Electricity and Heat'
                if elem[-6:] == 'w/ CCS': 
                    new_elem = new_elem  + change_nomnclature_element(elem[3:-6]) + elem[-6:]
                elif elem[-7:] == 'w/o CCS': 
                    new_elem = new_elem  + change_nomnclature_element(elem[3:-7]) + elem[-7:]
                else : 
                    new_elem = new_elem + '|' + change_nomnclature_element(elem[4:])
            energy_processes_new.append(new_elem)
        return energy_processes_new


def main(): 
    # ### Country Dict 
    file_path = "./Variable_Reference/reference.xlsx"  # Update this with the correct path

    # Read the Excel file into a pandas DataFrame
    country_IPCC_df = pd.read_excel(file_path,sheet_name=2)

    # Now you can work with the DataFrame 'df' as needed
    country_IPCC_df.head()  # Print the first few rows of the DataFrame



    # Put the country in list 
    country_IPCC_list = country_IPCC_df["Name"].to_list()

    # Get all the region used in Wiliam
    country_Wiliam_list = ['World',
    'EU27',
    'UK',
    'CHINA',
    'EASOC',
    'INDIA',
    'LATAM',
    'RUSSIA',
    'USMCA',
    'LROW',
    'AUSTRIA',
    'BELGIUM',
    'BULGARIA',
    'CROATIA',
    'CYPRUS',
    'CZECH_REPUBLIC',
    'DENMARK',
    'ESTONIA',
    'FINLAND',
    'FRANCE',
    'GERMANY',
    'GREECE',
    'HUNGARY',
    'IRELAND',
    'ITALY',
    'LATVIA',
    'LITHUANIA',
    'LUXEMBOURG',
    'MALTA',
    'NETHERLANDS',
    'POLAND',
    'PORTUGAL',
    'ROMANIA',
    'SLOVAKIA',
    'SLOVENIA',
    'SPAIN',
    'SWEDEN']

    
    new_country_Wiliam_list = rename_country(country_Wiliam_list)


    # Check the country that are not in the IPCC's list 
    for country in new_country_Wiliam_list:
        if country not in country_IPCC_list:
            print(country)


    # Create a dict that associated old name with the new name. 
    country_Wiliam_dict = dict(zip(country_Wiliam_list, new_country_Wiliam_list))

    # Change the name by hand for all the countries that appeared in the previous cell
    country_Wiliam_dict['EU27'] = 'European Union (27 member countries)' # 27 countries only different with the previous versions of 
    country_Wiliam_dict['SLOVAKIA'] = 'Slovak Republic'
    country_Wiliam_dict['UK'] = 'United Kingdom'
    country_Wiliam_dict['EASOC'] = 'East Asia and Oceania'
    country_Wiliam_dict['LATAM'] = 'Latin America' # Latin American countries 
    country_Wiliam_dict['USMCA'] = 'United States, Mexico and Canada' # not correponding in an according manner, there is mexico also. 
    country_Wiliam_dict['LROW'] = 'Rest of the World'



    # Save dictionary with pprint
    with open('Create_Variable_Dict/country_dict.txt', 'w') as f:
        pprint.pprint(country_Wiliam_dict, f)


    # ### Age Subscript 


    # Create the subscript list of the Wiliam model 
    number_list= [[0+5*k, 4+5*k] for k in range(16)]
    age_subscript_list = ['c'+str(number_list[k][0])+'c'+str(number_list[k][1]) for k in range(len(number_list))]
    age_subscript_list.append('cover80')
    age_subscript_list


    # Create the subscript list of the IAMC Compact format
    new_age_subscript_list = ['Age '+str(number_list[k][0])+'-'+str(number_list[k][1]) for k in range(len(number_list))]
    new_age_subscript_list.append('Age +80')
    new_age_subscript_list

    age_translation_dict = dict(zip(age_subscript_list, new_age_subscript_list))

    # ### GHG Dict

    # Old list of GHGs in Wiliam 
    old_ghgs_list = ['CO2', 'CH4', 'N2O', 'PFCs', 'SF6', 'HFC134a', 'HFC23', 'HFC32', 'HFC125', 'HFC143a', 'HFC152a', 'HFC227ea', 'HFC245ca', 'HFC4310mee']

    # New list for GHGs 
    new_ghgs_list = ['CO2', 'CH4', 'N2O', 'PFC', 'SF6', 'HFC134a', 'HFC23', 'HFC32', 'HFC125', 'HFC143a', 'HFC152a', 'HFC227ea', 'HFC245ca', 'HFC43-10']


    GHG_dict = dict(zip(old_ghgs_list, new_ghgs_list))

    rest_dict = dict(GHG_dict)
    rest_dict.update(age_translation_dict)


    # Save dictionary with pprint
    with open('Create_Variable_Dict/rest_dict.txt', 'w') as f:
        pprint.pprint(rest_dict, f)


    # ### Energies Subscripts 


    energy_sources_new = [
        "Electricity",
        "Gas",
        "Heat",
        "Hydrogen",
        "Liquid",
        "Solid Biomass",
        "Solid Fossil"
    ]
    energy_sources_old = [
        "TO_elec",
        "TO_gas",
        "TO_heat",
        "TO_hydrogen",
        "TO_liquid",
        "TO_solid_bio",
        "TO_solid_fossil"
    ]
    energy_vector_dict= dict(zip(energy_sources_old, energy_sources_new))

    energy_final_old = [
        "FE_elec",
        "FE_gas",
        "FE_heat",
        "FE_hydrogen",
        "FE_liquid",
        "FE_solid_bio",
        "FE_solid_fossil"
    ]
    energy_final_new = [
        "Electricity",
        "Gas",
        "Heat",
        "Hydrogen",
        "Liquid",
        "Solid|Biomass",
        "Solid|Fossil"
    ]

    energy_final_dict= dict(zip(energy_final_old, energy_final_new))


    input_string = "PE agriculture products,PE coal,PE oil,PE forestry products,PE geothermal,PE hydropower,PE natural gas,PE nuclear,PE oceanic,PE solar,PE waste,PE wind"

    # Split the string by commas to create a list
    primary_energy_raw_list = input_string.split(',')

    # Replace spaces with underscores
    primary_energy_list = [primary_energy.replace(' ', '_') for primary_energy in primary_energy_raw_list]
    transformed_primary_energy_list = [
        'Agriculture Products',
        'Coal',
        'Oil',
        'Forestry Products',
        'Geothermal',
        'Hydropower',
        'Natural Gas',
        'Nuclear',
        'Ocean',
        'Solar',
        'Waste',
        'Wind']

    energy_primary_dict= dict(zip(primary_energy_list, transformed_primary_energy_list))



    energy_processes_old = [
        "PROTRA_CHP_gas_fuels",
        "PROTRA_CHP_gas_fuels_CCS",
        "PROTRA_CHP_geothermal_DEACTIVATED",
        "PROTRA_CHP_liquid_fuels",
        "PROTRA_CHP_liquid_fuels_CCS",
        "PROTRA_CHP_solid_fossil",
        "PROTRA_CHP_solid_fossil_CCS",
        "PROTRA_CHP_waste",
        "PROTRA_CHP_solid_bio",
        "PROTRA_CHP_solid_bio_CCS",
        "PROTRA_HP_gas_fuels",
        "PROTRA_HP_solid_bio",
        "PROTRA_HP_geothermal",
        "PROTRA_HP_liquid_fuels",
        "PROTRA_HP_solar_DEACTIVATED",
        "PROTRA_HP_solid_fossil",
        "PROTRA_HP_waste",
        "PROTRA_PP_solid_bio",
        "PROTRA_PP_solid_bio_CCS",
        "PROTRA_PP_gas_fuels",
        "PROTRA_PP_gas_fuels_CCS",
        "PROTRA_PP_geothermal",
        "PROTRA_PP_hydropower_dammed",
        "PROTRA_PP_hydropower_run_of_river",
        "PROTRA_PP_liquid_fuels",
        "PROTRA_PP_liquid_fuels_CCS",
        "PROTRA_PP_nuclear",
        "PROTRA_PP_oceanic",
        "PROTRA_PP_solar_CSP",
        "PROTRA_PP_solar_open_space_PV",
        "PROTRA_PP_solar_urban_PV",
        "PROTRA_PP_solid_fossil",
        "PROTRA_PP_solid_fossil_CCS",
        "PROTRA_PP_waste",
        "PROTRA_PP_waste_CCS",
        "PROTRA_PP_wind_offshore",
        "PROTRA_PP_wind_onshore",
    ]

    

    energy_processes_transformed = apply_change_if_similar(energy_processes_old)
    energy_processes_transformed
    

    energy_processes_new = process_name_change(energy_processes_transformed)
    energy_processes_dict = dict(zip(energy_processes_old, energy_processes_new))
    energy_processes_dict


    transformation_output_old = [
        'PROTRA_blending_gas_fuels',
        'PROTRA_blending_liquid_fuels',
        'PROTRA_no_process_TI_hydrogen',
        'PROTRA_no_process_TI_solid_bio',
        'PROTRA_no_process_TI_solid_fossil'
    ]
    transformation_output_new = [
        'Gas Fuels',
        'Liquid Fuels',
        'Hydrogen',
        'Solids|Biomass',
        'Solids|Fossils'
    ]

    transformation_dict = dict(zip(transformation_output_old, transformation_output_new))



    energy_dict = dict(energy_processes_dict)
    energy_dict.update(energy_final_dict)
    energy_dict.update(energy_vector_dict)
    energy_dict.update(energy_primary_dict)
    energy_dict.update(transformation_dict)

    # Save dictionary with pprint
    with open('Create_Variable_Dict/energy_dict.txt', 'w') as f:
        pprint.pprint(energy_dict, f)

if __name__ == "__main__":
    main()