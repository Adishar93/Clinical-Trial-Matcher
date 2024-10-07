from patient_matching.data_preparation import load_and_process_patient_data
from patient_matching.scraping import scrape_clinical_trials, write_trials_to_csv
from patient_matching.match_algorithm import match_patients_to_trials
from patient_matching.match_algorithm_ai import match_patients_to_trials_ai

def main():

    # Step 1: Scrape active clinical trials
    clinical_trials = scrape_clinical_trials(20)
    write_trials_to_csv('./output/scraped_trials.csv', clinical_trials)

    # Step 2: Load patient data
    patient_processed_data = load_and_process_patient_data('data/csv/')
    patient_processed_data.to_csv('output/patient_processed.csv', index=False)

    # Step 3: Run matching algorithm and generate output
    match_patients_to_trials('output/patient_processed.csv', './output/scraped_trials.csv', 'output/matched_patients.json')

    # OR Step 3 (AI): Run matching algorithm using AI and generate output
    # match_patients_to_trials_ai('output/patient_processed.csv', './output/scraped_trials.csv', 'output/matched_patients_ai.json')


    print("Execution Completed!")

if __name__ == '__main__':
    main()