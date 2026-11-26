
import pandas as pd
from pathlib import Path

# Load research dataset
df = pd.read_csv("data/clean/vendors_researched_clean.csv")

# Load verification tracker
tracker = pd.read_csv("data/research/vendor_verification_tracker.csv")

# Create report
report = []

report.append("EVENTEASE - VENDOR RESEARCH PROGRESS REPORT")
report.append("=" * 50)

report.append(f"\nTotal research leads: {len(df)}")
report.append(f"Unique vendor IDs: {df['vendor_id'].nunique()}")

report.append("\nLOCATION DISTRIBUTION")
report.append(df["location"].value_counts().to_string())

report.append("\nCATEGORY DISTRIBUTION")
report.append(df["main_category"].value_counts().to_string())

report.append("\nVERIFICATION STATUS")
report.append(tracker["verification_status"].value_counts().to_string())

report.append("\nMISSING INFORMATION")
report.append(df.isnull().sum().to_string())

report.append("\nDATA QUALITY")
report.append(f"Duplicate IDs: {df['vendor_id'].duplicated().sum()}")
report.append(
    f"Duplicate vendor/location pairs: "
    f"{df.duplicated(['vendor_name', 'location']).sum()}"
)

report.append("\nNEXT ACTIONS")
report.append("1. Verify individual vendor business listings.")
report.append("2. Collect direct source URLs.")
report.append("3. Verify ratings and contact information.")
report.append("4. Research pricing and guest capacity.")
report.append("5. Update availability after confirmation.")

# Save report
output_folder = Path("reports")
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "vendor_research_progress_report.txt"
output_file.write_text("\n".join(report), encoding="utf-8")

print("\n".join(report))
print("\nReport saved:", output_file)
