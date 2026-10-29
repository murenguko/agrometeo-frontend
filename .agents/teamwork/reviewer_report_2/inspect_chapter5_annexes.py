import docx
import re

docx_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
doc = docx.Document(docx_path)

def extract_section(start_title, end_title):
    capturing = False
    paragraphs = []
    for p in doc.paragraphs:
        txt = p.text.strip()
        if start_title in txt:
            capturing = True
        elif end_title and end_title in txt and capturing:
            break
        if capturing:
            paragraphs.append(txt)
    return paragraphs

print("=== CHAPITRE V DETAILS ===")
chap5 = extract_section("CHAPITRE V", "CONCLUSION")
print(f"Chapitre V paragraphs count: {len(chap5)}")
for idx, p in enumerate(chap5):
    if p.startswith("Tableau") or p.startswith("Figure") or (p and p[0].isdigit() and "." in p[:3]):
        print(f"P{idx}: {p[:120]}")

print("\n=== ANNEXE A DETAILS ===")
annexe_a = extract_section("ANNEXE A", "ANNEXE B")
print(f"Annexe A paragraphs count: {len(annexe_a)}")
for idx, p in enumerate(annexe_a):
    if "Tableau" in p or "Figure" in p or (p and p[0].isdigit() and "." in p[:3]) or "Diagramme" in p:
        print(f"P{idx}: {p[:120]}")

print("\n=== ANNEXE B DETAILS ===")
annexe_b = extract_section("ANNEXE B", "ANNEXE D")
print(f"Annexe B paragraphs count: {len(annexe_b)}")
for idx, p in enumerate(annexe_b):
    if "Tableau" in p or "Figure" in p or (p and p[0].isdigit() and "." in p[:3]) or "Collection" in p or "Table" in p:
        print(f"P{idx}: {p[:120]}")

print("\n=== ANNEXE D DETAILS ===")
annexe_d = extract_section("ANNEXE D", "ANNEXE F")
print(f"Annexe D paragraphs count: {len(annexe_d)}")
for idx, p in enumerate(annexe_d):
    if "Tableau" in p or "Figure" in p or (p and p[0].isdigit() and "." in p[:3]) or "Étape" in p or "Manuel" in p:
        print(f"P{idx}: {p[:120]}")

print("\n=== ANNEXE F DETAILS ===")
annexe_f = extract_section("ANNEXE F", "RÉFÉRENCES")
print(f"Annexe F paragraphs count: {len(annexe_f)}")
for idx, p in enumerate(annexe_f):
    if "Tableau" in p or "Figure" in p or (p and p[0].isdigit() and "." in p[:3]) or "Dépôt" in p or "Structure" in p:
        print(f"P{idx}: {p[:120]}")

print("\n=== REFERENCES DETAILS ===")
refs = extract_section("RÉFÉRENCES", None)
print(f"References paragraphs count: {len(refs)}")
for p in refs:
    if p.startswith("["):
        print(f"  {p[:100]}")
