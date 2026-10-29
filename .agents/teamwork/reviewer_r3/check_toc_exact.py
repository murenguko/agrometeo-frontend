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

body_paras = [p.text.strip() for p in doc.paragraphs[p_intro_idx:] if p.text.strip()]

print(f"Total headings in json: {len(headings_dict)}")

not_exact = []
for h in headings_dict.keys():
    if h not in body_paras:
        # find closest
        closest = [bp for bp in body_paras if h.lower() in bp.lower() or bp.lower() in h.lower() or h[:15].lower() in bp.lower()]
        not_exact.append((h, closest))

print(f"Non-exact matches: {len(not_exact)}")
for h, c in not_exact:
    print(f"TOC:  {repr(h)}")
    print(f"BODY: {repr(c)}")
