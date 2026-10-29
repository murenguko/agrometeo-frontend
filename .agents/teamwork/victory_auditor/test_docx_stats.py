import docx
import json
import re

doc_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
doc = docx.Document(doc_path)

print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")
print(f"Total Sections: {len(doc.sections)}")

intro_idx = [i for i, p in enumerate(doc.paragraphs) if p.text.strip() == "INTRODUCTION GÉNÉRALE"][0]
biblio_idx = [i for i, p in enumerate(doc.paragraphs) if p.text.strip() == "RÉFÉRENCES BIBLIOGRAPHIQUES"][0]

print(f"Prelims range: 0 to {intro_idx - 1} ({intro_idx} paragraphs)")
print(f"Body range: {intro_idx} to {biblio_idx} ({biblio_idx - intro_idx + 1} paragraphs)")
print(f"Bibliography range: {biblio_idx + 1} to {len(doc.paragraphs) - 1} ({len(doc.paragraphs) - biblio_idx - 1} paragraphs)")

# Word count
total_words = sum(len(p.text.split()) for p in doc.paragraphs)
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            total_words += len(cell.text.split())
print(f"Estimated total words: {total_words}")
