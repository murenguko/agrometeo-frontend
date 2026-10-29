import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

print("All citations in body with their full paragraph text:")
for idx, p in enumerate(doc.paragraphs):
    if idx >= 474:
        continue
    # find [1] to [25]
    matches = re.findall(r'\[(\d+)\]', p.text)
    if matches:
        print(f"\nP[{idx}] (cites: {', '.join(matches)}):")
        print(f"  {p.text}")
