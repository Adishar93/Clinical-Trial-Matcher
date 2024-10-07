import openai
import pandas as pd
import json
import re


def match_patients_to_trials_ai(patient_csv_path, trial_csv_path, output_json_path='../output/matched_patients_ai.json'):
    """
    Matches patients to clinical trials based on eligibility criteria. This function uses ai based matching.
    It currently uses OpenAI gpt-40-mini model and because the tokens are cost sensitive, it uses limits and offsets to process
    the data to demonstrate its capability with small sample of data.
    it writes the output to a JSON file.

    Args:
        patient_csv_path (str): The file path to the CSV containing processed patient data.
        trial_csv_path (str): The file path to the CSV containing clinical trial data.
        output_json_path (str): The file path where the output JSON file will be saved.

    Returns:
        None

    """
    # Set your OpenAI API key
    openai.api_key = 'sk-XXXXXXXX'

    # Load the patient and clinical trial data
    patients_df = pd.read_csv(patient_csv_path)
    trials_df = pd.read_csv(trial_csv_path)

    # Define limits and offsets as the solution is cost sensitive
    PATIENT_LIMIT = 10   # Set the limit for the number of patients to compare
    PATIENT_OFFSET = 20   # Set the start offset for patients
    TRIAL_LIMIT = 30     # Set the limit for the number of trials to compare
    TRIAL_OFFSET = 30     # Set the start offset for trials

    # Limit the dataframes to the specified limits with offsets
    limited_patients = patients_df.iloc[PATIENT_OFFSET:PATIENT_OFFSET + PATIENT_LIMIT]
    limited_trials = trials_df.iloc[TRIAL_OFFSET:TRIAL_OFFSET + TRIAL_LIMIT]

    # Define the function to check eligibility
    def check_eligibility(patient, trial):
        prompt = f"""
        Patient: Age {patient['AGE']}, Gender {patient['GENDER']}, Conditions: {patient['CONDITIONS']}
        Trial: ID {trial['trialId']}, Name: {trial['trialTitle']}, Inclusion: {trial['inclusionCriteria']}, Exclusion: {trial['exclusionCriteria']}, Age: {trial['age_criteria']}, Gender: {trial['sex_criteria']}
        Is the patient eligible? Respond with 'yes' or 'no'. If 'yes' then only add criteria met.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use appropriate model
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response['choices'][0]['message']['content']

    # Match patients to trials
    def match_patients_to_trials(patients, trials):
        results = []
        
        for _, patient in patients.iterrows():
            eligible_trials = []

            for _, trial in trials.iterrows():
                eligibility_info = check_eligibility(patient, trial)
                print(eligibility_info)
                if 'yes' in eligibility_info.lower():
                    # Remove only the first instance of "yes" (case insensitive) and trim the remaining text
                    criteria_met = re.sub(r'(?i)\byes\b', '', eligibility_info, count=1).strip()
                    
                    eligible_trials.append({
                        "trialId": trial['trialId'],
                        "trialName": trial['trialTitle'],
                        "criteria_met": criteria_met if criteria_met else []
                    })

            results.append({
                "patientId": patient['Id'],
                "eligibleTrials": eligible_trials
            })
        
        return results

    # Run the matching with limited datasets
    matched_results = match_patients_to_trials(limited_patients, limited_trials)

    with open(output_json_path, 'w') as json_file:
        json.dump(matched_results, json_file, indent=2)

    print(f"Output written to {output_json_path}")