
import pandas as pd
from pathlib import Path

file_path = Path("data/research/vendor_verification_tracker.csv")
df = pd.read_csv(file_path)

print("EVENTEASE - VENDOR TRACKER VALIDATION")
print("=" * 45)

# Required tracker columns
required_columns = [
    "vendor_id",
    "vendor_name",
    "main_category",
    "location",
    "source_url",
    "verification_status",
    "direct_source_url",
    "verified_rating",
    "verified_contact",
    "verification_notes"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

print("Missing required columns:", missing_columns)

# Duplicate checks
print("Duplicate vendor IDs:", df["vendor_id"].duplicated().sum())

print(
    "Duplicate vendor/location pairs:",
    df.duplicated(subset=["vendor_name", "location"]).sum()
)

# Rating validation
ratings = pd.to_numeric(df["verified_rating"], errors="coerce")
invalid_ratings = ratings.notna() & ~ratings.between(0, 5)

print("Invalid verified ratings:", invalid_ratings.sum())

# Verification status
print("\nVerification status:")
print(df["verification_status"].value_counts().to_string())

# Direct source URL progress
print(
    "\nRecords with direct source URLs:",
    df["direct_source_url"].notna().sum()
)

# Missing information
print("\nMissing values:")
print(df.isnull().sum().to_string())

print("\nTotal records:", len(df))
print("Unique vendor IDs:", df["vendor_id"].nunique())

print("\nTracker validation completed.")
