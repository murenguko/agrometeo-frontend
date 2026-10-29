import docx
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
doc = docx.Document(docx_path)

print("=" * 60)
print("AUDIT COMPLET DU RAPPORT - REVIEWER 2 (REMPLAÇANT)")
print("=" * 60)

# 1. Verification des marges de sections
print("\n--- 1. AUDIT DES SECTIONS ET MARGES ---")
for i, section in enumerate(doc.sections):
    left_cm = section.left_margin.cm
    right_cm = section.right_margin.cm
    top_cm = section.top_margin.cm
    bottom_cm = section.bottom_margin.cm
    print(f"Section {i}: Gauche={left_cm:.2f} cm (attendu: 3.0 cm), Droite={right_cm:.2f} cm (attendu: 2.5 cm), Haut={top_cm:.2f} cm (attendu: 2.5 cm), Bas={bottom_cm:.2f} cm (attendu: 2.5 cm)")
    assert abs(left_cm - 3.0) < 0.05, f"Marge gauche non conforme: {left_cm}"
    assert abs(right_cm - 2.5) < 0.05, f"Marge droite non conforme: {right_cm}"
    assert abs(top_cm - 2.5) < 0.05, f"Marge haut non conforme: {top_cm}"
    assert abs(bottom_cm - 2.5) < 0.05, f"Marge bas non conforme: {bottom_cm}"
print("=> Marges : 100% CONFORMES UPG (3.0 cm gauche, 2.5 cm haut/bas/droite)")

# 2. Depart direct sur Introduction Generale
print("\n--- 2. DEMARRAGE DU LIVRABLE (PAGES LIMINAIRES) ---")
p0 = doc.paragraphs[0].text.strip()
print(f"Premier paragraphe du document: '{p0}'")
assert "INTRODUCTION G" in p0, f"Le document ne commence pas par INTRODUCTION GÉNÉRALE: {p0}"
print("=> Pages liminaires : STRICTEMENT OMISES, demarrage direct conforme.")

# 3. Police et interligne du style Normal
print("\n--- 3. POLICE, TAILLE ET INTERLIGNE (STYLE NORMAL) ---")
normal = doc.styles['Normal']
print(f"Style Normal - Font name: {normal.font.name}")
print(f"Style Normal - Font size: {normal.font.size.pt if normal.font.size else None} pt")
print(f"Style Normal - Line spacing: {normal.paragraph_format.line_spacing}")
print(f"Style Normal - Space after: {normal.paragraph_format.space_after.pt if normal.paragraph_format.space_after else None} pt")
print(f"Style Normal - Alignment: {normal.paragraph_format.alignment}")

# 4. Comptage global et ventilation par chapitre
print("\n--- 4. VOLUMETRIE ET VENTILATION PAR CHAPITRE ---")
total_paragraphs = len(doc.paragraphs)
total_tables = len(doc.tables)

words_in_paras = sum(len(p.text.split()) for p in doc.paragraphs)
words_in_tables = 0
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                words_in_tables += len(p.text.split())

total_words = words_in_paras + words_in_tables
print(f"Total paragraphes : {total_paragraphs}")
print(f"Total tableaux : {total_tables}")
print(f"Mots dans les paragraphes : {words_in_paras}")
print(f"Mots dans les tableaux : {words_in_tables}")
print(f"Total général des mots : {total_words}")

# Identifier les chapitres
chapters = [
    ("INTRODUCTION GÉNÉRALE", "CHAPITRE I"),
    ("CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC", "CHAPITRE II"),
    ("CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART", "CHAPITRE III"),
    ("CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE", "CHAPITRE IV"),
    ("CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION", "CHAPITRE V"),
    ("CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION", "CONCLUSION"),
    ("CONCLUSION GÉNÉRALE ET PERSPECTIVES", "ANNEXE A"),
    ("ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS", "ANNEXE B"),
    ("ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES", "ANNEXE D"),
    ("ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION", "ANNEXE F"),
    ("ANNEXE F — DÉPÔT GIT, STRUCTURE DU CODE SOURCE ET MÉTRIQUES", "RÉFÉRENCES"),
    ("RÉFÉRENCES BIBLIOGRAPHIQUES", None)
]

