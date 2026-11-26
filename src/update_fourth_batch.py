
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)
df["verification_notes"] = df["verification_notes"].astype("string")

updates = {
    "RES-016": "Matching Thane makeup artist and academy listing found. Public rating 4.9. Official website: https://ritanandubridalsolutionandacademy.com/. Contact details need independent confirmation.",
    "RES-017": "Matching Varsha's Makeovers listing found in Dhokali, Thane West. Ratings differ across sources: 5.0 and 4.5. Confirm rating source before recording.",
    "RES-018": "Matching Deepika's Makeover & Nail Academy listing found near Viviana Mall, Thane West. Public rating 5.0. Further details pending.",
    "RES-019": "Matching Sumit Sound event production and DJ listing found in Manpada, Thane West. Public rating 4.9. Confirm exact business-name match.",
    "RES-020": "Matching DJ@FERRAO DJ service listing found in Kalwa, Thane. Public rating 4.9. Further details pending."
}

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = "Public listing matched - details pending"
    df.loc[mask, "verification_notes"] = note

df.to_csv(file_path, index=False)

print("Fourth batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status", "verification_notes"]]
    .to_string(index=False)
)
