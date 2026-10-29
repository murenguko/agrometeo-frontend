import docx
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

print("Checking structure of actual sections and chapters:")

for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    
    # Check if bold or title
    is_bold = any(r.bold for r in p.runs if r.text.strip())
    
    # Chapter or main titles
    if text in ["INTRODUCTION GÉNÉRALE", "CONCLUSION GÉNÉRALE ET PERSPECTIVES", "RÉFÉRENCES BIBLIOGRAPHIQUES"]:
        print(f"\n[MAIN] P[{idx:03d}]: {text}")
    elif text.startswith("CHAPITRE ") or text.startswith("ANNEXE "):
        print(f"\n[CHAPTER/ANNEX] P[{idx:03d}]: {text}")
    elif re.match(r"^\d+\.\s+[A-ZÀ-Ÿ]", text) and p.style.name != "List Bullet":
        print(f"  [SEC Level 1] P[{idx:03d}]: {text}")
    elif re.match(r"^\d+\.\d+\s+[A-ZÀ-Ÿ]", text) and p.style.name != "List Bullet":
        print(f"    [SEC Level 2] P[{idx:03d}]: {text}")
    elif re.match(r"^[A-Z]\.\d+\s+[A-ZÀ-Ÿ]", text) and p.style.name != "List Bullet":
        print(f"    [ANNEX Level 2] P[{idx:03d}]: {text}")
