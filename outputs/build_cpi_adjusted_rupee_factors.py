"""Calculate the MoSPI report's CPI adjustment for rupee-based nutrient factors."""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
CPI_PATH = ROOT / "cpi_food_beverages_official_extracted.csv"
FACTOR_PATH = ROOT / "nutrient_conversion_table_report594.csv"

periods = {
    "2022-23": [f"{year}-{month:02d}" for year, months in [(2022, range(8, 13)), (2023, range(1, 8))] for month in months],
    "2023-24": [f"{year}-{month:02d}" for year, months in [(2023, range(8, 13)), (2024, range(1, 8))] for month in months],
}

with CPI_PATH.open(encoding="utf-8-sig", newline="") as f:
    cpi = {row["Month"]: row for row in csv.DictReader(f)}

reference = cpi["2024-12"]
if reference["Release Status"] != "Provisional":
    raise ValueError("Expected December 2024 CPI reference to be marked provisional")

stats = {}
for period, months in periods.items():
    if len(months) != 12 or any(month not in cpi for month in months):
        raise ValueError(f"Incomplete CPI period {period}")
    if any(cpi[month]["Release Status"] != "Final" for month in months):
        raise ValueError(f"Non-final monthly CPI value in survey period {period}")
    for sector in ("Rural", "Urban"):
        average = sum(float(cpi[month][f"{sector} Index"]) for month in months) / 12
        base = float(reference[f"{sector} Index"])
        stats[(period, sector.lower())] = {"average": average, "base": base, "ratio": base / average}

avg_path = ROOT / "cpi_period_averages_and_deflators.csv"
with avg_path.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Survey period", "Sector", "Months averaged", "Average CPI food-and-beverages index", "Dec 2024 reference index (provisional)", "Reference / survey-average ratio"])
    for period in periods:
        for sector in ("rural", "urban"):
            s = stats[(period, sector)]
            writer.writerow([period, sector.title(), 12, f"{s['average']:.6f}", f"{s['base']:.1f}", f"{s['ratio']:.9f}"])

with FACTOR_PATH.open(encoding="utf-8-sig", newline="") as f:
    factors = list(csv.DictReader(f))
rupee = [row for row in factors if row["unit"].strip().lower() == "re"]
if not rupee:
    raise ValueError("No rupee-denominated nutrient factors found")

out_path = ROOT / "cpi_adjusted_rupee_conversion_factors.csv"
with out_path.open("w", encoding="utf-8-sig", newline="") as f:
    fields = ["serial", "item_code", "item_name", "sector", "survey_period", "reference_unit", "Dec2024_kcal_per_rupee", "Dec2024_protein_g_per_rupee", "Dec2024_fat_g_per_rupee", "CPI_adjustment_ratio", "period_kcal_per_rupee", "period_protein_g_per_rupee", "period_fat_g_per_rupee"]
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for row in rupee:
        label = row["item_name"].lower()
        sector = "rural" if label.endswith("(rural)") else "urban" if label.endswith("(urban)") else None
        if sector is None:
            raise ValueError(f"Cannot determine sector for rupee factor: {row['item_name']}")
        for period in periods:
            ratio = stats[(period, sector)]["ratio"]
            kcal = float(row["kcal_per_unit"])
            protein = float(row["protein_g_per_unit"])
            fat = float(row["fat_g_per_unit"])
            writer.writerow({
                "serial": row["serial"], "item_code": row["item_code"], "item_name": row["item_name"],
                "sector": sector.title(), "survey_period": period, "reference_unit": "rupee",
                "Dec2024_kcal_per_rupee": row["kcal_per_unit"],
                "Dec2024_protein_g_per_rupee": row["protein_g_per_unit"],
                "Dec2024_fat_g_per_rupee": row["fat_g_per_unit"],
                "CPI_adjustment_ratio": f"{ratio:.9f}",
                "period_kcal_per_rupee": f"{kcal * ratio:.9f}",
                "period_protein_g_per_rupee": f"{protein * ratio:.9f}",
                "period_fat_g_per_rupee": f"{fat * ratio:.9f}",
            })

print(f"Wrote {avg_path} ({len(stats)} sector-period rows)")
print(f"Wrote {out_path} ({len(rupee) * len(periods)} adjusted rupee-factor rows)")
for (period, sector), s in stats.items():
    print(f"{period} {sector}: avg CPI={s['average']:.6f}, Dec24/avg={s['ratio']:.9f}")
