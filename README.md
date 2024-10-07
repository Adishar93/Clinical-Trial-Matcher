# Clinical-Trial-Matcher

# Python Project - Patient Data Processing

## Project Overview
This project processes patient data from CSV files and aims to match patients with active clinical trials. The project uses two approaches for matching:

1. **Traditional Rule-Based Matching**: A standard algorithm built with `if-else` logic that evaluates patient eligibility based on predefined trial criteria.
  
2. **LLM (Large Language Model) AI-Powered Matching**: An advanced algorithm powered by AI, which not only matches patients to clinical trials but also provides detailed reasoning for why a patient is eligible or ineligible for a particular trial.

The input data, containing patient details, should be placed in the `data/` folder. The project generates both intermediate data files and the final output, which includes matched trials and eligibility reasons, stored as JSON files in the `output/` folder.

## Setup Instructions

### 1. Clone the Repository
To get started, clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Install Requirements
Ensure you have Python 3.x installed on your system. Then, install the necessary dependencies by running:
```bash
pip install -r requirements.txt
```

### 3. Prepare the Input Data
Place your CSV files containing patient data in the `data/` folder. This folder must contain the CSV files before running the program.

### 4. Run the Project
To execute the data processing, run the following command:
```bash
python main.py
```

### 5. Output
The intermediate data files and the final output will be generated in the `output/` folder. The main result will be saved in `matched_patients.json`.

## Folder Structure

```bash
your-repo-name/
│
├── data/               # Place your input CSV files here
│
├── output/             # This folder will contain the generated intermediate and final output files
│
├── patient_matching/   # This folder contains the two matching algorithms along with data processing and the scraper implementations
│
├── requirements.txt    # List of Python dependencies
│
├── main.py             # Main script to run the project
│
└── README.md           # Project setup and instructions
```
