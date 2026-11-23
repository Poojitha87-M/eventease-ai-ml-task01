
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "raw" / "venue_leads_new.csv"

df = pd.read_csv(file_path)

print("NEW VENUE LEADS VALIDATION")
print("=" * 40)

# 1. Check total records
print("Total records:", len(df))

# 2. Check duplicate IDs
print("Duplicate vendor IDs:", df["vendor_id"].duplicated().sum())

# 3. Check duplicate vendor names
print("Duplicate vendor names:", df["vendor_name"].duplicated().sum())

# 4. Check locations
required_locations = {"Mumbai", "Bangalore", "Pune", "Thane"}
actual_locations = set(df["location"].dropna().unique())

print("Missing target locations:", required_locations - actual_locations)

# 5. Check verification status
print("\nVerification status:")
print(df["verification_status"].value_counts())

# 6. Check synthetic status
print("\nSynthetic status:")
print(df["is_synthetic"].value_counts())

# 7. Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# 8. Check required fields
required_fields = [
    "vendor_id",
    "vendor_name",
    "category",
    "location",
    "verification_status"
]

print("\nMissing required fields:")
print(df[required_fields].isnull().sum())

print("\nValidation completed!")
