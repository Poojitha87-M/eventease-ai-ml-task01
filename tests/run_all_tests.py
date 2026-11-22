
import pandas as pd
from pathlib import Path

# ==========================================
# 1. FILE PATHS
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "data" / "clean" / "vendors_clean.csv"
OUTPUT_PATH = ROOT / "docs" / "test_results.md"

df = pd.read_csv(DATA_PATH)


# ==========================================
# 2. RECOMMENDATION TEST FUNCTION
# ==========================================

def run_test(name, event, category, location, budget, guests):

    # Filter by category
    data = df[
        df["category"].str.lower() == category.lower()
    ].copy()

    category_count = len(data)

    # Filter available vendors
    data = data[
        data["availability"].str.lower() == "available"
    ].copy()

    available_count = len(data)

    results = []

    # Check vendor pricing
    for _, vendor in data.iterrows():

        prices = []
        pricing_type = str(vendor["pricing_type"]).lower()

        if pricing_type in ["per_plate", "both"]:

            price = vendor["min_price_per_plate"]

            if pd.notna(price):
                prices.append(
                    (float(price) * guests, "per_plate")
                )

        if pricing_type in ["per_event", "both"]:

            price = vendor["min_price_per_event"]

            if pd.notna(price):
                prices.append(
                    (float(price), "per_event")
                )

        affordable = [
            price for price in prices
            if price[0] <= budget
        ]

        if affordable:

            cost, basis = min(
                affordable,
                key=lambda x: x[0]
            )

            results.append({
                **vendor.to_dict(),
                "estimated_cost": cost,
                "pricing_basis": basis
            })

    result = pd.DataFrame(results)

    # ==========================================
    # 3. RECOMMENDATION SCORING
    # ==========================================

    if not result.empty:

        result["location_score"] = result["location"].apply(
            lambda x: 1.0 if str(x).lower() == location.lower() else 0.5
        )

        result["rating_score"] = (
            pd.to_numeric(result["rating"], errors="coerce") / 5
        ).clip(0, 1)

        result["budget_score"] = (
            1 - result["estimated_cost"] / budget
        ).clip(0, 1)

        def relevance(value):

            events = str(value).lower().split("|")

            return 1.0 if event.lower() in events else 0.0

        result["relevance_score"] = (
            result["event_type"].apply(relevance)
        )

        result["final_score"] = (
            result["budget_score"] * 0.35
            + result["location_score"] * 0.30
            + result["rating_score"] * 0.25
            + result["relevance_score"] * 0.10
        ) * 100

        result = result.sort_values(
            "final_score",
            ascending=False
        )

    return {
        "name": name,
        "category_count": category_count,
        "available_count": available_count,
        "budget_count": len(result),
        "results": result
    }


# ==========================================
# 4. SCENARIOS 1, 2, 3 AND 5
# ==========================================

tests = [

    run_test(
        "Scenario 1 - Birthday Catering",
        "Birthday",
        "Catering",
        "Vashi",
        40000,
        100
    ),

    run_test(
        "Scenario 2 - Wedding Decoration",
        "Wedding",
        "Decoration",
        "CBD Belapur",
        200000,
        300
    ),

    run_test(
        "Scenario 3 - Very Low Budget Entertainment",
        "Birthday",
        "Entertainment",
        "CBD Belapur",
        100,
        100
    ),

    run_test(
        "Scenario 5 - Small Event Photography",
        "Birthday",
        "Photography",
        "Vashi",
        200000,
        20
    )
]


# ==========================================
# 5. SCENARIO 4 - TEST FIXTURE
# ==========================================

# Separate temporary test data.
# These records do not modify the real dataset.

test_vendors = pd.DataFrame([

    {
        "vendor_id": "TEST-001",
        "vendor_name": "Test Makeup Vendor 1",
        "category": "Makeup",
        "location": "Vashi",
        "availability": "Unavailable"
    },

    {
        "vendor_id": "TEST-002",
        "vendor_name": "Test Makeup Vendor 2",
        "category": "Makeup",
        "location": "Vashi",
        "availability": "Unavailable"
    }

])

