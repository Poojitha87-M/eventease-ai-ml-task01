
import pandas as pd
from pathlib import Path
file_path = Path("data/research/vendor_verification_tracker.csv")
df = pd.read_csv(file_path)


print("RESEARCH VENDOR DATA VALIDATION")
print("=" * 40)

# Required columns
required_columns = [
    "vendor_id", "vendor_name", "main_category",
    "location", "pricing_type", "rating_listed",
    "availability", "verification_status", "source_url"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

print("Missing required columns:", missing_columns)

# Duplicate checks
print("Duplicate vendor IDs:", df["vendor_id"].duplicated().sum())
print(
    "Duplicate vendor names in same location:",
    df.duplicated(subset=["vendor_name", "location"]).sum()
)

# Rating validation
ratings = pd.to_numeric(df["rating_listed"], errors="coerce")
invalid_ratings = ratings.notna() & ~ratings.between(0, 5)

print("Invalid ratings:", invalid_ratings.sum())

# Location validation
expected_locations = {
    "Thane, Maharashtra",
    "Pune, Maharashtra",
    "Bangalore, Karnataka"
}

unexpected_locations = set(df["location"].dropna()) - expected_locations
print("Unexpected locations:", unexpected_locations)

# Synthetic record check
print("Synthetic records:", df["is_synthetic"].sum())

# Research status
print("\nVerification status:")
print(df["verification_status"].value_counts().to_string())

# Missing information report
print("\nMissing values:")
print(df.isnull().sum().to_string())

print("\nTotal records:", len(df))
print("Validation checks completed.")
