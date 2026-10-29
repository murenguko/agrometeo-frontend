import docx
import re

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

intro_idx = None
biblio_idx = None
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
    if intro_idx is not None and t == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        biblio_idx = i
        break

print(f"Body spans paragraphs {intro_idx} to {biblio_idx-1}")
print(f"Bibliography starts at {biblio_idx}")

# Scan all body paragraphs and tables for [X] citations
body_text = []
for p in doc.paragraphs[intro_idx:biblio_idx]:
    body_text.append(p.text)

for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            body_text.append(cell.text)

full_body_text = "\n".join(body_text)

# Regex to find citations like [1], [1, 2], [1]-[3], [12]
citations = re.findall(r'\[(\d+(?:\s*,\s*\d+)*|\d+\s*[-–—]\s*\d+)\]', full_body_text)

cited_numbers = set()
for c in citations:
    if '-' in c or '–' in c or '—' in c:
        parts = re.split(r'[-–—]', c)
        start, end = int(parts[0].strip()), int(parts[1].strip())
        for n in range(start, end + 1):
            cited_numbers.add(n)
    elif ',' in c:
        for part in c.split(','):
            cited_numbers.add(int(part.strip()))
    else:
        cited_numbers.add(int(c.strip()))

print(f"Unique cited reference numbers in text: {sorted(list(cited_numbers))}")

# Scan bibliography entries
biblio_entries = {}
for p in doc.paragraphs[biblio_idx + 1:]:
    t = p.text.strip()
    if not t:
        continue
    m = re.match(r'^\[(\d+)\]\s*(.*)', t)
    if m:
        num = int(m.group(1))
        biblio_entries[num] = m.group(2)
    else:
        print(f"Unmatched biblio paragraph: {repr(t[:50])}")

print(f"\nTotal bibliography entries: {len(biblio_entries)}")
print(f"Biblio entry numbers: {sorted(list(biblio_entries.keys()))}")

# Check if all cited numbers exist in biblio
missing_in_biblio = cited_numbers - set(biblio_entries.keys())
print(f"\nCited numbers missing from bibliography: {missing_in_biblio}")

# Check unreferenced bibliography entries
uncited_in_text = set(biblio_entries.keys()) - cited_numbers
print(f"Bibliography entries not cited in text: {uncited_in_text}")

# Check format consistency of bibliography entries
print("\n--- Bibliography Format Audit ---")
for num, content in sorted(biblio_entries.items()):
    # check standard IEEE format markers
    print(f"[{num}] {content[:80]}...")
