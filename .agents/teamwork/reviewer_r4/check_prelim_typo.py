import docx
from docx.shared import Pt

DOC_PATH = r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx'
doc = docx.Document(DOC_PATH)

intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

print(f"Checking preliminary paragraphs 0 to {intro_idx-1}...")
non_conforming_font = []
non_conforming_size = []
non_conforming_spacing = []

for i in range(intro_idx):
    p = doc.paragraphs[i]
    t = p.text.strip()
    if not t:
        continue
    
    # line spacing
    ls = p.paragraph_format.line_spacing
    # runs
    for r in p.runs:
        fn = r.font.name
        fs = r.font.size
        if fn != 'Times New Roman':
            non_conforming_font.append((i, t[:30], fn))
        if fs != Pt(12) and fs is not None:
            non_conforming_size.append((i, t[:30], fs.pt if fs else None))
    if ls != 1.5 and ls is not None:
        non_conforming_spacing.append((i, t[:30], ls))

print(f"Non conforming font count: {len(non_conforming_font)}")
for item in non_conforming_font[:10]:
    print("  Font:", item)

print(f"Non conforming size count: {len(non_conforming_size)}")
for item in non_conforming_size[:20]:
    print("  Size:", item)

print(f"Non conforming spacing count: {len(non_conforming_spacing)}")
for item in non_conforming_spacing[:20]:
    print("  Spacing:", item)
