import docx
from docx.shared import Inches, Pt, Cm
import os

DOC_PATH = r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx'
doc = docx.Document(DOC_PATH)

print(f"Total sections: {len(doc.sections)}")
for i, sec in enumerate(doc.sections):
    print(f"\n--- Section {i+1} ---")
    print(f"  Start type: {sec.start_type}")
    print(f"  Margins (cm): Top={sec.top_margin.cm:.2f}, Bottom={sec.bottom_margin.cm:.2f}, Left={sec.left_margin.cm:.2f}, Right={sec.right_margin.cm:.2f}")
    print(f"  Page dimensions: width={sec.page_width.cm:.2f}, height={sec.page_height.cm:.2f}")
    # Inspect footers
    footer = sec.footer
    print(f"  Footer paragraphs count: {len(footer.paragraphs)}")
    for fp in footer.paragraphs:
        print(f"    Footer text: {repr(fp.text)}, alignment: {fp.alignment}")
        for r in fp.runs:
            print(f"      run text: {repr(r.text)}, font: {r.font.name}, size: {r.font.size}")
        # check xml of footer paragraph
        xml = fp._element.xml
        if 'w:fldSimple' in xml or 'w:instrText' in xml or 'PAGE' in xml:
            print(f"      [DYNAMIC PAGE FIELD FOUND in footer]")

print(f"\nTotal paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

# Inspect the preliminary pages up to INTRODUCTION GÉNÉRALE
intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

print(f"\nINTRODUCTION GÉNÉRALE found at paragraph index: {intro_idx}")

prelim_paras = doc.paragraphs[:intro_idx]
print(f"Preliminary paragraphs count: {len(prelim_paras)}")

# Check preliminary sections headings
for i, p in enumerate(prelim_paras):
    t = p.text.strip()
    if any(h in t for h in ["RÉPUBLIQUE", "MINISTÈRE", "UNIVERSITÉ", "TABLE DES", "LISTE DES", "SIGLES", "ANNEXES"]):
        print(f"  p{i}: {t[:60]}")
