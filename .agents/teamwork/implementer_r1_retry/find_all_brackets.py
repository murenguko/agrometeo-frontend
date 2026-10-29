import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

body_citations = []
for idx, p in enumerate(doc.paragraphs):
    if idx >= 474:
        continue
    for m in re.finditer(r'\[([^\]]+)\]', p.text):
        content = m.group(1).strip()
        body_citations.append((idx, m.group(0), content, p.text[:80]))

for t_idx, t in enumerate(doc.tables):
    for r_idx, r in enumerate(t.rows):
        for c_idx, c in enumerate(r.cells):
            for m in re.finditer(r'\[([^\]]+)\]', c.text):
                content = m.group(1).strip()
                body_citations.append((f"T{t_idx}R{r_idx}", m.group(0), content, c.text[:60]))

print(f"Total bracketed expressions found in body: {len(body_citations)}")
for loc, raw, content, context in body_citations:
    print(f"{loc}: {raw:15s} --> context: {context}")
