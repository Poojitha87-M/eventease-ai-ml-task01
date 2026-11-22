
import pandas as pd
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Four potential vendor leads
data = [
    {
        "vendor_id": "ETL001",
        "vendor_name": "Kreative Keeda Entertainment",
        "category": "Entertainment",
        "location": "Nerul",
        "phone": "+91 77689 41772",
        "candidate_event_types": "College Event|Festival|Cultural Event|Concert"
    },
    {
        "vendor_id": "ETL002",
        "vendor_name": "A.L.S. Events",
        "category": "Event Planning",
        "location": "Vashi",
        "phone": "+91 99308 77368",
        "candidate_event_types": "College Event|Festival|Corporate Event|Private Party|Wedding"
    },
    {
        "vendor_id": "ETL003",
        "vendor_name": "Blink Events Vashi",
        "category": "Event Planning",
        "location": "Vashi",
        "phone": "+91 98338 65567",
        "candidate_event_types": "College Event|Private Party|Birthday|Farewell"
    },
    {
        "vendor_id": "ETL004",
        "vendor_name": "SDS Event Planner",
        "category": "Event Planning",
        "location": "Vashi",
        "phone": "+91 98198 71522",
        "candidate_event_types": "Private Party|Birthday|Family Celebration"
    }
]

# Convert records into a DataFrame
df = pd.DataFrame(data)

# Add verification information
df["event_type"] = ""
df["source_type"] = "Public Business Listing"
df["verification_status"] = "Pending"
df["is_synthetic"] = False

# Save CSV file
output_path = BASE_DIR / "data" / "raw" / "event_type_leads.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("Event type leads created successfully!")
print("\nDataset:")
print(df[["vendor_id", "vendor_name", "location",
          "candidate_event_types", "verification_status"]])

print("\nTotal leads:", len(df))
print("Pending verification:", 
      (df["verification_status"] == "Pending").sum())

print("\nSaved at:", output_path)
