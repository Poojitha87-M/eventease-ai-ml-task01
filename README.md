
# EventEase – AI/ML & Data Engineering Internship Project

## 1. Project Overview

EventEase is an AI-powered event vendor discovery and recommendation project. The objective is to prepare structured vendor datasets, clean and validate vendor information, track vendor verification, and develop a recommendation prototype to help users discover suitable event vendors.

This project currently focuses on data engineering, vendor research, data quality, and rule-based recommendations.

## 2. Project Objectives

- Create structured vendor datasets for different event categories.
- Organize vendors by category, subcategory, and location.
- Clean duplicate, missing, and inconsistent records.
- Collect vendor information from publicly available sources.
- Develop a vendor verification tracker.
- Build a rule-based vendor recommendation prototype.
- Test recommendation scenarios and document limitations.

## 3. Technology Stack

- Python
- Pandas
- NumPy
- CSV and Excel
- Git and GitHub
- VS Code
- Rule-based recommendation logic

## 4. Project Location Scope

The current approved target locations are:

1. Thane, Maharashtra
2. Pune, Maharashtra
3. Bangalore, Karnataka

**Note:** Vashi, CBD Belapur, and Mahape are not included in the current approved target-location scope.

## 5. Vendor Categories

The project covers six main vendor categories:

- Catering
- Decoration
- Photography
- Makeup
- Entertainment
- Event Planning

## 6. Dataset Preparation

The project includes structured vendor datasets with fields such as:

- Vendor ID
- Vendor name
- Main category
- Subcategory
- Location
- Minimum and maximum price
- Pricing type
- Rating
- Availability
- Event types supported
- Guest capacity
- Synthetic data indicator

Pricing fields are maintained separately for per-plate and per-event pricing wherever applicable.

The project distinguishes between per-plate pricing, per-event pricing, and both pricing models. Unknown pricing information is not treated as confirmed.

## 7. Synthetic Vendor Dataset

A synthetic vendor dataset was created for development and testing.

The dataset contains sample vendor records across different categories and locations.

Synthetic records are identified using the `is_synthetic` field.

These records are used for testing data-processing and recommendation functionality. They should not be treated as real, verified businesses.

## 8. Vendor Research Dataset

A separate vendor research dataset was prepared using publicly available business listings.

The current researched dataset contains **61 vendor leads**.

### Location distribution

| Location | Vendor leads |
|---|---:|
| Thane, Maharashtra | 20 |
| Pune, Maharashtra | 21 |
| Bangalore, Karnataka | 20 |
| **Total** | **61** |

### Category distribution

| Category | Vendor leads |
|---|---:|
| Catering | 14 |
| Decoration | 12 |
| Photography | 10 |
| Makeup | 9 |
| Entertainment | 9 |
| Event Planning | 7 |
| **Total** | **61** |

These records are research leads. A public listing match does not mean that all vendor details have been independently verified.

## 9. Vendor Verification Tracker

A vendor verification tracker was developed to record public listing matches and identify details that still require confirmation.

Current tracker results:

| Verification information | Result |
|---|---:|
| Total vendor records | 61 |
| Public listing matched - details pending | 59 |
| Pending - public listing found | 2 |
| Records with direct source URLs | 19 |
| High-priority verification records | 56 |
| Medium-priority verification records | 5 |

The tracker helps prioritize vendor verification before the information is used for actual recommendations or bookings.

## 10. Data Quality and Validation

Data preparation and validation include:

- Checking required columns.
- Identifying missing values.
- Checking duplicate vendor IDs.
- Checking duplicate vendor and location combinations.
- Validating rating ranges.
- Checking supported locations.
- Checking category consistency.
- Reviewing pricing information.
- Tracking verification status.

Validation scripts are used to identify data quality issues and maintain a consistent dataset structure.

## 11. Event Coverage

The datasets include multiple event types, such as:

- Wedding
- Birthday
- Corporate Event
- Engagement
- Baby Shower
- College Event
- Private Party
- Festival

Event coverage analysis is used to understand which vendor categories and event types are represented in the available data.

## 12. Recommendation Prototype

A rule-based vendor recommendation prototype was developed.

The prototype accepts user inputs such as:

- Vendor category
- Event type
- Location
- Budget
- Number of guests
- Recommendation mode

It filters vendors based on the selected criteria and calculates recommendation scores.

### Recommendation scoring weights

| Factor | Weight |
|---|---:|
| Budget compatibility | 35% |
| Location match | 30% |
| Rating | 25% |
| Event relevance | 10% |
| **Total** | **100%** |

Availability is treated as a filtering condition where confirmed availability is required.

### Recommendation modes

**Research/Demo Mode**

