from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re

def setup_driver():
    # Set up headless Chrome for faster execution
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver

def extract_trial_info(driver):
    trial_data = []
    page_limit = 100
    curr_page = 0

    # Loop through each page of results
    while True:
        # Wait for the trial elements to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ctg-search-results-page//ctg-search-results-list")))

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        results_list = soup.select_one("ctg-search-results-list")

        # Select all trial cards within the results list
        trials = results_list.select("ctg-search-hit-card")

        # Initialize a list to store trial data
        trial_data = []

        for trial in trials:
            # Extract basic trial information
            trial_id_element = trial.select_one('.nct-id')  # Find the element with class nct-id
            trial_id = trial_id_element.get_text() if trial_id_element else None 
            
            # Update the selector for the title to match the structure within ctg-search-hit-card
            trial_title = trial.select_one(".hit-card-title.usa-card__heading.font-body-md.desktop\\:font-body-lg.usa-link.text-no-underline.text-normal.text-primary-dark").get_text()

            # Simulate click to navigate to the detailed page (Selenium needed here)
            trial_element = driver.find_element(By.CSS_SELECTOR, ".hit-card-title.usa-card__heading.font-body-md.desktop\\:font-body-lg.usa-link.text-no-underline.text-normal.text-primary-dark")
            trial_element.click()

            # Wait for detailed trial page to load and parse it with BeautifulSoup
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "ctg-long-text")))
            soup_detail = BeautifulSoup(driver.page_source, "html.parser")

            # Extract detailed information (inclusion/exclusion criteria)
            detailed_info = soup_detail.select_one("#eligibility-criteria-description").get_text()
            age_criteria = soup_detail.select_one("ctg-standard-age").get_text()
            sex_criteria = soup_detail.select_one('[path="protocolSection.eligibilityModule.sex"]').get_text()
            healthy_volunteers_allowed = soup_detail.select_one('[path="protocolSection.eligibilityModule.healthyVolunteers"]').get_text()

            # Initialize inclusion and exclusion variables
            inclusion_criteria = ""
            exclusion_criteria = ""

            # Use regex to separate the inclusion and exclusion criteria
            match = re.search(r"Inclusion Criteria:(.*?)(Exclusion Criteria:|$)", detailed_info, re.DOTALL)
            if match:
                inclusion_criteria = match.group(1).strip()  # Extract inclusion criteria
                exclusion_match = re.search(r"Exclusion Criteria:(.*)", detailed_info, re.DOTALL)
                if exclusion_match:
                    exclusion_criteria = exclusion_match.group(1).strip()  # Extract exclusion criteria

            # Optional: Clean up the inclusion and exclusion criteria
            inclusion_criteria = re.sub(r'\s+', ' ', inclusion_criteria)  # Remove excessive whitespace
            exclusion_criteria = re.sub(r'\s+', ' ', exclusion_criteria)  # Remove excessive whitespace

            # Add the trial data to the list
            trial_data.append({
                "trialId": trial_id,
                "trialTitle": trial_title,
                "detailedInfo": {
                    "inclusionCriteria": inclusion_criteria,
                    "exclusionCriteria": exclusion_criteria
                },
                "age_criteria" :age_criteria,
                "sex_criteria" :sex_criteria,
                "healthy_volunteers_allowed" : healthy_volunteers_allowed
            })

            # Go back to the previous page
            driver.back()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ctg-search-results-page//ctg-search-results-list")))
        
        curr_page += 1
        if curr_page == page_limit:
            break

        # Find the 'Next' button and click it if it exists, otherwise break the loop
        try:
            next_page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".usa-pagination__link.usa-pagination__next-page")))
            next_page_button.click()
        except:
            break  # No more pages to scrape, exit the loop

    return trial_data

def scrape_clinical_trials():
    url = "https://clinicaltrials.gov/search?aggFilters=status:rec"
    driver = setup_driver()
    driver.get(url)

    # Extract all trial information across multiple pages
    trial_data = extract_trial_info(driver)

    # Close the driver
    driver.quit()

    return trial_data


# Function to write trial data to a CSV file using pandas
def write_trials_to_csv(filename, data):
    # Create a list to hold flattened data for DataFrame
    flattened_data = []
    
    for trial in data:
        flattened_data.append({
            "trialId": trial["trialId"],
            "trialTitle": trial["trialTitle"],
            "inclusionCriteria": trial["detailedInfo"]["inclusionCriteria"],
            "exclusionCriteria": trial["detailedInfo"]["exclusionCriteria"],
            "age_criteria": trial["age_criteria"],
            "sex_criteria": trial["sex_criteria"],
            "healthy_volunteers_allowed": trial["healthy_volunteers_allowed"]
        })

    # Create a DataFrame from the flattened data
    df = pd.DataFrame(flattened_data)

    # Write the DataFrame to a CSV file, overwriting if it exists
    df.to_csv(filename, index=False)

    
   