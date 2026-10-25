from pathlib import Path
import pdfplumber

pdf_path = Path(__file__).parents[1] / "Nutritional_Intake_in_India_L.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for page_no, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ""
        low = text.lower()
        if "cpi" in low or "price index" in low or "price change" in low:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            relevant = [line for line in lines if any(k in line.lower() for k in ["cpi", "price index", "price change", "rupee", "inflation"])]
            if relevant:
                print(f"PAGE {page_no}: " + " | ".join(relevant[:12]))
