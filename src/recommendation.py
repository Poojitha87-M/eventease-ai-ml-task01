
import pandas as pd
from pathlib import Path


# ==========================================
# 1. LOAD CLEANED VENDOR DATASET
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "clean" / "vendors_clean.csv"

df = pd.read_csv(DATA_PATH)

print("Vendor dataset loaded successfully!")
print("Total vendors:", len(df))

print("\nAvailable categories:")
print(df["category"].dropna().unique())

print("\nAvailable locations:")
print(df["location"].dropna().unique())


# ==========================================
# 2. CUSTOMER INPUT
# ==========================================

VALID_CATEGORIES = [
    "Catering",
    "Photography",
    "Decoration",
    "Event Planning",
    "Makeup Artist",
    "Entertainment"
]

VALID_LOCATIONS = [
    "CBD Belapur",
    "Vashi",
    "Nerul"
]


def get_customer_requirements():

    print("\nEnter Customer Requirements")

    event_type = input("Enter event type: ").strip()

    # Validate category
    while True:
        category_input = input("Enter vendor category: ").strip()

        category = next(
            (
                item for item in VALID_CATEGORIES
                if item.lower() == category_input.lower()
            ),
            None
        )

        if category:
            break

        print("Invalid category. Please choose:")
        print(", ".join(VALID_CATEGORIES))

    # Validate location
    while True:
        location_input = input("Enter location: ").strip()

        location = next(
            (
                item for item in VALID_LOCATIONS
                if item.lower() == location_input.lower()
            ),
            None
        )

        if location:
            break

        print("Invalid location. Please enter CBD Belapur, Vashi, or Nerul.")

    # Validate budget
    while True:
        try:
            budget = float(input("Enter budget in INR: "))

            if budget > 0:
                break

            print("Budget must be greater than zero.")

        except ValueError:
            print("Please enter a valid numeric budget.")

    # Validate guests
    while True:
        try:
            guests = int(input("Enter number of guests: "))

            if guests > 0:
                break

            print("Number of guests must be greater than zero.")

        except ValueError:
            print("Please enter a valid whole number.")

    return {
        "event_type": event_type,
        "category": category,
        "location": location,
        "budget": budget,
        "guests": guests
    }


# ==========================================
# 3. FILTER BY CATEGORY
# ==========================================

def filter_by_category(data, category):

    result = data[
        data["category"].astype(str).str.strip().str.lower()
        == category.strip().lower()
    ].copy()

    return result


# ==========================================
# 4. FILTER BY AVAILABILITY
# ==========================================

def filter_by_availability(data):

    result = data[
        data["availability"].astype(str).str.strip().str.lower()
        == "available"
    ].copy()

    return result


# ==========================================
# 5. FILTER BY BUDGET
# ==========================================

def filter_by_budget(data, budget, guests):

    results = []

    for _, vendor in data.iterrows():

        pricing_type = str(vendor["pricing_type"]).strip().lower()

        possible_prices = []

        # Per-plate pricing
        if pricing_type in ["per_plate", "both"]:

            price_per_plate = vendor["min_price_per_plate"]

            if pd.notna(price_per_plate):
                estimated_cost = float(price_per_plate) * guests

                if estimated_cost <= budget:
                    possible_prices.append(
                        (estimated_cost, "per_plate")
                    )

        # Per-event pricing
        if pricing_type in ["per_event", "both"]:

            price_per_event = vendor["min_price_per_event"]

            if pd.notna(price_per_event):
                estimated_cost = float(price_per_event)

                if estimated_cost <= budget:
                    possible_prices.append(
                        (estimated_cost, "per_event")
                    )

        # Keep the cheapest valid affordable pricing option
        if possible_prices:

            estimated_cost, pricing_basis = min(
                possible_prices,
                key=lambda item: item[0]
            )

            vendor_data = vendor.to_dict()

            vendor_data["estimated_cost"] = estimated_cost
            vendor_data["pricing_basis"] = pricing_basis

            results.append(vendor_data)

    # Preserve columns even when no vendors match
    result_columns = list(data.columns) + [
        "estimated_cost",
        "pricing_basis"
    ]

    return pd.DataFrame(results, columns=result_columns)


# ==========================================
# 6. LOCATION SCORING
# ==========================================

