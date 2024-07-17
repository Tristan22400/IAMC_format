#!/usr/bin/env python
# coding: utf-8

import os
import glob
import pandas as pd

def merge_csv_files(input_folder, output_file):
    # Get a list of all CSV files in the input folder
    csv_files = glob.glob(os.path.join(input_folder, '*.csv'))
    
    # Initialize a DataFrame to store the merged data
    merged_data = pd.DataFrame()

    for i, file_path in enumerate(csv_files):
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        
        
        # Append DataFrame to the merged_data DataFrame
        merged_data = merged_data._append(df, ignore_index=True)
    
    # Write the merged data to a CSV file
    merged_data.to_csv(output_file, index=False)
    print("Merged CSV file saved successfully.")

# Example usage:
input_folder = 'File_Converted'
output_file = 'Scenario.csv'
merge_csv_files(input_folder, output_file)

