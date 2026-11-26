
import pandas as pd
from pathlib import Path

# Load researched vendor dataset
input_file = Path("data/research/vendors_researched_initial.csv")
df = pd.read_csv(input_file)

print("Original dataset:", df.shape)

# Remove exact duplicate records
df = df.drop_duplicates()

# Remove duplicate vendor IDs
df = df.drop_duplicates(subset=["vendor_id"])

# Remove extra spaces from text columns
text_columns = df.select_dtypes(include=["object", "str"]).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# Standardize category names
df["main_category"] = df["main_category"].replace({
    "Makeup Artist": "Makeup"
})

# Standardize pricing type
df["pricing_type"] = df["pricing_type"].str.lower()

# Preserve unconfirmed values; do not invent prices or ratings

# Save cleaned research dataset
output_folder = Path("data/clean")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "vendors_researched_clean.csv"
df.to_csv(output_file, index=False)

print("\nUpdated categories:")
print(df["main_category"].value_counts())

print("\nFinal dataset shape:", df.shape)
print("\nCleaned research dataset saved:", output_file)
