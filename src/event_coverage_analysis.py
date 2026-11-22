
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

input_file = project_root / "data" / "clean" / "vendors_clean.csv"
output_file = project_root / "data" / "clean" / "event_coverage_report.csv"

df = pd.read_csv(input_file)

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

# Split multiple event types stored with |
all_events = (
    df["event_type"]
    .dropna()
    .astype(str)
    .str.split("|")
    .explode()
    .str.strip()
)

# Count vendor records supporting each event type
event_counts = all_events.value_counts()

report = pd.DataFrame({
    "event_type": required_events
})

report["vendor_count"] = (
    report["event_type"]
    .map(event_counts)
    .fillna(0)
    .astype(int)
)

report["coverage_status"] = report["vendor_count"].apply(
    lambda count: "Available" if count > 0 else "Missing"
)

# Save report
output_file.parent.mkdir(parents=True, exist_ok=True)
report.to_csv(output_file, index=False)

print("\n--- Event Coverage Report ---")
print(report.to_string(index=False))

print("\n--- Coverage Summary ---")
print(report["coverage_status"].value_counts())

print("\nReport saved at:", output_file)
