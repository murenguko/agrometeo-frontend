import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

for ref_num in range(1, 26):
    pattern = rf'\[{ref_num}\]'
    matches = []
    for idx, p in enumerate(doc.paragraphs):
        if idx >= 474: # biblio section
            continue
        if re.search(pattern, p.text):
            matches.append((idx, p.text[:100]))
    # also check in tables
    table_matches = []
    for t_idx, t in enumerate(doc.tables):
        for r_idx, r in enumerate(t.rows):
            for c_idx, c in enumerate(r.cells):
                if re.search(pattern, c.text):
                    table_matches.append((t_idx, r_idx, c.text[:60]))
    print(f"Ref [{ref_num:2d}]: {len(matches)} para matches, {len(table_matches)} table matches")
    if matches:
        print(f"   First para: P[{matches[0][0]}]: {matches[0][1]}")
    if table_matches:
        print(f"   First table: T[{table_matches[0][0]}], R[{table_matches[0][1]}]: {table_matches[0][2]}")
