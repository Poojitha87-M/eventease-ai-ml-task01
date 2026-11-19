
# EventEase – AI/ML Task 01
## Vendor Dataset and Recommendation Engine

### 1. Project Overview

EventEase is an event services marketplace prototype that helps customers find suitable vendors based on their event requirements.

This project focuses on creating a synthetic vendor dataset, cleaning and validating the data, and building a rule-based vendor recommendation engine using Python and Pandas.

### 2. Project Objectives

- Create a dataset containing at least 50 vendor records.
- Clean and validate vendor information.
- Support category, location, availability, and budget filtering.
- Rank vendors using a weighted scoring system.
- Test the recommendation engine with different customer scenarios.

### 3. Technology Stack

- Python
- Pandas
- NumPy
- Jupyter Notebook
- CSV
- Git and GitHub

### 4. Pilot Locations

- CBD Belapur
- Vashi
- Nerul

### 5. Vendor Categories

- Catering
- Photography
- Decoration
- Event Planning
- Makeup Artist
- Entertainment

### 6. Dataset Information

The project contains 60 synthetic vendor records.

Each record includes:
- Vendor ID and name
- Category and location
- Per-plate and per-event pricing
- Pricing type
- Rating and availability
- Supported event types
- Review count
- Synthetic data indicator

All vendor records are synthetic and are not real business listings or verified market prices.

### 7. Data Cleaning

Data cleaning and validation include:
- Checking missing values
- Removing duplicate records
- Validating vendor IDs
- Standardising text values
- Converting numeric columns
- Checking ratings and prices
- Validating pricing model consistency

### 8. Recommendation Logic

The recommendation engine follows these steps:

1. Filter vendors by category.
2. Remove unavailable vendors.
3. Filter vendors based on budget compatibility.
4. Calculate location matching score.
5. Calculate rating score.
6. Calculate event relevance score.
7. Rank vendors using a weighted score.

### 9. Recommendation Scoring

| Factor | Weight |
|---|---:|
| Budget compatibility | 35% |
| Location match | 30% |
| Vendor rating | 25% |
| Event relevance | 10% |

Final score:

`(Budget × 0.35) + (Location × 0.30) + (Rating × 0.25) + (Relevance × 0.10)`

The weights and scoring rules are initial prototype assumptions, not trained machine learning parameters.

### 10. Project Structure

```text
eventease-ai-ml-task01/
│
├── data/
│   ├── raw/
│   │   └── vendors.csv
│   └── clean/
│       └── vendors_clean.csv
│
├── notebooks/
│   └── data_cleaning.ipynb
│
├── src/
│   ├── generate_data.py
│   └── recommendation.py
│
├── tests/
│   ├── run_all_tests.py
│   └── test_scenario_4.py
│
├── docs/
│   ├── data_dictionary.md
│   └── test_results.md
│
└── README.md
```

### 11. How to Run the Project

Install dependencies:

```bash
pip install pandas numpy jupyter tabulate
```

Generate the synthetic dataset:

```bash
python src/generate_data.py
```

Run the data cleaning notebook:

```bash
jupyter notebook
```

Run the recommendation engine:

```bash
python src/recommendation.py
```

Run automated scenario tests:

```bash
python tests/run_all_tests.py
python tests/test_scenario_4.py
```

### 12. Testing

The recommendation engine is tested using five customer scenarios covering:

- Birthday catering
- Wedding decoration
- Very low budget entertainment
- Makeup Artist vendors with no availability
- Small-event photography

Refer to `docs/test_results.md` for test outcomes.

### 13. Limitations

- The dataset contains synthetic sample records.
- Pricing and ratings are illustrative.
- Location matching uses simplified area-based scores.
- Recommendation weights are manually defined.
- The prototype does not use a trained machine learning model.

### 14. Future Improvements

- Collect verified vendor information.
- Introduce distance-based location matching.
- Tune recommendation weights using real user feedback.
- Add vendor and customer feedback mechanisms.
- Evaluate machine learning-based ranking when sufficient real data is available.
