
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/clean/vendors_clean.csv")

# Check first 5 records
print("\n--- Cleaned Dataset ---")
print(df.head())

# Check dataset size
print("\n--- Dataset Shape ---")
print(df.shape)

# Check duplicate records
print("\n--- Duplicate Rows ---")
print(df.duplicated().sum())

# Check duplicate vendor IDs
print("\n--- Duplicate Vendor IDs ---")
print(df["vendor_id"].duplicated().sum())

# Check locations
print("\n--- Locations ---")
print(df["location"].value_counts())

# Check categories
print("\n--- Categories ---")
print(df["category"].value_counts())

print("\nValidation completed!")
