
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd

# Make src folder importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from recommendation import (
    filter_category,
    filter_location,
    prepare_demo_results,
    prepare_verified_results
)

REPORT_PATH = PROJECT_ROOT / "docs" / "test_results.md"

# All test records below are synthetic fixtures.
# They do not represent verified real vendors.

def create_test_data():

    return pd.DataFrame([
        {
            "vendor_id": "TEST-001",
            "vendor_name": "Demo Wedding Decorator",
            "main_category": "Decoration",
            "location": "Thane, Maharashtra",
            "event_types": "['Wedding']",
            "min_price": 5000,
            "max_price": 12000,
            "pricing_type": "per_event",
            "availability": "Available",
            "guest_capacity": 200,
            "verified_rating": 4.5,
            "rating_listed": 4.5
        },
        {
            "vendor_id": "TEST-002",
            "vendor_name": "Demo Birthday Caterer",
            "main_category": "Catering",
            "location": "Pune, Maharashtra",
            "event_types": "['Birthday']",
            "min_price": 8000,
            "max_price": 15000,
            "pricing_type": "per_event",
            "availability": "Available",
            "guest_capacity": 150,
            "verified_rating": 4.2,
            "rating_listed": 4.2
        },
        {
            "vendor_id": "TEST-003",
            "vendor_name": "Demo Corporate Photographer",
            "main_category": "Photography",
            "location": "Bangalore, Karnataka",
            "event_types": "['Corporate Event']",
            "min_price": 10000,
            "max_price": 20000,
            "pricing_type": "per_event",
            "availability": "Available",
            "guest_capacity": 300,
            "verified_rating": 4.8,
            "rating_listed": 4.8
        },
        {
            "vendor_id": "TEST-004",
            "vendor_name": "Demo Event Planner",
            "main_category": "Event Planning",
            "location": "Thane, Maharashtra",
            "event_types": "['Wedding', 'Birthday']",
            "min_price": 5000,
            "max_price": 10000,
            "pricing_type": "per_event",
            "availability": "Available",
            "guest_capacity": 100,
            "verified_rating": 4.0,
            "rating_listed": 4.0
        },
        {
            "vendor_id": "TEST-005",
            "vendor_name": "Demo Makeup Artist",
            "main_category": "Makeup",
            "location": "Pune, Maharashtra",
            "event_types": "['Wedding', 'Engagement']",
            "min_price": 3000,
            "max_price": 8000,
            "pricing_type": "per_event",
            "availability": "Available",
            "guest_capacity": 100,
            "verified_rating": 4.6,
            "rating_listed": 4.6
        }
    ])


def run_demo_scenario(df, category, location, event, budget, guests):

    customer = {
        "category": category,
        "location": location,
        "event": event,
        "budget": budget,
        "guests": guests
    }

    category_df = filter_category(df, category)
    location_df = filter_location(category_df, location)

    results = prepare_demo_results(location_df, customer)

    return results


def run_verified_scenario(df, category, location, event, budget, guests):

    customer = {
        "category": category,
        "location": location,
        "event": event,
        "budget": budget,
        "guests": guests
    }

    category_df = filter_category(df, category)
    location_df = filter_location(category_df, location)

    results = prepare_verified_results(location_df, customer)

    return results


