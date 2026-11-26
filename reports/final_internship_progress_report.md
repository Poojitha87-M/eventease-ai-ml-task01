# EVENTEASE - AI/ML & DATA ENGINEERING INTERNSHIP
## Final Progress Report - 26 November 2026

**Intern:** Poojitha

## 1. Objective

Build a structured vendor data foundation and a rule-based recommendation prototype that ranks event vendors according to customer requirements.

## 2. Vendor Research

- 61 researched vendor records collected.
- Six categories covered: Catering, Photography, Decoration, Event Planning, Makeup and Entertainment.
- Current research locations: Thane, Pune and Bangalore.
- Unique vendor IDs assigned.
- Researched and synthetic datasets maintained separately.

## 3. Data Engineering

Python and Pandas scripts were developed for:
- Data cleaning and standardisation.
- Duplicate detection.
- Vendor ID validation.
- Rating validation.
- Missing-value analysis.
- Vendor verification tracking.
- Verification priority classification.

## 4. Validation Results

| Check | Result |
|---|---:|
| Total researched records | 61 |
| Unique vendor IDs | 61 |
| Duplicate IDs | 0 |
| Duplicate vendor/location pairs | 0 |
| Invalid listed ratings | 0 |
| Invalid verified ratings | 0 |
| Public listing matched - details pending | 59 |
| Pending - public listing found | 2 |

## 5. Verification Analysis

The verification tracker contains 61 records.

- 19 records have direct source URLs.
- 56 records have high verification priority.
- 5 records have medium verification priority.
- Pricing and availability still need confirmation.
- Guest capacity is missing for all 61 records.

The verification-priority script generated:
- reports/vendor_verification_priority.csv
- reports/vendor_verification_priority_report.txt

## 6. Recommendation Prototype

A rule-based recommendation prototype was developed.

| Factor | Weight |
|---|---:|
| Budget compatibility | 35% |
| Location | 30% |
| Rating | 25% |
| Service relevance | 10% |

The system accepts category, location, event type, budget and guest count. Availability is used as a filter.

Two modes are supported:
- Research/Demo Mode: displays researched leads requiring further verification.
- Verified Mode: filters using confirmed information.

## 7. Testing Results

The existing automated tests were executed using the cleaned synthetic dataset.

| Scenario | Result |
|---|---|
| Birthday Catering | 1 budget-compatible vendor |
| Wedding Decoration | 9 budget-compatible vendors |
| Very Low Budget Entertainment | 0 suitable vendors |
| Small Event Photography | 8 budget-compatible vendors |
| Makeup Artist Unavailability | PASS |

Test documentation: docs/test_results.md

These tests demonstrate prototype functionality. They do not establish that the five exact scenarios in the original assignment have all been completed.

## 8. Demonstration Result

A Research/Demo Mode test was executed with:
- Category: Makeup
- Location: Thane
- Event type: Wedding
- Budget: Rs. 450,000
- Guest count: 876

Three researched vendor leads were returned. Their prices, verified ratings, availability and guest capacity were unconfirmed. They were correctly labelled Needs verification.

## 9. Limitations

- Researched vendor prices are not confirmed.
- Availability is unconfirmed for all 61 researched records.
- Guest capacity is missing for all 61 records.
- Verified ratings are missing for 56 records.
- Direct source URLs are available for 19 records.
- Existing automated recommendation tests use synthetic data.
- The recommendation prototype is rule-based, not a trained ML model.

## 10. Next Steps

1. Continue vendor-level verification.
2. Complete the five specified assignment scenarios.
3. Review the recommendation API response format.
4. Finalise documentation and the project demonstration.

## 11. Conclusion

The initial vendor research dataset, data-cleaning and validation workflow, vendor verification tracker, verification-priority analysis and rule-based recommendation prototype have been developed.

The next stage is to improve the completeness of researched vendor information, finish the required scenario testing and demonstrate the recommendation workflow.

