
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)

for col in ["verification_notes", "direct_source_url"]:
    df[col] = df[col].astype("string")

updates = {
    "RES-058": {
        "url": "https://www.sosparty.io/",
        "note": (
            "Matching SOS Party business website found. Bengaluru-based "
            "corporate event management, employee engagement and offsite "
            "event services listed. Exact listing rating and pricing need "
            "further confirmation."
        )
    },
    "RES-059": {
        "url": "https://www.revaaevent.com/",
        "note": (
            "Matching Revaa Events official website found in Bengaluru. "
            "Wedding planning, corporate events, birthdays and event "
            "management services listed. Exact listing rating and pricing "
            "need further confirmation."
        )
    },
    "RES-060": {
        "url": "https://framefusionphotography.co.in/events",
        "note": (
            "Matching FrameFusion Events website found in Bengaluru. "
            "Decoration, balloon decor, floral decor and event management "
            "services listed. Exact listing rating and pricing need "
            "further confirmation."
        )
    }
}

for vendor_id, details in updates.items():
    mask = df["vendor_id"] == vendor_id

    df.loc[mask, "verification_status"] = (
        "Public listing matched - details pending"
    )
    df.loc[mask, "direct_source_url"] = details["url"]
    df.loc[mask, "verification_notes"] = details["note"]

df.to_csv(file_path, index=False)

print("Twelfth batch tracker updated!")

print(
    df[df["vendor_id"].isin(
        ["RES-056", "RES-057", "RES-058", "RES-059", "RES-060"]
    )][
        ["vendor_id", "vendor_name", "verification_status",
         "direct_source_url"]
    ].to_string(index=False)
)
