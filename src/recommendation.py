
import ast
import re
from pathlib import Path

import pandas as pd


# Resolve the CSV path from the project root, even when this file is run
# from a different working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "clean" / "vendors_researched_final.csv"

WEIGHTS = {
    "budget": 0.35,
    "location": 0.30,
    "rating": 0.25,
    "relevance": 0.10,
}

CATEGORIES = [
    "Catering",
    "Photography",
    "Decoration",
    "Event Planning",
    "Makeup",
    "Entertainment",
]

LOCATIONS = {
    "Mumbai, Maharashtra": ["mumbai"],
    "Thane, Maharashtra": ["thane"],
    "Pune, Maharashtra": ["pune"],
    "Bangalore, Karnataka": ["bangalore", "bengaluru"],
}

EVENT_ALIASES = {
    "Wedding": ["wedding", "weddings", "marriage", "marriages"],
    "Birthday": ["birthday", "birthdays", "birthday party", "birthday parties"],
    "Corporate Event": [
        "corporate event", "corporate events", "corporate",
        "business event", "business events",
    ],
    "Engagement": ["engagement", "engagements"],
    "Baby Shower": ["baby shower", "baby showers"],
    "College Event": [
        "college event", "college events", "college function",
        "college functions", "campus event", "campus events",
    ],
    "Private Party": ["private party", "private parties"],
    "Festival": ["festival", "festivals", "festive event", "festive events"],
}


def clean_text(value):
    if value is None or pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip()).lower()


def normalize_category(category):
    value = clean_text(category)
    for item in CATEGORIES:
        if value == item.lower():
            return item
    return None


def normalize_location(location):
    value = clean_text(location)
    for canonical, aliases in LOCATIONS.items():
        if value == canonical.lower() or value in aliases:
            return canonical
    return value.title() if value else ""


def normalize_event(event):
    value = clean_text(event)
    for canonical, aliases in EVENT_ALIASES.items():
        if value == canonical.lower() or value in aliases:
            return canonical
    return None


def load_vendors():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Vendor dataset not found: {DATA_PATH}\n"
            "Check that data/clean/vendors_researched_final.csv exists."
        )

    df = pd.read_csv(DATA_PATH)
    df.columns = [str(column).strip() for column in df.columns]

    if "location" not in df.columns:
        raise ValueError("Dataset is missing the required 'location' column.")

    if "main_category" not in df.columns:
        raise ValueError("Dataset is missing the required 'main_category' column.")

    df["normalized_location"] = df["location"].apply(normalize_location)
    df["normalized_category"] = df["main_category"].apply(normalize_category)
    return df


def get_customer_input():
    print("\n--- EventEase Vendor Recommendation ---")

    print("\nCategories:")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")
    category = input("Enter category: ").strip()

    print("\nLocations:")
    for location in LOCATIONS:
        print(f"- {location}")
    location = input("Enter location: ").strip()

    print("\nEvents:")
    for event in EVENT_ALIASES:
        print(f"- {event}")
    event = input("Enter event type: ").strip()

    budget_text = input("Enter total budget (or press Enter to skip): ").strip()
    guests_text = input("Enter number of guests: ").strip()
    mode = input("Mode (research/verified): ").strip().lower() or "research"

    budget = float(budget_text.replace(",", "").replace("₹", "")) if budget_text else None
    guests = int(guests_text)

    return {
        "category": category,
        "location": location,
        "event": event,
        "budget": budget,
        "guests": guests,
        "mode": mode,
    }


def get_event_values(value):
    """Convert a dataset event field into a list of recognizable event names."""
    if value is None or pd.isna(value):
        return []

    if isinstance(value, (list, tuple, set)):
        raw_values = list(value)
    else:
        text = str(value).strip()
        if not text:
            return []

        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, (list, tuple, set)):
                raw_values = list(parsed)
            else:
                raw_values = re.split(r"[,;|]", text)
        except (ValueError, SyntaxError):
            raw_values = re.split(r"[,;|]", text)

    recognized = set()

    for item in raw_values:
        item_text = clean_text(item)
        if not item_text:
            continue

        # Match known event names inside descriptive phrases such as
        # "Weddings and traditional functions".
        for canonical, aliases in EVENT_ALIASES.items():
            candidates = [canonical.lower()] + aliases
            if any(
                re.search(r"(?<![a-z])" + re.escape(alias) + r"(?![a-z])", item_text)
                for alias in candidates
            ):
                recognized.add(canonical)

    return sorted(recognized)


