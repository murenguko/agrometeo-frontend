import docx
import json

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\figures_tables_pages.json', 'r', encoding='utf-8') as f:
    fig_tab_data = json.load(f)

intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

figures_in_doc = {}
tables_in_doc = {}
in_fig = False
in_tab = False
for i in range(intro_idx):
    t = doc.paragraphs[i].text.strip()
    if t == "LISTE DES FIGURES":
        in_fig = True
        in_tab = False
        continue
    elif t == "LISTE DES TABLEAUX":
        in_fig = False
        in_tab = True
        continue
    elif t == "LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES":
        in_fig = False
        in_tab = False
        continue
    if in_fig and "\t" in t:
        title, pg = t.split("\t", 1)
        figures_in_doc[title.strip()] = int(pg.strip())
    elif in_tab and "\t" in t:
        title, pg = t.split("\t", 1)
        tables_in_doc[title.strip()] = int(pg.strip())

print(f"Figures in doc: {len(figures_in_doc)}, expected: {len(fig_tab_data['figures'])}")
for k, v in fig_tab_data['figures'].items():
    assert figures_in_doc.get(k) == v, f"Figure {k}: got {figures_in_doc.get(k)}, exp {v}"

print(f"Tables in doc: {len(tables_in_doc)}, expected: {len(fig_tab_data['tables'])}")
for k, v in fig_tab_data['tables'].items():
    assert tables_in_doc.get(k) == v, f"Table {k}: got {tables_in_doc.get(k)}, exp {v}"

print("SUCCESS: All figures and tables in doc match figures_tables_pages.json exactly!")
