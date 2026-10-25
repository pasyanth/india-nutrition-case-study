"""Audit the HCES item codes against MoSPI Report 594's nutrient conversion table."""

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PDF = ROOT / "Nutritional_Intake_in_India_L.pdf"
OUT = ROOT / "outputs"


def csv_file(folder, starts):
    files = [p for p in (ROOT / folder).rglob("*.csv") if p.name.lower().startswith(starts.lower())]
    if len(files) != 1:
        raise FileNotFoundError(f"Expected one {starts} in {folder}; got {len(files)}")
    return files[0]


def nutrient_table():
    pdf = PdfReader(str(PDF))
    text = "\n".join((pdf.pages[i].extract_text() or "") for i in range(39, 45))
    starts = list(re.finditer(r"(?m)^\s*(\d{1,3})\.\s+(\d{3})\s+", text))
    entries = []
    value_pat = re.compile(r"\s+(kg\.?|gm\.?|litre|no\.?|Re\.?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", re.I)
    for i, m in enumerate(starts):
        serial, code = int(m.group(1)), m.group(2)
        segment = text[m.end():starts[i + 1].start() if i + 1 < len(starts) else len(text)]
        # Page headers/footers may trail the row; find the final unit-and-three-values sequence.
        matches = list(value_pat.finditer(segment))
        if not matches:
            # The text extractor sometimes leaves a page footer after the final value.
            matches = list(re.finditer(r"\s+(kg\.?|gm\.?|litre|no\.?|Re\.?)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?=\s|$)", segment, re.I))
        if not matches:
            raise ValueError(f"Could not parse nutrient conversion row {serial}, code {code}: {segment[:250]!r}")
        value_match = matches[-1]
        name = re.sub(r"\s+", " ", segment[:value_match.start()]).strip()
        unit = value_match.group(1).lower().rstrip(".")
        entries.append({
            "serial": serial, "item_code": code, "item_name": name, "unit": unit,
            "kcal_per_unit": float(value_match.group(2)),
            "protein_g_per_unit": float(value_match.group(3)),
            "fat_g_per_unit": float(value_match.group(4)),
        })
    if len(entries) != 176 or {e["serial"] for e in entries} != set(range(1, 177)):
        raise ValueError(f"Unexpected nutrient table parse: {len(entries)} entries")
    return entries


def inspect_food_file(path, item_field, qty_field, value_field):
    counts = Counter()
    qty_nonblank = Counter()
    value_nonblank = Counter()
    n = 0
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n += 1
            code = row[item_field].strip().zfill(3)
            counts[code] += 1
            if row[qty_field].strip():
                qty_nonblank[code] += 1
            if row[value_field].strip():
                value_nonblank[code] += 1
    return n, counts, qty_nonblank, value_nonblank


def main():
    entries = nutrient_table()
    with (OUT / "nutrient_conversion_table_report594.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(entries[0]))
        writer.writeheader()
        writer.writerows(entries)
    table_codes = {e["item_code"] for e in entries}
    result = []
    for year, folder in (("2022-23", "CSV_data_HH_Cons_exp_22_23"), ("2023-24", "HCES_Data_2023-24_Csv")):
        layout = "legacy" if year == "2022-23" else "modern"
        for prefix, group, item, qty, value in (
            ("LEVEL - 05", "FDQ sections 5-6", "b5pt1q2" if layout == "legacy" else "Item_Code",
             "b5pt1q5" if layout == "legacy" else "Total_Consumption_Quantity",
             "b5pt1q6" if layout == "legacy" else "Total_Consumption_Value"),
            ("LEVEL - 06", "FDQ section 7", "b7pt1q2" if layout == "legacy" else "Item_Code",
             "b7pt1q3" if layout == "legacy" else "Total_Consumption_Quantity",
             "b7pt1q4" if layout == "legacy" else "Total_Consumption_Value"),
            ("LEVEL - 10", "CSQ section 12", "b12pt1q2" if layout == "legacy" else "Item_Code_12_series",
             "b12pt1q5" if layout == "legacy" else "Total_Consumption_Quantity_12_se",
             "b12pt1q6" if layout == "legacy" else "Total_Consumption_Value_12_serie"),
        ):
            path = csv_file(folder, prefix)
            n, counts, qty_present, value_present = inspect_food_file(path, item, qty, value)
            unmatched = sorted(code for code in counts if code not in table_codes and code.strip("0"))
            result.append({
                "year": year, "file_group": group, "records": n,
                "unique_codes": len(counts), "codes_matched_to_conversion_table": len(set(counts) & table_codes),
                "unmatched_codes": ";".join(unmatched),
                "records_with_quantity": sum(qty_present.values()),
                "records_with_value": sum(value_present.values()),
            })
    with (OUT / "microdata_nutrient_input_audit.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(result[0]))
        writer.writeheader()
        writer.writerows(result)
    print(f"Parsed nutrient conversion table rows: {len(entries)}; distinct item codes: {len(table_codes)}")
    for r in result:
        print(r)


if __name__ == "__main__":
    main()
