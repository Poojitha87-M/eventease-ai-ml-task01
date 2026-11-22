
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

input_file = project_root / "data" / "raw" / "venue_leads.csv"
output_file = project_root / "data" / "raw" / "venue_verification_tracker.csv"

df = pd.read_csv(input_file)

# Add fields for future verification
new_columns = {
    "verification_method": "",
    "last_checked": "",
    "verified_fields": "",
    "verification_notes": ""
}

for column, default_value in new_columns.items():
    if column not in df.columns:
        df[column] = default_value

# Keep all leads pending until actual verification
df["verification_status"] = "Pending"

# Save separate verification tracker
df.to_csv(output_file, index=False)

print("Verification tracker created successfully!")

print("\n--- Venue Verification Tracker ---")
print(
    df[
        [
            "vendor_id",
            "vendor_name",
            "location",
            "verification_method",
            "verified_fields",
            "verification_status"
        ]
    ].to_string(index=False)
)

print("\nTotal venues:", len(df))
print("Pending verification:", (df["verification_status"] == "Pending").sum())
print("\nSaved at:", output_file)
