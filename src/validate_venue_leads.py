
import pandas as pd
from pathlib import Path

# Locate project folder
project_root = Path(__file__).resolve().parent.parent

# Load venue leads
file_path = project_root / "data" / "raw" / "venue_leads.csv"
df = pd.read_csv(file_path)

print("\n--- Venue Leads Preview ---")
print(df[["vendor_id", "vendor_name", "location", "verification_status"]])

print("\n--- Dataset Shape ---")
print(df.shape)

print("\n--- Duplicate Rows ---")
print(df.duplicated().sum())

print("\n--- Duplicate Vendor IDs ---")
print(df["vendor_id"].duplicated().sum())

print("\n--- Missing Vendor Names ---")
print(df["vendor_name"].isna().sum())

print("\n--- Locations ---")
print(df["location"].value_counts(dropna=False))

print("\n--- Categories ---")
print(df["category"].value_counts(dropna=False))

print("\n--- Verification Status ---")
print(df["verification_status"].value_counts(dropna=False))

print("\n--- Missing Contact Information ---")
print("Missing phone numbers:", df["phone"].isna().sum())
print("Blank phone numbers:", df["phone"].fillna("").str.strip().eq("").sum())

print("\n--- Synthetic vs Real Leads ---")
print(df["is_synthetic"].value_counts(dropna=False))

print("\nVenue lead validation completed!")
