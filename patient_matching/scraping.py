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

def safe_get_text(soup_element, default_value="NA"):
    """ Safely extracts text from a BeautifulSoup element, returns default_value if None """
    return soup_element.get_text().strip() if soup_element else default_value

def extract_trial_info(driver, page_limit = 10):
    trial_data = []
    
    curr_page = 0

    while True:
        # Wait for the trial elements to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ctg-search-results-page//ctg-search-results-list")))

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results_list = soup.select_one("ctg-search-results-list")
        trials = results_list.select("ctg-search-hit-card") if results_list else []

        for trial in trials:
            try:
                # Extract trial ID and title
                trial_id_element = trial.select_one('.nct-id')
                trial_id = safe_get_text(trial_id_element)

                trial_title_element = trial.select_one(".hit-card-title.usa-card__heading")
                trial_title = safe_get_text(trial_title_element)

                # Simulate click to navigate to detailed page
                trial_element = driver.find_element(By.CSS_SELECTOR, ".hit-card-title.usa-card__heading")
                trial_element.click()

                # Wait for detailed page to load and parse
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "ctg-long-text")))
                soup_detail = BeautifulSoup(driver.page_source, "html.parser")

                # Extract inclusion/exclusion criteria and other details
                age_criteria = safe_get_text(soup_detail.select_one("ctg-standard-age"))
                sex_criteria = safe_get_text(soup_detail.select_one('[path="protocolSection.eligibilityModule.sex"]'))
                healthy_volunteers_allowed = safe_get_text(soup_detail.select_one('[path="protocolSection.eligibilityModule.healthyVolunteers"]'))

                # Select the ctg-conditions element
                conditions_element = soup_detail.select_one("ctg-conditions")
                
                if conditions_element:
                    # Find the parent div that contains the list of divs
                    parent_div = conditions_element.find("div")
                    
                    if parent_div:
                        # Find all divs inside this parent div
                        condition_divs = parent_div.find_all("div")
                        
                        # Extract the text from each div and strip any extra whitespace
                        conditions_list = [div.get_text().strip() for div in condition_divs]
                        
                        # Join the extracted text into a dash-separated string
                        conditions = " - ".join(conditions_list)

                # Initialize variables
                inclusion_criteria = ""
                exclusion_criteria = ""

                try:
                    # Find the eligibility criteria container
                    eligibility_criteria_element = soup_detail.select_one("#eligibility-criteria-description")
                    
                    if eligibility_criteria_element:
                        # Extract the p tag for Inclusion Criteria
                        inclusion_p = eligibility_criteria_element.find("p", string=re.compile("Inclusion Criteria"))
                        if inclusion_p:
                            # Find the <ul> following the Inclusion Criteria <p> tag
                            inclusion_ul = inclusion_p.find_next("ul")
                            if inclusion_ul:
                                inclusion_list = [li.get_text().strip() for li in inclusion_ul.find_all("li")]  # Extract all <li> items
                                inclusion_criteria = " - ".join(inclusion_list)  # Join them as a dash string

                        # Extract the p tag for Exclusion Criteria
                        exclusion_p = eligibility_criteria_element.find("p", string=re.compile("Exclusion Criteria"))
                        if exclusion_p:
                            # Find the <ul> following the Exclusion Criteria <p> tag
                            exclusion_ul = exclusion_p.find_next("ul")
                            if exclusion_ul:
                                exclusion_list = [li.get_text().strip() for li in exclusion_ul.find_all("li")]  # Extract all <li> items
                                exclusion_criteria = " - ".join(exclusion_list)  # Join them as a dash string
                except Exception as e:
                    print(f"Error extracting criteria for this trial: {e}")
                    continue

                # Add the trial data to the list
                trial_data.append({
                    "trialId": trial_id.replace(',','_'),
                    "trialTitle": trial_title.replace(',','_'),
                    "detailedInfo": {
                        "inclusionCriteria": inclusion_criteria.replace(',','_'),
                        "exclusionCriteria": exclusion_criteria.replace(',','_')
                    },
                    "age_criteria": age_criteria.replace(',','_'),
                    "sex_criteria": sex_criteria.replace(',','_'),
                    "healthy_volunteers_allowed": healthy_volunteers_allowed.replace(',','_'),
                    "conditions": conditions.replace(',','_')
                })

                # Go back to the previous page
                driver.back()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ctg-search-results-page//ctg-search-results-list")))

            except Exception as e:
                print(f"Error processing trial: {e}")
                continue  # Skip trial if an error occurs

        curr_page += 1
        print("Page ", str(curr_page), ": Completed!")
        if curr_page == page_limit:
            break

        # Find the 'Next' button and click it if exists, otherwise break the loop
        try:
            next_page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".usa-pagination__link.usa-pagination__next-page")))
            next_page_button.click()
        except:
            break  # No more pages to scrape, exit the loop

    return trial_data

def scrape_clinical_trials(page_limit):
    url = "https://clinicaltrials.gov/search?aggFilters=status:rec"
    driver = setup_driver()
    driver.get(url)

    # Extract all trial information across multiple pages
    trial_data = extract_trial_info(driver, page_limit)

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
            "healthy_volunteers_allowed": trial["healthy_volunteers_allowed"],
            "conditions": trial["conditions"]
        })

    # Create a DataFrame from the flattened data
    df = pd.DataFrame(flattened_data)

    # Write the DataFrame to a CSV file, overwriting if it exists
    df.to_csv(filename, index=False)

    
   