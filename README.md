# EventEase – AI/ML & Data Engineering Internship

## Task 01: Dataset Collection and Preparation

## 1. Project Overview

The objective of this task is to collect, organize, clean, validate and analyze structured event vendor data for EventEase.

The prepared datasets will support the future development of an AI-powered event vendor recommendation and discovery system.

## 2. Project Scope

**Primary Pilot Location:**
- CBD Belapur, Navi Mumbai

**Secondary Locations:**
- Vashi
- Nerul

The location values are maintained separately to support location-based vendor filtering.

## 3. Datasets Created

### A. Event Categories

Contains eight required event types:

- Wedding
- Birthday
- Corporate Event
- Engagement
- Baby Shower
- College Event
- Private Party
- Festival

### B. Vendor Categories

Contains seven main vendor categories:

- Decoration
- Photography
- Catering
- Venues
- Entertainment
- Makeup
- Event Planning

Each category is organized with its corresponding subcategories.

### C. Decoration Subcategories

Contains four decoration service types:

- Stage
- Balloon
- Floral
- Theme Decoration

### D. Vendor Master Dataset

Contains 60 synthetic sample vendor records across six vendor categories and three pilot locations.

The dataset includes:

- Vendor ID
- Vendor Name
- Category
- Subcategory
- Event Type
- Location
- Pricing Information
- Description
- Services Offered
- Rating
- Availability
- Contact Information
- Synthetic Data Indicator

All 60 records are marked as synthetic. They are sample records and must not be treated as verified real businesses.

### E. Venue Leads

Contains seven potential venue/business leads across CBD Belapur, Vashi and Nerul.

- All seven records have Pending verification status.
- Some contact and address information is missing.
- Available information requires independent verification.

### F. Event-Type Leads

Contains four additional potential business leads for event coverage research.

- Candidate event types are stored separately from confirmed event types.
- All four records have Pending verification status.
- Candidate event types require confirmation before being treated as actual services.

## 4. Data Cleaning

Performed the following operations using Python and Pandas:

- Removed duplicate rows.
- Checked duplicate vendor IDs.
- Removed unnecessary whitespace.
- Standardized vendor category names.
- Standardized pricing type values.
- Checked missing values.
- Saved the cleaned vendor dataset.

**Output:**

`data/clean/vendors_clean.csv`

Latest cleaned vendor dataset:
- 60 records
- 14 columns
- Zero duplicate rows
- Zero duplicate vendor IDs

## 5. Data Validation

Validation checks included:

- Dataset dimensions.
- Duplicate records.
- Duplicate vendor IDs.
- Missing values.
- Vendor locations.
- Vendor categories.
- Verification status.
- Synthetic data identification.
- Venue lead validation.
- Event-type lead validation.

The synthetic vendor dataset contains six categories. Venues are maintained separately in the venue leads dataset.

## 6. Event Coverage Analysis

Analyzed coverage for all eight required event types using the latest cleaned synthetic vendor dataset.

| Event Type | Sample Vendor Count |
|---|---:|
| Wedding | 19 |
| Birthday | 18 |
| Corporate Event | 15 |
| Engagement | 17 |
| Baby Shower | 13 |
| College Event | 13 |
| Private Party | 20 |
| Festival | 11 |

All eight required event types are represented in the synthetic sample dataset.

The final coverage report also includes potential leads from the separate venue leads and event-type leads datasets.

Potential leads are not treated as verified vendors or confirmed services. Sample vendor counts and potential lead counts are maintained separately.

**Output:**

`data/clean/final_event_coverage_report.csv`

## 7. Pricing Data Handling

Pricing information is maintained using separate fields:

- `min_price_per_plate`
- `max_price_per_plate`
- `min_price_per_event`
- `max_price_per_event`
- `pricing_type`

Pricing types include:

- `per_plate`
- `per_event`
- `both`

Irrelevant pricing fields are left blank (NULL) instead of converting one pricing model into another.

No assumptions are made to infer per-plate pricing from per-event pricing or vice versa.

## 8. Recommendation Prototype

A basic rule-based vendor recommendation prototype was developed and tested using the cleaned synthetic vendor dataset.

The prototype evaluates:

- Vendor category.
- Availability.
- Budget compatibility.
- Location relevance.
- Rating.
- Event relevance.

**Scoring weights:**

| Factor | Weight |
|---|---:|
| Budget | 35% |
| Location | 30% |
| Rating | 25% |
| Event Relevance | 10% |

Five test scenarios were processed, including an unavailable-vendor test using a separate temporary test fixture.

The prototype is rule-based and does not use a trained Machine Learning model.

**Test documentation:**

`docs/test_results.md`

## 9. Current Limitations

