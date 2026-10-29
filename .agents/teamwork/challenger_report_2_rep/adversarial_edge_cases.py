import os
import re
import sys
import docx

DOCX_PATH = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
doc = docx.Document(DOCX_PATH)

paras = [p.text for p in doc.paragraphs if p.text.strip()]
tables_text = []
for t in doc.tables:
    for row in t.rows:
        tables_text.append(" | ".join(c.text.strip().replace('\n', ' ') for c in row.cells))

full_corpus = "\n".join(paras) + "\n" + "\n".join(tables_text)

print("=== ADVERSARIAL EDGE CASE MINING ===")

# 1. Check for old zone hallucination ("Rusizi" or "versants occidentaux")
rusizi_matches = list(re.finditer(r".{0,60}rusizi.{0,60}", full_corpus, re.IGNORECASE))
print(f"\n1. Rusizi mentions count: {len(rusizi_matches)}")
for i, m in enumerate(rusizi_matches[:5]):
    print(f"   [{i+1}] {m.group(0).strip()}")

# 2. Check coordinates fidelity
coords_found = {
    "-3.42708": "-3.42708 in doc: " + str("-3.42708" in full_corpus),
    "29.9246": "29.9246 in doc: " + str("29.9246" in full_corpus),
    "-3.38193": "-3.38193 in doc: " + str("-3.38193" in full_corpus),
    "29.36142": "29.36142 in doc: " + str("29.36142" in full_corpus),
    "-3.10139": "-3.10139 in doc: " + str("-3.10139" in full_corpus),
    "-3.9279": "-3.9279 in doc: " + str("-3.9279" in full_corpus),
    "-3.4292": "-3.4292 in doc: " + str("-3.4292" in full_corpus),
    "-3.4389": "-3.4389 in doc: " + str("-3.4389" in full_corpus)
}
print("\n2. Exact coordinates in document:")
for k, v in coords_found.items():
    print(f"   {k}: {v}")

# 3. Check for any Alembic or PostgreSQL migration confusion
alembic_matches = list(re.finditer(r".{0,80}alembic.{0,80}", full_corpus, re.IGNORECASE))
print(f"\n3. Alembic mentions count: {len(alembic_matches)}")
for i, m in enumerate(alembic_matches):
    print(f"   [{i+1}] {m.group(0).strip()}")

# 4. Check for 31 tests registry and names
test_names = [
    "test_classement_zones",
    "test_buja_rural_mixte",
    "test_invalides",
    "test_pluie_24h_zone_montagne",
    "test_pluie_24h_zone_plaine_50_mm",
    "test_vent_bananier_40_kmh",
    "test_debit_prevu_et_reference"
]
print("\n4. Sample Pytest function names in document:")
for tn in test_names:
    print(f"   {tn}: {tn in full_corpus}")

# 5. Check Python 3.14 and uv mentions
print(f"\n5. Python 3.14 in doc: {'3.14' in full_corpus}")
print(f"   uv packaging in doc: {'uv' in full_corpus}")

# 6. Check DUMMY_HASH details
dummy_matches = list(re.finditer(r".{0,80}dummy_hash.{0,80}", full_corpus, re.IGNORECASE))
print(f"\n6. DUMMY_HASH snippets: {len(dummy_matches)}")
for i, m in enumerate(dummy_matches[:3]):
    print(f"   [{i+1}] {m.group(0).strip()}")

# 7. Check 50mm vs 100mm threshold mentions
print(f"\n7. Threshold 50mm in doc: {'50 mm' in full_corpus or '50mm' in full_corpus}")
print(f"   Threshold 100mm in doc: {'100 mm' in full_corpus or '100mm' in full_corpus}")
print(f"   Threshold 40km/h in doc: {'40 km/h' in full_corpus or '40km/h' in full_corpus}")

print("\n=== EDGE CASE MINING COMPLETE ===")