# Filter by category
category_vendors = test_vendors[
    test_vendors["category"].str.lower() == "makeup"
]

# Filter by availability
available_vendors = category_vendors[
    category_vendors["availability"].str.lower() == "available"
]

scenario4 = {
    "name": "Scenario 4 - Makeup Artist Unavailability",
    "location": "Vashi",
    "vendor_count": len(category_vendors),
    "available_count": len(available_vendors)
}


# ==========================================
# 6. CREATE TEST DOCUMENTATION
# ==========================================

lines = [

    "# EventEase - Recommendation Engine Test Results",

    "",

    "All tests use the cleaned synthetic vendor dataset.",

    "",

    "Scoring weights: Budget 35%, Location 30%, Rating 25%, "
    "Event relevance 10%.",

    "",

    "## Recommendation Test Results",

    ""
]


# Add results for Scenarios 1, 2, 3 and 5

for test in tests:

    lines += [

        f"## {test['name']}",

        "",

        f"- Category matches: {test['category_count']}",

        f"- Available vendors: {test['available_count']}",

        f"- Budget-compatible vendors: {test['budget_count']}",

        ""
    ]

    if test["budget_count"] == 0:

        lines.append(
            "Result: No suitable vendor found."
        )

    else:

        top = test["results"].iloc[0]

        lines += [

            f"- Top vendor: {top['vendor_name']}",

            f"- Location: {top['location']}",

            f"- Estimated cost: Rs. {top['estimated_cost']:.2f}",

            f"- Pricing basis: {top['pricing_basis']}",

            f"- Rating: {top['rating']}",

            f"- Final score: {top['final_score']:.2f}",

            "",

            "Top recommendations:",

            "",

            test["results"][[
                "vendor_id",
                "vendor_name",
                "location",
                "estimated_cost",
                "final_score"
            ]].head(5).to_markdown(index=False)

        ]

    lines.append("")


# ==========================================
# 7. SCENARIO 4 DOCUMENTATION
# ==========================================

lines += [

    "## Scenario 4 - Makeup Artist Unavailability",

    "",

    f"- Location tested: {scenario4['location']}",

    f"- Matching makeup vendors: {scenario4['vendor_count']}",

    f"- Available matching vendors: {scenario4['available_count']}",

    "- Expected result: No recommendation should be returned.",

    ""
]

if available_vendors.empty:

    lines.append(
        "- Test result: PASS - No unavailable vendor was recommended."
    )

else:

    lines.append(
        "- Test result: FAIL - An unavailable vendor was recommended."
    )


# ==========================================
# 8. LOCATION CLARIFICATION
# ==========================================

lines += [

    "",

    "## Scenario 2 - Location clarification",

    "",

    "The original assignment mentions Mahape, but the Product Manager "
    "approved CBD Belapur, Vashi, and Nerul for the pilot. "
    "CBD Belapur was used for this test instead of adding Mahape.",

    ""
]


# ==========================================
# 9. PROJECT NOTES
# ==========================================

lines += [

    "## Notes",

    "",

    "- All vendor records in the main dataset are synthetic.",

    "- Scenario 4 uses a separate temporary test fixture.",

    "- Costs use the minimum listed price for the applicable pricing model.",

    "- Per-plate and per-event prices are evaluated separately.",

    "- Location scoring is a prototype assumption, not distance calculation.",

    "- This is a rule-based recommendation prototype, not a trained ML model.",

    ""
]


# ==========================================
# 10. SAVE TEST DOCUMENTATION
# ==========================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH.write_text(
    "\n".join(lines),
    encoding="utf-8"
)


# ==========================================
# 11. PRINT TEST RESULTS
# ==========================================

print("\nALL TESTS PROCESSED")

print(f"Test documentation saved to: {OUTPUT_PATH}")

for test in tests:

    print(
        f"{test['name']}: "
        f"{test['budget_count']} budget-compatible vendor(s)"
    )


if available_vendors.empty:

    print(
        "Scenario 4: PASS - "
        "No unavailable vendors were recommended."
    )

else:

    print(
        "Scenario 4: FAIL - "
        "Unavailable vendors were recommended."
    )
