from matching_algorithm.data_preparation import load_patient_data
from matching_algorithm.scraping import scrape_clinical_trials, write_trials_to_csv
from matching_algorithm.match_algorithm import match_patients_to_trials
from matching_algorithm.output_generation import generate_output

def main():
    # Step 1: Load patient data
    patient_data = load_patient_data('data/csv/')

    # Step 2: Scrape active clinical trials
    clinical_trials = scrape_clinical_trials()
    write_trials_to_csv('./output/scraped_trials.csv', clinical_trials)

    # Step 3: Run matching algorithm
    matches = match_patients_to_trials(patient_data, clinical_trials)

    # Step 4: Generate output (JSON and Excel)
    generate_output(matches, 'output/eligible_trials.json', 'output/eligible_trials.xlsx')

    print("Hello world")

if __name__ == '__main__':
    main()