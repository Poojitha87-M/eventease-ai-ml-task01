
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "raw" / "venue_leads_new.csv"

df = pd.read_csv(file_path)

official_sources = {
    "VEN008": "https://www.flagsbanquet.in/contact-us",
    "VEN009": "https://www.manekventures.com/hospitality",
    "VEN011": "https://www.marigoldbanquets.com/",
    "VEN012": "https://vishnukrupa.in/",
    "VEN013": "https://in.linkedin.com/company/siddhi-gardens-and-banquets-pune",
    "VEN015": "https://mahajangrandbanquet.com/",
    "VEN016": "https://murlidharbanquet.com/",
    "VEN017": "https://madhavbanquetthane.com/contact-us/",
    "VEN018": "https://www.ileafritz.com/contact.html",
    "VEN010": "https://banquethallhub.com/banquethall/sawai-banquets-lawns-by-atarah-mumbai-1008/",
    "VEN014": "https://magicpin.in/Bangalore/Kadugondanahalli/Other/Cma-Grand-Convention-and-Wedding-Hall/store/188a453"
}

for vendor_id, url in official_sources.items():
    df.loc[df["vendor_id"] == vendor_id, "source_url"] = url

# Keep CMA source blank until an official source is confirmed.
df.to_csv(file_path, index=False)

print("Venue source URLs updated!")
print(df[["vendor_id", "vendor_name", "source_url"]].to_string(index=False))
