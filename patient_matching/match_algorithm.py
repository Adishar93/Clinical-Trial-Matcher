import pandas as pd
import json
import re

def match_patients_to_trials(patient_csv_path, trial_csv_path, output_json_path='matched_patients.json'):
    """
    Matches patients to clinical trials based on eligibility criteria. This function uses traditional rule-based matching.
    It has very simple implementation to demonstrate the concept of matching patients to clinical trials. You can run these rules for large data (Millions of records) as well.
    it writes the output to a JSON file.

    Args:
        patient_csv_path (str): The file path to the CSV containing processed patient data.
        trial_csv_path (str): The file path to the CSV containing clinical trial data.
        output_json_path (str): The file path where the output JSON file will be saved.

    Returns:
        None

    """
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

    # Function to check inclusion and exclusion criteria
    def check_inclusion_exclusion(patient_conditions, inclusion_criteria, exclusion_criteria):
        patient_conditions = set(patient_conditions.split(' - ')) if pd.notna(patient_conditions) else set()
        included_conditions = set(inclusion_criteria.split(' - ')) if pd.notna(inclusion_criteria) else set()
        excluded_conditions = set(exclusion_criteria.split(' - ')) if pd.notna(exclusion_criteria) else set()

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
            age_eligible = is_age_eligible(patient['AGE'], trial['age_criteria'])
            gender_eligible = is_gender_eligible(patient['GENDER'], trial['sex_criteria'])

            # Check eligibility
            if age_eligible and gender_eligible:
                criteria_met.append("Age criteria met")
                criteria_met.append("Gender criteria met")
                
                # Get the criteria met for conditions
                condition_met = check_inclusion_exclusion(patient['CONDITIONS'], trial['inclusionCriteria'], trial['exclusionCriteria'])
                criteria_met.extend(condition_met)
                
                # Add the trial if any criteria are met
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