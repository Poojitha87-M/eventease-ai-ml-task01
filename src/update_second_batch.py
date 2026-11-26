
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)

updates = {
    "RES-006": "Google Business listing match found in Thane East, Kopri. Further details pending.",
    "RES-007": "Google Business listing match found in Thane West, Ghodbunder Road. Further details pending.",
    "RES-008": "Google Business listing match found in Thane West, Charai. Further details pending.",
    "RES-009": "Google Business listing match found in Thane, Majiwada. Further details pending.",
    "RES-010": "Google Business listing match found in Thane West, Owale. Further details pending."
}

df["verification_notes"] = df["verification_notes"].astype("string")

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = "Public listing matched - details pending"
    df.loc[mask, "verification_notes"] = note

df.to_csv(file_path, index=False)

print("Second batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status", "verification_notes"]]
    .to_string(index=False)
)