for title, next_title in chapters:
    paras = []
    in_chap = False
    for p in doc.paragraphs:
        txt = p.text.strip()
        if title in txt or (title.split("—")[0].strip() in txt and len(txt) < 80):
            in_chap = True
        elif next_title and (next_title in txt or (next_title.split("—")[0].strip() in txt and len(txt) < 80)) and in_chap:
            break
        if in_chap:
            paras.append(p)
    w_count = sum(len(p.text.split()) for p in paras)
    print(f"  * {title[:40]:<40} : {len(paras):3d} paras, ~{w_count:5d} mots (texte seul)")

# 5. Positionnement des légendes Tableaux et Figures
print("\n--- 5. POSITIONNEMENT DES LÉGENDES ---")
body = doc.element.body
elements = []
for child in body:
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        p = docx.text.paragraph.Paragraph(child, doc)
        t = p.text.strip()
        if t.startswith("Tableau ") or "Tableau " in t[:12]:
            elements.append(('TABLE_CAPTION', t[:50]))
        elif t.startswith("Figure ") or "Figure " in t[:12]:
            elements.append(('FIGURE_CAPTION', t[:50]))
    elif tag == 'tbl':
        elements.append(('TABLE', 'TABLE_OBJECT'))

table_captions_above = 0
for i, el in enumerate(elements):
    if el[0] == 'TABLE_CAPTION':
        # Check if following element is TABLE
        if i + 1 < len(elements) and elements[i+1][0] == 'TABLE':
            table_captions_above += 1
print(f"Légendes de tableaux identifiées immédiatement au-dessus de leur table: {table_captions_above}")

# 6. Citations IEEE et Sources S1 à S7
print("\n--- 6. SOURCES S1 À S7 DANS LA BIBLIOGRAPHIE IEEE ---")
full_text = "\n".join(p.text for p in doc.paragraphs)
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            full_text += "\n" + c.text

sources = {
    "S1 (Open-Meteo)": r"Open-Meteo",
    "S2 (Copernicus / GloFAS)": r"GloFAS|Copernicus",
    "S3 (NASA LHASA)": r"LHASA",
    "S4 (Leaflet / OSM)": r"Leaflet|OpenStreetMap",
    "S5 (ISABU)": r"ISABU",
    "S6 (IGEBU)": r"IGEBU",
    "S7 (CHIRPS)": r"CHIRPS"
}

for name, pat in sources.items():
    matches = len(re.findall(pat, full_text, re.IGNORECASE))
    print(f"  * {name:<26} : {matches:3d} mentions")

# 7. Verification des 5 critères prioritaires
print("\n--- 7. AUDIT DES 5 CRITÈRES PRIORITAIRES DE L'UTILISATEUR ---")
c1 = len(re.findall(r"MongoDB", full_text, re.IGNORECASE))
c2 = len(re.findall(r"PostgreSQL", full_text, re.IGNORECASE))
c3 = len(re.findall(r"LHASA", full_text, re.IGNORECASE))
c4 = len(re.findall(r"ISABU", full_text, re.IGNORECASE))
c5_zones = len(re.findall(r"Mumirwa|Imbo|Gitega|Karusi|Rutana", full_text, re.IGNORECASE))
c6_auth = len(re.findall(r"Argon2id|DUMMY_HASH|JWT", full_text, re.IGNORECASE))

print(f"  1. MongoDB: {c1} mentions | PostgreSQL: {c2} mentions")
print(f"  2. NASA LHASA (retrait): {c3} mentions")
print(f"  3. ISABU (cultures): {c4} mentions")
print(f"  4. 5 provinces & sous-zones: {c5_zones} mentions")
print(f"  5. Authentification (Argon2id/JWT/DUMMY_HASH): {c6_auth} mentions")

print("\nAUDIT TERMINE AVEC SUCCES.")

