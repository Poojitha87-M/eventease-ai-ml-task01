
import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# 1. INITIALIZE RANDOM GENERATOR
# ==========================================

rng = np.random.default_rng(42)


# ==========================================
# 2. DEFINE VENDOR CATEGORIES
# ==========================================

categories = [
    "Catering",
    "Photography",
    "Decoration",
    "Event Planning",
    "Makeup",
    "Entertainment"
]


# ==========================================
# 3. DEFINE PILOT LOCATIONS
# ==========================================

locations = [
    "Mumbai",
    "Bangalore",
    "Pune",
    "Thane"
]


# ==========================================
# 4. DEFINE ALL 8 REQUIRED EVENT TYPES
# ==========================================

event_types = [
    "Wedding",
    "Birthday",
    "Corporate Event",
    "Engagement",
    "Baby Shower",
    "College Event",
    "Private Party",
    "Festival"
]


# ==========================================
# 5. DEFINE SYNTHETIC PRICE RANGES
# ==========================================

category_prices = {
    "Catering": (500, 1500, 25000, 100000),
    "Photography": (None, None, 10000, 60000),
    "Decoration": (None, None, 15000, 80000),
    "Event Planning": (None, None, 20000, 120000),
    "Makeup": (None, None, 3000, 25000),
    "Entertainment": (None, None, 8000, 50000)
}


# ==========================================
# 6. PREPARE VENDOR LOCATIONS
# ==========================================

# Each location receives 20 vendors.
vendor_locations = np.tile(locations, 15)

rng.shuffle(vendor_locations)




# ==========================================
# 7. GENERATE 60 SYNTHETIC VENDORS
# ==========================================

records = []

for i in range(60):

    # Select vendor category.
    category = categories[i % len(categories)]

    # Select location.
    location = vendor_locations[i]

    # Generate vendor ID.
    vendor_id = f"VND-{i + 1:03d}"

    # Generate clearly labelled synthetic vendor name.
    vendor_name = f"Synthetic {category} Vendor {i + 1:03d}"

    # Get category price ranges.
    plate_min_range, plate_max_range, event_min_range, event_max_range = (
        category_prices[category]
    )

    # Initialize pricing fields as blank.
    min_price_per_plate = None
    max_price_per_plate = None
    min_price_per_event = None
    max_price_per_event = None

    # Catering can use different pricing models.
    if category == "Catering":
        pricing_type = rng.choice(
            ["per_plate", "per_event", "both"]
        )
    else:
        pricing_type = "per_event"

    # Generate per-plate prices only when applicable.
    if pricing_type in ["per_plate", "both"]:

        min_price_per_plate = int(
            rng.integers(plate_min_range, plate_max_range)
        )

        max_price_per_plate = int(
            rng.integers(min_price_per_plate, plate_max_range + 1)
        )

    # Generate per-event prices only when applicable.
    if pricing_type in ["per_event", "both"]:

        min_price_per_event = int(
            rng.integers(event_min_range, event_max_range)
        )

        max_price_per_event = int(
            rng.integers(min_price_per_event, event_max_range + 1)
        )

    # Guarantee coverage of all 8 event types.
    # Each vendor gets one primary event type.
    primary_event = event_types[i % len(event_types)]

    # Add zero, one, or two additional event types.
    other_events = [
        event for event in event_types
        if event != primary_event
    ]

    extra_count = int(rng.integers(0, 3))

    if extra_count > 0:
        additional_events = rng.choice(
            other_events,
            size=extra_count,
            replace=False
        ).tolist()
    else:
        additional_events = []

    selected_events = [primary_event] + additional_events

    # Create vendor record.
    records.append({

        "vendor_id": vendor_id,

        "vendor_name": vendor_name,

        "category": category,

        "location": location,

        "min_price_per_plate": min_price_per_plate,

        "max_price_per_plate": max_price_per_plate,

        "min_price_per_event": min_price_per_event,

        "max_price_per_event": max_price_per_event,

        "pricing_type": pricing_type,

        "rating": round(
            float(rng.uniform(3.0, 5.0)), 1
        ),

        "availability": rng.choice(
            ["Available", "Unavailable"],
            p=[0.75, 0.25]
        ),

        "event_type": "|".join(selected_events),

        "review_count": int(
            rng.integers(5, 501)
        ),

        "is_synthetic": True
    })


# ==========================================
# 8. CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(records)


# ==========================================
# 9. SAVE DATASET
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

output_path = (
    PROJECT_ROOT / "data" / "raw" / "vendors.csv"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)


# ==========================================
# 10. DISPLAY DATASET SUMMARY
# ==========================================

print("\nSynthetic vendor dataset generated successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nVendor categories:")
print(df["category"].value_counts())

print("\nLocation distribution:")
print(df["location"].value_counts())

print("\nPricing types:")
print(df["pricing_type"].value_counts())

print("\nEvent type coverage:")

found_events = set()

for events in df["event_type"]:
    found_events.update(events.split("|"))

for event in event_types:
    count = df["event_type"].apply(
        lambda value: event in value.split("|")
    ).sum()

    print(f"{event}: {count} vendors")

print("\nTotal required event types:", len(found_events))

print("\nAll records synthetic:")
print(df["is_synthetic"].all())

print("\nSaved file:")
print(output_path)
