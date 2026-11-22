
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load all three datasets
vendors = pd.read_csv(BASE_DIR / "data/clean/vendors_clean.csv")
venues = pd.read_csv(BASE_DIR / "data/raw/venue_leads.csv")
event_leads = pd.read_csv(BASE_DIR / "data/raw/event_type_leads.csv")

required_events = [
    "Wedding",
    "Birthday",
    "Corporate Event",
    "Engagement",
    "Baby Shower",
    "College Event",
    "Private Party",
    "Festival"
]

# Count sample vendor coverage
sample_counts = {event: 0 for event in required_events}

for value in vendors["event_type"].dropna():
    for event in str(value).split("|"):
        event = event.strip()
        if event in sample_counts:
            sample_counts[event] += 1

# Count possible leads separately
candidate_counts = {event: 0 for event in required_events}

# Venue leads: their event types are unverified
for value in venues["event_type"].dropna():
    for event in str(value).split("|"):
        event = event.strip()
        if event in candidate_counts:
            candidate_counts[event] += 1

# New event-type leads: use candidate_event_types
for value in event_leads["candidate_event_types"].dropna():
    for event in str(value).split("|"):
        event = event.strip()
        if event in candidate_counts:
            candidate_counts[event] += 1

# Create final report
report = pd.DataFrame({
    "event_type": required_events,
    "sample_vendor_count": [
        sample_counts[event] for event in required_events
    ],
    "potential_lead_count": [
        candidate_counts[event] for event in required_events
    ]
})

report["sample_coverage"] = report["sample_vendor_count"].apply(
    lambda count: "Available" if count > 0 else "Missing"
)

report["lead_status"] = report["potential_lead_count"].apply(
    lambda count: "Potential Leads Found" if count > 0 else "No Leads Found"
)

# Save report
output_path = BASE_DIR / "data/clean/final_event_coverage_report.csv"
report.to_csv(output_path, index=False)

print("\n--- FINAL EVENT COVERAGE REPORT ---")
print(report.to_string(index=False))

print("\n--- SUMMARY ---")
print("Event types:", len(report))
print("Covered by sample vendors:",
      (report["sample_coverage"] == "Available").sum())
print("Missing in sample vendors:",
      (report["sample_coverage"] == "Missing").sum())
print("Event types with potential leads:",
      (report["potential_lead_count"] > 0).sum())

print("\nImportant: Potential leads are not verified vendors.")
print("\nReport saved at:", output_path)
