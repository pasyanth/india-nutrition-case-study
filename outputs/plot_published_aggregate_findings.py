"""Render simple descriptive PNG figures from validated published-table CSVs."""

from pathlib import Path
import csv
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)
NAVY = (23, 107, 135)
ORANGE = (217, 119, 50)
INK = (38, 48, 56)
MUTED = (95, 104, 111)
GRID = (222, 226, 229)
BG = (255, 255, 255)


def font(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def load_csv(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def f(row, field):
    return float(row[field])


def base(title, subtitle, size=(1400, 720)):
    im = Image.new("RGB", size, BG)
    d = ImageDraw.Draw(im)
    d.text((60, 35), title, fill=INK, font=font(30, True))
    d.text((60, 78), subtitle, fill=MUTED, font=font(16))
    return im, d


def line_chart(draw, box, years, series, yrange, ylabel, valuefmt):
    x0, y0, x1, y1 = box
    lo, hi = yrange
    draw.text((x0, y0 - 45), ylabel, fill=INK, font=font(18, True))
    for i in range(5):
        val = lo + (hi - lo) * i / 4
        y = y1 - (y1 - y0) * i / 4
        draw.line((x0, y, x1, y), fill=GRID, width=1)
        draw.text((x0 - 72, y - 10), valuefmt(val), fill=MUTED, font=font(14))
    xs = [x0 + 100, x1 - 100]
    for x, year in zip(xs, years):
        draw.text((x - 42, y1 + 20), year, fill=MUTED, font=font(15))
    for label, vals, color in series:
        pts = [(xs[i], y1 - (v - lo) / (hi - lo) * (y1 - y0)) for i, v in enumerate(vals)]
        draw.line(pts, fill=color, width=4)
        for (x, y), v in zip(pts, vals):
            draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=color)
            draw.text((x - 30, y - 30), valuefmt(v), fill=color, font=font(15, True))


def national():
    rows = [r for r in load_csv("analysis_ready_nutrition_state_sector.csv") if r["state_ut"] == "All-India"]
    yrs = ["2022-23", "2023-24"]
    im, d = base("Protein and calorie estimates changed little nationally",
                 "MoSPI published household-consumption-based estimates; point values only, no significance test.")
    for box, metric, yrange, ylabel, fmt in (
        ((180, 205, 650, 560), "protein_g_per_capita_per_day", (58, 66), "Protein (g/person/day)", lambda x: f"{x:.1f}"),
        ((900, 205, 1370, 560), "calories_kcal_per_capita_per_day", (2150, 2300), "Calories (kcal/person/day)", lambda x: f"{x:,.0f}"),
    ):
        series = []
        for sector, color in (("Rural", NAVY), ("Urban", ORANGE)):
            vals = [f(next(r for r in rows if r["year"] == y and r["sector"] == sector), metric) for y in yrs]
            series.append((sector, vals, color))
        line_chart(d, box, yrs, series, yrange, ylabel, fmt)
    d.text((180, 630), "Rural", fill=NAVY, font=font(17, True))
    d.line((250, 640, 295, 640), fill=NAVY, width=4)
    d.text((340, 630), "Urban", fill=ORANGE, font=font(17, True))
    d.line((410, 640, 455, 640), fill=ORANGE, width=4)
    im.save(FIG / "national-protein-calories.png")


def mpce():
    rows = load_csv("mpce_fractile_nutrition.csv")
    im, d = base("Bottom and top MPCE fractiles moved in different directions",
                 "Fractiles are separately ranked in each round; the same households are not followed.")
    panels = [
        ((190, 225, 650, 550), "protein_g_per_capita_per_day", (-10, 3), "Protein change (g/person/day)", 1),
        ((900, 225, 1360, 550), "calories_kcal_per_capita_per_day", (-450, 150), "Calorie change (kcal/person/day)", 0),
    ]
    cats = [("Rural", "0-5%"), ("Rural", "95-100%"), ("Urban", "0-5%"), ("Urban", "95-100%")]
    bar_colors = {"0-5%": NAVY, "95-100%": ORANGE}
    for box, metric, (lo, hi), ylabel, decimals in panels:
        x0, y0, x1, y1 = box
        d.text((x0, y0 - 48), ylabel, fill=INK, font=font(18, True))
        yzero = y1 - (0 - lo) / (hi - lo) * (y1 - y0)
        for i in range(5):
            v = lo + (hi - lo) * i / 4
            y = y1 - (v - lo) / (hi - lo) * (y1 - y0)
            d.line((x0, y, x1, y), fill=(130, 135, 140) if abs(v) < 1e-9 else GRID,
                   width=2 if abs(v) < 1e-9 else 1)
            d.text((x0 - 65, y - 10), f"{v:.0f}", fill=MUTED, font=font(14))
        xs = [x0 + 55 + i * ((x1-x0-110)/3) for i in range(4)]
        bar_h = 26
        for x, (sector, fractile) in zip(xs, cats):
            lo_fr = "0-5%" if fractile == "0-5%" else "95-100%"
            current = f(next(r for r in rows if r["mpce_population_fractile"] == lo_fr and r["year"] == "2023-24" and r["sector"] == sector), metric)
            prior = f(next(r for r in rows if r["mpce_population_fractile"] == lo_fr and r["year"] == "2022-23" and r["sector"] == sector), metric)
            delta = current - prior
            xbar = x
            yval = y1 - (delta - lo) / (hi - lo) * (y1-y0)
            left = xbar - 24
            top = min(yzero, yval)
            bottom = max(yzero, yval)
            d.rectangle((left, top, left+48, bottom), fill=bar_colors[fractile])
            label = f"{delta:+.{decimals}f}" if decimals else f"{delta:+,.0f}"
            d.text((left - 4, top - 23 if delta >= 0 else bottom + 4), label,
                   fill=bar_colors[fractile], font=font(14, True))
            d.text((xbar - 35, y1 + 14), sector, fill=INK, font=font(13, True))
            d.text((xbar - 35, y1 + 34), "Bottom 5%" if fractile == "0-5%" else "Top 5%",
                   fill=MUTED, font=font(12))
    d.text((260, 655), "Bottom 5%", fill=NAVY, font=font(16, True)); d.rectangle((235,657,250,672),fill=NAVY)
    d.text((420, 655), "Top 5%", fill=ORANGE, font=font(16, True)); d.rectangle((395,657,410,672),fill=ORANGE)
    im.save(FIG / "mpce-bottom-top-nutrients.png")


def state_scatter():
    rows = [r for r in load_csv("nutrition_changes_by_state_sector.csv") if r["state_ut"] != "All-India"]
    im, d = base("State/UT changes varied across the two survey rounds",
                 "Each mark is one State/UT-sector; published rounded point estimates, without uncertainty intervals.", (1200, 800))
    x0, y0, x1, y1 = 150, 180, 1110, 650
    xmin, xmax, ymin, ymax = -150, 550, -5, 20
    for xv in (-100, 0, 100, 200, 300, 400, 500):
        x=x0+(xv-xmin)/(xmax-xmin)*(x1-x0)
        d.line((x,y0,x,y1),fill=GRID,width=1); d.text((x-22,y1+14),f"{xv:.0f}",fill=MUTED,font=font(14))
    for yv in (-5, 0, 5, 10, 15, 20):
        y=y1-(yv-ymin)/(ymax-ymin)*(y1-y0)
        d.line((x0,y,x1,y),fill=GRID,width=1); d.text((x0-42,y-9),f"{yv:.0f}",fill=MUTED,font=font(14))
    xzero=x0+(0-xmin)/(xmax-xmin)*(x1-x0); yzero=y1-(0-ymin)/(ymax-ymin)*(y1-y0)
    d.line((xzero,y0,xzero,y1),fill=(135,140,144),width=2); d.line((x0,yzero,x1,yzero),fill=(135,140,144),width=2)
    for r in rows:
        xv=f(r,"calories_change_kcal_per_capita_day"); yv=f(r,"protein_change_g_per_capita_day")
        x=x0+(xv-xmin)/(xmax-xmin)*(x1-x0); y=y1-(yv-ymin)/(ymax-ymin)*(y1-y0)
        color=NAVY if r["sector"]=="Rural" else ORANGE
        d.ellipse((x-6,y-6,x+6,y+6),fill=color,outline=BG,width=1)
    d.text((450, 700), "Change in calories (kcal/person/day)", fill=INK, font=font(17, True))
    ylab = Image.new("RGBA", (330, 42), (255, 255, 255, 0))
    ImageDraw.Draw(ylab).text((0, 4), "Change in protein (g/person/day)", fill=INK, font=font(17, True))
    ylab = ylab.rotate(90, expand=True)
    im.paste(ylab, (28, 330), ylab)
    d.text((170, 115), "Rural", fill=NAVY, font=font(16, True)); d.line((225,125,265,125),fill=NAVY,width=4)
    d.text((300, 115), "Urban", fill=ORANGE, font=font(16, True)); d.line((365,125,405,125),fill=ORANGE,width=4)
    im.save(FIG / "state-calorie-protein-changes.png")


if __name__ == "__main__":
    national()
    mpce()
    state_scatter()
    print(f"Wrote figures to {FIG}")