- Allows exploration of researched vendor leads.
- Displays available public listing information.
- Clearly identifies unconfirmed pricing and availability.
- Labels results as research leads rather than confirmed booking options.

**Verified Mode**

- Applies stricter checks for information required for actual vendor selection.
- Avoids treating missing pricing, availability, or capacity information as confirmed.
- Excludes vendors that do not meet the required verification conditions.

## 13. Recommendation Output

The recommendation prototype displays information such as:

- Vendor ID
- Vendor name
- Category
- Location
- Price information
- Listed rating
- Availability status
- Recommendation score
- Recommendation status

For example, a research lead may display:

- Price: Not confirmed
- Rating: Listed rating, not independently verified
- Availability: Unconfirmed
- Status: Research lead - verify before booking

A recommendation score does not guarantee vendor suitability or booking availability.

## 14. Assignment Scenario Testing

A separate assignment scenario test file was created:

`tests/test_assignment_scenarios.py`

Five scenarios were tested:

1. Wedding Decoration – Thane
2. Birthday Catering – Pune
3. Corporate Photography – Bangalore
4. Low-budget Event Planning
5. Search without budget

### Test results

| Test result | Count |
|---|---:|
| Total scenarios | 5 |
| Passed | 5 |
| Failed | 0 |

**All five assignment scenarios passed successfully.**

These tests use synthetic test fixtures to validate recommendation logic and filtering behaviour. They do not establish real-world vendor pricing, availability, or booking status.

## 15. Existing Test Suite

The project also contains the existing test runner:

`tests/run_all_tests.py`

The assignment scenario tests and the existing test suite are separate. Their results should be reported independently.

## 16. Project Structure

The project contains source scripts, datasets, documentation, and test files.

```text
eventease-ai-ml-task01/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── research/
│
├── src/
│   ├── data_cleaning.py
│   ├── generate_data.py
│   ├── complete_vendor_schema.py
│   ├── recommendation.py
│   ├── validate_data.py
│   ├── create_category_datasets.py
│   ├── create_event_type_leads.py
│   ├── prepare_verification_tracker.py
│   └── venue_verification_report.py
│
├── tests/
│   ├── run_all_tests.py
│   └── test_assignment_scenarios.py
│
├── docs/
│   ├── data_dictionary.md
│   └── test_results.md
│
└── README.md
```

This is a high-level overview. Refer to the actual repository for the complete list of files and scripts.

## 17. How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/Poojitha87-M/eventease-ai-ml-task01.git
cd eventease-ai-ml-task01
```

### Step 2: Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install pandas numpy
```

Install any additional dependencies required by individual project scripts.

### Step 4: Run the recommendation prototype

```bash
python src/recommendation.py
```

### Step 5: Run assignment scenario tests

```bash
python tests/test_assignment_scenarios.py
```

Expected result:

```text
Total scenarios: 5
Passed: 5
Failed: 0
```

### Step 6: Run the existing test suite

```bash
python tests/run_all_tests.py
```

## 18. Current Project Achievements

- Prepared structured vendor datasets.
- Created synthetic data for development and testing.
- Collected 61 researched vendor leads.
- Organized researched leads across Thane, Pune, and Bangalore.
- Prepared a vendor verification tracker.
- Generated verification-priority information.
- Implemented a rule-based recommendation prototype.
- Corrected location normalization and filtering.
- Added Research/Demo and Verified recommendation modes.
- Created five assignment scenario tests.
- Achieved five passing assignment scenario tests.
- Documented current data quality limitations and future improvements.

## 19. Current Limitations

The current project still has limitations:

- Vendor pricing and pricing models require confirmation.
- Vendor availability has not been independently confirmed.
- Guest capacity information requires verification.
- Listed ratings are not necessarily independently verified.
- Only 19 of the 61 researched records currently have direct source URLs in the tracker.
- More verified contact information is required.
- Real-world recommendation performance has not yet been established.

The five assignment scenarios passed using synthetic test fixtures. They validate prototype behaviour and filtering logic, not the real-world accuracy of vendor recommendations.

## 20. Future Work

- Confirm researched vendor prices and pricing models.
- Verify vendor availability and guest capacity.
- Collect more direct source links and verified contact details.
- Review the recommendation API response format.
- Improve recommendation accuracy using verified vendor data.
- Expand testing with verified real-world vendor information.
- Consider machine-learning-based ranking after sufficient verified data becomes available.

## 21. Important Project Note

The current recommendation system is a **rule-based recommendation prototype, not a trained machine-learning model**.

Synthetic data is used for development and scenario testing, while researched vendor leads are maintained separately for verification.

The project does not claim that researched vendors are ready for booking. Vendor details must be confirmed before real-world use.

## 22. Repository

GitHub Repository:

https://github.com/Poojitha87-M/eventease-ai-ml-task01
