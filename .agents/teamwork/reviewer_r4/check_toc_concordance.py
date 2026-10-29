import docx
import re

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

# Extract TOC items
toc_paras = []
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
            toc_paras.append((title.strip(), pg.strip()))

print(f"Total TOC entries: {len(toc_paras)}")

# Extract all headings from body
body_paras = doc.paragraphs[intro_idx:]
print(f"Total body paragraphs: {len(body_paras)}")

# Let's find headings in body (e.g. bold or heading styles or numbered titles)
body_headings = []
for i, p in enumerate(body_paras):
    t = p.text.strip()
    if not t:
        continue
    # check if heading-like
    is_heading = False
    if p.style.name.startswith("Heading"):
        is_heading = True
    elif any(t.startswith(prefix) for prefix in [
        "INTRODUCTION GÉNÉRALE", "CHAPITRE", "CONCLUSION GÉNÉRALE", "ANNEXE", "RÉFÉRENCES BIBLIOGRAPHIQUES"
    ]):
        is_heading = True
    elif re.match(r'^(?:[0-9]+\.|[A-Z]\.[0-9]+)\s+[A-ZÀ-Ÿ]', t):
        # Starts with number like 1. Contexte or 4.1 Diagramme or A.1 Matrice
        # check if bold
        if any(r.bold for r in p.runs):
            is_heading = True

    if is_heading:
        body_headings.append((i + intro_idx, t))

print(f"Total body headings found: {len(body_headings)}")

# Check concordance between body_headings and toc_paras
toc_titles = [t[0] for t in toc_paras]

print("\n--- Checking body headings against TOC ---")
missing_in_toc = []
for idx, bh in body_headings:
    # check if bh matches any toc title
    matched = False
    for tt in toc_titles:
        if bh == tt or bh.startswith(tt) or tt.startswith(bh):
            matched = True
            break
    if not matched:
        missing_in_toc.append((idx, bh))

if missing_in_toc:
    print(f"Found {len(missing_in_toc)} body headings MISSING in TOC:")
    for idx, bh in missing_in_toc:
        print(f"  p{idx}: {bh}")
else:
    print("ALL body headings are present in TOC!")

print("\n--- Checking TOC titles against body ---")
missing_in_body = []
for tt, pg in toc_paras:
    matched = False
    for idx, bh in body_headings:
        if tt == bh or bh.startswith(tt) or tt.startswith(bh):
            matched = True
            break
    if not matched:
        missing_in_body.append((tt, pg))

if missing_in_body:
    print(f"Found {len(missing_in_body)} TOC entries NOT found in body headings:")
    for tt, pg in missing_in_body:
        print(f"  {tt} (pg {pg})")
else:
    print("ALL TOC entries match a body heading!")
