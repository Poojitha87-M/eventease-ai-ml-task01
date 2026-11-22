
import pandas as pd

# Load cleaned vendor dataset
file_path = "data/clean/vendors_clean.csv"
df = pd.read_csv(file_path)

# Subcategory options for each vendor category
subcategory_map = {
    "Catering": ["Veg", "Non-Veg", "Buffet", "Live Counters"],
    "Photography": ["Wedding", "Candid", "Traditional", "Videography"],
    "Decoration": ["Stage", "Balloon", "Floral", "Theme Decoration"],
    "Entertainment": ["DJs", "Singers", "Anchors", "Dance Groups"],
    "Makeup": ["Bridal Makeup", "Hairstyling"],
    "Event Planning": ["Wedding Planners", "Corporate Planners"]
}

# Add subcategory to each synthetic sample record
df["subcategory"] = df.groupby("category").cumcount().map(
    lambda index: index
)

df["subcategory"] = df.apply(
    lambda row: subcategory_map[row["category"]][
        int(row["subcategory"]) % len(subcategory_map[row["category"]])
    ],
    axis=1
)

# Add clearly labelled sample descriptions and services
df["description"] = df.apply(
    lambda row: (
        f"Synthetic sample description for {row['subcategory']} "
        f"under {row['category']}."
    ),
    axis=1
)

df["services_offered"] = df["subcategory"].apply(
    lambda value: f"Synthetic sample service: {value}"
)

# No verified public contact information is available
df["contact_information"] = pd.NA

# Save updated dataset
df.to_csv(file_path, index=False)

print("Updated vendor dataset:", df.shape)
print("Columns:", df.columns.tolist())
print("Missing contact information:", df["contact_information"].isna().sum())
print("\nSubcategory distribution:")
print(df["subcategory"].value_counts())
