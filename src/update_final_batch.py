
import pandas as pd

tracker_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(tracker_path)

updates = {
    "RES-048": {
        "url": "https://www.localsaathi.in/business/bloom-lane-events-marathahalli-bengaluru",
        "notes": "Matching Bloom Lane Events listing found in Marathahalli, Bengaluru. Decoration and event services listed. Exact rating, contact, pricing and availability require confirmation."
    },
    "RES-050": {
        "url": "https://www.cliqora.com/photographer/len-freelance-photography-bengaluru",
        "notes": "Matching Len Freelance Photography listing found in Bengaluru. Photography and videography services listed. Exact rating, contact, pricing and availability require confirmation."
    },
    "RES-052": {
        "url": "https://instantpix.co/photographers",
        "notes": "Plutography.in listed as a Bengaluru wedding and pre-wedding photographer on InstantPix. Exact business identity, rating, contact and availability require confirmation."
    },
    "RES-053": {
        "url": "https://instantpix.co/photographers",
        "notes": "Limelight Photography Bangalore listed as a Bengaluru wedding and birthday photographer on InstantPix. Exact business identity, rating, contact and availability require confirmation."
    },
    "RES-057": {
        "url": "https://mytribe.in/djnitizh/club-public-event-dj",
        "notes": "DJ Nithish profile found in Kengeri, Bengaluru, offering DJ services for events. Exact identity against the original lead, rating, contact and availability require confirmation."
    }
}

for vendor_id, details in updates.items():
    mask = df["vendor_id"] == vendor_id

    df.loc[mask, "verification_status"] = (
        "Public listing matched - details pending"
    )
    df.loc[mask, "direct_source_url"] = details["url"]
    df.loc[mask, "verification_notes"] = details["notes"]

df.to_csv(tracker_path, index=False)

print("Updated matching vendor records:", len(updates))
print(df["verification_status"].value_counts().to_string())
