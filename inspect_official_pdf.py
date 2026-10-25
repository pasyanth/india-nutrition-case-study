import sys
import json
import re
from pathlib import Path

# Paths
pdf_path = Path(r"C:/Users/pragn/.gemini/antigravity/scratch/india_nutrition_case_study/Nutritional_Intake_in_India_L.pdf")
output_dir = Path(r"C:/Users/pragn/.gemini/antigravity/scratch/india_nutrition_case_study/outputs")
output_file = output_dir / "official_pdf_table_search.txt"

# Ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# Phrases to look for (case‑insensitive)
phrases = [
    r"Statement\s*5",
    r"Average daily protein intake per capita",
    r"per consumer unit",
    r"State/UT",
]

def find_matches(text, page_num):
    matches = []
    # Split text into lines preserving line numbers
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for pat in phrases:
            if re.search(pat, line, re.I):
                # Capture a few surrounding lines for context
                start = max(i - 2, 0)
                end = min(i + 3, len(lines))
                snippet = "\n".join(lines[start:end])
                matches.append({
                    "phrase": pat,
                    "page": page_num,
                    "line_idx": i + 1,  # 1‑based line number within page text
                    "snippet": snippet,
                })
    return matches

try:
    import pdfplumber
except ImportError as e:
    print("pdfplumber not available", file=sys.stderr)
    sys.exit(1)

if not pdf_path.is_file():
    print(f"PDF not found at {pdf_path}", file=sys.stderr)
    sys.exit(1)

# Open PDF with pdfplumber
with pdfplumber.open(str(pdf_path)) as pdf:
    all_matches = []
    for idx, page in enumerate(pdf.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            print(f"Failed to extract text from page {idx}: {exc}", file=sys.stderr)
            continue
        page_matches = find_matches(text, idx)
        if page_matches:
            all_matches.extend(page_matches)

# Prepare output
output_lines = []
if all_matches:
    for m in all_matches:
        output_lines.append(
            f"---\nPage (PDF internal number): {m['page']}\nMatched phrase regex: {m['phrase']}\nSnippet:\n{m['snippet']}\n"
        )
else:
    output_lines.append("No matching phrases were found in the PDF.")

result_text = "\n".join(output_lines)

# Write to file
output_file.write_text(result_text, encoding="utf-8")

# Also print to stdout for immediate visibility
sys.stdout.reconfigure(encoding='utf-8')
print(result_text)
