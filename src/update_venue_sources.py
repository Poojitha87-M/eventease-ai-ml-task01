
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "raw" / "venue_leads.csv"

df = pd.read_csv(file_path)

source_updates = {
    "VEN001": {
        "source_url": "https://www.theparkhotels.com/amp/navi-mumbai/banquets/",
        "source_type": "Official Website",
        "event_type": "Wedding|Corporate Event|Private Party"
    },
    "VEN002": {
        "source_url": "",
        "source_type": "Public Business Listing",
        "event_type": "Wedding|Family Function|Community Event"
    },
    "VEN003": {
        "source_url": "https://grandgoldenbanquet.com/",
        "source_type": "Official Website",
        "event_type": "Wedding|Birthday|Corporate Event|Private Party"
    },
    "VEN004": {
        "source_url": "",
        "source_type": "Public Business Listing",
        "event_type": ""
    },
    "VEN005": {
        "source_url": "https://bhanushalibanquets.in/nerul-venue/",
        "source_type": "Official Website",
        "event_type": "Wedding|Birthday|Engagement"
    },
    "VEN006": {
        "source_url": "https://madhavbanquetnerul.com/contact/",
        "source_type": "Official Website",
        "event_type": "Wedding|Birthday|Corporate Event|Engagement|Baby Shower"
    },
    "VEN007": {
        "source_url": "https://weddingz.in/wedding-lawns/mumbai/navi-mumbai/",
        "source_type": "Third-party Directory",
        "event_type": "Wedding"
    }
}

if "source_type" not in df.columns:
    df["source_type"] = ""

for vendor_id, details in source_updates.items():
    mask = df["vendor_id"] == vendor_id

    for column, value in details.items():
        if value:
            df.loc[mask, column] = value

# Do not mark any venue verified automatically
df["verification_status"] = "Pending"

df.to_csv(file_path, index=False)

print("Source records updated successfully!")
print("\n", df[
    ["vendor_id", "vendor_name", "source_type",
     "event_type", "verification_status"]
].to_string(index=False))

print("\nTotal records:", len(df))
print("Pending records:", (df["verification_status"] == "Pending").sum())
