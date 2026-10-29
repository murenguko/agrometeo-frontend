import docx
import re

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

# Extract listed figures and tables
figures_listed = []
tables_listed = []

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
        figures_listed.append((title.strip(), pg.strip()))
    elif in_tab and "\t" in t:
        title, pg = t.split("\t", 1)
        tables_listed.append((title.strip(), pg.strip()))

print(f"Figures listed in preliminary pages ({len(figures_listed)}):")
for f, pg in figures_listed:
    print(f"  {f} -> {pg}")

print(f"\nTables listed in preliminary pages ({len(tables_listed)}):")
for t, pg in tables_listed:
    print(f"  {t} -> {pg}")

# Find figures and tables in the body
body_figures = []
body_tables = []

for i, p in enumerate(doc.paragraphs[intro_idx:]):
    t = p.text.strip()
    if re.match(r'^Figure\s+[0-9]+\.[0-9]+', t, re.IGNORECASE):
        body_figures.append((i + intro_idx, t))
    elif re.match(r'^Tableau\s+[0-9A-Z]+\.[0-9]+', t, re.IGNORECASE):
        body_tables.append((i + intro_idx, t))

print(f"\nFigures found in body: {len(body_figures)}")
for idx, f in body_figures:
    print(f"  p{idx}: {f}")

print(f"\nTables found in body (from paragraphs): {len(body_tables)}")
for idx, t in body_tables:
    print(f"  p{idx}: {t}")

print(f"Actual docx table elements count: {len(doc.tables)}")

# Check concordance
print("\n--- Concordance Check ---")
for f_title, pg in figures_listed:
    prefix = f_title.split('—')[0].strip()
    match = [bf for idx, bf in body_figures if prefix in bf]
    if not match:
        print(f"ERROR: Listed figure not found in body: {f_title}")
    else:
        # Check if text matches
        pass
print("Figures check done.")

for t_title, pg in tables_listed:
    prefix = t_title.split('—')[0].strip()
    match = [bt for idx, bt in body_tables if prefix in bt]
    if not match:
        print(f"ERROR: Listed table not found in body: {t_title}")
print("Tables check done.")
