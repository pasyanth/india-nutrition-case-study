"""Build state/sector/year calorie and protein datasets from NSS Report 594.

Inputs are left untouched. Published table values are extracted from Summary
Statements 1 and 5 in the local MoSPI PDF and protein is cross-checked against
the supplied protein CSV. Requires pypdf (available in the Codex Python bundle).
"""

import csv
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
PDF = ROOT / "Nutritional_Intake_in_India_L.pdf"
PROTEIN_CSV = ROOT / "protein_intake_state_sector_2022_23_2023_24.csv"
OUT = ROOT / "outputs"
YEARS = ("2022-23", "2023-24")
SECTORS = ("Rural", "Urban")
TABLE_ALIASES = {"Andaman & Nicobar Islands": "Andaman & N. Island"}


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def summary_statement(pages, statement_no):
    marker = f"Statement {statement_no}:"
    for page in pages:
        text = page.extract_text() or ""
        if marker in normalize(text):
            return normalize(text)
    raise ValueError(f"Could not find {marker} in report")


def extract_table(text, labels, numeric_count=8):
    """Read rows by known state labels and fixed-length numeric sequences."""
    found = {}
    for label in sorted(labels, key=len, reverse=True):
        printed_label = TABLE_ALIASES.get(label, label)
        match = re.search(
            re.escape(printed_label) + r"\s+((?:\d+(?:\.\d+)?\s+){" + str(numeric_count - 1)
            + r"}\d+(?:\.\d+)?)",
            text,
        )
        if match:
            found[label] = [float(x) for x in match.group(1).split()]
    missing = sorted(set(labels) - set(found))
    if missing:
        raise ValueError(f"Rows not parsed from report table: {missing}")
    return found


def rows_from_table(table):
    rows = []
    for state, vals in table.items():
        for i, year in enumerate(YEARS):
            for j, sector in enumerate(SECTORS):
                rows.append({
                    "state_ut": state,
                    "year": year,
                    "sector": sector,
                    "calories_kcal_per_capita_per_day": vals[i * 2 + j],
                    "calories_kcal_per_consumer_unit_per_day": vals[4 + i * 2 + j],
                })
    return rows


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"No rows to write to {path}")
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    protein = list(csv.DictReader(PROTEIN_CSV.open(encoding="utf-8-sig", newline="")))
    states = sorted({row["state_ut"] for row in protein})
    if len(protein) != 148 or len(states) != 37:
        raise ValueError(f"Unexpected protein dataset size: {len(protein)} rows, {len(states)} states/UTs")

    pages = PdfReader(str(PDF)).pages
    calorie_text = summary_statement(pages, 1)
    protein_text = summary_statement(pages, 5)
    calorie_table = extract_table(calorie_text, states)
    protein_table = extract_table(protein_text, states)

    # Validate every published per-capita protein cell against the supplied file.
    expected = {(r["state_ut"], r["year"], r["sector"]): float(r["protein_g_per_capita_per_day"]) for r in protein}
    for state, vals in protein_table.items():
        for i, year in enumerate(YEARS):
            for j, sector in enumerate(SECTORS):
                key = (state, year, sector)
                if expected.get(key) != vals[i * 2 + j]:
                    raise ValueError(f"Protein CSV does not match Report 594 at {key}: {expected.get(key)} vs {vals[i * 2 + j]}")

    calorie_rows = rows_from_table(calorie_table)
    write_csv(OUT / "calorie_intake_state_sector_2022_23_2023_24.csv", calorie_rows)

    protein_lookup = {(r["state_ut"], r["year"], r["sector"]): r for r in protein}
    combined = []
    for row in calorie_rows:
        p = protein_lookup[(row["state_ut"], row["year"], row["sector"])]
        calories = row["calories_kcal_per_capita_per_day"]
        protein_g = float(p["protein_g_per_capita_per_day"])
        row.update({
            "protein_g_per_capita_per_day": protein_g,
            "protein_g_per_consumer_unit_per_day": float(p["protein_g_per_consumer_unit_per_day"]),
            "protein_to_calorie_ratio_g_per_1000_kcal": round(protein_g / calories * 1000, 4),
            "ratio_interpretation": "ratio of published per-capita means; not mean household/person density",
            "source_report": p["source_report"],
            "calorie_source_statement": "Summary Statement 1",
            "protein_source_statement": "Summary Statement 5",
        })
        combined.append(row)
    write_csv(OUT / "analysis_ready_nutrition_state_sector.csv", combined)

    # Paired descriptive changes across the two published survey estimates.
    lookup = {(r["state_ut"], r["sector"], r["year"]): r for r in combined}
    paired = []
    for state in states:
        for sector in SECTORS:
            a = lookup[(state, sector, YEARS[0])]
            b = lookup[(state, sector, YEARS[1])]
            paired.append({
                "state_ut": state,
                "sector": sector,
                "calories_2022_23_kcal_per_capita_day": a["calories_kcal_per_capita_per_day"],
                "calories_2023_24_kcal_per_capita_day": b["calories_kcal_per_capita_per_day"],
                "calories_change_kcal_per_capita_day": b["calories_kcal_per_capita_per_day"] - a["calories_kcal_per_capita_per_day"],
                "protein_2022_23_g_per_capita_day": a["protein_g_per_capita_per_day"],
                "protein_2023_24_g_per_capita_day": b["protein_g_per_capita_per_day"],
                "protein_change_g_per_capita_day": round(b["protein_g_per_capita_per_day"] - a["protein_g_per_capita_per_day"], 1),
                "protein_ratio_2022_23_g_per_1000_kcal": a["protein_to_calorie_ratio_g_per_1000_kcal"],
                "protein_ratio_2023_24_g_per_1000_kcal": b["protein_to_calorie_ratio_g_per_1000_kcal"],
                "protein_ratio_change_g_per_1000_kcal": round(b["protein_to_calorie_ratio_g_per_1000_kcal"] - a["protein_to_calorie_ratio_g_per_1000_kcal"], 4),
            })
    write_csv(OUT / "nutrition_changes_by_state_sector.csv", paired)

    # Check the report-derived All-India records against the published headline values.
    all_india = {(r["year"], r["sector"]): r for r in combined if r["state_ut"] == "All-India"}
    expected_headlines = {
        ("2022-23", "Rural"): (2233, 61.9), ("2022-23", "Urban"): (2250, 63.2),
        ("2023-24", "Rural"): (2212, 61.8), ("2023-24", "Urban"): (2240, 63.4),
    }
    for key, target in expected_headlines.items():
        actual = (all_india[key]["calories_kcal_per_capita_per_day"], all_india[key]["protein_g_per_capita_per_day"])
        if actual != target:
            raise ValueError(f"All-India published headline check failed for {key}: {actual} != {target}")

    print(f"Protein cells matched report: {len(protein)} / {len(protein)}")
    print(f"Calories extracted: {len(calorie_rows)} rows ({len(states)} states/UTs incl. All-India, 2 years, 2 sectors)")
    print(f"Combined analysis panel: {len(combined)} rows; paired change panel: {len(paired)} rows")
    for key in expected_headlines:
        r = all_india[key]
        print(key, r["calories_kcal_per_capita_per_day"], r["protein_g_per_capita_per_day"], r["protein_to_calorie_ratio_g_per_1000_kcal"])


if __name__ == "__main__":
    main()
