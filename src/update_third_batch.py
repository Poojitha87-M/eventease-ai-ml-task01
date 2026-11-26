
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)
df["verification_notes"] = df["verification_notes"].astype("string")

updates = {
    "RES-011": "Matching public photography listing found in Vartak Nagar, Thane West. Listed rating 4.9. Further details pending.",
    "RES-012": "Matching public photography listing found in Uthalsar, Thane West. Listed rating 4.9. Further details pending.",
    "RES-013": "Matching public photography listing found in Dhokali, Thane West. Listed rating 4.9. Further details pending.",
    "RES-014": "Matching public photography listing found at Cadbury Junction, Thane West. Listed rating 4.9. Further details pending.",
    "RES-015": "Matching public photography listing found in Vartak Nagar, Thane West. Listed rating 4.9. Further details pending."
}

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = "Public listing matched - details pending"
    df.loc[mask, "verification_notes"] = note

df.to_csv(file_path, index=False)

print("Third batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status"]]
    .to_string(index=False)
)
