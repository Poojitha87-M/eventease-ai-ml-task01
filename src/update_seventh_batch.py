
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)
df["verification_notes"] = df["verification_notes"].astype("string")
df["direct_source_url"] = df["direct_source_url"].astype("string")

updates = {
    "RES-031": (
        "Matching Ajinkya Jadhav Photography listing found in Bavdhan, Pune. "
        "Public listing rating: 4.9. Official website: https://www.ajinkyajadhav.co.in/"
    ),
    "RES-032": (
        "Matching Madhuri Khese Makeup Studio listing found in Bhosari, Pune. "
        "Public listing rating: 4.9. Makeup services and academy listed."
    ),
    "RES-033": (
        "Matching Farida's Makeup Studio listing found in Pune Camp. "
        "Public listing rating: 4.9. Bridal makeup and beauty services listed."
    ),
    "RES-034": (
        "Matching Srushti Makeup Studio, Academy & Salon listing found in Katraj, Pune. "
        "Public listing rating: 4.9. Makeup and salon services listed."
    ),
    "RES-035": (
        "Matching Anchor Sanjay Potdar listing found in Nanded City, Pune. "
        "Public listing rating: 4.9. Event anchoring and emcee services listed."
    )
}

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = "Public listing matched - details pending"
    df.loc[mask, "verification_notes"] = note

# Save the official website found for RES-031
df.loc[df["vendor_id"] == "RES-031", "direct_source_url"] = (
    "https://www.ajinkyajadhav.co.in/"
)

df.to_csv(file_path, index=False)

print("Seventh batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status", "direct_source_url"]]
    .to_string(index=False)
)
