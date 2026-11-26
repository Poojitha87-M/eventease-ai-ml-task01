
import pandas as pd
from pathlib import Path
import re

# ============================================================
# EVENTEASE - VENDOR RECOMMENDATION SYSTEM
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "clean" / "vendors_researched_final.csv"

WEIGHTS = {
    "budget": 0.35,
    "location": 0.30,
    "rating": 0.25,
    "relevance": 0.10
}

VALID_CATEGORIES = [
    "Catering",
    "Photography",
    "Decoration",
    "Event Planning",
    "Makeup",
    "Entertainment"
]

LOCATION_ALIASES = {
    "thane": "Thane, Maharashtra",
    "pune": "Pune, Maharashtra",
    "bangalore": "Bangalore, Karnataka",
    "bengaluru": "Bangalore, Karnataka",
    "karnataka": "Bangalore, Karnataka"
}

EVENT_ALIASES = {
    "marriage": "Wedding",
    "marriage function": "Wedding",
    "wedding": "Wedding",
    "birthday party": "Birthday",
    "birthday": "Birthday",
    "corporate": "Corporate Event",
    "corporate event": "Corporate Event",
    "engagement": "Engagement",
    "baby shower": "Baby Shower",
    "college event": "College Event",
    "private party": "Private Party",
    "festival": "Festival"
}


# ============================================================
# 1. LOAD DATA
# ============================================================

