
import pandas as pd

file_path = "data/research/vendor_verification_tracker.csv"

df = pd.read_csv(file_path)

df["verification_notes"] = df["verification_notes"].astype("string")

updates = {
    "RES-041": (
        "Matching Chrizanta Caterers public listing found in Benson Town, Bengaluru. "
        "Public listing rating: 4.8. Catering services listed. "
        "Contact, pricing and exact business identity need further confirmation."
    ),
    "RES-042": (
        "Matching Sri Lakshmi Caterers & Marriage Contractors listing found in Indiranagar, Bengaluru. "
        "Public listing rating: 4.6. Catering and marriage event services listed. "
        "Contact and pricing need further confirmation."
    ),
    "RES-043": (
        "Matching SS Caterers listing found in Bilekahalli, Bengaluru. "
        "Public listing rating: 4.8. Vegetarian event catering services listed. "
        "Contact and pricing need further confirmation."
    ),
    "RES-044": (
        "Matching Iyer Caterers listing found in RT Nagar, Bengaluru. "
        "Public listing rating: 4.9. Vegetarian and wedding catering services listed. "
        "Contact and pricing need further confirmation."
    ),
    "RES-045": (
        "Matching R U Caterers listing found in Subramanyapura, Bengaluru. "
        "Public listing rating: 4.8. Event catering services listed. "
        "Contact and pricing need further confirmation."
    )
}

for vendor_id, note in updates.items():
    mask = df["vendor_id"] == vendor_id
    df.loc[mask, "verification_status"] = (
        "Public listing matched - details pending"
    )
    df.loc[mask, "verification_notes"] = note

df.to_csv(file_path, index=False)

print("Ninth batch tracker updated!")
print(
    df[df["vendor_id"].isin(updates)]
    [["vendor_id", "vendor_name", "verification_status", "verification_notes"]]
    .to_string(index=False)
)
