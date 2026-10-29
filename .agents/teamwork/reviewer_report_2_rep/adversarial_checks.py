import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

print("=" * 60)
print("ADVERSARIAL STRESS-TEST & INTEGRITY AUDIT")
print("=" * 60)

# Check 1: Context of PostgreSQL mentions
print("\n--- TEST 1: CONTEXT OF 'POSTGRESQL' MENTIONS ---")
pg_contexts = []
for idx, p in enumerate(doc.paragraphs):
    if "postgres" in p.text.lower():
        pg_contexts.append((f"P{idx}", p.text.strip()))

for t_idx, t in enumerate(doc.tables):
    for r_idx, r in enumerate(t.rows):
        for c_idx, c in enumerate(r.cells):
            if "postgres" in c.text.lower():
                pg_contexts.append((f"T{t_idx}_R{r_idx}_C{c_idx}", c.text.strip().replace("\n", " ")))

print(f"Total occurrences containing 'postgres': {len(pg_contexts)}")
for loc, ctx in pg_contexts:
    print(f"[{loc}] {ctx[:140]}...")

# Check 2: Context of LHASA / Glissements
print("\n--- TEST 2: CONTEXT OF 'LHASA' / 'GLISSEMENT' MENTIONS ---")
lhasa_contexts = []
for idx, p in enumerate(doc.paragraphs):
    if "lhasa" in p.text.lower() or "glissement" in p.text.lower():
        lhasa_contexts.append((f"P{idx}", p.text.strip()))

for t_idx, t in enumerate(doc.tables):
    for r_idx, r in enumerate(t.rows):
        for c_idx, c in enumerate(r.cells):
            if "lhasa" in c.text.lower() or "glissement" in c.text.lower():
                lhasa_contexts.append((f"T{t_idx}_R{r_idx}_C{c_idx}", c.text.strip().replace("\n", " ")))

print(f"Total occurrences: {len(lhasa_contexts)}")
for loc, ctx in lhasa_contexts:
    print(f"[{loc}] {ctx[:140]}...")

# Check 3: Check Annexes content depth
print("\n--- TEST 3: DEPTH OF ANNEXES ---")
annexes = ["ANNEXE A", "ANNEXE B", "ANNEXE D", "ANNEXE F"]
for ann in annexes:
    matching_paras = [p.text.strip() for p in doc.paragraphs if ann in p.text]
    print(f"  * Header found for {ann}: {matching_paras}")

# Check 4: Check if any dummy or placeholder text remains
print("\n--- TEST 4: CHECK FOR PLACEHOLDER OR LOREM IPSUM ARTIFACTS ---")
forbidden_keywords = ["lorem ipsum", "todo", "tbd", "placeholder", "xxx", "à compléter", "fixme", "dummy_text"]
found_placeholders = []
for idx, p in enumerate(doc.paragraphs):
    for kw in forbidden_keywords:
        if kw in p.text.lower():
            found_placeholders.append((f"P{idx}", kw, p.text[:100]))

for t_idx, t in enumerate(doc.tables):
    for r_idx, r in enumerate(t.rows):
        for c_idx, c in enumerate(r.cells):
            for kw in forbidden_keywords:
                if kw in c.text.lower():
                    found_placeholders.append((f"T{t_idx}_R{r_idx}_C{c_idx}", kw, c.text[:100]))

print(f"Placeholders found: {len(found_placeholders)}")
for loc, kw, txt in found_placeholders:
    print(f"  [{loc}] Found '{kw}': {txt}")

print("\nADVERSARIAL CHECKS COMPLETE.")

