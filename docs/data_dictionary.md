# EventEase – Vendor Data Dictionary

## Project Overview

This document defines the structure, meaning, data types, and validation rules for the EventEase vendor dataset.

All records created for this initial prototype are synthetic sample data and must be clearly labelled.

## Dataset Fields

| Column | Data Type | Description | Validation Rules |
|---|---|---|---|
| vendor_id | String | Unique vendor identifier | Must be unique; format VND-001 |
| vendor_name | String | Vendor display name | Synthetic names must be clearly labelled |
| category | String | Vendor service category | Catering, Photography, Decoration, Event Planning, Makeup Artist, Entertainment |
| location | String | Vendor service location | CBD Belapur, Vashi, Nerul |
| min_price_per_plate | Numeric | Minimum per-plate price in INR | Must be non-negative; blank if not applicable |
| max_price_per_plate | Numeric | Maximum per-plate price in INR | Must be greater than or equal to minimum |
| min_price_per_event | Numeric | Minimum per-event price in INR | Must be non-negative; blank if not applicable |
| max_price_per_event | Numeric | Maximum per-event price in INR | Must be greater than or equal to minimum |
| pricing_type | String | Vendor pricing model | per_plate, per_event, both |
| rating | Float | Vendor rating | Between 0 and 5 |
| availability | String | Current availability status | Available or Unavailable |
| event_type | String | Events supported by the vendor | Multiple values separated by `|` |
| review_count | Integer | Number of customer reviews | Must be a non-negative integer |
| is_synthetic | Boolean | Identifies artificially created sample records | TRUE for all prototype sample records |

## Pricing Rules

- Per-plate pricing is stored separately from per-event pricing.
- Per-plate estimated cost = price per plate × number of guests.
- Per-event estimated cost = event price.
- Vendors offering both models must have values for both pricing models.
- Vendors offering only one model must leave the other model's price fields blank.
- Do not convert or estimate one pricing model from the other.

## Data Quality Rules

1. Vendor IDs must not contain duplicates.
2. Required text fields must not be empty.
3. Prices must not be negative.
4. Minimum prices must not exceed maximum prices.
5. Ratings must be between 0 and 5.
6. Availability must use the approved values.
7. Locations must use the pilot locations.
8. Every sample record must be labelled as synthetic.

## Pilot Locations

- CBD Belapur – Primary location
- Vashi – Secondary location
- Nerul – Secondary location

## Synthetic Data Notice

The initial dataset is created for development and testing purposes. Vendor names, ratings, prices, review counts, and availability values are illustrative, not verified real-world vendor information.