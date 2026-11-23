
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

input_file = project_root / "data" / "raw" / "venue_leads_new.csv"
output_folder = project_root / "data" / "clean"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "venue_verification_report.csv"

df = pd.read_csv(input_file)

# Source-review notes based on the pages checked.
review_notes = {
    "VEN008": "Official contact page matches the listed address and phone.",
    "VEN009": "Venue listing supports the address; phone needs independent confirmation.",
    "VEN010": "Third-party venue listing provides address and phone details; cross-check with the business directly.",
    "VEN013": "LinkedIn company profile shows a different address format and PIN code. Confirm the correct address with the business."
}

review_status = {
    "VEN008": "Source details matched",
    "VEN009": "Partially checked",
    "VEN010": "Partially checked",
    "VEN013": "Address discrepancy",
}

report = df[
    [
        "vendor_id",
        "vendor_name",
        "location",
        "address",
        "phone",
        "source_url",
        "verification_status"
    ]
].copy()

report["source_review_status"] = (
    report["vendor_id"].map(review_status).fillna("Not reviewed")
)

report["review_notes"] = (
    report["vendor_id"].map(review_notes).fillna(
        "Source details still need checking."
    )
)

report.to_csv(output_file, index=False)

print("Venue verification report created!")
print("Total records:", len(report))

print("\nSource review status:")
print(report["source_review_status"].value_counts())

print("\nVerification status:")
print(report["verification_status"].value_counts())

print("\nSaved to:", output_file)
