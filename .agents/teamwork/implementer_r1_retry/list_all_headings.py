import docx
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

print(f"Total paragraphs: {len(doc.paragraphs)}")

for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    
    # Check style
    style_name = p.style.name
    
    # Let's see if it looks like a section/chapter/heading
    is_heading = False
    level = None
    
    if style_name.startswith("Heading"):
        is_heading = True
        level = style_name
    elif text in ["INTRODUCTION GÉNÉRALE", "CONCLUSION GÉNÉRALE ET PERSPECTIVES", "RÉFÉRENCES BIBLIOGRAPHIQUES"]:
        is_heading = True
        level = "Main Title"
    elif text.startswith("CHAPITRE ") or text.startswith("ANNEXE "):
        is_heading = True
        level = "Chapter/Annex"
    elif re.match(r"^(\d+\.|\d+\.\d+|\d+\.\d+\.\d+|[A-Z]\.\d+)\s+[A-ZÀ-Ÿ]", text):
        is_heading = True
        level = "Numbered Heading"
        
    if is_heading:
        print(f"P[{idx:03d}] [{style_name:15s}] [{str(level):16s}] : {text}")
