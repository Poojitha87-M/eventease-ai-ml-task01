# EventEase Assignment Scenario Test Results

**Test date:** 26-11-2026 21:13:54

## Test summary

- Total scenarios: 5
- Passed: 5
- Failed: 0

## Scenario results

| scenario                             | expected                                     | actual                             | status   |
|:-------------------------------------|:---------------------------------------------|:-----------------------------------|:---------|
| 1. Wedding Decoration - Thane        | 1 matching research lead                     | 1 matching lead(s)                 | PASS     |
| 2. Birthday Catering - Pune          | 1 matching research lead                     | 1 matching lead(s)                 | PASS     |
| 3. Corporate Photography - Bangalore | 1 matching research lead                     | 1 matching lead(s)                 | PASS     |
| 4. Low-budget Event Planning         | Vendor rejected because price exceeds budget | No matching vendors                | PASS     |
| 5. Search without budget             | 1 matching lead with a calculated score      | 1 matching lead(s); budget skipped | PASS     |

## Recommendation scoring weights

- Budget: 35%
- Location: 30%
- Rating: 25%
- Event relevance: 10%

## Test data note

All five scenarios use synthetic test fixtures created specifically
for functional testing. They are not real vendor verification results.

The scenarios test:

1. Wedding Decoration in Thane
2. Birthday Catering in Pune
3. Corporate Photography in Bangalore
4. Rejection of an over-budget vendor in Verified Mode
5. Research/Demo search without entering a budget

## Important limitations

- Synthetic fixtures do not prove real vendor availability.
- Real vendor prices and guest capacities require confirmation.
- Listed ratings should not be treated as verified ratings.
- Research/Demo results are not confirmed booking recommendations.
- The recommendation prototype uses rule-based scoring, not a trained ML model.
