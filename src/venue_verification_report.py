
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

input_file = project_root / "data" / "raw" / "venue_leads.csv"
output_file = project_root / "data" / "clean" / "venue_verification_report.csv"

df = pd.read_csv(input_file)

# Check which important fields are blank
fields_to_check = [
    "address",
    "phone",
    "event_type",
    "source_url"
]

for field in fields_to_check:
    df[f"{field}_status"] = df[field].fillna("").astype(str).str.strip().apply(
        lambda value: "Missing" if value == "" else "Available - Needs Verification"
    )

# Keep every lead pending until its details are checked
df["verification_status"] = "Pending"

# Create output folder
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save report
df.to_csv(output_file, index=False)

print("Venue verification report created!")

print("\n--- Verification Summary ---")
for field in fields_to_check:
    print(f"\n{field}:")
    print(df[f"{field}_status"].value_counts())

print("\n--- Venue Verification Details ---")
print(
    df[
        [
            "vendor_name",
            "location",
            "address_status",
            "phone_status",
            "event_type_status",
            "source_url_status",
            "verification_status"
        ]
    ].to_string(index=False)
)

print("\nReport saved at:", output_file)
