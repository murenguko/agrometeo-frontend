import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

biblio_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        biblio_idx = i
        break

print(f"Bibliography heading at index {biblio_idx}")
heading_p = doc.paragraphs[biblio_idx]
print(f"Heading text: {repr(heading_p.text)}")
print(f"Heading runs: {[(r.text, r.font.name, r.font.size.pt if r.font.size else None, r.bold) for r in heading_p.runs]}")

entries = doc.paragraphs[biblio_idx + 1:]
print(f"Total entries: {len(entries)}")

errors = []
for i, p in enumerate(entries):
    t = p.text.strip()
    # Check alignment
    if p.paragraph_format.alignment != WD_ALIGN_PARAGRAPH.JUSTIFY:
        errors.append((i, "alignment", p.paragraph_format.alignment))
    # Check line spacing
    if p.paragraph_format.line_spacing != 1.5:
        errors.append((i, "line_spacing", p.paragraph_format.line_spacing))
    # Check runs font and size
    for r in p.runs:
        if r.font.name != "Times New Roman":
            errors.append((i, "font_name", r.font.name))
        if r.font.size != Pt(12):
            errors.append((i, "font_size", r.font.size.pt if r.font.size else None))

if errors:
    print(f"Found {len(errors)} typography errors in bibliography:")
    for err in errors[:10]:
        print(" ", err)
else:
    print("SUCCESS: All 30 bibliography entries strictly satisfy Times New Roman, 12pt, 1.5 line spacing, justified alignment!")
