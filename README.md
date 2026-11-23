# EventEase – AI/ML & Data Engineering Internship

## Task 01: Dataset Collection and Preparation

## 1. Project Overview

The objective of this task is to collect, organize, clean, validate and analyze structured event vendor data for EventEase.

The prepared datasets will support the future development of an AI-powered event vendor recommendation and discovery system.

## 2. Project Scope

**Synthetic vendor dataset locations:**
- Mumbai
- Bangalore
- Pune
- Thane

**Venue lead locations:**
- Legacy leads: CBD Belapur, Vashi and Nerul
- New leads: Mumbai, Pune, Bangalore and Thane

Location values are maintained separately to support location-based vendor filtering.

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

File: `data/reference/event_categories.csv`

### B. Vendor Categories

Contains seven main vendor categories:
- Decoration
- Photography
- Catering
- Venues
- Entertainment
- Makeup
- Event Planning

Each category is organized with corresponding subcategories.

File: `data/reference/vendor_categories.csv`

### C. Decoration Subcategories

Contains four decoration service types:
- Stage
- Balloon
- Floral
- Theme Decoration

File: `data/reference/decoration_subcategories.csv`

### D. Synthetic Vendor Master Dataset

Contains 60 synthetic sample vendor records across six vendor categories and four locations.

Current location distribution:
- Mumbai: 15
- Bangalore: 15
- Pune: 15
- Thane: 15

The dataset includes vendor identification, category, subcategory, event type, location, pricing, description, services offered, rating, availability and contact information.

All 60 records are marked as synthetic. Ratings, review counts, descriptions and services are sample data, not independently verified business information.

Main output: `data/clean/vendors_clean.csv`

### E. Venue Leads

Venue leads are maintained separately from synthetic vendor records.

**Legacy venue leads:**
- 7 potential leads
- Locations: CBD Belapur, Vashi and Nerul
- File: `data/raw/venue_leads_legacy.csv`

**New venue leads:**
- 11 potential leads
- Locations: Mumbai, Pune, Bangalore and Thane
- File: `data/raw/venue_leads_new.csv`

**Combined venue leads:**
- 18 total records
- 16 columns
- Zero duplicate vendor IDs
- All records marked non-synthetic
- All records have Pending verification status

File: `data/clean/all_venue_leads.csv`

### F. Venue Verification Report

Tracks source-review progress for the 11 new venue leads.

| Source review status | Count |
|---|---:|
| Source details matched | 1 |
| Partially checked | 2 |
| Address discrepancy | 1 |
| Not reviewed | 7 |

All 11 leads remain Pending verification. Source review does not mean that the businesses have been fully verified.

File: `data/clean/venue_verification_report.csv`

### G. Event-Type Leads

Contains four additional potential business leads for event coverage research.

- Candidate event types are stored separately from confirmed event types.
- All four records have Pending verification status.
- Candidate event types require confirmation before being treated as actual services.

## 4. Data Cleaning

Data cleaning was performed using Python and Pandas.

Operations included:
- Removing duplicate rows.
- Checking duplicate vendor IDs.
- Removing unnecessary whitespace.
- Standardizing vendor category names.
- Standardizing pricing type values.
- Checking missing values.
- Preparing the cleaned vendor dataset.

Latest synthetic vendor dataset:
- 60 records
- 18 columns
- Zero duplicate rows
- Zero duplicate vendor IDs

Output: `data/clean/vendors_clean.csv`

## 5. Data Validation

Validation checks included:
- Dataset dimensions.
- Duplicate records and vendor IDs.
- Missing values.
- Vendor locations and categories.
- Verification status.
- Synthetic data identification.
- Venue lead validation.
- Event-type lead validation.

The synthetic vendor dataset contains six categories. Real-world venue leads are maintained separately.

The combined venue dataset contains 18 records, with no duplicate IDs and no missing required fields.

## 6. Event Coverage Analysis

Analyzed coverage for all eight required event types using the synthetic vendor dataset.

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

