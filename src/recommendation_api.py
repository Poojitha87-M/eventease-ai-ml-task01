import json
import math

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from .recommendation import (
        load_vendors,
        normalize_category,
        normalize_location,
        normalize_event,
        filter_category,
        filter_location,
        filter_event,
        prepare_demo_results,
        prepare_verified_results,
        get_vendor_price,
        get_vendor_rating,
        calculate_relevance_score,
    )
except ImportError:
    from recommendation import (
        load_vendors,
        normalize_category,
        normalize_location,
        normalize_event,
        filter_category,
        filter_location,
        filter_event,
        prepare_demo_results,
        prepare_verified_results,
        get_vendor_price,
        get_vendor_rating,
        calculate_relevance_score,
    )


app = FastAPI(
    title="EventEase Vendor Recommendation API",
    description="Rule-based vendor discovery and recommendation prototype.",
    version="1.0.0",
)


class RecommendationRequest(BaseModel):
    category: str
    location: str
    event: str
    guests: int = Field(gt=0)
    budget: float | None = Field(default=None, gt=0)
    mode: str = "research"


def safe_value(value):
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, float) and not math.isfinite(value):
        return None

    return value


def generate_reasons(row, customer):
    reasons = []

    if normalize_location(row.get("location")) == normalize_location(
        customer["location"]
    ):
        reasons.append(
            "Vendor location matches the requested location."
        )

    relevance = calculate_relevance_score(
        row, customer["event"]
    )

    if relevance == 100:
        reasons.append(
            "Vendor's listed event information matches the selected event."
        )

    price_range = get_vendor_price(
        row, customer["guests"]
    )

    if price_range is not None:
        reasons.append(
            "Listed price information is available for the requested guest count."
        )
    else:
        reasons.append(
            "Price information is not confirmed."
        )

    rating = get_vendor_rating(row)

    if rating is not None:
        reasons.append(
            f"Available listed rating: {rating}/5."
        )
    else:
        reasons.append(
            "Rating information is not confirmed."
        )

    availability = str(
        row.get("availability", "Unconfirmed")
    )

    if availability.strip().lower() == "available":
        reasons.append(
            "Availability is listed as Available."
        )
    else:
        reasons.append(
            "Availability is not confirmed; contact the vendor."
        )

    return reasons


