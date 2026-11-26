
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)
df["verification_notes"] = df["verification_notes"].astype("string")

updates = {
    "RES-021": "Matching-name public catering listing found in Balewadi, Pune. Address and business identity need final confirmation.",
    "RES-022": "Matching-name public catering listing found in Kelgaon, Alandi, Pune. Address and business identity need final confirmation.",
    "RES-023": "Matching-name public catering listing found in Sukhsagar Nagar, Kondhwa Budruk, Pune. Address and business identity need final confirmation.",
    "RES-024": "Matching-name public catering listing found in Sasane Nagar, Hadapsar, Pune. Address and business identity need final confirmation.",
    "RES-025": "Matching-name public catering listing found in Bibwewadi, Pune. Address and business identity need final confirmation."
}

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = "Public listing matched - details pending"
    df.loc[mask, "verification_notes"] = note

df.to_csv(file_path, index=False)

print("Fifth batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status", "verification_notes"]]
    .to_string(index=False)
)
