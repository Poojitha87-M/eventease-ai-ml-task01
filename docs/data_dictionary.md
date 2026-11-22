
# EventEase – Data Dictionary

## 1. Project Overview

This document describes the datasets created for the EventEase AI-powered event vendor discovery and recommendation prototype.

The project uses synthetic sample vendor records and separately maintained public business research leads.

Synthetic records must never be presented as verified real businesses.

## 2. Dataset Inventory

| Dataset | File | Purpose |
|---|---|---|
| Vendor Master | data/raw/vendors.csv | Original synthetic vendor data |
| Cleaned Vendors | data/clean/vendors_clean.csv | Cleaned synthetic vendor data |
| Event Categories | data/reference/event_categories.csv | Approved event types |
| Vendor Categories | data/reference/vendor_categories.csv | Vendor categories and subcategories |
| Decoration Subcategories | data/reference/decoration_subcategories.csv | Decoration service types |
| Venue Leads | data/raw/venue_leads.csv | Potential venue business leads |
| Event-Type Leads | data/raw/event_type_leads.csv | Potential leads for missing event categories |
| Verification Tracker | data/raw/venue_verification_tracker.csv | Tracks manual verification |
| Venue Verification Report | data/clean/venue_verification_report.csv | Field-level verification status |
| Event Coverage Report | data/clean/event_coverage_report.csv | Coverage from synthetic sample data |
| Final Event Coverage Report | data/clean/final_event_coverage_report.csv | Sample coverage and potential leads |

## 3. Vendor Master Dataset

Files:
- data/raw/vendors.csv
- data/clean/vendors_clean.csv

| Column | Data Type | Description | Validation Rules |
|---|---|---|---|
| vendor_id | String | Unique vendor identifier | Unique; format VND-001 |
| vendor_name | String | Vendor display name | Required |
| category | String | Main vendor service category | Approved category |
| location | String | Vendor service location | CBD Belapur, Vashi, Nerul |
| min_price_per_plate | Numeric | Minimum per-plate price in INR | Non-negative or blank |
| max_price_per_plate | Numeric | Maximum per-plate price in INR | Greater than or equal to minimum |
| min_price_per_event | Numeric | Minimum per-event price in INR | Non-negative or blank |
| max_price_per_event | Numeric | Maximum per-event price in INR | Greater than or equal to minimum |
| pricing_type | String | Pricing model | per_plate, per_event, both |
| rating | Float | Illustrative vendor rating | Between 0 and 5 |
| availability | String | Illustrative availability | Available or Unavailable |
| event_type | String | Supported event types | Pipe-separated values |
| review_count | Integer | Illustrative review count | Non-negative integer |
| is_synthetic | Boolean | Identifies synthetic records | True for every sample vendor |

## 4. Event Categories

File: data/reference/event_categories.csv

Column:
- event_category: Approved event category.

Expected categories:
1. Wedding
2. Birthday
3. Corporate Event
4. Engagement
5. Baby Shower
6. College Event
7. Private Party
8. Festival

## 5. Vendor Categories

File: data/reference/vendor_categories.csv

| Main Category | Subcategories |
|---|---|
| Decoration | Stage, Balloon, Floral, Theme Decoration |
| Photography | Wedding, Candid, Traditional, Videography |
| Catering | Veg, Non-Veg, Buffet, Live Counters |
| Venues | Banquet Halls, Resorts, Lawns |
| Entertainment | DJs, Singers, Anchors, Dance Groups |
| Makeup | Bridal Makeup, Hairstyling |
| Event Planning | Wedding Planners, Corporate Planners |

Columns:
- main_category
- subcategory

## 6. Decoration Subcategories

File: data/reference/decoration_subcategories.csv

Column:
- decoration_subcategory

Expected values:
- Stage
- Balloon
- Floral
- Theme Decoration

## 7. Venue Leads

File: data/raw/venue_leads.csv

