# matching_algorithm/match_algorithm.py

import pandas as pd
import json
import re

def match_patients_to_trials(patient_csv_path, trial_csv_path, output_json_path='matched_patients.json'):
    # Load patient data
    patients = pd.read_csv(patient_csv_path)
    # Load clinical trial data
    trials = pd.read_csv(trial_csv_path)

    # Function to check age eligibility
    def is_age_eligible(age, age_criteria):
        # Find all integers in the age criteria string
        age_matches = re.findall(r'\d+', age_criteria)
        
        if not age_matches:
            return False
        
        ages = list(map(int, age_matches))
        
        # Determine eligibility based on the number of ages found
        if len(ages) == 1:
            # Only one age found, interpret as "age >= x"
            return age >= ages[0]
        elif len(ages) == 2:
            # Two ages found, interpret as a range "x <= age <= y"
            return ages[0] <= age <= ages[1]
        return False

    # Function to check gender eligibility
    def is_gender_eligible(gender, sex_criteria):
        # Check if gender is allowed based on criteria
        if sex_criteria == "All":
            return True
        return (gender == 'M' and 'Male' in sex_criteria) or (gender == 'F' and 'Female' in sex_criteria)

    # Function to check condition eligibility
    def is_condition_eligible(conditions, inclusion_criteria, exclusion_criteria):
        # Split conditions into a set for easier checking
        included_conditions = set(inclusion_criteria.split(' - '))
        excluded_conditions = set(exclusion_criteria.split(' - ')) if exclusion_criteria else set()

        # Check inclusion and exclusion
        patient_conditions = set(conditions.split(' - '))
        met_criteria = []
        
        # Check inclusion criteria
        if not included_conditions.isdisjoint(patient_conditions):
            met_criteria.append("Inclusion criteria met")
        # Check exclusion criteria
        if excluded_conditions.isdisjoint(patient_conditions):
            met_criteria.append("No exclusion criteria matched")
        
        return met_criteria

    # Create a list to hold patient matches
    patient_matches = []

    # Iterate over each patient and trial to find matches
    for _, patient in patients.iterrows():
        eligible_trials = []
        for _, trial in trials.iterrows():
            criteria_met = []
            
            # Check eligibility
            if (is_age_eligible(patient['AGE'], trial['age_criteria']) and
                is_gender_eligible(patient['GENDER'], trial['sex_criteria'])):
                # Get the criteria met
                criteria_met = is_condition_eligible(patient['CONDITIONS'], trial['inclusionCriteria'], trial['exclusionCriteria'])
                if criteria_met:
                    eligible_trials.append({
                        "trialId": trial['trialId'],
                        "trialName": trial['trialTitle'],
                        "eligibilityCriteriaMet": criteria_met
                    })
        
        # Append patient info if they have eligible trials
        if eligible_trials:
            patient_matches.append({
                "patientId": patient['Id'],
                "eligibleTrials": eligible_trials
            })

    # Write to JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(patient_matches, json_file, indent=4)

    print(f"Matching completed. Results saved to {output_json_path}")