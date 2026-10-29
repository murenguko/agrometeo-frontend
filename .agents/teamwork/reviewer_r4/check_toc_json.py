import docx
import json

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\headings_pages.json', 'r', encoding='utf-8') as f:
    expected_pages = json.load(f)

intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

toc_items = {}
in_toc = False
for i in range(intro_idx):
    t = doc.paragraphs[i].text.strip()
    if t == "TABLE DES MATIÈRES":
        in_toc = True
        continue
    if in_toc:
        if t in ["LISTE DES FIGURES", "LISTE DES TABLEAUX", "LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES"]:
            in_toc = False
            continue
        if "\t" in t:
            title, pg = t.split("\t", 1)
            toc_items[title.strip()] = int(pg.strip())

print(f"Total TOC items parsed: {len(toc_items)}")
print(f"Total expected headings: {len(expected_pages)}")

mismatches = []
for title, exp_pg in expected_pages.items():
    if title not in toc_items:
        mismatches.append((title, exp_pg, "NOT IN TOC"))
    elif toc_items[title] != exp_pg:
        mismatches.append((title, exp_pg, toc_items[title]))

if mismatches:
    print(f"Found {len(mismatches)} mismatches:")
    for m in mismatches:
        print(" ", m)
else:
    print("SUCCESS: 100% of the 75 headings match between TOC and headings_pages.json!")
