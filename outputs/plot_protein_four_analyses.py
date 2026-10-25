"""Create four protein figures from validated published HCES aggregate tables."""
from pathlib import Path
import csv
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
BLUE = (33, 104, 151)
ORANGE = (218, 126, 52)
INK = (40, 48, 56)
MUTED = (96, 105, 113)
GRID = (222, 226, 229)
BG = (255, 255, 255)


def font(size, bold=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def read_csv(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def base(title, subtitle, size):
    im = Image.new("RGB", size, BG)
    d = ImageDraw.Draw(im)
    d.text((55, 28), title, fill=INK, font=font(30, True))
    d.text((55, 72), subtitle, fill=MUTED, font=font(16))
    return im, d


def xmap(v, lo, hi, x0, x1):
    return x0 + (v - lo) / (hi - lo) * (x1 - x0)


def ymap(v, lo, hi, y0, y1):
    return y1 - (v - lo) / (hi - lo) * (y1 - y0)


def national_protein():
    rows = [r for r in read_csv("analysis_ready_nutrition_state_sector.csv")
            if r["state_ut"] == "All-India"]
    im, d = base("National protein estimates were nearly unchanged",
                 "Published household-consumption-derived estimates; two survey rounds, point values only.",
                 (1250, 690))
    x0, x1, y0, y1 = 205, 1110, 190, 515
    lo, hi = 60, 65
    for tick in range(lo, hi + 1):
        y = ymap(tick, lo, hi, y0, y1)
        d.line((x0, y, x1, y), fill=GRID, width=1)
        d.text((x0 - 43, y - 10), str(tick), fill=MUTED, font=font(15))
    xs = [390, 900]
    years = ["2022-23", "2023-24"]
    for x, year in zip(xs, years):
        d.text((x - 38, y1 + 24), year, fill=INK, font=font(17, True))
    for sector, color in (("Rural", BLUE), ("Urban", ORANGE)):
        vals = [float(next(r for r in rows if r["sector"] == sector and r["year"] == year)
                       ["protein_g_per_capita_per_day"]) for year in years]
        pts = [(xs[i], ymap(v, lo, hi, y0, y1)) for i, v in enumerate(vals)]
        d.line(pts, fill=color, width=5)
        for pt, value in zip(pts, vals):
            x, y = pt
            d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=color)
            d.text((x - 25, y - 35), f"{value:.1f}", fill=color, font=font(18, True))
    d.text((x0, y0 - 36), "Protein (g/person/day)", fill=INK, font=font(18, True))
    d.text((410, 600), "Rural", fill=BLUE, font=font(17, True)); d.line((470, 610, 520, 610), fill=BLUE, width=5)
    d.text((570, 600), "Urban", fill=ORANGE, font=font(17, True)); d.line((640, 610, 690, 610), fill=ORANGE, width=5)
    d.text((55, 650), "Rural: 61.9 → 61.8 (-0.1)     Urban: 63.2 → 63.4 (+0.2)", fill=INK, font=font(16))
    im.save(FIG / "protein-national-rural-urban.png")


def state_changes():
    rows = [r for r in read_csv("nutrition_changes_by_state_sector.csv")
            if r["state_ut"] != "All-India"]
    states = sorted({r["state_ut"] for r in rows},
                    key=lambda s: sum(float(next(r for r in rows if r["state_ut"] == s and r["sector"] == sec)
                                           ["protein_change_g_per_capita_day"]) for sec in ("Rural", "Urban")) / 2)
    w, h = 1480, 1680
    im, d = base("Protein changes varied across States/UTs",
                 "Change in published estimate from 2022-23 to 2023-24; rounded point estimates, no uncertainty intervals.", (w, h))
    x0, x1 = 330, 1300
    lo, hi = -4, 19
    for tick in range(-4, 20, 2):
        x = xmap(tick, lo, hi, x0, x1)
        d.line((x, 140, x, 1550), fill=GRID, width=1)
        d.text((x - 12, 112), str(tick), fill=MUTED, font=font(14))
    zero = xmap(0, lo, hi, x0, x1)
    d.line((zero, 140, zero, 1550), fill=(125, 132, 138), width=2)
    rural_y0, urban_y0 = 180, 900
    step = 18
    for sect, start, color in (("Rural", rural_y0, BLUE), ("Urban", urban_y0, ORANGE)):
        d.text((55, start - 30), sect, fill=color, font=font(21, True))
        for i, state in enumerate(states):
            y = start + i * step
            r = next(r for r in rows if r["state_ut"] == state and r["sector"] == sect)
            delta = float(r["protein_change_g_per_capita_day"])
            x = xmap(delta, lo, hi, x0, x1)
            d.text((55, y - 8), state, fill=INK, font=font(13))
            d.line((zero, y, x, y), fill=color, width=3)
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
            if ((sect == "Rural" and state in ("Sikkim", "Bihar"))
                    or (sect == "Urban" and state in ("Lakshadweep", "Jharkhand"))):
                d.text((x + 8, y - 9), f"{delta:+.1f}", fill=color, font=font(12, True))
    d.text((570, 1600), "Change in protein (g/person/day)", fill=INK, font=font(17, True))
    d.text((55, 1640), "Each sector includes 36 State/UTs. Values describe estimates, not verified state rankings.", fill=MUTED, font=font(14))
    im.save(FIG / "protein-state-changes.png")


def mpce_gradient():
    rows = read_csv("mpce_fractile_nutrition.csv")
    order = ["0-5%", "5-10%", "10-20%", "20-30%", "30-40%", "40-50%",
             "50-60%", "60-70%", "70-80%", "80-90%", "90-95%", "95-100%"]
    im, d = base("Protein estimates rise across MPCE fractiles",
                 "Published per-capita means; fractiles are separately ranked within each survey round.", (1550, 750))
    panels = [("Rural", 170, 755), ("Urban", 875, 1460)]
    lo, hi = 35, 105
    years = [("2022-23", BLUE), ("2023-24", ORANGE)]
    for sector, x0, x1 in panels:
        y0, y1 = 190, 535
        d.text((x0, 135), sector, fill=INK, font=font(20, True))
        for tick in range(40, 101, 10):
            y = ymap(tick, lo, hi, y0, y1)
            d.line((x0, y, x1, y), fill=GRID, width=1)
            d.text((x0 - 38, y - 9), str(tick), fill=MUTED, font=font(13))
        xs = [x0 + i * (x1 - x0) / (len(order) - 1) for i in range(len(order))]
        for year, color in years:
            vals = []
            for fractile in order:
                r = next(r for r in rows if r["year"] == year and r["sector"] == sector
                         and r["mpce_population_fractile"] == fractile)
                vals.append(float(r["protein_g_per_capita_per_day"]))
            pts = [(xs[i], ymap(v, lo, hi, y0, y1)) for i, v in enumerate(vals)]
            d.line(pts, fill=color, width=4)
            for pt, value in zip(pts, vals):
                x, y = pt
                d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=color)
            d.text((x1 - 120, ymap(vals[-1], lo, hi, y0, y1) - 24), f"{year}: {vals[-1]:.1f}",
                   fill=color, font=font(13, True))
        for x, label in zip(xs, order):
            d.text((x - 20, y1 + 12), label, fill=MUTED, font=font(10))
    d.text((500, 630), "MPCE population fractile (lowest to highest)", fill=INK, font=font(17, True))
    d.text((545, 680), "2022-23", fill=BLUE, font=font(15, True)); d.line((620, 690, 670, 690), fill=BLUE, width=4)
    d.text((725, 680), "2023-24", fill=ORANGE, font=font(15, True)); d.line((800, 690, 850, 690), fill=ORANGE, width=4)
    im.save(FIG / "protein-mpce-fractiles.png")


