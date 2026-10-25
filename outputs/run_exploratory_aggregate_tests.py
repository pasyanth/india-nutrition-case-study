"""Exploratory tests on published HCES state/sector and MPCE aggregate tables.

These tests describe patterns among published aggregate cells. They are not
survey-design-adjusted population inference and must not be read as such.
Uses only Python's standard library.
"""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def mean(xs):
    return sum(xs) / len(xs)


def variance(xs):
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def ranks(xs):
    order = sorted(range(len(xs)), key=xs.__getitem__)
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and xs[order[j]] == xs[order[i]]:
            j += 1
        r = ((i + 1) + j) / 2.0
        for k in range(i, j):
            out[order[k]] = r
        i = j
    return out


def corr(xs, ys):
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den


def betacf(a, b, x):
    # Continued fraction for the incomplete beta function.
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    tiny = 1e-300
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 301):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-14:
            break
    return h


def regularized_beta(x, a, b):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t, df):
    x = df / (df + t * t)
    return regularized_beta(x, df / 2.0, 0.5)


def one_sample_t(xs):
    n = len(xs)
    m = mean(xs)
    se = math.sqrt(variance(xs) / n)
    t = m / se
    return m, se, t, n - 1, t_two_sided_p(t, n - 1)


def correlation_test(xs, ys, rank=False):
    if rank:
        xs, ys = ranks(xs), ranks(ys)
    r = corr(xs, ys)
    n = len(xs)
    if rank and abs(abs(r) - 1.0) < 1e-12:
        # Exact two-sided permutation p for a perfect rank ordering with no ties.
        return r, n - 2, min(1.0, 2.0 / math.factorial(n))
    t = r * math.sqrt((n - 2) / max(1e-300, 1 - r * r))
    return r, n - 2, t_two_sided_p(t, n - 2)


def holm_adjust(rows):
    ordered = sorted(enumerate(rows), key=lambda x: x[1]["p_value"])
    m = len(rows)
    running = 0.0
    for rank, (idx, row) in enumerate(ordered):
        adj = min(1.0, (m - rank) * row["p_value"])
        running = max(running, adj)
        rows[idx]["holm_p_within_family"] = running


def label(metric, sector, population, method, n, estimate, se, stat, df, p, family):
    return {"test_family": family, "metric": metric, "sector": sector,
            "population_or_groups": population, "method": method, "n": n,
            "estimate": estimate, "standard_error_or_naive_se": se,
            "test_statistic": stat, "df": df, "p_value": p,
            "holm_p_within_family": ""}


state = [r for r in read_csv(ROOT / "nutrition_changes_by_state_sector.csv")
         if r["state_ut"] != "All-India"]
mpce = read_csv(ROOT / "mpce_fractile_nutrition.csv")
fractile_order = ["0-5%", "5-10%", "10-20%", "20-30%", "30-40%", "40-50%",
                  "50-60%", "60-70%", "70-80%", "80-90%", "90-95%", "95-100%"]
mpce = [r for r in mpce if r["mpce_population_fractile"] in fractile_order]
results = []

# One-sample tests on the 36 State/UT displayed point-estimate changes.
for sector in ("Rural", "Urban"):
    rows = [r for r in state if r["sector"] == sector]
    for metric, col in (("calories_change_kcal_per_capita_day", "calorie"),
                        ("protein_change_g_per_capita_day", "protein")):
        vals = [float(r[metric]) for r in rows]
        m, se, t, df, p = one_sample_t(vals)
        results.append(label(col, sector, "36 State/UT published changes",
                             "one-sample t-test of mean state change = 0", len(vals),
                             m, se, t, df, p, "state_change_tests"))

# Spearman rank association between MPCE fractile rank and published group means.
for year, suffix in (("2022-23", "2022_23"), ("2023-24", "2023_24")):
    for sector in ("Rural", "Urban"):
        rows = [r for r in mpce if r["year"] == year and r["sector"] == sector]
        rows.sort(key=lambda r: fractile_order.index(r["mpce_population_fractile"]))
        x = list(range(1, 13))
        for metric, column in (("calories", "calories_kcal_per_capita_per_day"),
                               ("protein", "protein_g_per_capita_per_day")):
            y = [float(r[column]) for r in rows]
            rho, df, p = correlation_test(x, y, rank=True)
            results.append(label(metric, sector, f"12 MPCE fractile means, {year}",
                                 "Spearman rank correlation; t approximation for p", len(y),
                                 rho, "", rho, df, p, "mpce_gradient_tests"))

# Association between state-level calorie and protein changes within each sector.
for sector in ("Rural", "Urban"):
    rows = [r for r in state if r["sector"] == sector]
    x = [float(r["calories_change_kcal_per_capita_day"]) for r in rows]
    y = [float(r["protein_change_g_per_capita_day"]) for r in rows]
    r, df, p = correlation_test(x, y, rank=False)
    results.append(label("calorie-protein co-change (Pearson r)", sector,
                         "36 State/UT change pairs", "Pearson correlation; t approximation for p",
                         len(x), r, "", r, df, p, "state_comovement_tests"))

# State starting level versus change: descriptive trajectory diagnostic only.
for sector in ("Rural", "Urban"):
    rows = [r for r in state if r["sector"] == sector]
    baseline = [float(r["protein_2022_23_g_per_capita_day"]) for r in rows]
    change = [float(r["protein_change_g_per_capita_day"]) for r in rows]
    for method, ranked in (("Pearson correlation; t approximation for p", False),
                           ("Spearman rank correlation; t approximation for p", True)):
        r, df, p = correlation_test(baseline, change, rank=ranked)
        results.append(label("baseline protein vs protein change", sector,
                             "36 State/UT point estimates", method, len(rows),
                             r, "", r, df, p, "state_trajectory_tests"))

for family in ("state_change_tests", "mpce_gradient_tests", "state_comovement_tests",
               "state_trajectory_tests"):
    fam = [r for r in results if r["test_family"] == family]
    holm_adjust(fam)

out = ROOT / "exploratory_aggregate_test_results.csv"
with out.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(results[0]))
    writer.writeheader()
    writer.writerows(results)

print(f"Wrote {out}")
for r in results:
    print(r["test_family"], r["metric"], r["sector"],
          f"estimate={r['estimate']:.4f}", f"p={r['p_value']:.5g}",
          f"Holm={float(r['holm_p_within_family']):.5g}")
