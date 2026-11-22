
import pandas as pd
from pathlib import Path

# Load raw dataset
df = pd.read_csv("data/raw/vendors.csv")

print("Original dataset:", df.shape)

# Remove duplicate records
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["vendor_id"])

# Remove extra spaces from text columns
text_columns = df.select_dtypes(include=["object", "str"]).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# Standardize category names
df["category"] = df["category"].replace({
    "Makeup Artist": "Makeup"
})

# Standardize pricing type
df["pricing_type"] = df["pricing_type"].str.lower()

# Save cleaned dataset
output_folder = Path("data/clean")
output_folder.mkdir(parents=True, exist_ok=True)

df.to_csv(output_folder / "vendors_clean.csv", index=False)

print("\nUpdated categories:")
print(df["category"].value_counts())

print("\nFinal dataset shape:", df.shape)
print("\nCleaned dataset saved successfully!")