def add_location_score(data, requested_location):

    result = data.copy()

    result["location_score"] = result["location"].apply(
        lambda location:
        1.0 if str(location).strip().lower()
        == requested_location.strip().lower()
        else 0.5
    )

    return result


# ==========================================
# 7. RATING SCORING
# ==========================================

def add_rating_score(data):

    result = data.copy()

    result["rating_score"] = (
        pd.to_numeric(result["rating"], errors="coerce")
        .fillna(0)
        .clip(0, 5) / 5
    )

    return result


# ==========================================
# 8. BUDGET COMPATIBILITY SCORING
# ==========================================

def add_budget_score(data, budget):

    result = data.copy()

    result["budget_score"] = (
        1 - result["estimated_cost"] / budget
    ).clip(0, 1)

    return result


# ==========================================
# 9. EVENT RELEVANCE SCORING
# ==========================================

def add_relevance_score(data, event_type):

    result = data.copy()

    def check_event(events):

        if pd.isna(events):
            return 0.0

        event_list = [
            item.strip().lower()
            for item in str(events).split("|")
        ]

        return (
            1.0 if event_type.strip().lower() in event_list
            else 0.0
        )

    result["relevance_score"] = (
        result["event_type"].apply(check_event)
    )

    return result


# ==========================================
# 10. CALCULATE FINAL RECOMMENDATION SCORE
# ==========================================

def calculate_final_score(data):

    result = data.copy()

    result["final_score"] = (
        result["budget_score"] * 0.35
        + result["location_score"] * 0.30
        + result["rating_score"] * 0.25
        + result["relevance_score"] * 0.10
    ) * 100

    result = result.sort_values(
        by="final_score",
        ascending=False
    ).reset_index(drop=True)

    return result


# ==========================================
# 11. MAIN RECOMMENDATION PIPELINE
# ==========================================

customer = get_customer_requirements()

print("\nCustomer Requirements:")
print(customer)


# Step 1: Category filtering

category_results = filter_by_category(
    df,
    customer["category"]
)

print("\n1. CATEGORY FILTERING RESULTS")

print(
    category_results[
        ["vendor_id", "vendor_name", "category"]
    ].to_string(index=False)
)

print("Total vendors:", len(category_results))


# Step 2: Availability filtering

available_results = filter_by_availability(
    category_results
)

print("\n2. AVAILABLE VENDORS")

print(
    available_results[
        ["vendor_id", "vendor_name", "availability"]
    ].to_string(index=False)
)

print("Available vendors:", len(available_results))


# Step 3: Budget filtering

budget_results = filter_by_budget(
    available_results,
    customer["budget"],
    customer["guests"]
)

print("\n3. BUDGET COMPATIBLE VENDORS")

if not budget_results.empty:

    print(
        budget_results[
            [
                "vendor_id",
                "vendor_name",
                "pricing_type",
                "estimated_cost",
                "pricing_basis"
            ]
        ].to_string(index=False)
    )

print("Budget-compatible vendors:", len(budget_results))


# Step 4 onwards: Scoring and ranking

if budget_results.empty:

    print("\nNo suitable vendors found within your budget.")
    print("Try increasing your budget or changing your requirements.")

else:

    location_results = add_location_score(
        budget_results,
        customer["location"]
    )

    rating_results = add_rating_score(
        location_results
    )

    budget_scored = add_budget_score(
        rating_results,
        customer["budget"]
    )

    relevance_results = add_relevance_score(
        budget_scored,
        customer["event_type"]
    )

    final_results = calculate_final_score(
        relevance_results
    )

    print("\n4. LOCATION MATCHING RESULTS")

    print(
        final_results[
            ["vendor_name", "location", "location_score"]
        ].to_string(index=False)
    )

    print("\n5. VENDOR RATING RESULTS")

    print(
        final_results[
            ["vendor_name", "rating", "rating_score"]
        ].to_string(index=False)
    )

    print("\n6. FINAL VENDOR RECOMMENDATIONS")

    print(
        final_results[
            [
                "vendor_id",
                "vendor_name",
                "category",
                "location",
                "estimated_cost",
                "pricing_basis",
                "rating",
                "budget_score",
                "location_score",
                "rating_score",
                "relevance_score",
                "final_score"
            ]
        ].to_string(index=False)
    )