Potential leads from the separate venue and event-type lead datasets are maintained separately from synthetic vendor counts.

Output: `data/clean/final_event_coverage_report.csv`

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

Irrelevant pricing fields are left blank (NULL). Per-plate pricing is not inferred from per-event pricing or vice versa.

## 8. Recommendation Prototype

A basic rule-based vendor recommendation prototype was developed and tested using the cleaned synthetic vendor dataset.

The prototype evaluates:
- Vendor category.
- Availability.
- Budget compatibility.
- Location relevance.
- Rating.
- Event relevance.

Scoring weights:

| Factor | Weight |
|---|---:|
| Budget | 35% |
| Location | 30% |
| Rating | 25% |
| Event Relevance | 10% |

Five test scenarios were processed, including an unavailable-vendor test using a separate temporary test fixture.

The prototype is rule-based and does not use a trained Machine Learning model.

Test documentation: `docs/test_results.md`

## 9. Current Limitations

- The 60 vendor records are synthetic sample data.
- Venue leads and event-type leads are potential business leads, not confirmed vendors.
- All 18 combined venue leads currently have Pending verification status.
- The 11 new venue leads have a separate source-review report.
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
- Git and GitHub

## 11. Project Folder Structure

```text
eventease-ai-ml-task01/
│
├── data/
│   ├── raw/
│   │   ├── vendors.csv
│   │   ├── venue_leads_legacy.csv
│   │   ├── venue_leads_new.csv
│   │   └── event_type_leads.csv
│   │
│   ├── clean/
│   │   ├── vendors_clean.csv
│   │   ├── all_venue_leads.csv
│   │   ├── venue_verification_report.csv
│   │   ├── event_coverage_report.csv
│   │   └── final_event_coverage_report.csv
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
│   ├── create_category_datasets.py
│   ├── generate_data.py
│   ├── data_cleaning.py
│   ├── complete_vendor_schema.py
│   ├── create_venue_leads.py
│   ├── create_new_venue_leads.py
│   ├── combine_venue_leads.py
│   ├── create_venue_verification_report.py
│   ├── create_event_type_leads.py
│   ├── update_venue_sources.py
│   ├── validate_data.py
│   ├── validate_venue_leads.py
│   ├── validate_event_type_leads.py
│   ├── category_analysis.py
│   ├── event_coverage_analysis.py
│   ├── final_event_coverage_analysis.py
│   ├── recommendation.py
│   └── prepare_verification_tracker.py
│
├── tests/
│   ├── run_all_tests.py
│   └── test_scenario_4.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

Note: This is the main project structure. Additional scripts and generated reports may also exist. The virtual environment (`venv/`) and Jupyter checkpoint files are excluded from GitHub.

## 12. How to Run the Project

Run commands from the project root directory.

### A. Install Dependencies

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

### B. Generate and Prepare Synthetic Vendor Data

```bash
python src/create_category_datasets.py
python src/generate_data.py
python src/data_cleaning.py
python src/complete_vendor_schema.py
```

Important: Dataset generation scripts may overwrite existing CSV files. Keep backups of manually updated data before regenerating datasets.

### C. Prepare and Combine Venue Leads

Run these scripts when creating or updating the venue lead datasets:

```bash
python src/create_venue_leads.py
python src/create_new_venue_leads.py
python src/combine_venue_leads.py
python src/create_venue_verification_report.py
```

Important: The lead creation scripts may overwrite existing files. Do not rerun them after manual updates unless regeneration is intentional.

### D. Validate Existing Datasets

```bash
python src/validate_data.py
python src/validate_venue_leads.py
python src/validate_event_type_leads.py
python src/category_analysis.py
```

### E. Run Event Coverage Analysis

```bash
python src/event_coverage_analysis.py
python src/final_event_coverage_analysis.py
```

### F. Run Recommendation Tests

```bash
python tests/run_all_tests.py
```

The recommendation prototype uses synthetic vendor data and a separate temporary fixture for the unavailable-vendor test.

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
