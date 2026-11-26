
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "clean" / "vendors_researched_final.csv"
OUTPUT_DIR = ROOT / "reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

def has_value(value):
    return pd.notna(value) and str(value).strip().lower() not in {
        "", "nan", "none", "null", "not confirmed", "unconfirmed"
    }

def check_vendor(row):
    missing = []

    if not has_value(row.get("direct_source_url")):
        missing.append("Direct source URL")

    if not has_value(row.get("verified_rating")):
        missing.append("Verified rating")

    if not has_value(row.get("verified_contact")):
        missing.append("Verified contact")

    if not has_value(row.get("min_price")) or not has_value(row.get("max_price")):
        missing.append("Price")

    availability = str(row.get("availability", "")).strip().lower()
    if availability not in ["available", "unavailable"]:
        missing.append("Availability")

    if not has_value(row.get("guest_capacity")):
        missing.append("Guest capacity")

    if not has_value(row.get("verification_notes")):
        missing.append("Verification notes")

    return missing

df["missing_information"] = df.apply(
    lambda row: ", ".join(check_vendor(row)), axis=1
)

df["missing_count"] = df["missing_information"].apply(
    lambda value: len(value.split(", ")) if value else 0
)

def priority(count):
    if count >= 5:
        return "High"
    elif count >= 3:
        return "Medium"
    elif count >= 1:
        return "Low"
    return "Ready for review"

df["verification_priority"] = df["missing_count"].apply(priority)

task_list = df[
    [
        "vendor_id",
        "vendor_name",
        "main_category",
        "location",
        "verification_status",
        "verification_priority",
        "missing_count",
        "missing_information"
    ]
].sort_values(
    by=["missing_count", "vendor_name"],
    ascending=[False, True]
)

output_csv = OUTPUT_DIR / "vendor_verification_priority.csv"
output_txt = OUTPUT_DIR / "vendor_verification_priority_report.txt"

task_list.to_csv(output_csv, index=False)

with open(output_txt, "w", encoding="utf-8") as file:
    file.write("EVENTEASE - VENDOR VERIFICATION PRIORITY REPORT\n")
    file.write("=" * 55 + "\n\n")
    file.write(f"Total vendors: {len(df)}\n")
    file.write(
        f"Vendors needing verification: "
        f"{(df['missing_count'] > 0).sum()}\n\n"
    )

    file.write("PRIORITY SUMMARY\n")
    file.write("-" * 30 + "\n")
    file.write(
        df["verification_priority"].value_counts().to_string()
    )

    file.write("\n\nMISSING INFORMATION SUMMARY\n")
    file.write("-" * 30 + "\n")

    missing_counts = {}
    for items in df["missing_information"]:
        if items:
            for item in items.split(", "):
                missing_counts[item] = missing_counts.get(item, 0) + 1

    for item, count in sorted(
        missing_counts.items(), key=lambda x: x[1], reverse=True
    ):
        file.write(f"{item}: {count}\n")

    file.write("\nVENDOR VERIFICATION TASK LIST\n")
    file.write("-" * 30 + "\n")
    file.write(task_list.to_string(index=False))

print("\nEVENTEASE - VERIFICATION PRIORITY REPORT")
print("=" * 45)
print(f"Total vendors: {len(df)}")
print("\nPriority summary:")
print(df["verification_priority"].value_counts().to_string())

print("\nTop 10 vendors requiring verification:")
print(task_list.head(10).to_string(index=False))

print("\nFiles created:")
print(output_csv)
print(output_txt)
