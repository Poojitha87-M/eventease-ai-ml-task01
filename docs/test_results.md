# EventEase - Recommendation Engine Test Results

All tests use the cleaned synthetic vendor dataset.

Scoring weights: Budget 35%, Location 30%, Rating 25%, Event relevance 10%.

## Recommendation Test Results

## Scenario 1 - Birthday Catering

- Category matches: 10
- Available vendors: 7
- Budget-compatible vendors: 1

- Top vendor: Synthetic Catering Vendor 019
- Location: Mumbai
- Estimated cost: Rs. 39116.00
- Pricing basis: per_event
- Rating: 3.2
- Final score: 41.77

Top recommendations:

| vendor_id   | vendor_name                   | location   |   estimated_cost |   final_score |
|:------------|:------------------------------|:-----------|-----------------:|--------------:|
| VND-019     | Synthetic Catering Vendor 019 | Mumbai     |            39116 |       41.7735 |

## Scenario 2 - Wedding Decoration

- Category matches: 10
- Available vendors: 9
- Budget-compatible vendors: 9

- Top vendor: Synthetic Decoration Vendor 057
- Location: Bangalore
- Estimated cost: Rs. 47828.00
- Pricing basis: per_event
- Rating: 4.4
- Final score: 73.63

Top recommendations:

| vendor_id   | vendor_name                     | location   |   estimated_cost |   final_score |
|:------------|:--------------------------------|:-----------|-----------------:|--------------:|
| VND-057     | Synthetic Decoration Vendor 057 | Bangalore  |            47828 |       73.6301 |
| VND-015     | Synthetic Decoration Vendor 015 | Bangalore  |            66285 |       72.4001 |
| VND-009     | Synthetic Decoration Vendor 009 | Thane      |            58024 |       71.3458 |
| VND-003     | Synthetic Decoration Vendor 003 | Pune       |            69127 |       69.4028 |
| VND-021     | Synthetic Decoration Vendor 021 | Pune       |            24847 |       68.6518 |

## Scenario 3 - Very Low Budget Entertainment

- Category matches: 10
- Available vendors: 10
- Budget-compatible vendors: 0

Result: No suitable vendor found.

## Scenario 5 - Small Event Photography

- Category matches: 10
- Available vendors: 8
- Budget-compatible vendors: 8

- Top vendor: Synthetic Photography Vendor 056
- Location: Mumbai
- Estimated cost: Rs. 16988.00
- Pricing basis: per_event
- Rating: 3.5
- Final score: 74.53

Top recommendations:

| vendor_id   | vendor_name                      | location   |   estimated_cost |   final_score |
|:------------|:---------------------------------|:-----------|-----------------:|--------------:|
| VND-056     | Synthetic Photography Vendor 056 | Mumbai     |            16988 |       74.5271 |
| VND-050     | Synthetic Photography Vendor 050 | Bangalore  |            19074 |       74.162  |
| VND-026     | Synthetic Photography Vendor 026 | Thane      |            40732 |       73.3719 |
| VND-014     | Synthetic Photography Vendor 014 | Bangalore  |            55429 |       73.2999 |
| VND-002     | Synthetic Photography Vendor 002 | Thane      |            50238 |       73.2083 |

## Scenario 4 - Makeup Artist Unavailability

- Location tested: Vashi
- Matching makeup vendors: 2
- Available matching vendors: 0
- Expected result: No recommendation should be returned.

- Test result: PASS - No unavailable vendor was recommended.

## Scenario 2 - Location clarification

The original assignment mentions Mahape, but the Product Manager approved CBD Belapur, Vashi, and Nerul for the pilot. CBD Belapur was used for this test instead of adding Mahape.

## Notes

- All vendor records in the main dataset are synthetic.
- Scenario 4 uses a separate temporary test fixture.
- Costs use the minimum listed price for the applicable pricing model.
- Per-plate and per-event prices are evaluated separately.
- Location scoring is a prototype assumption, not distance calculation.
- This is a rule-based recommendation prototype, not a trained ML model.
