
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

legacy_path = project_root / "data" / "raw" / "venue_leads_legacy.csv"
new_path = project_root / "data" / "raw" / "venue_leads_new.csv"

output_path = project_root / "data" / "clean" / "all_venue_leads.csv"

# Load both datasets
legacy_df = pd.read_csv(legacy_path)
new_df = pd.read_csv(new_path)

# Combine datasets
combined_df = pd.concat(
    [legacy_df, new_df],
    ignore_index=True
)

# Save combined dataset
combined_df.to_csv(output_path, index=False)

print("Venue datasets combined successfully!")
print("Total records:", len(combined_df))
print("Columns:", len(combined_df.columns))
print("Duplicate IDs:", combined_df["vendor_id"].duplicated().sum())
print("Saved to:", output_path)
