import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import re

docx_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
doc = docx.Document(docx_path)

print("=== 1. STYLE & FONT AUDIT ===")
normal_style = doc.styles['Normal']
print(f"Normal style font name: {normal_style.font.name}")
print(f"Normal style font size: {normal_style.font.size.pt if normal_style.font.size else None} pt")

# Check run-level font and rFonts xml
sample_fonts = set()
for p in doc.paragraphs[:100]:
    for r in p.runs:
        rPr = r._r.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is not None:
            ascii_f = rFonts.get(qn('w:ascii'))
            hAnsi_f = rFonts.get(qn('w:hAnsi'))
            sample_fonts.add((ascii_f, hAnsi_f))
        elif r.font.name:
            sample_fonts.add(r.font.name)

print(f"Sample run fonts detected: {sample_fonts}")

# Check paragraph alignments and line spacing
alignments = set()
spacings = set()
for p in doc.paragraphs[:100]:
    if p.text.strip():
        alignments.add(p.alignment)
        spacings.add(p.paragraph_format.line_spacing)

print(f"Sample alignments: {alignments}")
print(f"Sample line spacings: {spacings}")

print("\n=== 2. DETAILED SECTIONS & SUBSECTIONS ===")
subsections = []
for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if any(txt.startswith(prefix) for prefix in [
        "INTRODUCTION", "CHAPITRE", "CONCLUSION", "ANNEXE", "RÉFÉRENCES",
        "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10."
    ]):
        if len(txt) < 120 and (p.runs and p.runs[0].bold or txt.isupper() or p.style.name.startswith("Heading")):
            subsections.append((idx, txt))

print(f"Found {len(subsections)} major section headers:")
for idx, txt in subsections:
    print(f"  P{idx:3d}: {txt}")

print("\n=== 3. CHAPTER V CONTENT ANALYSIS ===")
chap5_paragraphs = []
in_chap5 = False
for idx, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    if "CHAPITRE V" in txt:
        in_chap5 = True
    elif "CONCLUSION" in txt and in_chap5:
        in_chap5 = False
    if in_chap5:
        chap5_paragraphs.append((idx, txt))

print(f"Chapter V contains {len(chap5_paragraphs)} paragraphs.")
chap5_fulltext = "\n".join(t for _, t in chap5_paragraphs)

# Also check tables in Chapter V
# Tables don't have a direct chapter attribute, but let's check table content
chap5_tables = []
for t_idx, t in enumerate(doc.tables):
    t_text = "\n".join(" | ".join(c.text.strip() for c in r.cells) for r in t.rows)
    if any(k in t_text for k in ["Cadrage Initial (MVP)", "Écart / Adaptation Réalisée", "MongoDB", "NASA LHASA", "5.1", "5.2", "5.3", "5.4"]):
        chap5_tables.append((t_idx, t_text))

print(f"Tables matching Chapter V themes: {len(chap5_tables)}")
for t_idx, t_text in chap5_tables:
    first_row = t_text.split("\n")[0][:120]
    print(f"  Table {t_idx}: {first_row}")

print("\n=== 4. SPECIFIC COMPARISON CRITERIA IN CHAPITRE V ===")
crit1_mongo = re.findall(r"MongoDB|PostgreSQL|NoSQL|persistance", chap5_fulltext, re.IGNORECASE)
crit2_lhasa = re.findall(r"LHASA|glissement|NASA", chap5_fulltext, re.IGNORECASE)
crit3_cultures = re.findall(r"culture|ISABU|CULTURES_PAR_ZONE|spécifique|région", chap5_fulltext, re.IGNORECASE)
crit4_zones = re.findall(r"province|sous-zone|Imbo|Mumirwa|Gitega|Karusi|Rutana", chap5_fulltext, re.IGNORECASE)
crit5_auth = re.findall(r"authentification|Argon2id|JWT|OAuth2|sécurité", chap5_fulltext, re.IGNORECASE)

print(f"MongoDB/PostgreSQL mentions in text: {len(crit1_mongo)}")
print(f"NASA LHASA/Glissements mentions in text: {len(crit2_lhasa)}")
print(f"Cultures ISABU mentions in text: {len(crit3_cultures)}")
print(f"Provinces/Zones mentions in text: {len(crit4_zones)}")
print(f"Authentification/Argon2id mentions in text: {len(crit5_auth)}")

# Let's inspect Table 5.2 or the comparison matrix
print("\n=== 5. COMPARISON MATRIX CONTENT (TABLE 5.2) ===")
for t_idx, t in enumerate(doc.tables):
    for r in t.rows[:2]:
        for c in r.cells:
            if "Cadrage Initial" in c.text or "Matrice Comparative" in c.text or "Écart" in c.text or "Composante" in c.text:
                print(f"--- Table {t_idx} is Comparison Matrix ---")
                for r_idx, row in enumerate(t.rows):
                    row_cells = [c.text.replace("\n", " ") for c in row.cells]
                    print(f"Row {r_idx}: {' | '.join(row_cells[:4])}")
                break