def load_vendor_data():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    required_columns = [
        "vendor_id",
        "vendor_name",
        "main_category",
        "location",
        "pricing_type",
        "availability",
        "verification_status"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


# ============================================================
# 2. NORMALIZE TEXT
# ============================================================

def normalize_text(value):

    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def normalize_location(user_location):

    key = normalize_text(user_location)

    for alias, full_location in LOCATION_ALIASES.items():

        if key == alias:
            return full_location

        if key == normalize_text(full_location):
            return full_location

    return None


def normalize_event_type(event_type):

    key = normalize_text(event_type)

    return EVENT_ALIASES.get(
        key,
        event_type.strip().title()
    )


# ============================================================
# 3. CUSTOMER INPUT
# ============================================================

def get_customer_input():

    print("\n========== EVENTEASE VENDOR RECOMMENDATION ==========")

    print("\nAvailable categories:")

    for category in VALID_CATEGORIES:
        print("-", category)

    while True:

        category_input = input(
            "\nEnter vendor category: "
        ).strip()

        category = next(
            (
                item for item in VALID_CATEGORIES
                if normalize_text(item) == normalize_text(category_input)
            ),
            None
        )

        if category:
            break

        print("Invalid category. Please choose from the list.")

    print("\nAvailable locations:")
    print("Thane, Pune, Bangalore")

    while True:

        location_input = input(
            "\nEnter location: "
        ).strip()

        location = normalize_location(location_input)

        if location:
            break

        print("Invalid location. Enter Thane, Pune, or Bangalore.")

    while True:

        event_input = input(
            "\nEnter event type (Wedding/Marriage/Birthday): "
        ).strip()

        if event_input:
            event_type = normalize_event_type(event_input)
            break

        print("Event type cannot be empty.")

    while True:

        try:

            budget = float(
                input("\nEnter total event budget (₹): ")
            )

            if budget > 0:
                break

            print("Budget must be greater than zero.")

        except ValueError:
            print("Enter a valid budget.")

    while True:

        try:

            guests = int(
                input("\nEnter number of guests: ")
            )

            if guests > 0:
                break

            print("Guest count must be greater than zero.")

        except ValueError:
            print("Enter a valid whole number.")

    print("\nRecommendation mode:")
    print("1. Verified Mode")
    print("2. Research/Demo Mode")

    while True:

        mode = input(
            "Choose mode (1 or 2): "
        ).strip()

        if mode in ["1", "2"]:
            break

        print("Please enter 1 or 2.")

    return {
        "category": category,
        "location": location,
        "event_type": event_type,
        "budget": budget,
        "guests": guests,
        "mode": mode
    }


# ============================================================
# 4. FILTER BY CATEGORY
# ============================================================

def filter_by_category(df, category):

    return df[
        df["main_category"].apply(normalize_text)
        == normalize_text(category)
    ].copy()


# ============================================================
# 5. FILTER BY LOCATION
# ============================================================

def filter_by_location(df, location):

    return df[
        df["location"].apply(normalize_text)
        == normalize_text(location)
    ].copy()


# ============================================================
# 6. CHECK AVAILABILITY
# ============================================================

def is_available(row):

    return normalize_text(
        row.get("availability", "")
    ) == "available"


# ============================================================
# 7. NUMERIC VALUE
# ============================================================

def get_numeric_value(row, column):

    value = row.get(column, None)

    if value is None or pd.isna(value):
        return None

    try:

        number = float(value)

        if number < 0:
            return None

        return number

    except (ValueError, TypeError):
        return None


# ============================================================
# 8. ESTIMATE VENDOR COST
# ============================================================

def estimate_vendor_cost(row, guests):

    pricing_type = normalize_text(
        row.get("pricing_type", "")
    )

    per_plate_price = get_numeric_value(
        row, "max_price_per_plate"
    )

    per_event_price = get_numeric_value(
        row, "max_price_per_event"
    )

    generic_max_price = get_numeric_value(
        row, "max_price"
    )

    if pricing_type in ["per_plate", "per plate"]:

        price = per_plate_price

        if price is None:
            price = generic_max_price

        if price is not None:
            return price * guests

    elif pricing_type in ["per_event", "per event"]:

        price = per_event_price

        if price is None:
            price = generic_max_price

        if price is not None:
            return price

    elif pricing_type == "both":

        if per_event_price is not None:
            return per_event_price

        if per_plate_price is not None:
            return per_plate_price * guests

    return None


# ============================================================
# 9. GUEST CAPACITY
# ============================================================

def get_capacity(row):

    capacity = row.get("guest_capacity", None)

    if capacity is None or pd.isna(capacity):
        return None

    numbers = re.findall(
        r"\d+",
        str(capacity)
    )

    if not numbers:
        return None

    return max(int(number) for number in numbers)


# ============================================================
# 10. EVENT RELEVANCE SCORE
# ============================================================

def calculate_relevance_score(row, event_type):

    vendor_events = row.get("event_type", "")

    if pd.isna(vendor_events):
        return 0.0

    supported_events = [
        normalize_event_type(item.strip())
        for item in str(vendor_events).split("|")
    ]

    return float(
        normalize_text(event_type)
        in [normalize_text(item) for item in supported_events]
    )


# ============================================================
# 11. RATING SCORE
# ============================================================

def calculate_rating_score(row):

    rating = get_numeric_value(
        row,
        "verified_rating"
    )

    if rating is None or rating > 5:
        return 0.0

    return rating / 5.0


# ============================================================
# 12. BUDGET SCORE
# ============================================================

def calculate_budget_score(cost, budget):

    if cost is None or budget <= 0:
        return 0.0

    return max(
        0.0,
        1.0 - (cost / budget)
    )


# ============================================================
# 13. DATA COMPLETENESS SCORE
# ============================================================

def has_text_value(value):

    if value is None or pd.isna(value):
        return False

    return str(value).strip().lower() not in [
        "",
        "nan",
        "none",
        "null"
    ]


def calculate_data_completeness(row, guests):

    checks = [
        has_text_value(row.get("direct_source_url")),

        get_numeric_value(
            row, "verified_rating"
        ) is not None,

        has_text_value(
            row.get("verified_contact")
        ),

        estimate_vendor_cost(row, guests) is not None,

        normalize_text(
            row.get("availability", "")
        ) in ["available", "unavailable"],

        get_capacity(row) is not None
    ]

    completed = sum(checks)

    return round(
        (completed / len(checks)) * 100,
        2
    )


# ============================================================
# 14. RESEARCH / DEMO MODE
# ============================================================

def prepare_demo_results(df, customer):

    results = df.copy()

    results["estimated_cost"] = results.apply(
        lambda row: estimate_vendor_cost(
            row,
            customer["guests"]
        ),
        axis=1
    )

    results["capacity_value"] = results.apply(
        get_capacity,
        axis=1
    )

    results["data_completeness_percentage"] = results.apply(
        lambda row: calculate_data_completeness(
            row,
            customer["guests"]
        ),
        axis=1
    )

    results["availability_status"] = results[
        "availability"
    ].fillna("Unconfirmed")

    results["price_status"] = results[
        "pricing_type"
    ].fillna("Not confirmed")

    results["rating_status"] = results.apply(
        lambda row: (
            "Verified"
            if get_numeric_value(
                row, "verified_rating"
            ) is not None
            else "Not verified"
        ),
        axis=1
    )

    results["capacity_status"] = results[
        "capacity_value"
    ].apply(
        lambda value: (
            "Available"
            if value is not None
            else "Not confirmed"
        )
    )

    results["budget_score"] = results[
        "estimated_cost"
    ].apply(
        lambda cost: (
            calculate_budget_score(
                cost,
                customer["budget"]
            )
            if cost is not None
            else 0.0
        )
    )

    results["location_score"] = 1.0

    results["rating_score"] = results.apply(
        calculate_rating_score,
        axis=1
    )

    results["relevance_score"] = results.apply(
        lambda row: calculate_relevance_score(
            row,
            customer["event_type"]
        ),
        axis=1
    )

    results["final_score"] = (
        results["budget_score"] * WEIGHTS["budget"]
        + results["location_score"] * WEIGHTS["location"]
        + results["rating_score"] * WEIGHTS["rating"]
        + results["relevance_score"] * WEIGHTS["relevance"]
    )

    results["final_score_percentage"] = (
        results["final_score"] * 100
    ).round(2)

    results["recommendation_status"] = results.apply(
        lambda row: (
            "Needs verification"
            if (
                not is_available(row)
                or row["estimated_cost"] is None
                or row["capacity_value"] is None
                or row["rating_status"] != "Verified"
            )
            else "Confirmed"
        ),
        axis=1
    )

    return results.sort_values(
        by=[
            "final_score",
            "data_completeness_percentage"
        ],
        ascending=False
    )


# ============================================================
# 15. VERIFIED MODE
# ============================================================

def prepare_verified_results(df, customer):

    results = df.copy()

    results = results[
        results["availability"].apply(
            lambda value: normalize_text(value) == "available"
        )
    ].copy()

    if results.empty:
        return results

    results["estimated_cost"] = results.apply(
        lambda row: estimate_vendor_cost(
            row,
            customer["guests"]
        ),
        axis=1
    )

    results = results[
        results["estimated_cost"].notna()
    ].copy()

    results = results[
        results["estimated_cost"] <= customer["budget"]
    ].copy()

    if results.empty:
        return results

    results["capacity_value"] = results.apply(
        get_capacity,
        axis=1
    )

    results = results[
        results["capacity_value"].notna()
    ].copy()

    results = results[
        results["capacity_value"] >= customer["guests"]
    ].copy()

    if results.empty:
        return results

    results["data_completeness_percentage"] = results.apply(
        lambda row: calculate_data_completeness(
            row,
            customer["guests"]
        ),
        axis=1
    )

    results["budget_score"] = results[
        "estimated_cost"
    ].apply(
        lambda cost: calculate_budget_score(
            cost,
            customer["budget"]
        )
    )

    results["location_score"] = 1.0

    results["rating_score"] = results.apply(
        calculate_rating_score,
        axis=1
    )

    results["relevance_score"] = results.apply(
        lambda row: calculate_relevance_score(
            row,
            customer["event_type"]
        ),
        axis=1
    )

    results["final_score"] = (
        results["budget_score"] * WEIGHTS["budget"]
        + results["location_score"] * WEIGHTS["location"]
        + results["rating_score"] * WEIGHTS["rating"]
        + results["relevance_score"] * WEIGHTS["relevance"]
    )

    results["final_score_percentage"] = (
        results["final_score"] * 100
    ).round(2)

    return results.sort_values(
        by=[
            "final_score",
            "data_completeness_percentage"
        ],
        ascending=False
    )


# ============================================================
# 16. DISPLAY RESULTS
# ============================================================

def display_results(df, mode):

    print("\n========== RECOMMENDATION RESULTS ==========")

    if df.empty:

        print("\nNo matching vendors found.")

        if mode == "1":
            print(
                "No vendors currently satisfy all confirmed "
                "availability, pricing, budget, and capacity checks."
            )

        return

    if mode == "2":

        display_columns = [
            "vendor_id",
            "vendor_name",
            "main_category",
            "location",
            "estimated_cost",
            "verified_rating",
            "availability_status",
            "price_status",
            "capacity_status",
            "data_completeness_percentage",
            "recommendation_status",
            "final_score_percentage"
        ]

    else:

        display_columns = [
            "vendor_id",
            "vendor_name",
            "main_category",
            "location",
            "estimated_cost",
            "verified_rating",
            "data_completeness_percentage",
            "final_score_percentage"
        ]

    available_columns = [
        col for col in display_columns
        if col in df.columns
    ]

    print(
        df[available_columns]
        .head(10)
        .to_string(index=False)
    )

    print("\nTotal matching vendors:", len(df))

    if mode == "2":

        print(
            "\nIMPORTANT: Research/Demo Mode displays "
            "researched leads, not confirmed bookings."
        )

        print(
            "Verify availability, pricing, ratings, "
            "and capacity before recommending a vendor."
        )


# ============================================================
# 17. DATASET SUMMARY
# ============================================================

def show_dataset_status(df):

    print("\n========== DATASET STATUS ==========")

    print("Total researched vendors:", len(df))

    print("\nAvailability:")
    print(
        df["availability"]
        .fillna("Missing")
        .value_counts()
        .to_string()
    )

    print("\nPricing type:")
    print(
        df["pricing_type"]
        .fillna("Missing")
        .value_counts()
        .to_string()
    )

    if "guest_capacity" in df.columns:
        print(
            "\nMissing guest capacity:",
            df["guest_capacity"].isna().sum()
        )

    if "verified_rating" in df.columns:
        print(
            "Missing verified ratings:",
            df["verified_rating"].isna().sum()
        )


# ============================================================
# 18. MAIN FUNCTION
# ============================================================

def main():

    try:

        df = load_vendor_data()

        show_dataset_status(df)

        customer = get_customer_input()

        print("\n========== FILTERING VENDORS ==========")

        category_df = filter_by_category(
            df,
            customer["category"]
        )

        print(
            "After category filter:",
            len(category_df)
        )

        location_df = filter_by_location(
            category_df,
            customer["location"]
        )

        print(
            "After location filter:",
            len(location_df)
        )

        if customer["mode"] == "1":

            print("\nRunning VERIFIED recommendation mode...")

            results = prepare_verified_results(
                location_df,
                customer
            )

        else:

            print("\nRunning RESEARCH/DEMO recommendation mode...")

            results = prepare_demo_results(
                location_df,
                customer
            )

        display_results(
            results,
            customer["mode"]
        )

    except FileNotFoundError as error:

        print("\nFILE ERROR:", error)

    except Exception as error:

        print("\nERROR:", error)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()