def get_recommendations(request):

    if not isinstance(request, dict):
        return {
            "success": False,
            "message": "Request must be a JSON object.",
            "recommendations": [],
        }

    # Normalize customer inputs
    category = normalize_category(
        request.get("category", "")
    )

    location = normalize_location(
        request.get("location", "")
    )

    event = normalize_event(
        request.get("event", "")
    )

    # Validate guest count
    try:
        guests = int(request.get("guests", 0))
    except (TypeError, ValueError, OverflowError):
        guests = 0

    # Validate budget
    budget_value = request.get("budget")

    try:
        budget = (
            None
            if budget_value in (None, "")
            else float(
                str(budget_value)
                .replace(",", "")
                .replace("\u20b9", "")
                .strip()
            )
        )
    except (TypeError, ValueError, OverflowError):
        budget = None

        if budget_value not in (None, ""):
            budget = float("nan")

    # Validate recommendation mode
    mode = str(
        request.get("mode", "research")
    ).strip().lower()

    # Input validation
    if not category:
        return {
            "success": False,
            "message": "Invalid or missing category.",
            "recommendations": [],
        }

    if not location:
        return {
            "success": False,
            "message": "Location is required.",
            "recommendations": [],
        }

    if not event:
        return {
            "success": False,
            "message": "Invalid or missing event type.",
            "recommendations": [],
        }

    if guests <= 0:
        return {
            "success": False,
            "message": "Guests must be a positive integer.",
            "recommendations": [],
        }

    # Reject zero, negative, NaN, and infinite budgets
    if budget is not None and (
        not math.isfinite(budget) or budget <= 0
    ):
        return {
            "success": False,
            "message": "Budget must be a positive number when supplied.",
            "recommendations": [],
        }

    if mode not in {"research", "verified"}:
        return {
            "success": False,
            "message": "Mode must be research or verified.",
            "recommendations": [],
        }

    customer = {
        "category": category,
        "location": location,
        "event": event,
        "guests": guests,
        "budget": budget,
        "mode": mode,
    }

    # Load and filter vendor data
    try:
        vendors = load_vendors()

        filtered = filter_category(
            vendors, category
        )

        filtered = filter_location(
            filtered, location
        )

        filtered = filter_event(
            filtered, event
        )

        if mode == "verified":
            results = prepare_verified_results(
                filtered, customer
            )
        else:
            results = prepare_demo_results(
                filtered, customer
            )

    except Exception as error:
        return {
            "success": False,
            "message": f"Could not process vendor data: {error}",
            "recommendations": [],
        }

    # Build recommendations
    recommendations = []

    for rank, (_, row) in enumerate(
        results.iterrows(), start=1
    ):

        price_range = get_vendor_price(
            row, guests
        )

        rating = get_vendor_rating(row)

        pricing_type = (
            str(row.get("pricing_type", ""))
            .strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        event_min = pd.to_numeric(
            row.get("min_price_per_event"),
            errors="coerce",
        )

        event_max = pd.to_numeric(
            row.get("max_price_per_event"),
            errors="coerce",
        )

        has_event_price = (
            pd.notna(event_min)
            and pd.notna(event_max)
        )

        # Identify the actual pricing basis
        if price_range is None:
            price_basis = "not_confirmed"

        elif pricing_type == "per_event":
            price_basis = "listed_event_price"

        elif pricing_type == "both" and has_event_price:
            price_basis = "listed_event_price"

        elif pricing_type in {"per_plate", "both"}:
            price_basis = (
                "estimated_total_for_requested_guests"
            )

        elif has_event_price:
            price_basis = "listed_event_price"

        else:
            price_basis = (
                "estimated_total_for_requested_guests"
            )

        recommendations.append({
            "rank": rank,

            "vendor_id": safe_value(
                row.get("vendor_id")
            ),

            "vendor_name": safe_value(
                row.get("vendor_name")
            ),

            "category": safe_value(
                row.get("main_category")
            ),

            "subcategory": safe_value(
                row.get("subcategory")
            ),

            "location": safe_value(
                row.get("location")
            ),

            "minimum_price": (
                safe_value(price_range[0])
                if price_range is not None
                else None
            ),

            "maximum_price": (
                safe_value(price_range[1])
                if price_range is not None
                else None
            ),

            "price_basis": price_basis,

            "rating": safe_value(rating),

            "rating_type": (
                "listed_or_recorded_rating"
                if rating is not None
                else "not_confirmed"
            ),

            "availability": safe_value(
                row.get("availability")
            ),

            "recommendation_score": safe_value(
                row.get("recommendation_score")
            ),

            "status": safe_value(
                row.get("recommendation_status")
            ),

            "reasons": generate_reasons(
                row, customer
            ),
        })

    # Response message
    if mode == "verified" and not recommendations:

        message = (
            "No vendors currently meet all Verified Mode requirements. "
            "Availability, usable pricing, and guest capacity must be confirmed."
        )

    elif not recommendations:

        message = (
            "No research leads matched the selected category, location, and event. "
            "Try different criteria."
        )

    else:

        message = (
            "Recommendations generated. "
            "Research leads must be verified before booking."
        )

    return {
        "success": True,
        "message": message,
        "mode": mode,
        "count": len(recommendations),

        "criteria": {
            "category": category,
            "location": location,
            "event": event,
            "guests": guests,
            "budget": budget,
        },

        "recommendations": recommendations,
    }


def get_recommendations_json(request):
    return json.dumps(
        get_recommendations(request),
        indent=4,
        ensure_ascii=False,
        default=str,
    )


@app.get("/")
def home():
    return {
        "message": "EventEase Vendor Recommendation API is running.",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "EventEase Recommendation API",
    }


@app.post("/recommendations")
def recommendations_endpoint(
    request: RecommendationRequest
):

    result = get_recommendations(
        request.dict()
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get("message"),
        )

    return result


if __name__ == "__main__":

    sample_request = {
        "category": "Makeup",
        "location": "Pune",
        "event": "Wedding",
        "budget": 30000,
        "guests": 76,
        "mode": "research",
    }

    print(
        get_recommendations_json(sample_request)
    )