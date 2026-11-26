import pandas as pd
import re
import ast
from pathlib import Path

# ============================================================
# EVENTEASE - VENDOR RECOMMENDATION SYSTEM
# ============================================================

DATA_PATH = Path("data/clean/vendors_researched_final.csv")

WEIGHTS = {
    "budget": 0.35,
    "location": 0.30,
    "rating": 0.25,
    "relevance": 0.10
}

CATEGORIES = [
    "Catering",
    "Photography",
    "Decoration",
    "Event Planning",
    "Makeup",
    "Entertainment"
]

LOCATIONS = {
    "Thane, Maharashtra": [
        "thane",
        "thane maharashtra"
    ],
    "Pune, Maharashtra": [
        "pune",
        "pune maharashtra"
    ],
    "Bangalore, Karnataka": [
        "bangalore",
        "bangalore karnataka",
        "bengaluru",
        "bengaluru karnataka"
    ]
}

EVENT_TYPES = [
    "Wedding",
    "Birthday",
    "Corporate Event",
    "Engagement",
    "Baby Shower",
    "College Event",
    "Private Party",
    "Festival"
]


# ============================================================
# NORMALIZATION FUNCTIONS
# ============================================================

def clean_text(value):
    if pd.isna(value):
        return ""

    return " ".join(str(value).strip().lower().split())


def normalize_category(category):
    value = clean_text(category)

    for item in CATEGORIES:
        if value == item.lower():
            return item

    return None


def normalize_location(location):
    """
    Supports both short user inputs and full dataset locations.
    """

    value = clean_text(location)

    # Normalize punctuation and spaces
    value = re.sub(r"[,]+", " ", value)
    value = " ".join(value.split())

    aliases = {
        "thane": "Thane, Maharashtra",
        "thane maharashtra": "Thane, Maharashtra",

        "pune": "Pune, Maharashtra",
        "pune maharashtra": "Pune, Maharashtra",

        "bangalore": "Bangalore, Karnataka",
        "bangalore karnataka": "Bangalore, Karnataka",

        "bengaluru": "Bangalore, Karnataka",
        "bengaluru karnataka": "Bangalore, Karnataka"
    }

    return aliases.get(value)


def normalize_event(event):
    value = clean_text(event)

    event_aliases = {
        "wedding": "Wedding",
        "birthday": "Birthday",
        "corporate": "Corporate Event",
        "corporate event": "Corporate Event",
        "engagement": "Engagement",
        "baby shower": "Baby Shower",
        "college event": "College Event",
        "private party": "Private Party",
        "festival": "Festival"
    }

    return event_aliases.get(value, event.strip().title() if event else "")


# ============================================================
# DATA LOADING
# ============================================================

