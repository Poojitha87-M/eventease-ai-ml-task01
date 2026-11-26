
import pandas as pd
from pathlib import Path

research_path = Path("data/clean/vendors_researched_clean.csv")
tracker_path = Path("data/research/vendor_verification_tracker.csv")
output_path = Path("data/clean/vendors_researched_final.csv")

# Load both datasets
vendors = pd.read_csv(research_path)
tracker = pd.read_csv(tracker_path)

# Select verification information
verification = tracker[
    [
        "vendor_id",
        "verification_status",
        "direct_source_url",
        "verified_rating",
        "verified_contact",
        "verification_notes"
    ]
].copy()

# Rename status to avoid column conflicts
verification = verification.rename(
    columns={"verification_status": "tracker_status"}
)

# Merge using vendor ID
final_df = vendors.merge(
    verification,
    on="vendor_id",
    how="left",
    validate="one_to_one"
)

# Use the latest tracker status
final_df["verification_status"] = final_df["tracker_status"]
final_df = final_df.drop(columns=["tracker_status"])

# Save final dataset
output_path.parent.mkdir(parents=True, exist_ok=True)
final_df.to_csv(output_path, index=False)

print("FINAL RESEARCH DATASET CREATED")
print("=" * 40)
print("Total vendors:", len(final_df))
print("Unique vendor IDs:", final_df["vendor_id"].nunique())
print("\nVerification status:")
print(final_df["verification_status"].value_counts().to_string())
print("\nNew verification columns:")
print(final_df[
    [
        "direct_source_url",
        "verified_rating",
        "verified_contact",
        "verification_notes"
    ]
].notna().sum().to_string())

print("\nSaved:", output_path)
