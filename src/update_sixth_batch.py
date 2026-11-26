
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)
df["verification_notes"] = df["verification_notes"].astype("string")

updates = {
    "RES-026": "Matching Moryaa Caterers public listing found in Katraj, Pune. Listing rating: 5.0. Contact and pricing need further confirmation.",
    "RES-027": "Matching K FARID MANDAP AND EVENTS listing found in Salunke Vihar, Pune. Listing rating: 4.9. Decoration services listed.",
    "RES-028": "Matching GOD SKY Wedding Decoration listing found in Dhanori, Pune. Listing rating: 5.0. Wedding and balloon decoration services listed.",
    "RES-029": "Matching DD Events & Decoration listing found in Pimple Saudagar, Pune. Listing rating: 5.0. Event decoration services listed.",
    "RES-030": "Matching Eventer - The Perfect Celebration listing found in Dhanori, Pune. Listing rating: 4.9. Event planning and balloon decoration services listed."
}

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = "Public listing matched - details pending"
    df.loc[mask, "verification_notes"] = note

df.to_csv(file_path, index=False)

print("Sixth batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status", "verification_notes"]]
    .to_string(index=False)
)
