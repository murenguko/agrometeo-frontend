import docx
import json

doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\implementer_r1_retry\doc_analysis.json', 'r', encoding='utf-8') as f:
    orig = json.load(f)

print("Original analysis keys:", orig.keys())
print("Original paragraphs count:", orig.get('num_paragraphs'))
print("Original tables count:", orig.get('num_tables'))

intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

# The original document started directly at INTRODUCTION GÉNÉRALE before preliminary pages were inserted!
# So original paragraph 0 was INTRODUCTION GÉNÉRALE!
orig_paras = orig.get('paragraphs', [])
current_body_paras = doc.paragraphs[intro_idx:]

print(f"Original paragraphs count: {len(orig_paras)}")
print(f"Current body paragraphs count: {len(current_body_paras)}")

# Compare text of body paragraphs up to bibliography
biblio_idx = None
for i, p in enumerate(current_body_paras):
    if p.text.strip() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        biblio_idx = i
        break

print(f"Body has {biblio_idx} paragraphs before RÉFÉRENCES BIBLIOGRAPHIQUES.")

mismatches = []
for i in range(biblio_idx):
    orig_text = orig_paras[i]['text'].strip() if i < len(orig_paras) else None
    curr_text = current_body_paras[i].text.strip()
    if orig_text != curr_text:
        mismatches.append((i, orig_text, curr_text))

print(f"Mismatches before RÉFÉRENCES BIBLIOGRAPHIQUES: {len(mismatches)}")
if mismatches:
    for i, ot, ct in mismatches[:5]:
        print(f"  Mismatch at {i}:")
        print(f"    orig: {repr(ot)[:60]}")
        print(f"    curr: {repr(ct)[:60]}")
else:
    print("ALL body paragraphs before RÉFÉRENCES BIBLIOGRAPHIQUES are 100% IDENTICAL to the original!")
