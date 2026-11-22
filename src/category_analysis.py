
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/clean/vendors_clean.csv")

# Required vendor categories
required_categories = [
    "Decoration",
    "Photography",
    "Catering",
    "Venues",
    "Entertainment",
    "Makeup",
    "Event Planning"
]

# Required event types
required_events = [
    "Wedding",
    "Birthday",
    "Corporate Event",
    "Engagement",
    "Baby Shower",
    "College Event",
    "Private Party",
    "Festival"
]

# Existing vendor categories
existing_categories = set(df["category"].dropna())

# Existing individual event types
existing_events = set(
    df["event_type"]
    .dropna()
    .str.split("|")
    .explode()
    .str.strip()
)

# Find missing categories and events
missing_categories = [
    category for category in required_categories
    if category not in existing_categories
]

missing_events = [
    event for event in required_events
    if event not in existing_events
]

print("\n--- Missing Vendor Categories ---")
print(missing_categories)

print("\n--- Missing Event Types ---")
print(missing_events)

print("\nCategory analysis completed!")
