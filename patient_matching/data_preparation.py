import pandas as pd
from datetime import datetime

# matching_algorithm/data_preparation.py
def load_and_process_patient_data(file_path):
    # Load patients.csv
    patients = pd.read_csv(file_path + 'patients.csv')

    # Remove patients with a DEATHDATE
    if 'DEATHDATE' in patients.columns:
        patients = patients[patients['DEATHDATE'].isnull() | (patients['DEATHDATE'].str.strip() == '')]
    
    # Convert BIRTHDATE to datetime from string
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'], format='%Y-%m-%d', errors='coerce')

    # Calculate age based on today's date
    today = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))

    # Calculate the AGE column
    patients['AGE'] = today.year - patients['BIRTHDATE'].dt.year

    # Load conditions.csv
    conditions = pd.read_csv(file_path + 'conditions.csv')
    
    # Create separate columns for current and previous conditions based on the STOP column
    conditions['current_conditions'] = conditions.apply(
        lambda x: x['DESCRIPTION'] if pd.isnull(x['STOP']) else '', axis=1
    )
    conditions['previous_conditions'] = conditions.apply(
        lambda x: x['DESCRIPTION'] if not pd.isnull(x['STOP']) else '', axis=1
    )
    
    # Group by PATIENT and concatenate current and previous conditions, filtering out empty strings
    current_conditions_grouped = conditions.groupby('PATIENT')['current_conditions'].apply(
        lambda x: ' - '.join(x[x != ''])  # Join non-empty strings
    ).reset_index()
    
    previous_conditions_grouped = conditions.groupby('PATIENT')['previous_conditions'].apply(
        lambda x: ' - '.join(x[x != ''])  # Join non-empty strings
    ).reset_index()

    # Merge the patients with the grouped conditions
    merged_data = pd.merge(patients, current_conditions_grouped, left_on='Id', right_on='PATIENT', how='left')
    merged_data = pd.merge(merged_data, previous_conditions_grouped, left_on='Id', right_on='PATIENT', how='left', suffixes=('', '_previous'))
    
    # Drop the redundant 'PATIENT' column from conditions after the merge
    merged_data = merged_data.drop(columns=['PATIENT'])
    
    # Rename current_conditions and previous_conditions columns
    merged_data.rename(columns={'current_conditions': 'CONDITIONS', 'previous_conditions': 'PREVIOUS_CONDITIONS'}, inplace=True)

    # Filter out rows where CONDITIONS is blank
    merged_data = merged_data[merged_data['CONDITIONS'].str.strip() != '']

    # Keep only the specified columns
    merged_data = merged_data[['Id', 'PREFIX', 'FIRST', 'LAST', 'GENDER', 'AGE', 'CONDITIONS', 'PREVIOUS_CONDITIONS']]
 
    # Return the merged data with combined descriptions
    return merged_data