def main():

    df = create_test_data()

    results = []

    print("\n============================================")
    print("EVENTEASE - ASSIGNMENT SCENARIO TESTING")
    print("============================================")

    # Scenario 1: Wedding Decoration - Thane
    try:
        output = run_demo_scenario(
            df, "Decoration", "Thane, Maharashtra",
            "Wedding", 15000, 100
        )

        passed = len(output) == 1

        results.append({
            "scenario": "1. Wedding Decoration - Thane",
            "expected": "1 matching research lead",
            "actual": f"{len(output)} matching lead(s)",
            "status": "PASS" if passed else "FAIL"
        })

    except Exception as error:
        results.append({
            "scenario": "1. Wedding Decoration - Thane",
            "expected": "1 matching research lead",
            "actual": str(error),
            "status": "FAIL"
        })

    # Scenario 2: Birthday Catering - Pune
    try:
        output = run_demo_scenario(
            df, "Catering", "Pune, Maharashtra",
            "Birthday", 20000, 80
        )

        passed = len(output) == 1

        results.append({
            "scenario": "2. Birthday Catering - Pune",
            "expected": "1 matching research lead",
            "actual": f"{len(output)} matching lead(s)",
            "status": "PASS" if passed else "FAIL"
        })

    except Exception as error:
        results.append({
            "scenario": "2. Birthday Catering - Pune",
            "expected": "1 matching research lead",
            "actual": str(error),
            "status": "FAIL"
        })

    # Scenario 3: Corporate Photography - Bangalore
    try:
        output = run_demo_scenario(
            df, "Photography", "Bangalore, Karnataka",
            "Corporate Event", 25000, 100
        )

        passed = len(output) == 1

        results.append({
            "scenario": "3. Corporate Photography - Bangalore",
            "expected": "1 matching research lead",
            "actual": f"{len(output)} matching lead(s)",
            "status": "PASS" if passed else "FAIL"
        })

    except Exception as error:
        results.append({
            "scenario": "3. Corporate Photography - Bangalore",
            "expected": "1 matching research lead",
            "actual": str(error),
            "status": "FAIL"
        })

    # Scenario 4: Low-budget Event Planning
    # Verified Mode should reject a vendor whose minimum price
    # exceeds the customer's budget.
    try:
        output = run_verified_scenario(
            df, "Event Planning", "Thane, Maharashtra",
            "Wedding", 1000, 50
        )

        passed = output.empty

        results.append({
            "scenario": "4. Low-budget Event Planning",
            "expected": "Vendor rejected because price exceeds budget",
            "actual": (
                "No matching vendors" if output.empty
                else f"{len(output)} vendor(s) returned"
            ),
            "status": "PASS" if passed else "FAIL"
        })

    except Exception as error:
        results.append({
            "scenario": "4. Low-budget Event Planning",
            "expected": "Vendor rejected because price exceeds budget",
            "actual": str(error),
            "status": "FAIL"
        })

    # Scenario 5: Search without a budget
    # Demo Mode should work when budget=None.
    try:
        output = run_demo_scenario(
            df, "Makeup", "Pune, Maharashtra",
            "Wedding", None, 50
        )

        passed = (
            len(output) == 1
            and output["recommendation_score"].notna().all()
        )

        results.append({
            "scenario": "5. Search without budget",
            "expected": "1 matching lead with a calculated score",
            "actual": (
                f"{len(output)} matching lead(s); "
                "budget skipped"
            ),
            "status": "PASS" if passed else "FAIL"
        })

    except Exception as error:
        results.append({
            "scenario": "5. Search without budget",
            "expected": "1 matching lead with a calculated score",
            "actual": str(error),
            "status": "FAIL"
        })

    # Print report
    report_df = pd.DataFrame(results)

    print("\nTEST RESULTS")
    print("--------------------------------------------")
    print(report_df.to_string(index=False))

    passed_count = (report_df["status"] == "PASS").sum()
    failed_count = (report_df["status"] == "FAIL").sum()

    print("\nSUMMARY")
    print("--------------------------------------------")
    print("Total scenarios:", len(results))
    print("Passed:", passed_count)
    print("Failed:", failed_count)

    # Generate Markdown report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    report = f"""# EventEase Assignment Scenario Test Results

**Test date:** {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

## Test summary

- Total scenarios: {len(results)}
- Passed: {passed_count}
- Failed: {failed_count}

## Scenario results

{report_df.to_markdown(index=False)}

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
"""

    REPORT_PATH.write_text(report, encoding="utf-8")

    print("\nReport saved to:", REPORT_PATH)

    if failed_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