def state_trajectory():
    rows = [r for r in read_csv("nutrition_changes_by_state_sector.csv")
            if r["state_ut"] != "All-India"]
    im, d = base("State starting levels related differently to later protein changes",
                 "Each point is a State/UT; change includes the baseline value, so associations are exploratory.", (1450, 780))
    panels = [("Rural", 190, 680), ("Urban", 820, 1310)]
    xlo, xhi, ylo, yhi = 35, 105, -4, 19
    for sector, x0, x1 in panels:
        y0, y1 = 185, 575
        d.text((x0, 130), sector, fill=INK, font=font(20, True))
        for tick in range(40, 101, 10):
            x = xmap(tick, xlo, xhi, x0, x1)
            d.line((x, y0, x, y1), fill=GRID, width=1)
            d.text((x - 10, y1 + 10), str(tick), fill=MUTED, font=font(12))
        for tick in (-4, 0, 4, 8, 12, 16):
            y = ymap(tick, ylo, yhi, y0, y1)
            d.line((x0, y, x1, y), fill=GRID, width=1)
            d.text((x0 - 28, y - 8), str(tick), fill=MUTED, font=font(12))
        zero_y = ymap(0, ylo, yhi, y0, y1)
        d.line((x0, zero_y, x1, zero_y), fill=(130, 137, 143), width=2)
        subset = [r for r in rows if r["sector"] == sector]
        xs = [float(r["protein_2022_23_g_per_capita_day"]) for r in subset]
        ys = [float(r["protein_change_g_per_capita_day"]) for r in subset]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        slope = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sum((x-mx)**2 for x in xs)
        intercept = my - slope * mx
        for xv in (min(xs), max(xs)):
            yv = intercept + slope * xv
            d.line((xmap(xv, xlo, xhi, x0, x1), ymap(yv, ylo, yhi, y0, y1)), fill=MUTED, width=3)
        for r, xv, yv in zip(subset, xs, ys):
            x, y = xmap(xv, xlo, xhi, x0, x1), ymap(yv, ylo, yhi, y0, y1)
            d.ellipse((x-5, y-5, x+5, y+5), fill=BLUE if sector == "Rural" else ORANGE)
        d.text((x0, 615), f"r = {0.271 if sector == 'Rural' else 0.546:+.3f}; n = 36 states",
               fill=INK, font=font(14, True))
    d.text((390, 690), "2022-23 protein estimate (g/person/day)", fill=INK, font=font(16, True))
    d.text((55, 735), "Vertical axis: change in protein estimate, 2022-23 to 2023-24 (g/person/day). Trend lines are unweighted OLS.", fill=MUTED, font=font(13))
    im.save(FIG / "protein-state-baseline-vs-change.png")


if __name__ == "__main__":
    national_protein()
    state_changes()
    mpce_gradient()
    state_trajectory()
    print(f"Created four protein figures in {FIG}")
