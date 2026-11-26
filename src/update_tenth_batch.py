
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)

for col in ["verification_notes", "direct_source_url"]:
    df[col] = df[col].astype("string")

updates = {
    "RES-046": {
        "note": (
            "Matching Butterflies Event Management - Event Planner listing "
            "found in Indiranagar, Bengaluru. Public directory rating: 5.0. "
            "Event planning services listed. Contact and pricing need confirmation."
        ),
        "url": "https://bengaluruconnect.com/businesses/butterflies-event-management-event-planner"
    },
    "RES-047": {
        "note": (
            "Dreamstrokes Wedding Planners matched with the Bengaluru wedding "
            "planning business. Official website found. Wedding planning and "
            "decoration services listed. Contact and pricing need confirmation."
        ),
        "url": "https://www.dreamstrokes.in/"
    }
}

for vendor_id, details in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = (
        "Public listing matched - details pending"
    )
    df.loc[mask, "verification_notes"] = details["note"]
    df.loc[mask, "direct_source_url"] = details["url"]

# Keep the other three records pending until their identity is confirmed.
df.to_csv(file_path, index=False)

print("Tenth batch tracker updated!")
print(
    df[df["vendor_id"].isin(
        ["RES-046", "RES-047", "RES-048", "RES-049", "RES-050"]
    )][
        ["vendor_id", "vendor_name", "verification_status",
         "direct_source_url"]
    ].to_string(index=False)
)
