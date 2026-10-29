"""
audit_script.py - Independent in-depth academic & adversarial audit
Run by reviewer_report_1
"""
import os
import sys
import docx
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

DOCX_PATH = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"

def run_audit():
    print("=" * 80)
    print("INDEPENDENT AUDIT BY REVIEWER_REPORT_1")
    print(f"Target: {DOCX_PATH}")
    print("=" * 80)

    if not os.path.exists(DOCX_PATH):
        print(f"CRITICAL: {DOCX_PATH} does not exist!")
        return

    doc = docx.Document(DOCX_PATH)
    file_size = os.path.getsize(DOCX_PATH)
    print(f"File size: {file_size} bytes ({file_size/1024:.2f} KB)")

    # 1. Section and Margins
    print("\n--- 1. SECTION & MARGINS ---")
    section = doc.sections[0]
    top_cm = round(section.top_margin.cm, 2)
    bottom_cm = round(section.bottom_margin.cm, 2)
    left_cm = round(section.left_margin.cm, 2)
    right_cm = round(section.right_margin.cm, 2)
    print(f"Left: {left_cm} cm (Target: 3.0 cm)")
    print(f"Right: {right_cm} cm (Target: 2.5 cm)")
    print(f"Top: {top_cm} cm (Target: 2.5 cm)")
    print(f"Bottom: {bottom_cm} cm (Target: 2.5 cm)")

    # 2. First Paragraph (Liminary pages check)
    print("\n--- 2. FIRST PARAGRAPHS (LIMINARY CHECK) ---")
    non_empty_paras = [p for p in doc.paragraphs if p.text.strip()]
    for i, p in enumerate(non_empty_paras[:5]):
        print(f"P[{i}]: '{p.text[:80]}...' (style: {p.style.name if p.style else 'None'})")

    # 3. Typography & Styling Analysis
    print("\n--- 3. TYPOGRAPHY & STYLING SAMPLE AUDIT ---")
    font_names = set()
    font_sizes = set()
    alignments = set()
    line_spacings = set()

    for p in doc.paragraphs:
        if p.alignment is not None:
            alignments.add(p.alignment)
        if p.paragraph_format.line_spacing is not None:
            line_spacings.add(p.paragraph_format.line_spacing)
        for r in p.runs:
            if r.font.name:
                font_names.add(r.font.name)
            if r.font.size:
                font_sizes.add(r.font.size.pt)

    print(f"Detected fonts in runs: {font_names}")
    print(f"Detected font sizes (pt): {sorted(list(font_sizes))}")
    print(f"Detected paragraph alignments: {alignments}")
    print(f"Detected line spacings: {line_spacings}")

    # Check Default Normal Style
    normal_style = doc.styles['Normal']
    print(f"Normal style font: {normal_style.font.name}, size: {normal_style.font.size.pt if normal_style.font.size else 'default'}")

    # 4. Heading Hierarchy & Capitalization
    print("\n--- 4. HEADING HIERARCHY ---")
    h1_list = []
    h2_list = []
    h3_list = []
    for p in doc.paragraphs:
        txt = p.text.strip()
        if p.style and p.style.name.startswith('Heading 1') or (txt.startswith("CHAPITRE") or txt.startswith("INTRODUCTION") or txt.startswith("CONCLUSION") or txt.startswith("ANNEXE") or txt.startswith("RÉFÉRENCES")):
            h1_list.append(txt)
        elif p.style and p.style.name.startswith('Heading 2'):
            h2_list.append(txt)
        elif p.style and p.style.name.startswith('Heading 3'):
            h3_list.append(txt)

    print(f"Found {len(h1_list)} H1 titles:")
    for h in h1_list:
        print(f"  - {h}")

    print(f"\nFound {len(h2_list)} H2 titles. Sample of first 10:")
    for h in h2_list[:10]:
        print(f"  - {h}")

    print(f"\nFound {len(h3_list)} H3 titles. Sample of first 10:")
    for h in h3_list[:10]:
        print(f"  - {h}")

    # 5. Tables & Figures
    print("\n--- 5. TABLES AND FIGURES AUDIT ---")
    print(f"Total tables: {len(doc.tables)}")

    # Check table captions (Tableau X.Y)
    tableau_captions = [p.text.strip() for p in doc.paragraphs if re.match(r'^Tableau\s+\d+\.\d+', p.text.strip(), re.IGNORECASE) or re.match(r'^Tableau\s+[A-F]\.\d+', p.text.strip(), re.IGNORECASE)]
    figure_captions = [p.text.strip() for p in doc.paragraphs if re.match(r'^Figure\s+\d+\.\d+', p.text.strip(), re.IGNORECASE) or re.match(r'^Figure\s+[A-F]\.\d+', p.text.strip(), re.IGNORECASE)]

    print(f"Found {len(tableau_captions)} table captions:")
    for c in tableau_captions:
        print(f"  {c}")

    print(f"\nFound {len(figure_captions)} figure captions:")
    for c in figure_captions:
        print(f"  {c}")

    # 6. IEEE References Audit
    print("\n--- 6. IEEE REFERENCES AUDIT ---")
    references = []
    in_ref = False
    for p in doc.paragraphs:
        txt = p.text.strip()
        if "RÉFÉRENCES BIBLIOGRAPHIQUES" in txt:
            in_ref = True
            continue
        if in_ref:
            if re.match(r'^\[\d+\]', txt):
                references.append(txt)

    print(f"Total IEEE references detected: {len(references)}")
    for r in references:
        print(f"  {r[:100]}...")

    # Check S1 to S7 presence
    s_sources = {
        "S1 (Open-Meteo)": any("Open-Meteo" in r for r in references),
        "S2 (Copernicus / GloFAS)": any("Copernicus" in r or "GloFAS" in r for r in references),
        "S3 (NASA LHASA)": any("NASA" in r or "LHASA" in r for r in references),
        "S4 (Leaflet / OSM)": any("Leaflet" in r or "OpenStreetMap" in r for r in references),
        "S5 (ISABU)": any("ISABU" in r for r in references),
        "S6 (IGEBU)": any("IGEBU" in r for r in references),
        "S7 (CHIRPS / Funk)": any("CHIRPS" in r or "Funk" in r for r in references)
    }
    print("\nSources S1 à S7 check:")
    for k, v in s_sources.items():
        print(f"  {k}: {'FOUND' if v else 'MISSING'}")

    # 7. Word count breakdown by chapter
    print("\n--- 7. WORD COUNT BREAKDOWN ---")
    current_section = "START"
    section_words = {}
    current_words = 0

    for p in doc.paragraphs:
        txt = p.text.strip()
        if any(txt.startswith(prefix) for prefix in ["INTRODUCTION", "CHAPITRE", "CONCLUSION", "ANNEXE", "RÉFÉRENCES"]):
            if current_words > 0:
                section_words[current_section] = current_words
            current_section = txt[:40]
            current_words = 0
        current_words += len(txt.split())

    # Add table words to sections if possible, or print total
    total_para_words = sum(len(p.text.split()) for p in doc.paragraphs)
    total_table_words = sum(sum(len(cell.text.split()) for cell in row.cells) for t in doc.tables for row in t.rows)
    print(f"Paragraph words: {total_para_words}")
    print(f"Table words: {total_table_words}")
    print(f"Total document words: {total_para_words + total_table_words}")

    for sec, w in section_words.items():
        print(f"  {sec}: {w} words")

    # 8. Check for Placeholders / Suspicious words
    print("\n--- 8. PLACEHOLDER / INTEGRITY SCAN ---")
    suspicious = ["lorem ipsum", "todo", "tbd", "xxx", "placeholder", "en attente de", "a completer", "à compléter"]
    full_text_lower = ("\n".join(p.text for p in doc.paragraphs) + "\n" + "\n".join(c.text for t in doc.tables for r in t.rows for c in r.cells)).lower()

    for s in suspicious:
        count = full_text_lower.count(s)
        if count > 0:
            print(f"  WARNING: Suspicious string '{s}' found {count} times!")
        else:
            print(f"  Clean: '{s}' not found (0)")

if __name__ == "__main__":
    run_audit()
