
import json
import pandas as pd

try:
    from .recommendation import (
        load_vendors,
        normalize_category,
        normalize_location,
        normalize_event,
        filter_category,
        filter_location,
        prepare_demo_results,
        prepare_verified_results,
        get_vendor_price,
        get_vendor_rating,
        calculate_relevance_score
    )
except ImportError:
    from recommendation import (
        load_vendors,
        normalize_category,
        normalize_location,
        normalize_event,
        filter_category,
        filter_location,
        prepare_demo_results,
        prepare_verified_results,
        get_vendor_price,
        get_vendor_rating,
        calculate_relevance_score
    )


def safe_value(value):
    """Convert Pandas and NumPy values into JSON-compatible values."""

    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if hasattr(value, "item"):
        value = value.item()

    return value


def generate_reasons(row, customer):
    """Generate short explanations for a recommendation."""

    reasons = []

    vendor_location = normalize_location(row.get("location"))

    if vendor_location == customer["location"]:
        reasons.append("Vendor location matches the requested location.")

    relevance = calculate_relevance_score(
        row,
        customer["event"]
    )

    if relevance == 100:
        reasons.append("Vendor supports the selected event type.")
    elif relevance > 0:
        reasons.append("Vendor has partial event-type relevance.")

    minimum, maximum = get_vendor_price(row)

    if customer["budget"] is None:
        reasons.append("No budget limit was provided.")

    elif minimum is not None and maximum is not None:
        if customer["budget"] >= minimum:
            reasons.append("Available price range was considered against the budget.")
        else:
            reasons.append("Vendor minimum price exceeds the entered budget.")

    rating = get_vendor_rating(row)

    if rating is not None:
        reasons.append(f"Available listed or verified rating: {rating}/5.")
    else:
        reasons.append("Rating is not confirmed.")

    if not reasons:
        reasons.append("Recommendation score calculated from available information.")

    return reasons


def get_recommendations(request):
    """
    API-style recommendation function.

    Required request fields:
        category, location, event, guests

    Optional request fields:
        budget, mode

    mode:
        research / demo / 2
        verified / 1
    """

    # -----------------------------
    # Validate customer input
    # -----------------------------

    if not isinstance(request, dict):
        return {
            "success": False,
            "message": "Request must be a dictionary.",
            "count": 0,
            "recommendations": []
        }

    category = normalize_category(request.get("category", ""))

    location = normalize_location(request.get("location", ""))

    event = normalize_event(request.get("event", ""))

    if not category:
        return {
            "success": False,
            "message": "Invalid vendor category.",
            "count": 0,
            "recommendations": []
        }

    if not location:
        return {
            "success": False,
            "message": "Invalid location. Choose Thane, Pune or Bangalore.",
            "count": 0,
            "recommendations": []
        }

    valid_events = [
        "Wedding",
        "Birthday",
        "Corporate Event",
        "Engagement",
        "Baby Shower",
        "College Event",
        "Private Party",
        "Festival"
    ]

    if event not in valid_events:
        return {
            "success": False,
            "message": "Invalid event type.",
            "count": 0,
            "recommendations": []
        }

    try:
        guests = int(request.get("guests"))

        if guests <= 0:
            raise ValueError

    except (TypeError, ValueError):
        return {
            "success": False,
            "message": "Guests must be a positive whole number.",
            "count": 0,
            "recommendations": []
        }

    budget = request.get("budget")

    if budget in ("", None):
        budget = None
    else:
        try:
            budget = float(budget)

            if budget <= 0:
                raise ValueError

        except (TypeError, ValueError):
            return {
                "success": False,
                "message": "Budget must be a positive number or null.",
                "count": 0,
                "recommendations": []
            }

    mode_input = str(request.get("mode", "research")).strip().lower()

    if mode_input in ("1", "verified"):
        mode = "verified"
    elif mode_input in ("2", "research", "demo", "research/demo"):
        mode = "research"
    else:
        return {
            "success": False,
            "message": "Mode must be research or verified.",
            "count": 0,
            "recommendations": []
        }

    customer = {
        "category": category,
        "location": location,
        "event": event,
        "budget": budget,
        "guests": guests
    }

    # -----------------------------
    # Load vendor dataset
    # -----------------------------

    df = load_vendors()

    if df.empty:
        return {
            "success": False,
            "message": "Vendor dataset is empty or unavailable.",
            "count": 0,
            "criteria": customer,
            "recommendations": []
        }

    # -----------------------------
    # Filter vendors
    # -----------------------------

    results = filter_category(df, category)
    results = filter_location(results, location)

    # -----------------------------
    # Generate recommendations
    # -----------------------------

    if mode == "verified":
        results = prepare_verified_results(results, customer)
    else:
        results = prepare_demo_results(results, customer)

    # -----------------------------
    # Build API response
    # -----------------------------

    recommendations = []

    for rank, (_, row) in enumerate(results.iterrows(), start=1):

        minimum, maximum = get_vendor_price(row)

        rating = get_vendor_rating(row)

        vendor = {
            "rank": rank,
            "vendor_id": safe_value(row.get("vendor_id")),
            "vendor_name": safe_value(row.get("vendor_name")),
            "category": safe_value(row.get("main_category")),
            "subcategory": safe_value(row.get("subcategory")),
            "location": safe_value(row.get("location")),
            "minimum_price": minimum,
            "maximum_price": maximum,
            "rating": rating,
            "availability": safe_value(row.get("availability")),
            "recommendation_score": round(
                float(row.get("recommendation_score", 0)), 2
            ),
            "status": safe_value(
                row.get("recommendation_status")
            ),
            "reasons": generate_reasons(row, customer)
        }

        recommendations.append(vendor)

    message = (
        "Recommendations generated successfully."
        if recommendations
        else "No matching vendors found for the given criteria."
    )

    return {
        "success": True,
        "message": message,
        "mode": mode,
        "count": len(recommendations),
        "criteria": customer,
        "recommendations": recommendations
    }


def get_recommendations_json(request):
    """Return the API response as formatted JSON text."""

    response = get_recommendations(request)

    return json.dumps(
        response,
        indent=4,
        ensure_ascii=False,
        default=str
    )


# -----------------------------
# SAMPLE API TEST
# -----------------------------

if __name__ == "__main__":

    sample_request = {
        "category": "Makeup",
        "location": "Pune",
        "event": "Festival",
        "budget": 30000,
        "guests": 76,
        "mode": "research"
    }

    print("\nEVENTEASE API RESPONSE")
    print("======================")

    print(get_recommendations_json(sample_request))
