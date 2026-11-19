
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "clean" / "vendors_clean.csv"
OUTPUT_PATH = ROOT / "docs" / "test_results.md"

df = pd.read_csv(DATA_PATH)

def run_test(name, event, category, location, budget, guests):
    data = df[df["category"].str.lower() == category.lower()].copy()
    category_count = len(data)

    data = data[data["availability"].str.lower() == "available"].copy()
    available_count = len(data)

    results = []

    for _, vendor in data.iterrows():
        prices = []
        pricing_type = str(vendor["pricing_type"]).lower()

        if pricing_type in ["per_plate", "both"]:
            price = vendor["min_price_per_plate"]
            if pd.notna(price):
                prices.append((float(price) * guests, "per_plate"))

        if pricing_type in ["per_event", "both"]:
            price = vendor["min_price_per_event"]
            if pd.notna(price):
                prices.append((float(price), "per_event"))

        affordable = [p for p in prices if p[0] <= budget]

        if affordable:
            cost, basis = min(affordable, key=lambda x: x[0])
            results.append({
                **vendor.to_dict(),
                "estimated_cost": cost,
                "pricing_basis": basis
            })

    result = pd.DataFrame(results)

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

        result["relevance_score"] = result["event_type"].apply(relevance)

        result["final_score"] = (
            result["budget_score"] * 0.35
            + result["location_score"] * 0.30
            + result["rating_score"] * 0.25
            + result["relevance_score"] * 0.10
        ) * 100

        result = result.sort_values("final_score", ascending=False)

    return {
        "name": name,
        "category_count": category_count,
        "available_count": available_count,
        "budget_count": len(result),
        "results": result
    }


tests = [
    run_test(
        "Scenario 1 - Birthday Catering",
        "Birthday", "Catering", "Vashi", 40000, 100
    ),
    run_test(
        "Scenario 2 - Wedding Decoration",
        "Wedding", "Decoration", "CBD Belapur", 200000, 300
    ),
    run_test(
        "Scenario 3 - Very Low Budget Entertainment",
        "Birthday", "Entertainment", "CBD Belapur", 100, 100
    ),
    run_test(
        "Scenario 5 - Small Event Photography",
        "Birthday", "Photography", "Vashi", 200000, 20
    )
]

# Find a Makeup Artist location where all matching vendors are unavailable.
makeup = df[df["category"].str.lower() == "makeup artist"]

scenario4 = None
for area in ["CBD Belapur", "Vashi", "Nerul"]:
    area_vendors = makeup[makeup["location"].str.lower() == area.lower()]
    if len(area_vendors) > 0 and not (
        area_vendors["availability"].str.lower() == "available"
    ).any():
        scenario4 = {
            "name": "Scenario 4 - Makeup Artist Unavailability",
            "location": area,
            "vendor_count": len(area_vendors)
        }
        break

lines = [
    "# EventEase - Recommendation Engine Test Results",
    "",
    "All tests use the cleaned synthetic vendor dataset.",
    "",
    "Scoring weights: Budget 35%, Location 30%, Rating 25%, "
    "Event relevance 10%.",
    "",
    "## Scenario 1 - Birthday Catering",
    "",
    "Input: Birthday, Catering, Vashi, Rs. 40,000, 100 guests.",
    "",
    "Expected: Only available catering vendors with an applicable "
    "price within budget should be recommended.",
    "",
]

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
        lines.append("Result: No suitable vendor found.")
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
                "vendor_id", "vendor_name", "location",
                "estimated_cost", "final_score"
            ]].head(5).to_markdown(index=False)
        ]

    lines.append("")

lines += [
    "## Scenario 4 - Makeup Artist Unavailability",
    ""
]

if scenario4:
    lines += [
        f"- Location tested: {scenario4['location']}",
        f"- Matching makeup artist vendors: {scenario4['vendor_count']}",
        "- Available matching vendors: 0",
        "- Result: No recommendation should be returned.",
    ]
else:
    lines += [
        "- Result: The current synthetic dataset does not contain a "
        "Makeup Artist location where every matching vendor is unavailable.",
        "- This scenario needs a dedicated test fixture or a carefully "
        "documented dataset adjustment."
    ]

lines += [
    "",
    "## Scenario 2 - Location clarification",
    "",
    "The original assignment mentions Mahape, but the Product Manager "
    "approved CBD Belapur, Vashi, and Nerul for the pilot. "
    "CBD Belapur was used for this test instead of adding Mahape.",
    "",
    "## Notes",
    "",
    "- All vendor records are synthetic.",
    "- Costs use the minimum listed price for the applicable pricing model.",
    "- Per-plate and per-event prices are evaluated separately.",
    "- Location scoring is a prototype assumption, not distance calculation.",
    "- This is a rule-based recommendation prototype, not a trained ML model.",
]

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")

print("\nALL TESTS PROCESSED")
print(f"Test documentation saved to: {OUTPUT_PATH}")

for test in tests:
    print(
        f"{test['name']}: "
        f"{test['budget_count']} budget-compatible vendor(s)"
    )

if scenario4:
    print("Scenario 4: Matching unavailable-only location found.")
else:
    print("Scenario 4: Dataset needs a test fixture for this case.")
