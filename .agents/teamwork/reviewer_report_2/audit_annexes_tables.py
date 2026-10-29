import docx

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

def get_section_paras_and_tables(title_start, title_end):
    capturing = False
    items = []
    for idx, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        if title_start in txt:
            capturing = True
        elif title_end and title_end in txt and capturing:
            break
        if capturing:
            items.append((idx, "P", txt))
    return items

print("=== DETAILED INSPECTION OF ANNEXE A ===")
annexe_a_items = get_section_paras_and_tables("ANNEXE A", "ANNEXE B")
for idx, kind, txt in annexe_a_items:
    print(f"[{kind}] {txt[:120]}")

print("\n=== DETAILED INSPECTION OF ANNEXE B ===")
annexe_b_items = get_section_paras_and_tables("ANNEXE B", "ANNEXE D")
for idx, kind, txt in annexe_b_items:
    print(f"[{kind}] {txt[:120]}")

print("\n=== DETAILED INSPECTION OF ANNEXE D ===")
annexe_d_items = get_section_paras_and_tables("ANNEXE D", "ANNEXE F")
for idx, kind, txt in annexe_d_items:
    print(f"[{kind}] {txt[:120]}")

print("\n=== DETAILED INSPECTION OF ANNEXE F ===")
annexe_f_items = get_section_paras_and_tables("ANNEXE F", "RÉFÉRENCES")
for idx, kind, txt in annexe_f_items:
    print(f"[{kind}] {txt[:120]}")

print("\n=== FIGURES AUDIT ===")
figures = []
for idx, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("Figure ") or "Figure " in p.text.strip()[:15]:
        figures.append((idx, p.text.strip()))
print(f"Total Figures identified in paragraphs: {len(figures)}")
for f in figures:
    print(f"  P{f[0]}: {f[1]}")

print("\n=== TABLES AUDIT ===")
tables = []
for idx, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("Tableau ") or "Tableau " in p.text.strip()[:15]:
        tables.append((idx, p.text.strip()))
print(f"Total Table captions identified in paragraphs: {len(tables)}")
for t in tables:
    print(f"  P{t[0]}: {t[1]}")
