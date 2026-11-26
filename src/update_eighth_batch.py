
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)

df["verification_notes"] = df["verification_notes"].astype("string")

updates = {
    "RES-036": (
        "Matching Anchor Vishal Dumbre public listing found in Shivajinagar, Pune. "
        "Public listing rating: 5.0. Event anchoring services listed."
    ),
    "RES-037": (
        "Matching Anchor Tulika public listing found in Baner, Pune. "
        "Public listing rating: 5.0. Wedding, birthday and corporate anchoring services listed."
    ),
    "RES-038": (
        "Matching Emcee Aman Agrawal public listing found in Wakad, Pune. "
        "Public listing rating: 4.8. Event hosting and anchoring services listed."
    ),
    "RES-039": (
        "Matching Sai Sound & Events public listing found in Thergaon, Pune. "
        "Public listing rating: 4.8. DJ, sound and event equipment services listed."
    ),
    "RES-040": (
        "Matching Rhythm Sound public listing found on Pune-Solapur Road, Pune. "
        "Public listing rating: 4.8. DJ and sound equipment rental services listed."
    )
}

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = (
        "Public listing matched - details pending"
    )
    df.loc[mask, "verification_notes"] = note

df.to_csv(file_path, index=False)

print("Eighth batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status", "verification_notes"]]
    .to_string(index=False)
)
