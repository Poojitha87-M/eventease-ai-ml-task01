
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"
df = pd.read_csv(file_path)

for col in ["verification_notes", "direct_source_url"]:
    df[col] = df[col].astype("string")

mask = df["vendor_id"] == "RES-061"

df.loc[mask, "verification_status"] = (
    "Public listing matched - details pending"
)

df.loc[mask, "direct_source_url"] = (
    "https://aundh.in/item/rudransh-party-decor-and-event-management/"
)

df.loc[mask, "verification_notes"] = (
    "Matching Rudransh Party Decor and Event Management listing found "
    "in Pimple Saudagar, Pune. Party decoration and event planning "
    "services listed. Public listings show different ratings and "
    "locations; exact listing identity and rating need confirmation. "
    "Contact and pricing also need confirmation."
)

df.to_csv(file_path, index=False)

print("Final vendor RES-061 updated!")
print(df[df["vendor_id"] == "RES-061"].to_string(index=False))
