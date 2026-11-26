
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"
df = pd.read_csv(file_path)
# Convert initially empty text columns to string type
text_columns = [
    "direct_source_url",
    "verified_contact",
    "verification_notes"
]

for column in text_columns:
    df[column] = df[column].astype("string")

updates = {
    "RES-001": {
        "direct_source_url": "https://polibhajikendra.in/famouscaterers/",
        "verified_rating": 5.0,
        "verified_contact": "+91 75061 06988",
        "verification_notes": "Matching Thane listing found. Google listing rating 5.0; another directory reports 4.8. Contact not independently confirmed."
    },
    "RES-002": {
        "direct_source_url": "https://www.bdir.in/p/best/in/catering-services-in-thane-mh/MTA3MDI4",
        "verified_rating": 4.9,
        "verified_contact": "+91 81690 06737",
        "verification_notes": "Matching Thane listing found. Ratings differ across directories. Contact not independently confirmed."
    },
    "RES-003": {
        "direct_source_url": "https://radhafoodservices.com/",
        "verified_rating": 4.9,
        "verified_contact": "+91 92212 35728",
        "verification_notes": "Matching Thane East listing and business website found. Public rating recorded; contact not independently confirmed."
    },
    "RES-004": {
        "direct_source_url": "https://www.avcreation.in/",
        "verified_rating": 5.0,
        "verified_contact": "+91 81082 43703",
        "verification_notes": "Matching Thane listing found. Decoration and party planning services listed. Contact not independently confirmed."
    },
    "RES-005": {
        "direct_source_url": "",
        "verified_rating": 5.0,
        "verified_contact": "+91 97694 83370",
        "verification_notes": "Matching Kalwa, Thane listing found. Direct business website not established. Contact not independently confirmed."
    }
}

for vendor_id, details in updates.items():
    mask = df["vendor_id"] == vendor_id

    for column, value in details.items():
        df.loc[mask, column] = value

    df.loc[mask, "verification_status"] = (
        "Public listing matched - details pending"
    )

df.to_csv(file_path, index=False)

print("First batch tracker updated!")
print(df[df["vendor_id"].isin(updates)].to_string(index=False))
