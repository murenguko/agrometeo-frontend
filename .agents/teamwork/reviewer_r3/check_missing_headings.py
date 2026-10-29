import docx
import re
import json

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

p_intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == 'INTRODUCTION GÉNÉRALE':
        p_intro_idx = i
        break

with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\headings_pages.json', 'r', encoding='utf-8') as f:
    headings_dict = json.load(f)

toc_set = set(headings_dict.keys())

# Find potential headings in body:
# 1. Chapters: CHAPITRE, INTRODUCTION, CONCLUSION, ANNEXE, RÉFÉRENCES
# 2. Numbered: 1. , 1.1 , etc.
potential_headings = []
for idx, p in enumerate(doc.paragraphs[p_intro_idx:], start=p_intro_idx):
    t = p.text.strip()
    if not t:
        continue
    # Check if heading-like
    if re.match(r'^(CHAPITRE|INTRODUCTION|CONCLUSION|ANNEXE|RÉFÉRENCES)\b', t, re.I):
        potential_headings.append((idx, t))
    elif re.match(r'^\d+\.\s+[A-ZÀ-ÖØ-ß]', t):
        # Is it a heading or a list item?
        potential_headings.append((idx, t))
    elif re.match(r'^\d+\.\d+(\.\d+)?\s+[A-ZÀ-ÖØ-ß]', t):
        potential_headings.append((idx, t))
    elif re.match(r'^[A-Z]\.\d+\s+[A-ZÀ-ÖØ-ß]', t):
        potential_headings.append((idx, t))

print(f"Total potential headings in body: {len(potential_headings)}")
missing_from_toc = []
for idx, ph in potential_headings:
    if ph not in toc_set:
        # Check if list item
        p = doc.paragraphs[idx]
        missing_from_toc.append((idx, ph, p.style.name))

print(f"Missing from TOC count: {len(missing_from_toc)}")
for idx, ph, style in missing_from_toc:
    print(f"p{idx} (style={style}): {repr(ph)}")
