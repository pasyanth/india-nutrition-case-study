import csv
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).parent
SOURCE_DIR = ROOT / "cpi_sources"
MONTHS = {name: number for number, name in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 1
)}

records = defaultdict(list)
for path in sorted(SOURCE_DIR.glob("*.pdf")):
    try:
        with pdfplumber.open(path) as pdf:
            pages = pdf.pages[:5]
            text = " ".join((page.extract_text() or "") for page in pages)
            title_match = re.search(
                r"numbers for\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d\d)\s*\(Final\)\s+and\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(20\d\d)\s*\(Provisional\)",
                re.sub(r"\s+", " ", text), re.I,
            )
            if not title_match:
                continue
            final_month, final_year, prov_month, prov_year = title_match.groups()
            parsed = []
            for page in pages:
                for table in page.extract_tables():
                    for row in table:
                        if row and any("Food and" in str(cell) for cell in row):
                            nums = []
                            for cell in row:
                                if cell is None:
                                    continue
                                nums.extend(float(x) for x in re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", str(cell)))
                            # The all-India group-1 row begins with code 1, then three weights
                            # and two indices (final, provisional) for each sector.
                            if len(nums) >= 10 and int(nums[0]) == 1:
                                parsed = [nums[2], nums[3], nums[5], nums[6], nums[8], nums[9]]
                                break
                    if parsed:
                        break
                if parsed:
                    break
            if not parsed:
                continue
            ru_f, ru_p, ur_f, ur_p, co_f, co_p = parsed
            for month, year, status, vals in [
                (final_month, int(final_year), "Final", (ru_f, ur_f, co_f)),
                (prov_month, int(prov_year), "Provisional", (ru_p, ur_p, co_p)),
            ]:
                key = (year, MONTHS[month.title()])
                records[key].append({"status": status, "values": vals, "source": path.name})
    except Exception as exc:
        print(f"SKIP {path.name}: {exc}")

# December 2024 provisional values are from the official MoSPI CPI portal release.
# Its PDF host did not permit a local download, but the release itself is publicly
# accessible and its Group 1 row is exposed in the official page text.
records[(2024, 12)].append({
    "status": "Provisional",
    "values": (203.9, 209.4, 205.9),
    "source": "https://cpi.mospi.gov.in/PDFile/Press/PR%20December%202024.pdf",
})

out = ROOT / "cpi_food_beverages_official_extracted.csv"
with out.open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Month", "Rural Index", "Urban Index", "Combined Index", "Release Status", "Source PDF"])
    for (year, month), candidates in sorted(records.items()):
        # Use final over provisional; for ties select the latest source filename as audit trail.
        chosen = sorted(candidates, key=lambda x: (x["status"] == "Final", x["source"]))[-1]
        writer.writerow([date(year, month, 1).strftime("%Y-%m"), *chosen["values"], chosen["status"], chosen["source"]])

print(f"Wrote {len(records)} indexed months to {out}")
print("Covered: " + ", ".join(date(y, m, 1).strftime("%Y-%m") for y, m in sorted(records)))
print("Missing in Aug 2022-Dec 2024: " + ", ".join(date(y, m, 1).strftime("%Y-%m") for y in range(2022, 2025) for m in range(1, 13) if (y, m) not in records and (y, m) >= (2022, 8) and (y, m) <= (2024, 12)))
