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

### 4. Optionally switch to the AI matchmaker
To do that comment line ```match_patients_to_trials('output/patient_processed.csv', './output/scraped_trials.csv', 'output/matched_patients.json')```
and uncomment ```# match_patients_to_trials_ai('output/patient_processed.csv', './output/scraped_trials.csv', 'output/matched_patients_ai.json')```
in the main.py file.

### 5. Run the Project
To execute the data processing, run the following command:
```bash
python main.py
```

### 6. Output
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

## Approach and Thought Process

### Problem Understanding and Decomposition
To approach this problem, I first analyzed the patient dataset available at [Synthea's download page](https://synthea.mitre.org/downloads). The full dataset is around 20 GB, but for the purpose of this assignment, I decided to limit the scope to 1,000 patient records. This decision was driven by the need to first validate the matching model in a more controlled setting, ensuring efficiency and feasibility without overwhelming the initial testing process.

After reviewing the patient CSV files, I selected relevant files containing crucial patient data such as demographics and medical history. I cleaned the dataset by removing unnecessary columns, creating a more focused and structured patient record set that could effectively support clinical trial matching.

### User Empathy and Motivation
The goal of the project was to build an efficient solution for matching patients to clinical trials. My primary users would be clinicians or researchers looking to quickly identify eligible patients. I empathized with their need for clarity and accuracy in the eligibility reasoning, as well as the importance of streamlining the trial-patient matching process to improve healthcare outcomes.

### Thought Process and Product Solution
To provide meaningful matches, I explored two methods:

1. **Rule-Based Matching**: I started by implementing a traditional approach using basic parameters like age, gender, and simple text matching in the inclusion/exclusion criteria. While this produced functional matches, the eligibility reasoning was static and not deeply personalized, which limited its impact in real-world applications.

2. **AI-Powered Matching**: I recognized that generative AI and Large Language Models (LLMs) offered greater potential in terms of extracting more nuanced eligibility criteria. My exploration of research papers and recent advancements in NLP led me to consider multiple ways to leverage LLMs, such as:
   - **Direct Matching**: Using LLMs to directly analyze patient and trial data for eligibility.
   - **NLP for Unstructured Data**: Processing free-text inclusion/exclusion criteria into structured data for easier matching.
   - **Preprocessing with Vector Databases**: Reducing token usage and improving efficiency by preprocessing data before running AI models.

Given the time constraints and the costs involved in using a large amount of tokens, I opted for straightforward matching without preprocessing the strings. This approach provided good insights into eligibility criteria and why patients were matched, even though it was tested with a smaller dataset of 5 patients and 30 clinical trials.

### Identifying Key Hypotheses and Experiments
I hypothesized that the LLM-based matching could outperform rule-based methods in terms of accuracy and reasoning depth. To validate this hypothesis, I tested a limited dataset and compared the outcomes. While initial results were promising, I acknowledge the need for larger-scale experiments to truly assess the model’s capabilities.

### Prioritization and Execution
In prioritizing the solution, I focused on building a shippable product within the limited time frame, ensuring that both the rule-based and AI-powered approaches could deliver a working solution. While a more robust AI-based system would require preprocessing and optimization for cost, I ensured that the current implementation demonstrates the potential for more complex matching.

### Conclusion
This project is an initial exploration of how AI can assist in clinical trial matching. While the results are promising with limited data, future iterations could scale this solution with additional preprocessing, token optimization, and larger datasets. This would significantly enhance the system's ability to explain the reasoning behind patient eligibility for clinical trials.

## Future Work

In future iterations of this project, several enhancements can be made to improve both the accuracy and efficiency of the patient-trial matching system:

1. **Combining Rule-Based and AI-Powered Matching**: By integrating rule-based matching with AI-powered algorithms, we can ensure that simpler cases are handled quickly by the rule-based system, while more complex eligibility determinations are processed using AI. This hybrid approach would optimize both speed and accuracy, giving us the best of both methods.

2. **Preprocessing for Improved Efficiency**: Before passing data to the LLM, we could preprocess the inclusion and exclusion criteria using NLP techniques to convert unstructured text into a structured format. This preprocessing step would reduce the complexity of the data and help minimize the number of tokens needed for LLM processing, significantly lowering costs while preserving accuracy.

3. **Using Vector Databases**: Implementing a vector database for similarity search and efficient retrieval could further optimize the AI-powered matching process. By storing processed patient and trial data as vectors, we could reduce the need for token-heavy operations, as the database would precompute similarities between patients and trials. This would not only reduce costs but also provide highly accurate results with detailed reasoning for eligibility decisions.

4. **Scaling the Solution**: With more patient data and a larger set of clinical trials, the AI model could be further fine-tuned and optimized to handle real-world datasets. This would allow the system to handle thousands of patients and trials efficiently, making it a valuable tool for healthcare providers and researchers.

By incorporating these future enhancements, the system could offer a scalable, cost-effective, and highly accurate patient-trial matching solution that delivers rich reasoning for each eligibility decision, ensuring better outcomes for both patients and clinical researchers.
