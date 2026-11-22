
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "reference"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Event Categories
event_categories = [
    "Wedding",
    "Birthday",
    "Corporate Event",
    "Engagement",
    "Baby Shower",
    "College Event",
    "Private Party",
    "Festival"
]

pd.DataFrame({
    "event_category": event_categories
}).to_csv(OUTPUT_DIR / "event_categories.csv", index=False)

# 2. Vendor Categories
vendor_categories = {
    "Decoration": [
        "Stage",
        "Balloon",
        "Floral",
        "Theme Decoration"
    ],
    "Photography": [
        "Wedding",
        "Candid",
        "Traditional",
        "Videography"
    ],
    "Catering": [
        "Veg",
        "Non-Veg",
        "Buffet",
        "Live Counters"
    ],
    "Venues": [
        "Banquet Halls",
        "Resorts",
        "Lawns"
    ],
    "Entertainment": [
        "DJs",
        "Singers",
        "Anchors",
        "Dance Groups"
    ],
    "Makeup": [
        "Bridal Makeup",
        "Hairstyling"
    ],
    "Event Planning": [
        "Wedding Planners",
        "Corporate Planners"
    ]
}

vendor_rows = []

for category, subcategories in vendor_categories.items():
    for subcategory in subcategories:
        vendor_rows.append({
            "main_category": category,
            "subcategory": subcategory
        })

pd.DataFrame(vendor_rows).to_csv(
    OUTPUT_DIR / "vendor_categories.csv",
    index=False
)

# 3. Decoration Subcategories
decoration_subcategories = [
    "Stage",
    "Balloon",
    "Floral",
    "Theme Decoration"
]

pd.DataFrame({
    "decoration_subcategory": decoration_subcategories
}).to_csv(
    OUTPUT_DIR / "decoration_subcategories.csv",
    index=False
)

print("Category datasets created successfully!")
print("Event categories:", len(event_categories))
print("Vendor category-subcategory records:", len(vendor_rows))
print("Decoration subcategories:", len(decoration_subcategories))
print("Saved inside:", OUTPUT_DIR)
