from pathlib import Path
import pdfplumber

root = Path(__file__).parent / "cpi_sources"
for path in sorted(root.glob("*.pdf")):
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages[:4])
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    print(f"\n### {path.name}")
    for i, line in enumerate(lines):
        if "All-India General" in line or "Food and" in line or "Description" in line and i < 40:
            print(" | ".join(lines[max(0, i-2):i+5]))
