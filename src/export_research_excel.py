
from pathlib import Path
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# Project paths
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "clean" / "vendors_researched_final.csv"
OUTPUT_DIR = ROOT / "deliverables"
OUTPUT_FILE = OUTPUT_DIR / "vendor_research_workbook.xlsx"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load researched vendor dataset
df = pd.read_csv(INPUT_FILE)

# Check required columns
required_columns = [
    "vendor_id",
    "vendor_name",
    "main_category",
    "location",
    "source_url",
    "verification_status"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Create verification tracker
tracker_columns = [
    "vendor_id",
    "vendor_name",
    "main_category",
    "location",
    "source_url",
    "direct_source_url",
    "source_type",
    "verification_status",
    "verified_rating",
    "verified_contact",
    "availability",
    "pricing_type",
    "guest_capacity",
    "verification_notes"
]

tracker = df[
    [col for col in tracker_columns if col in df.columns]
].copy()

# Category and location summary
summary = (
    df.groupby(["main_category", "location"])
    .size()
    .reset_index(name="vendor_count")
)

# Read Me information
readme = pd.DataFrame({
    "Field": [
        "Project",
        "Dataset",
        "Total researched vendors",
        "Target locations",
        "Vendor categories",
        "Synthetic data",
        "Pricing",
        "Availability",
        "Ratings",
        "Verification",
        "Important note"
    ],
    "Description": [
        "EventEase - Vendor Intelligence and Recommendation System",
        "Researched vendor leads",
        len(df),
        "Thane, Maharashtra; Pune, Maharashtra; Bangalore, Karnataka",
        "Catering, Photography, Decoration, Event Planning, Makeup, Entertainment",
        "Research dataset is maintained separately from synthetic recommendation test data.",
        "Unconfirmed prices must not be treated as verified prices.",
        "Unconfirmed availability must not be treated as available.",
        "Listed ratings are not necessarily independently verified.",
        "Public listing matches do not mean all vendor details are verified.",
        "Contact vendors directly before booking."
    ]
})

# Export workbook
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Vendor Research", index=False)
    tracker.to_excel(writer, sheet_name="Verification Tracker", index=False)
    summary.to_excel(writer, sheet_name="Category Summary", index=False)
    readme.to_excel(writer, sheet_name="Read Me", index=False)

    workbook = writer.book

    for worksheet in workbook.worksheets:
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        # Header formatting
        for cell in worksheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(
                start_color="1F4E78",
                end_color="1F4E78",
                fill_type="solid"
            )
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )

        worksheet.row_dimensions[1].height = 30

        # Adjust column widths
        for column in worksheet.columns:
            column_letter = get_column_letter(column[0].column)
            max_length = max(
                len(str(cell.value)) if cell.value is not None else 0
                for cell in column
            )
            worksheet.column_dimensions[column_letter].width = min(
                max(max_length + 3, 14), 45
            )

        # Wrap data cells
        for row in worksheet.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(
                    vertical="top",
                    wrap_text=True
                )

    # Make source URLs clickable
    for sheet_name in ["Vendor Research", "Verification Tracker"]:
        ws = workbook[sheet_name]

        headers = {
            cell.value: cell.column
            for cell in ws[1]
        }

        for url_column in ["source_url", "direct_source_url"]:
            if url_column in headers:
                col_number = headers[url_column]

                for row_number in range(2, ws.max_row + 1):
                    cell = ws.cell(row=row_number, column=col_number)

                    if cell.value and str(cell.value).startswith("http"):
                        cell.hyperlink = str(cell.value)
                        cell.style = "Hyperlink"

print("EVENTEASE EXCEL WORKBOOK CREATED")
print("=================================")
print(f"Total vendors: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Output file: {OUTPUT_FILE}")
print(f"File exists: {OUTPUT_FILE.exists()}")
print("\nWorkbook sheets:")
print("1. Vendor Research")
print("2. Verification Tracker")
print("3. Category Summary")
print("4. Read Me")