- The 60 vendor records are synthetic sample data.
- The seven venue leads and four event-type leads are pending verification.
- Candidate event types are not confirmed services.
- Real business contact details, availability, ratings and services require verification.
- Location scoring is a prototype assumption and does not calculate actual geographical distance.
- Recommendation results from synthetic data are for testing purposes only.
- Advanced machine learning model training is outside the scope of this initial dataset preparation task.

## 10. Tools and Technologies

- Python
- Pandas
- NumPy
- Excel
- CSV
- VS Code

## 11. Project Folder Structure

```text
eventease-ai-ml-task01/
│
├── data/
│   ├── raw/
│   │   ├── event_type_leads.csv
│   │   ├── vendors.csv
│   │   ├── venue_leads.csv
│   │   └── venue_verification_tracker.csv
│   │
│   ├── clean/
│   │   ├── event_coverage_report.csv
│   │   ├── final_event_coverage_report.csv
│   │   ├── vendors_clean.csv
│   │   └── venue_verification_report.csv
│   │
│   └── reference/
│       ├── decoration_subcategories.csv
│       ├── event_categories.csv
│       └── vendor_categories.csv
│
├── docs/
│   ├── data_dictionary.md
│   └── test_results.md
│
├── notebooks/
│   └── data_cleaning.ipynb
│
├── src/
│   ├── category_analysis.py
│   ├── create_category_datasets.py
│   ├── create_event_type_leads.py
│   ├── create_venue_leads.py
│   ├── data_cleaning.py
│   ├── event_coverage_analysis.py
│   ├── final_event_coverage_analysis.py
│   ├── generate_data.py
│   ├── prepare_verification_tracker.py
│   ├── recommendation.py
│   ├── update_venue_sources.py
│   ├── validate_data.py
│   ├── validate_event_type_leads.py
│   ├── validate_venue_leads.py
│   └── venue_verification_report.py
│
├── tests/
│   ├── run_all_tests.py
│   └── test_scenario_4.py
│
├── .gitignore
└── README.md
```

Note: The virtual environment (`venv/`) and Jupyter checkpoint files are excluded from GitHub.

```text
eventease-ai-ml-task01/
│
├── data/
│   ├── raw/
│   ├── clean/
│   └── reference/
│
├── docs/
│   ├── data_dictionary.md
│   └── test_results.md
│
├── notebooks/
│
├── src/
│
├── tests/
│
├── README.md
└── .gitignore
```

## 12. How to Run the Project

Run commands from the project root directory.

### A. Install Dependencies

Activate the virtual environment and install the required packages:

```bash
pip install pandas numpy tabulate
```

### B. Generate and Prepare Datasets

Run these commands when setting up or intentionally regenerating the datasets:

```bash
python src/create_category_datasets.py
python src/generate_data.py
python src/data_cleaning.py
```

**Important:** Dataset generation scripts may overwrite existing CSV files. Keep backups of any manually updated data before regenerating datasets.

### C. Validate Existing Datasets

```bash
python src/validate_data.py
python src/category_analysis.py
python src/venue_verification_report.py
python src/validate_venue_leads.py
python src/validate_event_type_leads.py
```

### D. Run Event Coverage Analysis

```bash
python src/event_coverage_analysis.py
python src/final_event_coverage_analysis.py
```

### E. Run Recommendation Tests

```bash
python tests/run_all_tests.py
```

The recommendation prototype uses synthetic vendor data and a separate temporary fixture for the unavailable-vendor test.

**Important:** Venue leads and event-type leads are maintained separately. Avoid rerunning their creation scripts after manual updates unless regeneration is intentional.

Activate the Python virtual environment before running the scripts.

Install the required dependencies:

```bash
pip install pandas numpy tabulate
```

Run the scripts from the project root directory in the following order:

```bash
python src/create_category_datasets.py
python src/generate_data.py
python src/data_cleaning.py
python src/validate_data.py
python src/category_analysis.py
python src/venue_verification_report.py
python src/validate_venue_leads.py
python src/validate_event_type_leads.py
python src/event_coverage_analysis.py
python src/final_event_coverage_analysis.py
python tests/run_all_tests.py
```

**Note:** The venue leads and event-type leads are maintained separately. Do not rerun their creation scripts after manual updates unless you intend to regenerate those files.

## 13. Future Work

- Verify real vendor information.
- Collect additional vendors for missing event categories and services.
- Improve dataset coverage.
- Confirm vendor services and availability.
- Prepare verified data for future AI/ML development.
- Explore trained recommendation models when verified data becomes available.

## 14. Conclusion

Task 01 established the initial structured datasets for the EventEase platform.

Data collection, cleaning, validation, category analysis, event coverage analysis and a basic rule-based recommendation prototype were implemented using Python and Pandas.

The prepared datasets provide a foundation for future vendor discovery and AI-powered recommendation development.

**Data integrity note:** Synthetic records, potential business leads and verified business information are maintained as distinct data types. Pending records must not be presented as verified vendors.