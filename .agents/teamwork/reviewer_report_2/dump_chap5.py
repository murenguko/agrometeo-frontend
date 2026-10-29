import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

capturing = False
chap5_lines = []
for p in doc.paragraphs:
    txt = p.text.strip()
    if "CHAPITRE V" in txt:
        capturing = True
    elif "CONCLUSION" in txt and capturing:
        break
    if capturing:
        chap5_lines.append(txt)

print(f"=== FULL TEXT OF CHAPTER V ({len(chap5_lines)} paragraphs) ===")
for i, line in enumerate(chap5_lines):
    print(f"--- P{i} ---")
    print(line)
