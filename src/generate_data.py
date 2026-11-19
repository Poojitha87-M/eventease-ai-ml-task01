
import pandas as pd
import numpy as np
from pathlib import Path

rng = np.random.default_rng(42)

# ==========================================
# 1. DEFINE CATEGORIES AND LOCATIONS
# ==========================================

categories = [
    "Catering",
    "Photography",
    "Decoration",
    "Event Planning",
    "Makeup Artist",
    "Entertainment"
]

locations = ["CBD Belapur", "Vashi", "Nerul"]

event_types = [
    "Birthday",
    "Wedding",
    "Engagement",
    "Anniversary",
    "Corporate Event",
    "Baby Shower"
]


# ==========================================
# 2. DEFINE SYNTHETIC PRICE RANGES
# ==========================================

category_prices = {
    "Catering": (500, 1500, 25000, 100000),
    "Photography": (None, None, 10000, 60000),
    "Decoration": (None, None, 15000, 80000),
    "Event Planning": (None, None, 20000, 120000),
    "Makeup Artist": (None, None, 3000, 25000),
    "Entertainment": (None, None, 8000, 50000)
}


# ==========================================
# 3. PREPARE VENDOR LOCATIONS
# ==========================================

# Each category has 10 vendors.
# Distribute them across all 3 locations.

vendor_locations = np.tile(
    locations,
    20
)

# Shuffle locations so categories are not grouped
# by a fixed location pattern.
rng.shuffle(vendor_locations)


# ==========================================
# 4. GENERATE 60 SYNTHETIC VENDORS
# ==========================================

records = []

for i in range(60):

    category = categories[i % len(categories)]
    location = vendor_locations[i]

    vendor_id = f"VND-{i + 1:03d}"
    vendor_name = f"Synthetic {category} Vendor {i + 1:03d}"

    p_min, p_max, e_min, e_max = category_prices[category]

    plate_min = None
    plate_max = None
    event_min = None
    event_max = None

    # Catering supports all three pricing models.
    if category == "Catering":
        pricing_type = rng.choice(
            ["per_plate", "per_event", "both"]
        )
    else:
        pricing_type = "per_event"

    # Generate per-plate prices where applicable.
    if pricing_type in ["per_plate", "both"]:

        plate_min = int(rng.integers(p_min, p_max))
        plate_max = int(rng.integers(plate_min, p_max + 1))

    # Generate per-event prices where applicable.
    if pricing_type in ["per_event", "both"]:

        event_min = int(rng.integers(e_min, e_max))
        event_max = int(rng.integers(event_min, e_max + 1))

    selected_events = rng.choice(
        event_types,
        size=int(rng.integers(1, 4)),
        replace=False
    )

    records.append({
        "vendor_id": vendor_id,
        "vendor_name": vendor_name,
        "category": category,
        "location": location,
        "min_price_per_plate": plate_min,
        "max_price_per_plate": plate_max,
        "min_price_per_event": event_min,
        "max_price_per_event": event_max,
        "pricing_type": pricing_type,
        "rating": round(float(rng.uniform(3.0, 5.0)), 1),
        "availability": rng.choice(
            ["Available", "Unavailable"],
            p=[0.75, 0.25]
        ),
        "event_type": "|".join(selected_events),
        "review_count": int(rng.integers(5, 501)),
        "is_synthetic": True
    })


# ==========================================
# 5. CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(records)


# ==========================================
# 6. SAVE RAW DATASET
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

output_path = PROJECT_ROOT / "data" / "raw" / "vendors.csv"

output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)


# ==========================================
# 7. DISPLAY DATASET SUMMARY
# ==========================================

print("Dataset generated successfully!")

print("Total records:", len(df))
print("Total columns:", len(df.columns))

print("\nCategory counts:")
print(df["category"].value_counts())

print("\nLocation counts:")
print(df["location"].value_counts())

print("\nCategory-wise location distribution:")
print(pd.crosstab(df["category"], df["location"]))

print("\nPricing type counts:")
print(df["pricing_type"].value_counts())

print("\nAll records are synthetic:", df["is_synthetic"].all())
