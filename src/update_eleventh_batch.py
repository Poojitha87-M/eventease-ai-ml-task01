
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)

for col in ["verification_notes", "direct_source_url"]:
    df[col] = df[col].astype("string")

updates = {
    "RES-051": {
        "url": "https://parichayphotography.com/",
        "note": (
            "Matching Parichay Photography business website found in "
            "Bengaluru. Photography, videography and cinematography "
            "services listed. Exact listing rating, contact and pricing "
            "need further confirmation."
        )
    },
    "RES-054": {
        "url": "https://mjgorgeous.com/",
        "note": (
            "Matching MJ Gorgeous Makeup Studio official website found. "
            "Bengaluru bridal and occasion makeup services listed. "
            "Exact listing rating and pricing need further confirmation."
        )
    },
    "RES-055": {
        "url": "https://makeupstudiobysuu.com/",
        "note": (
            "Matching Makeup Studio by Suu official website found in "
            "Frazer Town, Bengaluru. Bridal makeup and makeup training "
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

print("Eleventh batch tracker updated!")

print(
    df[df["vendor_id"].isin(
        ["RES-051", "RES-052", "RES-053", "RES-054", "RES-055"]
    )][
        ["vendor_id", "vendor_name", "verification_status",
         "direct_source_url"]
    ].to_string(index=False)
)
