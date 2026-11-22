
import pandas as pd
from pathlib import Path

# Project root is the parent of the src folder
project_root = Path(__file__).resolve().parent.parent

# Initial real-world venue leads
# Blank fields mean the information has not yet been confirmed.
venue_data = [
    {
        "vendor_id": "VEN001",
        "vendor_name": "The Park Navi Mumbai",
        "category": "Venues",
        "subcategory": "Hotel and Banquet Hall",
        "location": "CBD Belapur",
        "address": "No 1, Sector 10, CBD Belapur, Navi Mumbai, Maharashtra 400614",
        "phone": "+91 22 6758 9000",
        "event_type": "Wedding|Corporate Event|Social Events",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://www.theparkhotels.com/navi-mumbai/banquets/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN002",
        "vendor_name": "Warkari Bhawan",
        "category": "Venues",
        "subcategory": "Community Function Hall",
        "location": "CBD Belapur",
        "address": "B-10/5, YMCA Marg, Sector 4, CBD Belapur, Navi Mumbai, Maharashtra 400614",
        "phone": "+91 98670 98046",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN003",
        "vendor_name": "Grand Golden Banquet",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Vashi",
        "address": "4th Floor, Palm Beach Galleria Mall, Sector 19D, Vashi, Navi Mumbai, Maharashtra 400703",
        "phone": "+91 88986 81403",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://grandgoldenbanquet.com/contact-banquet-hall/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN004",
        "vendor_name": "Ashoka Banquet Hall",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Vashi",
        "address": "Plot No. 61 C, Juhu Nagar, Sector 15, Vashi, Navi Mumbai, Maharashtra 400703",
        "phone": "088795 50505",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN005",
        "vendor_name": "Bhanushali Banquets",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Nerul",
        "address": "1-2, Basveshewar Maharaj Marg, Near Ryan International School, Sector 19A, Nerul, Navi Mumbai, Maharashtra 400706",
        "phone": "+91 88505 40493",
        "event_type": "Wedding|Birthday|Engagement",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://bhanushalibanquets.in/nerul-venue/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN006",
        "vendor_name": "Madhav Banquet",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Nerul",
        "address": "Jagatguru Aadi Shankracharya Marg, Near Haware Mall, Sector 19A, Nerul East, Navi Mumbai, Maharashtra 400706",
        "phone": "+91 97698 44111",
        "event_type": "Wedding|Birthday|Corporate Event|Engagement|Baby Shower",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://madhavbanquetnerul.com/contact/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN007",
        "vendor_name": "Sterling Banquet & Lawn",
        "category": "Venues",
        "subcategory": "Banquet Hall and Lawn",
        "location": "Nerul",
        "address": "",
        "phone": "",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "",
        "verification_status": "Pending",
        "is_synthetic": False
    }
]

# Create DataFrame
df = pd.DataFrame(venue_data)

# Create output folder if it does not exist
output_folder = project_root / "data" / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

# Save CSV
output_file = output_folder / "venue_leads.csv"
df.to_csv(output_file, index=False)

print("Venue leads CSV created successfully!")
print("Total venue leads:", len(df))
print("\nVenue leads by location:")
print(df["location"].value_counts())

print("\nVerification status:")
print(df["verification_status"].value_counts())

print("\nSaved file:", output_file)
