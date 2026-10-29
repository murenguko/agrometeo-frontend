import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

print("--- ALL OCCURRENCES OF 'Figure' ---")
for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if "figure" in text.lower():
        print(f"P[{idx}]: {text[:120]}")

print("\n--- ALL OCCURRENCES OF 'Tableau' ---")
for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if "tableau" in text.lower():
        print(f"P[{idx}]: {text[:120]}")

print("\n--- TABLES IN DOCUMENT ---")
for idx, t in enumerate(doc.tables):
    # check preceding paragraph
    # find table's parent or position
    # Let's inspect the first row of each table
    row0 = [cell.text.strip().replace("\n", " ") for cell in t.rows[0].cells]
    print(f"Table {idx} (rows={len(t.rows)}, cols={len(t.columns)}): Header={row0[:3]}")
