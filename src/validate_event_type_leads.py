
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "raw" / "event_type_leads.csv"

# Load dataset
df = pd.read_csv(file_path)

print("----- EVENT TYPE LEADS VALIDATION -----")

# Dataset information
print("\nDataset Shape:", df.shape)

# Check duplicate rows
print("\nDuplicate Rows:", df.duplicated().sum())

# Check duplicate vendor IDs
print("Duplicate Vendor IDs:", df["vendor_id"].duplicated().sum())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check missing vendor names
print("\nMissing Vendor Names:",
      df["vendor_name"].isnull().sum())

# Check locations
print("\nVendor Locations:")
print(df["location"].value_counts())

# Check verification status
print("\nVerification Status:")
print(df["verification_status"].value_counts())

# Check candidate event types
print("\nCandidate Event Types:")
for _, row in df.iterrows():
    print(row["vendor_name"], ":", row["candidate_event_types"])

# Check synthetic records
print("\nSynthetic Records:")
print(df["is_synthetic"].value_counts())

print("\nValidation completed!")
