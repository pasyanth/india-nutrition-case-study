"""Extract comparable MPCE-fractile protein and calorie tables from MoSPI Report 594."""

import csv
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
PDF = ROOT / "Nutritional_Intake_in_India_L.pdf"
OUT = ROOT / "outputs"
YEARS = ("2022-23", "2023-24")
SECTORS = ("Rural", "Urban")
FRACTILES = ("0-5%", "5-10%", "10-20%", "20-30%", "30-40%", "40-50%",
             "50-60%", "60-70%", "70-80%", "80-90%", "90-95%", "95-100%", "All-India")


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def page_with_table(pages, table_name):
    for page in pages:
        text = normalize(page.extract_text() or "")
        if table_name in text:
            return text
    raise ValueError(f"Could not find {table_name}")


def extract_rows(text, table_name):
    # Limit parsing to the named table, preventing a duplicate row elsewhere in the page.
    start = text.index(table_name)
    body = text[start:]
    rows = {}
    for fractile in FRACTILES:
        match = re.search(
            re.escape(fractile) + r"\s+((?:\d+(?:\.\d+)?\s+){7}\d+(?:\.\d+)?)",
            body,
        )
        if not match:
            raise ValueError(f"Could not parse row {fractile} in {table_name}")
        rows[fractile] = [float(v) for v in match.group(1).split()]
    return rows


def as_records(table, variable, unit):
    result = []
    for fractile, values in table.items():
        for year_index, year in enumerate(YEARS):
            for sector_index, sector in enumerate(SECTORS):
                result.append({
                    "mpce_population_fractile": fractile,
                    "year": year,
                    "sector": sector,
                    f"{variable}_{unit}_per_capita_per_day": values[year_index * 2 + sector_index],
                    f"{variable}_{unit}_per_consumer_unit_per_day": values[4 + year_index * 2 + sector_index],
                })
    return result


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    pages = PdfReader(str(PDF)).pages
    calorie_rows = as_records(
        extract_rows(page_with_table(pages, "Table 3.2:"), "Table 3.2:"),
        "calories", "kcal",
    )
    protein_rows = as_records(
        extract_rows(page_with_table(pages, "Table 3.9"), "Table 3.9"),
        "protein", "g",
    )
    c = {(r["mpce_population_fractile"], r["year"], r["sector"]): r for r in calorie_rows}
    p = {(r["mpce_population_fractile"], r["year"], r["sector"]): r for r in protein_rows}
    merged = []
    for key in c:
        merged.append({**c[key], **p[key],
                       "source_report": "NSS Report No. 594: Nutritional Intake in India (2022-23 & 2023-24)",
                       "calorie_source_table": "Table 3.2",
                       "protein_source_table": "Table 3.9"})

    # Cross-check the all-India row against the previously validated state/sector panel.
    aggregate_path = OUT / "analysis_ready_nutrition_state_sector.csv"
    aggregate = list(csv.DictReader(aggregate_path.open(encoding="utf-8-sig", newline="")))
    a = {(r["year"], r["sector"]): r for r in aggregate if r["state_ut"] == "All-India"}
    all_india = [r for r in merged if r["mpce_population_fractile"] == "All-India"]
    for r in all_india:
        key = (r["year"], r["sector"])
        if r["calories_kcal_per_capita_per_day"] != float(a[key]["calories_kcal_per_capita_per_day"]):
            raise ValueError(f"Calorie all-India check failed for {key}")
        if r["protein_g_per_capita_per_day"] != float(a[key]["protein_g_per_capita_per_day"]):
            raise ValueError(f"Protein all-India check failed for {key}")

    # Pair each fractile and sector across the two survey years.
    lookup = {(r["mpce_population_fractile"], r["sector"], r["year"]): r for r in merged}
    changes = []
    for fractile in FRACTILES:
        for sector in SECTORS:
            before = lookup[(fractile, sector, YEARS[0])]
            after = lookup[(fractile, sector, YEARS[1])]
            changes.append({
                "mpce_population_fractile": fractile,
                "sector": sector,
                "calories_2022_23_kcal_per_capita_day": before["calories_kcal_per_capita_per_day"],
                "calories_2023_24_kcal_per_capita_day": after["calories_kcal_per_capita_per_day"],
                "calories_change_kcal_per_capita_day": after["calories_kcal_per_capita_per_day"] - before["calories_kcal_per_capita_per_day"],
                "protein_2022_23_g_per_capita_day": before["protein_g_per_capita_per_day"],
                "protein_2023_24_g_per_capita_day": after["protein_g_per_capita_per_day"],
                "protein_change_g_per_capita_day": round(after["protein_g_per_capita_per_day"] - before["protein_g_per_capita_per_day"], 1),
            })
    write_csv(OUT / "mpce_fractile_nutrition.csv", merged)
    write_csv(OUT / "mpce_fractile_nutrition_changes.csv", changes)

    print(f"MPCE fractile panel: {len(merged)} rows ({len(FRACTILES)} fractiles incl. All-India × 2 sectors × 2 years)")
    print("All-India calorie/protein rows match the validated state/sector dataset.")


if __name__ == "__main__":
    main()
