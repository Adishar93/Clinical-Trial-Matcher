from matching_algorithm.data_preparation import load_and_process_patient_data
from matching_algorithm.scraping import scrape_clinical_trials, write_trials_to_csv
from matching_algorithm.match_algorithm import match_patients_to_trials
from matching_algorithm.output_generation import generate_output

def main():

    # Step 1: Scrape active clinical trials
    clinical_trials = scrape_clinical_trials()
    write_trials_to_csv('./output/scraped_trials.csv', clinical_trials)

    # Step 2: Load patient data
    patient_processed_data = load_and_process_patient_data('data/csv/')
    patient_processed_data.to_csv('output/patient_processed.csv', index=False)

    # Step 3: Run matching algorithm
    matches = match_patients_to_trials('output/patient_processed.csv', './output/scraped_trials.csv', 'output/matched_patients.json')

    # Step 4: Generate output (JSON and Excel)
    #generate_output(matches, 'output/eligible_trials.json', 'output/eligible_trials.xlsx')

    print("Hello world")

if __name__ == '__main__':
    main()