def load_vendors():
    if not DATA_PATH.exists():
        print(f"\nDataset not found: {DATA_PATH}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as error:
        print("Error loading dataset:", error)
        return pd.DataFrame()

    df.columns = df.columns.str.strip()

    if "location" in df.columns:
        df["normalized_location"] = df["location"].apply(
            normalize_location
        )

    if "main_category" in df.columns:
        df["normalized_category"] = df["main_category"].apply(
            normalize_category
        )

    return df


# ============================================================
# CUSTOMER INPUT
# ============================================================

def get_customer_input():

    print("\n========== EVENTEASE VENDOR RECOMMENDATION ==========")

    print("\nAvailable categories:")
    for category in CATEGORIES:
        print("-", category)

    while True:
        category_input = input("\nEnter vendor category: ").strip()
        category = normalize_category(category_input)

        if category:
            break

        print("Invalid category. Please choose from the available categories.")

    print("\nAvailable locations:")
    available_locations = list(LOCATIONS.keys())

    for index, location in enumerate(available_locations, start=1):
        print(f"{index}. {location}")

    while True:
        location_input = input("\nEnter location: ").strip()
        location = normalize_location(location_input)

        if location:
            break

        print("Invalid location. Please choose Thane, Pune or Bangalore.")

    print("\nAvailable event types:")
    for event in EVENT_TYPES:
        print("-", event)

    while True:
        event_input = input("\nEnter event type: ").strip()
        event = normalize_event(event_input)

        if event in EVENT_TYPES:
            break

        print("Invalid event type. Please enter a listed event type.")

    while True:
        budget_input = input(
            "\nEnter total event budget (₹), or press Enter to skip: "
        ).strip()

        if budget_input == "":
            budget = None
            break

        try:
            budget = float(budget_input)

            if budget <= 0:
                print("Budget must be greater than zero.")
                continue

            break

        except ValueError:
            print("Please enter a valid number.")

    while True:
        guests_input = input("\nEnter number of guests: ").strip()

        try:
            guests = int(guests_input)

            if guests <= 0:
                print("Number of guests must be greater than zero.")
                continue

            break

        except ValueError:
            print("Please enter a valid whole number.")

    print("\nRecommendation mode:")
    print("1. Verified Mode")
    print("2. Research/Demo Mode")

    while True:
        mode = input("Choose mode (1 or 2): ").strip()

        if mode in ["1", "2"]:
            break

        print("Please choose 1 or 2.")

    return {
        "category": category,
        "location": location,
        "event": event,
        "budget": budget,
        "guests": guests,
        "mode": mode
    }


# ============================================================
# EVENT RELEVANCE
# ============================================================

def get_event_values(value):

    if pd.isna(value):
        return []

    if isinstance(value, list):
        return [clean_text(x) for x in value]

    text_value = str(value).strip()

    try:
        parsed = ast.literal_eval(text_value)

        if isinstance(parsed, list):
            return [clean_text(x) for x in parsed]

    except (ValueError, SyntaxError):
        pass

    return [
        clean_text(x)
        for x in re.split(r"[,;|]", text_value)
        if clean_text(x)
    ]


def calculate_relevance_score(row, selected_event):

    possible_columns = [
        "event_types",
        "event_categories",
        "events_supported",
        "event_type",
        "events"
    ]

    event_values = []

    for column in possible_columns:
        if column in row.index:
            event_values.extend(get_event_values(row[column]))

    if not event_values:
        return 50

    selected = clean_text(selected_event)

    if selected in event_values:
        return 100

    if any(selected in item or item in selected for item in event_values):
        return 75

    return 0


# ============================================================
# BUDGET SCORING
# ============================================================

def get_numeric_price(value):

    if pd.isna(value):
        return None

    try:
        number = float(
            str(value).replace(",", "").replace("₹", "").strip()
        )

        if number < 0:
            return None

        return number

    except (ValueError, TypeError):
        return None


def get_vendor_price(row):

    min_price = get_numeric_price(row.get("min_price"))
    max_price = get_numeric_price(row.get("max_price"))

    if min_price is not None and max_price is not None:
        return min_price, max_price

    min_event = get_numeric_price(row.get("min_price_per_event"))
    max_event = get_numeric_price(row.get("max_price_per_event"))

    if min_event is not None and max_event is not None:
        return min_event, max_event

    return None, None


def calculate_budget_score(row, budget):

    if budget is None:
        return None

    minimum, maximum = get_vendor_price(row)

    if minimum is None or maximum is None:
        return None

    if budget < minimum:
        return 0

    if budget >= maximum:
        return 100

    if maximum == minimum:
        return 100

    return ((budget - minimum) / (maximum - minimum)) * 100


# ============================================================
# RATING SCORING
# ============================================================

def get_vendor_rating(row):

    possible_columns = [
        "verified_rating",
        "rating_listed",
        "rating"
    ]

    for column in possible_columns:
        if column in row.index:
            value = get_numeric_price(row[column])

            if value is not None and 0 <= value <= 5:
                return value

    return None


def calculate_rating_score(row):

    rating = get_vendor_rating(row)

    if rating is None:
        return None

    return (rating / 5) * 100


# ============================================================
# LOCATION SCORING
# ============================================================

def calculate_location_score(row, selected_location):

    vendor_location = normalize_location(row.get("location"))

    if vendor_location == selected_location:
        return 100

    return 0


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(row, budget, selected_location, selected_event):

    scores = {
        "budget": calculate_budget_score(row, budget),
        "location": calculate_location_score(row, selected_location),
        "rating": calculate_rating_score(row),
        "relevance": calculate_relevance_score(row, selected_event)
    }

    available_weight = 0
    weighted_score = 0

    for name, score in scores.items():

        if score is None:
            continue

        weight = WEIGHTS[name]

        weighted_score += score * weight
        available_weight += weight

    if available_weight == 0:
        return 0

    # Redistribute weights when budget or rating is unavailable
    final_score = weighted_score / available_weight

    return round(final_score, 2)


# ============================================================
# FILTERING
# ============================================================

def filter_category(df, category):

    if df.empty:
        return df

    return df[
        df["main_category"].astype(str).str.strip().str.lower()
        == category.lower()
    ].copy()


def filter_location(df, location):

    if df.empty:
        return df

    return df[
        df["location"].apply(normalize_location) == location
    ].copy()


def filter_event(df, event):

    if df.empty:
        return df

    mask = df.apply(
        lambda row: calculate_relevance_score(row, event) > 0,
        axis=1
    )

    return df[mask].copy()


# ============================================================
# RESEARCH / DEMO MODE
# ============================================================

def prepare_demo_results(df, customer):

    if df.empty:
        return df

    results = df.copy()

    results["recommendation_score"] = results.apply(
        lambda row: calculate_final_score(
            row,
            customer["budget"],
            customer["location"],
            customer["event"]
        ),
        axis=1
    )

    results["recommendation_status"] = (
        "Research lead - verify before booking"
    )

    results = results.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return results


# ============================================================
# VERIFIED MODE
# ============================================================

def prepare_verified_results(df, customer):

    if df.empty:
        return df

    results = df.copy()

    # Only vendors explicitly marked Available are considered
    if "availability" in results.columns:

        results = results[
            results["availability"].astype(str).str.strip().str.lower()
            == "available"
        ].copy()

    else:
        return pd.DataFrame()

    if results.empty:
        return results

    # Verified pricing is required
    results = results[
        results.apply(
            lambda row: get_vendor_price(row)[0] is not None
            and get_vendor_price(row)[1] is not None,
            axis=1
        )
    ].copy()

    if results.empty:
        return results

    # Apply budget filter only when the customer entered a budget
    if customer["budget"] is not None:

        results = results[
            results.apply(
                lambda row: get_vendor_price(row)[0] <= customer["budget"],
                axis=1
            )
        ].copy()

    if results.empty:
        return results

    # Guest capacity must be known and sufficient
    if "guest_capacity" in results.columns:

        results["guest_capacity_numeric"] = pd.to_numeric(
            results["guest_capacity"],
            errors="coerce"
        )

        results = results[
            results["guest_capacity_numeric"].notna()
            & (
                results["guest_capacity_numeric"]
                >= customer["guests"]
            )
        ].copy()

    else:
        return pd.DataFrame()

    if results.empty:
        return results

    results["recommendation_score"] = results.apply(
        lambda row: calculate_final_score(
            row,
            customer["budget"],
            customer["location"],
            customer["event"]
        ),
        axis=1
    )

    results["recommendation_status"] = "Verified criteria matched"

    results = results.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return results


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(results, mode):

    print("\n========== RECOMMENDATION RESULTS ==========\n")

    if results.empty:
        print("No matching vendors found.")
        return

    for index, (_, row) in enumerate(results.iterrows(), start=1):

        print(f"\n{index}. {row.get('vendor_name', 'Unknown Vendor')}")

        print("Vendor ID:", row.get("vendor_id", "Not available"))
        print("Category:", row.get("main_category", "Not available"))
        print("Location:", row.get("location", "Not available"))

        minimum, maximum = get_vendor_price(row)

        if minimum is not None and maximum is not None:
            print(f"Price range: ₹{minimum:,.0f} - ₹{maximum:,.0f}")
        else:
            print("Price: Not confirmed")

        rating = get_vendor_rating(row)

        if rating is not None:
            print("Rating:", rating, "/ 5")
        else:
            print("Rating: Not verified")

        print(
            "Availability:",
            row.get("availability", "Unconfirmed")
        )

        print(
            "Recommendation score:",
            row.get("recommendation_score", 0),
            "/ 100"
        )

        print(
            "Status:",
            row.get(
                "recommendation_status",
                "Research lead - verify before booking"
            )
        )

        print("-" * 50)

    if mode == "2":
        print(
            "\nNote: These are research/demo recommendations. "
            "Vendor pricing, availability, ratings and capacity "
            "must be confirmed before booking."
        )


# ============================================================
# DATASET STATUS
# ============================================================

def show_dataset_status(df):

    print("\n========== DATASET STATUS ==========\n")

    print("Total vendors:", len(df))

    if df.empty:
        return

    if "availability" in df.columns:
        print("\nAvailability status:")
        print(df["availability"].value_counts(dropna=False).to_string())

    if "pricing_type" in df.columns:
        print("\nPricing type:")
        print(df["pricing_type"].value_counts(dropna=False).to_string())

    if "guest_capacity" in df.columns:
        missing_capacity = df["guest_capacity"].isna().sum()
        print("\nMissing guest capacity:", missing_capacity)

    if "verified_rating" in df.columns:
        missing_rating = df["verified_rating"].isna().sum()
        print("Missing verified ratings:", missing_rating)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    df = load_vendors()

    if df.empty:
        print("No vendor data available.")
        return

    show_dataset_status(df)

    customer = get_customer_input()

    print("\n========== FILTERING VENDORS ==========")

    category_df = filter_category(
        df,
        customer["category"]
    )

    print("After category filter:", len(category_df))

    location_df = filter_location(
        category_df,
        customer["location"]
    )

    print("After location filter:", len(location_df))

    if location_df.empty:
        print(
            "\nNo vendors found for this category and location."
        )
        return

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


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()