def calculate_relevance_score(row, selected_event):
    selected = normalize_event(selected_event)
    if not selected:
        return 0

    possible_columns = [
        "event_types",
        "event_categories",
        "events_supported",
        "event_type",
        "events",
    ]

    supported_events = set()
    for column in possible_columns:
        if column in row.index:
            supported_events.update(get_event_values(row[column]))

    # Unknown event information is not treated as proof of support.
    return 100 if selected in supported_events else 0


def get_numeric_price(value):
    if value is None or pd.isna(value):
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.replace(",", "").replace("₹", "").replace("INR", "").strip()
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None

    try:
        number = float(match.group())
        return number if number >= 0 else None
    except ValueError:
        return None


def _get_range(row, minimum_column, maximum_column):
    minimum = get_numeric_price(row.get(minimum_column))
    maximum = get_numeric_price(row.get(maximum_column))

    if minimum is None or maximum is None or maximum < minimum:
        return None

    return minimum, maximum


def get_vendor_price(row, guests=None):
    """
    Return the estimated total-cost range for the requested guest count.

    Explicit per-plate/per-event columns take priority. Generic min_price and
    max_price are used only when pricing_type clearly identifies their basis.
    For pricing_type='both', an explicit per-event range is preferred;
    otherwise an explicit per-plate range is used.
    """
    pricing_type = clean_text(row.get("pricing_type")).replace("-", "_").replace(" ", "_")

    per_plate = (
        _get_range(row, "min_price_per_plate", "max_price_per_plate")
        or (_get_range(row, "min_price", "max_price")
            if pricing_type in {"per_plate", "both"} else None)
    )

    per_event = (
        _get_range(row, "min_price_per_event", "max_price_per_event")
        or (_get_range(row, "min_price", "max_price")
            if pricing_type == "per_event" else None)
    )

    if pricing_type == "per_plate":
        chosen_range = per_plate
        if chosen_range is None or guests is None:
            return None
        return chosen_range[0] * guests, chosen_range[1] * guests

    if pricing_type == "per_event":
        return per_event

    if pricing_type == "both":
        # Prefer event pricing because it is already a total-event amount.
        if per_event is not None:
            return per_event
        if per_plate is not None and guests is not None:
            return per_plate[0] * guests, per_plate[1] * guests
        return None

    # If the pricing model is unknown, do not guess how the price is charged.
    if _get_range(row, "min_price_per_event", "max_price_per_event") is not None:
        return _get_range(row, "min_price_per_event", "max_price_per_event")

    if (
        _get_range(row, "min_price_per_plate", "max_price_per_plate") is not None
        and guests is not None
    ):
        low, high = _get_range(row, "min_price_per_plate", "max_price_per_plate")
        return low * guests, high * guests

    return None


def calculate_budget_score(row, budget, guests=None):
    if budget is None:
        return None

    price_range = get_vendor_price(row, guests)
    if price_range is None:
        return None

    minimum, maximum = price_range

    if budget < minimum:
        return 0.0
    if budget >= maximum:
        return 100.0
    if maximum == minimum:
        return 100.0

    return ((budget - minimum) / (maximum - minimum)) * 100.0


def get_vendor_rating(row):
    # Listed/public ratings are not described as independently verified.
    for column in ["verified_rating", "rating_listed", "rating"]:
        if column not in row.index:
            continue
        value = get_numeric_price(row[column])
        if value is not None and 0 <= value <= 5:
            return value
    return None


def calculate_rating_score(row):
    rating = get_vendor_rating(row)
    return None if rating is None else (rating / 5.0) * 100.0


def calculate_location_score(row, selected_location):
    vendor_location = normalize_location(row.get("location"))
    requested_location = normalize_location(selected_location)
    return 100.0 if vendor_location == requested_location else 0.0


def calculate_final_score(row, customer):
    guests = customer.get("guests")
    budget_score = calculate_budget_score(row, customer.get("budget"), guests)
    location_score = calculate_location_score(row, customer["location"])
    rating_score = calculate_rating_score(row)
    relevance_score = calculate_relevance_score(row, customer["event"])

    scores = {
        "budget": budget_score,
        "location": location_score,
        "rating": rating_score,
        "relevance": relevance_score,
    }

    available_weight = sum(
        WEIGHTS[key] for key, value in scores.items() if value is not None
    )
    if available_weight == 0:
        return 0.0

    total = sum(
        value * WEIGHTS[key]
        for key, value in scores.items()
        if value is not None
    )
    return round(total / available_weight, 2)


def filter_category(df, category):
    normalized = normalize_category(category)
    if not normalized:
        return df.iloc[0:0].copy()
    return df[df["normalized_category"] == normalized].copy()


