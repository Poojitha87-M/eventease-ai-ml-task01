# EventEase - Recommendation Engine Test Results

All tests use the cleaned synthetic vendor dataset.

Scoring weights: Budget 35%, Location 30%, Rating 25%, Event relevance 10%.

## Scenario 1 - Birthday Catering

Input: Birthday, Catering, Vashi, Rs. 40,000, 100 guests.

Expected: Only available catering vendors with an applicable price within budget should be recommended.

## Scenario 1 - Birthday Catering

- Category matches: 10
- Available vendors: 8
- Budget-compatible vendors: 1

- Top vendor: Synthetic Catering Vendor 043
- Location: CBD Belapur
- Estimated cost: Rs. 28260.00
- Pricing basis: per_event
- Rating: 3.5
- Final score: 42.77

Top recommendations:

| vendor_id   | vendor_name                   | location    |   estimated_cost |   final_score |
|:------------|:------------------------------|:------------|-----------------:|--------------:|
| VND-043     | Synthetic Catering Vendor 043 | CBD Belapur |            28260 |       42.7725 |

## Scenario 2 - Wedding Decoration

- Category matches: 10
- Available vendors: 8
- Budget-compatible vendors: 8

- Top vendor: Synthetic Decoration Vendor 021
- Location: CBD Belapur
- Estimated cost: Rs. 68708.00
- Pricing basis: per_event
- Rating: 4.3
- Final score: 84.48

Top recommendations:

| vendor_id   | vendor_name                     | location    |   estimated_cost |   final_score |
|:------------|:--------------------------------|:------------|-----------------:|--------------:|
| VND-021     | Synthetic Decoration Vendor 021 | CBD Belapur |            68708 |       84.4761 |
| VND-057     | Synthetic Decoration Vendor 057 | CBD Belapur |            48971 |       80.9301 |
| VND-003     | Synthetic Decoration Vendor 003 | CBD Belapur |            67318 |       76.2193 |
| VND-033     | Synthetic Decoration Vendor 033 | Vashi       |            46757 |       75.8175 |
| VND-015     | Synthetic Decoration Vendor 015 | Nerul       |            16269 |       68.6529 |

## Scenario 3 - Very Low Budget Entertainment

- Category matches: 10
- Available vendors: 6
- Budget-compatible vendors: 0

Result: No suitable vendor found.

## Scenario 5 - Small Event Photography

- Category matches: 10
- Available vendors: 7
- Budget-compatible vendors: 7

- Top vendor: Synthetic Photography Vendor 020
- Location: Vashi
- Estimated cost: Rs. 37112.00
- Pricing basis: per_event
- Rating: 3.9
- Final score: 78.01

Top recommendations:

| vendor_id   | vendor_name                      | location    |   estimated_cost |   final_score |
|:------------|:---------------------------------|:------------|-----------------:|--------------:|
| VND-020     | Synthetic Photography Vendor 020 | Vashi       |            37112 |       78.0054 |
| VND-002     | Synthetic Photography Vendor 002 | Vashi       |            29373 |       76.3597 |
| VND-026     | Synthetic Photography Vendor 026 | CBD Belapur |            47430 |       74.1997 |
| VND-032     | Synthetic Photography Vendor 032 | CBD Belapur |            51297 |       70.023  |
| VND-044     | Synthetic Photography Vendor 044 | Nerul       |            57442 |       68.4477 |

## Scenario 4 - Makeup Artist Unavailability

- Result: The current synthetic dataset does not contain a Makeup Artist location where every matching vendor is unavailable.
- This scenario needs a dedicated test fixture or a carefully documented dataset adjustment.

## Scenario 2 - Location clarification

The original assignment mentions Mahape, but the Product Manager approved CBD Belapur, Vashi, and Nerul for the pilot. CBD Belapur was used for this test instead of adding Mahape.

## Notes

- All vendor records are synthetic.
- Costs use the minimum listed price for the applicable pricing model.
- Per-plate and per-event prices are evaluated separately.
- Location scoring is a prototype assumption, not distance calculation.
- This is a rule-based recommendation prototype, not a trained ML model.

## Scenario 4: Makeup Artist – All Vendors Unavailable

**Customer requirements:**
- Category: Makeup Artist
- Location: Vashi

**Test approach:**
Used a separate test fixture with two Makeup Artist vendors, both marked Unavailable.

**Expected result:** No vendors should be recommended.

**Actual result:** 0 available vendors.

**Status:** PASS

**Note:** This test fixture is separate from the original synthetic vendor dataset. The original dataset remains unchanged.

## Scenario 2: Location Adjustment

The original assignment mentioned Mahape. However, the Product Manager approved CBD Belapur, Vashi, and Nerul as the pilot locations. Therefore, CBD Belapur was used for this test instead of Mahape.

This adjustment follows the Product Manager's clarification.
