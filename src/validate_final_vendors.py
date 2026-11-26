
import pandas as pd
from pathlib import Path

file_path = Path("data/clean/vendors_researched_final.csv")
df = pd.read_csv(file_path)

print("EVENTEASE - FINAL VENDOR DATA VALIDATION")
print("=" * 45)

required_columns = [
    "vendor_id",
    "vendor_name",
    "main_category",
    "location",
    "pricing_type",
    "rating_listed",
    "availability",
    "verification_status",
    "source_url",
    "is_synthetic",
    "direct_source_url",
    "verified_rating"
]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

print("Missing required columns:", missing_columns)
print("Total records:", len(df))
print("Unique vendor IDs:", df["vendor_id"].nunique())
print("Duplicate IDs:", df["vendor_id"].duplicated().sum())
print(
    "Duplicate vendor/location pairs:",
    df.duplicated(subset=["vendor_name", "location"]).sum()
)

ratings = pd.to_numeric(df["rating_listed"], errors="coerce")
print("Invalid listed ratings:", (
    ratings.notna() & ~ratings.between(0, 5)
).sum())

verified = pd.to_numeric(df["verified_rating"], errors="coerce")
print("Invalid verified ratings:", (
    verified.notna() & ~verified.between(0, 5)
).sum())

print("\nVerification status:")
print(df["verification_status"].value_counts().to_string())

print("\nSynthetic records:", df["is_synthetic"].sum())

print("\nValidation completed.")