def filter_location(df, location):
    normalized = normalize_location(location)
    return df[df["normalized_location"] == normalized].copy()


def filter_event(df, event):
    return df[
        df.apply(lambda row: calculate_relevance_score(row, event) > 0, axis=1)
    ].copy()


def prepare_demo_results(df, customer):
    results = df.copy()
    results["recommendation_score"] = results.apply(
        lambda row: calculate_final_score(row, customer), axis=1
    )
    results["recommendation_status"] = "Research lead - verify before booking"
    return results.sort_values("recommendation_score", ascending=False)


def prepare_verified_results(df, customer):
    results = df.copy()

    if "availability" not in results.columns:
        return results.iloc[0:0].copy()

    results = results[
        results["availability"].apply(clean_text) == "available"
    ].copy()

    # Verified mode requires a usable price range for this guest count.
    results = results[
        results.apply(
            lambda row: get_vendor_price(row, customer.get("guests")) is not None,
            axis=1,
        )
    ].copy()

    budget = customer.get("budget")
    if budget is not None:
        results = results[
            results.apply(
                lambda row: get_vendor_price(row, customer.get("guests"))[0] <= budget,
                axis=1,
            )
        ].copy()

    if "guest_capacity" not in results.columns:
        return results.iloc[0:0].copy()

    results["_capacity"] = pd.to_numeric(
        results["guest_capacity"], errors="coerce"
    )
    results = results[
        results["_capacity"].notna()
        & (results["_capacity"] >= int(customer["guests"]))
    ].copy()
    results.drop(columns=["_capacity"], inplace=True)

    results["recommendation_score"] = results.apply(
        lambda row: calculate_final_score(row, customer), axis=1
    )
    results["recommendation_status"] = "Verified criteria matched"
    return results.sort_values("recommendation_score", ascending=False)


def display_results(results, customer):
    if results.empty:
        print("\nNo vendors match all the selected criteria.")
        print("Try another event, location, category, or mode.")
        return

    print(f"\nFound {len(results)} matching vendor(s):\n")

    for rank, (_, row) in enumerate(results.iterrows(), start=1):
        price_range = get_vendor_price(row, customer.get("guests"))
        rating = get_vendor_rating(row)

        print(f"{rank}. {row.get('vendor_name', 'Unknown vendor')}")
        print(f"   Category: {row.get('main_category', 'Not listed')}")
        print(f"   Location: {row.get('location', 'Not listed')}")

        if price_range is None:
            print("   Estimated total price: Not confirmed")
        else:
            print(
                f"   Estimated total price: ₹{price_range[0]:,.0f}"
                f" - ₹{price_range[1]:,.0f}"
            )

        print(f"   Listed rating: {rating}/5" if rating is not None
              else "   Rating: Not confirmed")
        print(f"   Availability: {row.get('availability', 'Unconfirmed')}")
        print(f"   Score: {row.get('recommendation_score', 0)}")
        print(f"   Status: {row.get('recommendation_status', '')}\n")


def show_dataset_status(df):
    print("\n--- Dataset Status ---")
    print(f"Total vendors: {len(df)}")

    if "availability" in df.columns:
        print("Availability counts:")
        print(df["availability"].fillna("Missing").value_counts().to_string())

    for column in ["min_price", "max_price", "guest_capacity", "rating_listed"]:
        if column in df.columns:
            missing = df[column].isna().sum()
            print(f"{column} missing: {missing}/{len(df)}")


def main():
    try:
        vendors = load_vendors()
        show_dataset_status(vendors)
        customer = get_customer_input()

        category = normalize_category(customer["category"])
        event = normalize_event(customer["event"])
        if not category:
            print("Invalid category. Please enter one of the listed categories.")
            return
        if not event:
            print("Invalid event type. Please enter one of the listed event types.")
            return
        if customer["guests"] <= 0:
            print("Guest count must be greater than zero.")
            return
        if customer["budget"] is not None and customer["budget"] <= 0:
            print("Budget must be greater than zero.")
            return
        if customer["mode"] not in {"research", "verified"}:
            print("Mode must be research or verified.")
            return

        customer["category"] = category
        customer["event"] = event
        customer["location"] = normalize_location(customer["location"])

        filtered = filter_category(vendors, category)
        filtered = filter_location(filtered, customer["location"])
        # Event filtering is now applied in the main recommendation flow.
        filtered = filter_event(filtered, event)

        if customer["mode"] == "verified":
            results = prepare_verified_results(filtered, customer)
        else:
            results = prepare_demo_results(filtered, customer)

        display_results(results, customer)

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
