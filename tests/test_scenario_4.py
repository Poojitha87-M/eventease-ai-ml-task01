
import pandas as pd

# Separate test data: all matching Makeup Artist vendors are unavailable
test_vendors = pd.DataFrame([
    {
        "vendor_id": "TEST-001",
        "vendor_name": "Test Makeup Vendor 1",
        "category": "Makeup Artist",
        "location": "Vashi",
        "availability": "Unavailable"
    },
    {
        "vendor_id": "TEST-002",
        "vendor_name": "Test Makeup Vendor 2",
        "category": "Makeup Artist",
        "location": "Vashi",
        "availability": "Unavailable"
    }
])

# Customer requirements
category = "Makeup Artist"
location = "Vashi"

# Apply category filter
category_vendors = test_vendors[
    test_vendors["category"] == category
]

# Apply availability filter
available_vendors = category_vendors[
    category_vendors["availability"] == "Available"
]

print("Scenario 4: Makeup Artist Availability Test")
print("Matching category vendors:", len(category_vendors))
print("Available vendors:", len(available_vendors))

if available_vendors.empty:
    print("PASS: No recommendations returned because all matching vendors are unavailable.")
else:
    print("FAIL: Unavailable vendors were incorrectly recommended.")
