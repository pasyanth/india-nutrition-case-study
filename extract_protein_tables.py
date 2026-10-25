import sys, re, json
from pathlib import Path

pdf_path = Path(r'C:/Users/pragn/.gemini/antigravity/brain/5b6e2196-2e59-4bf6-a26f-5f2833e01dd1/.tempmediaStorage/e52b082833b1170b.pdf')

try:
    import PyPDF2
except ImportError:
    print('PyPDF2 not available', file=sys.stderr)
    sys.exit(1)

reader = PyPDF2.PdfReader(str(pdf_path))
results = []
for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    if re.search(r'protein', text, re.I):
        # capture a snippet around protein mentions
        snippet = '\n'.join(line for line in text.splitlines() if re.search(r'protein', line, re.I))
        results.append({'page': i, 'snippet': snippet})

output = {'matches': results}
print(json.dumps(output, ensure_ascii=False))
