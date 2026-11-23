
import pandas as pd
from pathlib import Path

# Project root
project_root = Path(__file__).resolve().parent.parent

# New real-world venue research leads
# All records are pending verification.
# Prices and ratings are intentionally left blank.

venue_data = [
    # MUMBAI
    {
        "vendor_id": "VEN008",
        "vendor_name": "Flag's Banquet",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Mumbai",
        "address": "Kavi Ram Basakhetre Road, Lokhandwala Complex, Andheri West, Mumbai, Maharashtra 400053",
        "phone": "+91 93268 99552",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://turtlepic.com/wedding-vendors/mumbai/wedding-venues/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN009",
        "vendor_name": "Star Banquets",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Mumbai",
        "address": "2nd and 3rd Floor, Skicity Harmony, Lake Road, Bhandup West, Mumbai, Maharashtra 400078",
        "phone": "+91 98200 25720",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://turtlepic.com/wedding-vendors/mumbai/wedding-venues/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN010",
        "vendor_name": "Sawai Banquets & Lawns by Atarah",
        "category": "Venues",
        "subcategory": "Banquet Hall and Lawn",
        "location": "Mumbai",
        "address": "Waman Tukaram Patil Marg, Opposite Amar Theatre, Ghatla, Chembur, Mumbai, Maharashtra 400071",
        "phone": "+91 84240 24210",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://turtlepic.com/wedding-vendors/mumbai/wedding-venues/",
        "verification_status": "Pending",
        "is_synthetic": False
    },

    # PUNE
    {
        "vendor_id": "VEN011",
        "vendor_name": "Marigold Banquets 'N' Conventions",
        "category": "Venues",
        "subcategory": "Banquet Hall and Convention Centre",
        "location": "Pune",
        "address": "Opposite Windmill Village Road, Bavdhan, Pune, Maharashtra 411021",
        "phone": "+91 90904 04444",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://turtlepic.com/wedding-vendors/pune/wedding-venues/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN012",
        "vendor_name": "Vishnukrupa Hall",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Pune",
        "address": "259, T Saheb KK Marg, Near Omkareshwar Mandir, Shaniwar Peth, Pune, Maharashtra 411030",
        "phone": "+91 20 2445 7202",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://turtlepic.com/wedding-vendors/pune/wedding-venues/",
        "verification_status": "Pending",
        "is_synthetic": False
    },
    {
        "vendor_id": "VEN013",
        "vendor_name": "Siddhi Gardens and Banquets",
        "category": "Venues",
        "subcategory": "Banquet Hall and Lawn",
        "location": "Pune",
        "address": "7/2-4, 100 Ft DP Road, Near Mhatre Bridge, Erandwane, Pune, Maharashtra 411052",
        "phone": "+91 82828 24640",
        "event_type": "",
        "pricing_type": "",
        "min_price_per_plate": None,
        "max_price_per_plate": None,
        "min_price_per_event": None,
        "max_price_per_event": None,
        "source_url": "https://turtlepic.com/wedding-vendors/pune/wedding-venues/",
        "verification_status": "Pending",
        "is_synthetic": False
    },

    # BANGALORE
    {
        "vendor_id": "VEN014",
        "vendor_name": "CMA Grand Convention & Wedding Hall",
        "category": "Venues",
        "subcategory": "Convention Centre",
        "location": "Bangalore",
        "address": "19th Bazar Street, Arabic College Main Road, Gandhi Nagar, Kadugondanahalli, Bengaluru, Karnataka 560045",
        "phone": "+91 98809 24545",
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

    # THANE
    {
        "vendor_id": "VEN015",
        "vendor_name": "Mahajan Grand Banquet",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Thane",
        "address": "2nd Floor, Amber Arcade, Majiwada Circle, Near Laxvas Hotel, Thane West, Maharashtra 400601",
        "phone": "+91 99204 33555",
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
        "vendor_id": "VEN016",
        "vendor_name": "Murlidhar Banquet",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Thane",
        "address": "Ghodbunder Road, Opposite Mahanagar Gas Pump, Owale, Thane West, Maharashtra 400615",
        "phone": "+91 90760 10022",
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
        "vendor_id": "VEN017",
        "vendor_name": "Madhav Banquet Hall",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Thane",
        "address": "Ghodbunder Road, Opposite G Corp IT Park, Kasarvadavali, Thane West, Maharashtra 400615",
        "phone": "+91 77770 91884",
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
        "vendor_id": "VEN018",
        "vendor_name": "iLeaf Ritz Banquets",
        "category": "Venues",
        "subcategory": "Banquet Hall",
        "location": "Thane",
        "address": "R Mall, 3rd Floor, Ghodbunder Road, Thane, Maharashtra 400607",
        "phone": "+91 82914 46666",
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

# Create output folder
output_folder = project_root / "data" / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

# Save new venue leads separately
output_file = output_folder / "venue_leads_new.csv"
df.to_csv(output_file, index=False)

# Display summary
print("New venue leads CSV created successfully!")
print("Total venue leads:", len(df))

print("\nVenue leads by location:")
print(df["location"].value_counts())

print("\nVerification status:")
print(df["verification_status"].value_counts())

print("\nSynthetic status:")
print(df["is_synthetic"].value_counts())

print("\nSaved file:")
print(output_file)
