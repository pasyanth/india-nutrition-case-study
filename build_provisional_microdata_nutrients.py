"""Build an explicitly provisional HCES microdata nutrient reconstruction.

This is a diagnostic reproduction attempt, not an official MoSPI estimator.
Food DDM aggregates 092-095 are omitted because the released files have no
sub-item split. See outputs/microdata_reproduction_plan.md.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
ID_POSITIONS = tuple(range(2, 16))
UNRESOLVED = {"092", "093", "094", "095"}
MEAL_CODES = {"076", "280", "281", "282"}
SECTION6_7DAY_CODES = {"003", "004", "005", "011", "092"} | {
    str(code).zfill(3) for code in range(180, 280)
}


def find_csv(folder: str, prefix: str) -> Path:
    paths = [p for p in (ROOT / folder).rglob("*.csv") if p.name.lower().startswith(prefix.lower())]
    if len(paths) != 1:
        raise FileNotFoundError(f"Expected one {prefix} in {folder}; got {len(paths)}")
    return paths[0]


def norm(v: str) -> str:
    v = (v or "").strip()
    if v.endswith(".0") and v[:-2].isdigit():
        v = v[:-2]
    return (v.lstrip("0") or "0") if v.isdigit() else v


def key(row: list[str]) -> tuple[str, ...]:
    return tuple(norm(row[i]) for i in ID_POSITIONS)


def idx(headers: list[str], *names: str) -> int:
    lookup = {h.lower(): i for i, h in enumerate(headers)}
    for name in names:
        if name.lower() in lookup:
            return lookup[name.lower()]
    raise KeyError(f"Missing expected column among {names}")


def number(value: str) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def load_factors() -> tuple[dict, dict]:
    factors: dict[str, dict] = {}
    for r in csv.DictReader((OUT / "nutrient_conversion_table_report594.csv").open(encoding="utf-8-sig", newline="")):
        factors.setdefault(r["item_code"].zfill(3), r)
    adjusted = {}
    for r in csv.DictReader((OUT / "cpi_adjusted_rupee_conversion_factors.csv").open(encoding="utf-8-sig", newline="")):
        adjusted[(r["item_code"].zfill(3), r["sector"], r["survey_period"])] = r
    crosswalk = {}
    for r in csv.DictReader((OUT / "nutrient_code_crosswalk.csv").open(encoding="utf-8-sig", newline="")):
        if r["decision"] == "map_to_factor":
            crosswalk[r["observed_item_code"].zfill(3)] = r["Report594_factor_code"].zfill(3)
    return factors, (adjusted, crosswalk)


def nutrient_for(code: str, sector: str, period: str, qty: float, value: float,
                 factors: dict, adjusted: dict) -> tuple[float, float, float] | None:
    if code in UNRESOLVED:
        return None
    factor_code = adjusted[1].get(code, code)
    row = factors.get(factor_code)
    if row is None:
        return None
    unit = row["unit"].lower()
    if unit == "re":
        conv = adjusted[0].get((factor_code, sector, period))
        if not conv:
            return None
        return tuple(value * float(conv[k]) for k in (
            "period_kcal_per_rupee", "period_protein_g_per_rupee", "period_fat_g_per_rupee"))
    # Table 2.2 quantities are kg, g, litres, or counts as named by the item.
    amount = qty
    if not amount and value and unit in {"kg", "gm", "litre", "no"}:
        # Quantity is required for physical-unit nutrient factors; value alone
        # is deliberately not converted into an invented quantity.
        amount = 0.0
    return (amount * float(row["kcal_per_unit"]),
            amount * float(row["protein_g_per_unit"]),
            amount * float(row["fat_g_per_unit"]))


def read_rows(path: Path):
    stream = path.open(encoding="utf-8-sig", newline="")
    reader = csv.reader(stream)
    headers = next(reader)
    return stream, reader, headers


def build_year(folder: str, period: str, factors: dict, adjusted: dict, crosswalk: dict,
               state_names: dict[str, str]) -> list[dict]:
    # FDQ household particulars are the denominator and source of the annual weight.
    hh_path = find_csv(folder, "LEVEL - 03")
    households = {}
    with hh_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f); h = next(reader)
        size_i = idx(h, "HH_Size_FDQ", "b2q2pt1")
        weight_i = idx(h, "Multiplier", "mult")
        state_i, sector_i = idx(h, "State", "state"), idx(h, "Sector", "sector")
        for row in reader:
            households[key(row)] = {
                "size": number(row[size_i]), "weight": number(row[weight_i]),
                "state": row[state_i].strip().zfill(2), "sector": row[sector_i].strip(),
            }

    nutrient = defaultdict(lambda: [0.0, 0.0, 0.0])
    coverage = defaultdict(int)
    unresolved_rows = defaultdict(int)
    # 30-day FDQ Section 5/6.
    specs = [
        ("LEVEL - 05", ("Item_Code", "b5pt1q2"), ("Total_Consumption_Quantity", "b5pt1q5"),
         ("Total_Consumption_Value", "b5pt1q6"), 1.0),
        ("LEVEL - 06", ("Item_Code", "b7pt1q2"), ("Total_Consumption_Quantity", "b7pt1q3"),
         ("Total_Consumption_Value", "b7pt1q4"), 30.0 / 7.0),
        ("LEVEL - 10", ("Item_Code_12_series", "b12pt1q2"),
         ("Total_Consumption_Quantity_12_se", "b12pt1q5"),
         ("Total_Consumption_Value_12_serie", "b12pt1q6"), 30.0 / 7.0),
    ]
    for prefix, item_names, qty_names, value_names, scale in specs:
        path = find_csv(folder, prefix)
        stream, reader, h = read_rows(path)
        try:
            item_i, qty_i, val_i = idx(h, *item_names), idx(h, *qty_names), idx(h, *value_names)
            for row in reader:
                k = key(row)
                if k not in households:
                    continue
                code = row[item_i].strip().zfill(3)
                # Meal counts are included only through the Report 594 meal adjustment.
                if code in MEAL_CODES:
                    continue
                if code in UNRESOLVED:
                    unresolved_rows[code] += 1
                    continue
                row_scale = scale
                # Level 05 combines Sections 5 (30-day) and 6 (7-day).
                # Section 6 item codes need the same 30/7 expansion as Section 7.
                if prefix == "LEVEL - 05" and code in SECTION6_7DAY_CODES:
                    row_scale *= 30.0 / 7.0
                try:
                    vals = nutrient_for(code, households[k]["sector"], period,
                                        number(row[qty_i]) * row_scale, number(row[val_i]) * row_scale,
                                        factors, (adjusted, crosswalk))
                except (ValueError, KeyError):
                    vals = None
                if vals is None:
                    continue
                for i, v in enumerate(vals):
                    nutrient[k][i] += v
                coverage[code] += 1
        finally:
            stream.close()
        print(f"{period}: processed {prefix} ({len(coverage):,} matched item codes so far)", flush=True)

    # Meals outside the home (X), at-home meals (B), and meals served (A).
    away = defaultdict(lambda: [0.0, 0.0, 0.0])
    at_home = defaultdict(float)
    path = find_csv(folder, "LEVEL - 02")
    stream, reader, h = read_rows(path)
    try:
        member_i = idx(h, "FDQ_Original_Member", "fdq")
        home_i = idx(h, "Meals_At_Home", "b3q16")
        school_i = idx(h, "Meals_From_School", "b3q12")
        employer_i = idx(h, "Meals_From_Employer", "b3q13")
        other_i = idx(h, "Meals_Other", "b3q14")
        paid_i = idx(h, "Meals_On_Payment", "b3q15")
        for row in reader:
            if norm(row[member_i]) != "1":
                continue
            k = key(row)
            if k not in households:
                continue
            at_home[k] += number(row[home_i])
            # Mapping follows the Section 3 source categories to the report's
            # meal factors: school/other assistance=282, employer=281, paid=280.
            meals = ((school_i, "282"), (employer_i, "281"),
                     (other_i, "282"), (paid_i, "280"))
            for col, code in meals:
                n = number(row[col])
                fac = factors[code]
                for j, colname in enumerate(("kcal_per_unit", "protein_g_per_unit", "fat_g_per_unit")):
                    away[k][j] += n * float(fac[colname])
    finally:
        stream.close()

    path = find_csv(folder, "LEVEL - 04")
    served = defaultdict(float)
    stream, reader, h = read_rows(path)
    try:
        served_i = idx(h, "Meals_Served_to_Non_HH_Members", "b4pt1415")
        for row in reader:
            k = key(row)
            if k in households:
                served[k] += number(row[served_i])
    finally:
        stream.close()

    results = []
    for k, hh in households.items():
        size, weight = hh["size"], hh["weight"]
        if size <= 0 or weight <= 0:
            continue
        a, b = served[k], at_home[k]
        total_g = nutrient[k]
        # G* = G * B/(A+B), then add away-from-home meal nutrients X.
        ratio = b / (a + b) if a + b > 0 else 1.0
        adj = [total_g[i] * ratio + away[k][i] for i in range(3)]
        results.append({
            "period": period, "state_code": hh["state"], "sector_code": hh["sector"],
            "fsu": k[0], "stratum": k[5], "household_size_fdq": size,
            "fdq_multiplier": weight, "meals_served_nonhousehold": a,
            "meals_at_home_fdq_members": b,
            "calorie_kcal_person_day": adj[0] / (30 * size),
            "protein_g_person_day": adj[1] / (30 * size),
            "fat_g_person_day": adj[2] / (30 * size),
        })
    print(f"{period}: households={len(results):,}; unresolved item rows="
          f"{sum(unresolved_rows.values()):,}; excluded codes={','.join(sorted(UNRESOLVED))}", flush=True)
    return results


def main() -> None:
    factors, (adjusted, crosswalk) = load_factors()
    state_names = {}
    try:
        from openpyxl import load_workbook
        ws = load_workbook(ROOT / "tabulation_state_code_2.xlsx", read_only=True, data_only=True).active
        state_names = {str(r[0]).zfill(2): str(r[1]) for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None}
    except Exception:
        pass
    data = build_year("CSV_data_HH_Cons_exp_22_23", "2022-23", factors, adjusted, crosswalk, state_names)
    data += build_year("HCES_Data_2023-24_Csv", "2023-24", factors, adjusted, crosswalk, state_names)
    household_path = OUT / "provisional_microdata_nutrient_households.csv"
    fields = list(data[0])
    with household_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(data)

    accum = defaultdict(lambda: [0.0] * 5)
    for r in data:
        domains = [(r["period"], r["sector_code"]), (r["period"], "All")]
        for domain in domains:
            a = accum[domain]; w = r["fdq_multiplier"]
            a[0] += w * r["household_size_fdq"]
            a[1] += w
            a[2] += w * r["calorie_kcal_person_day"] * r["household_size_fdq"]
            a[3] += w * r["protein_g_person_day"] * r["household_size_fdq"]
            a[4] += w * r["fat_g_person_day"] * r["household_size_fdq"]
    summary = []
    for (period, sector), a in sorted(accum.items()):
        summary.append({"period": period, "sector": sector,
                        "households_unweighted": sum(1 for r in data if r["period"] == period and (sector == "All" or r["sector_code"] == sector)),
                        "calories_kcal_person_day": a[2] / a[0],
                        "protein_g_person_day": a[3] / a[0], "fat_g_person_day": a[4] / a[0]})
    with (OUT / "provisional_microdata_nutrient_summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0])); w.writeheader(); w.writerows(summary)
    print(f"Wrote {len(data):,} household records and {len(summary)} weighted domain summaries.", flush=True)


if __name__ == "__main__":
    main()