| Column | Description |
|---|---|
| vendor_id | Unique venue lead identifier |
| vendor_name | Publicly listed business name |
| category | Vendor category |
| subcategory | Venue type |
| location | Business area |
| address | Publicly listed address |
| phone | Publicly listed contact number |
| event_type | Potentially supported event types |
| pricing_type | Pricing model, if available |
| min_price_per_plate | Minimum per-plate price |
| max_price_per_plate | Maximum per-plate price |
| min_price_per_event | Minimum per-event price |
| max_price_per_event | Maximum per-event price |
| source_url | Source listing or website |
| verification_status | Verification status |
| is_synthetic | False for public business leads |
| source_type | Source classification |

All venue leads remain Pending until independently verified.

## 8. Event-Type Leads

File: data/raw/event_type_leads.csv

| Column | Description |
|---|---|
| vendor_id | Unique lead identifier |
| vendor_name | Publicly listed business name |
| category | Vendor category |
| location | Business location |
| phone | Publicly listed contact |
| candidate_event_types | Potential event services |
| event_type | Confirmed event type, blank until verified |
| source_type | Source classification |
| verification_status | Verification status |
| is_synthetic | False for public business leads |

Candidate event types are research leads, not confirmed services.

## 9. Venue Verification Tracker

File: data/raw/venue_verification_tracker.csv

Additional verification fields:

| Column | Description |
|---|---|
| verification_method | Method used to verify information |
| last_checked | Date of last verification |
| verified_fields | Fields independently confirmed |
| verification_notes | Notes from verification |

Blank verification fields mean verification has not yet been recorded.

## 10. Venue Verification Report

File: data/clean/venue_verification_report.csv

Includes the venue lead information and these field-level status columns:

- address_status
- phone_status
- event_type_status
- source_url_status

These indicate whether information is available, missing, or still needs verification.

## 11. Event Coverage Reports

### Event Coverage Report

File: data/clean/event_coverage_report.csv

Columns:
- event_type
- vendor_count
- coverage_status

This report measures coverage in the synthetic vendor dataset only.

### Final Event Coverage Report

File: data/clean/final_event_coverage_report.csv

Columns:
- event_type
- sample_vendor_count
- potential_lead_count
- sample_coverage
- lead_status

Potential leads must not be interpreted as confirmed vendor coverage.

## 12. Pricing Rules

1. Per-plate and per-event prices are stored separately.
2. Per-plate estimated cost = price per plate × number of guests.
3. Per-event estimated cost = event price.
4. Vendors supporting both pricing models must have both sets of price fields.
5. Fields for an inapplicable pricing model must remain blank.
6. Do not convert or estimate one pricing model from another.
7. Do not replace intentional blank pricing values with zero or averages.

## 13. Data Quality Rules

1. Vendor IDs must be unique within each dataset.
2. Required vendor names must not be empty.
3. Prices must not be negative.
4. Minimum prices must not exceed maximum prices.
5. Ratings must be between 0 and 5.
6. Approved categories must be used consistently.
7. Locations must preserve their area-specific values.
8. Synthetic records must be labelled True.
9. Public business leads must remain separate from synthetic records.
10. Unverified information must not be represented as confirmed.

## 14. Pilot Locations

- CBD Belapur – Primary pilot location.
- Vashi – Secondary location.
- Nerul – Secondary location.

## 15. Synthetic Data Notice

The 60-record Vendor Master dataset contains artificially generated sample data for development, testing, and analysis.

Vendor names, ratings, prices, review counts, and availability are illustrative and are not verified real-world information.

Venue and event-type leads are separate public business research records. Their information and services require independent verification before being treated as confirmed.

## Additional Vendor Dataset Fields

The cleaned vendor dataset contains four additional fields:

| Column | Data Type | Description | Validation Rules |
|---|---|---|---|
| subcategory | String | Vendor's specific service type | Must belong to the corresponding main category |
| description | String | Sample description of the vendor service | Clearly identified as synthetic sample content |
| services_offered | String | Sample service associated with the subcategory | Clearly identified as synthetic sample content |
| contact_information | String | Public vendor contact information | Keep NULL when verified information is unavailable |

## Data Authenticity Note

The 60 vendor records are synthetic sample data created for the EventEase prototype.

Subcategories, descriptions and services offered in these records are also sample values. They must not be treated as verified business information.

Contact information is currently NULL because verified public contact details are not available for these synthetic records.

Real venue and event-planner leads are maintained separately with Pending verification status.
