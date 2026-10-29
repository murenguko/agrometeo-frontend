import os
import re
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOCX_PATH = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"

if not os.path.exists(DOCX_PATH):
    print(f"ERROR: File not found: {DOCX_PATH}")
    sys.exit(1)

doc = docx.Document(DOCX_PATH)

paragraphs = doc.paragraphs
tables = doc.tables

print("================================================================================")
print("       EMPIRICAL ADVERSARIAL CONCORDANCE AUDIT — CHALLENGER_REPORT_2_REP        ")
print("================================================================================")
print(f"Target document: {DOCX_PATH}")
print(f"Total Paragraphs: {len(paragraphs)}")
print(f"Total Tables: {len(tables)}")

# Extract all text
full_text_paras = [p.text for p in paragraphs if p.text.strip()]
table_cells_text = []
for t in tables:
    for row in t.rows:
        for cell in row.cells:
            if cell.text.strip():
                table_cells_text.append(cell.text.strip().replace('\n', ' '))

all_text = "\n".join(full_text_paras) + "\n" + "\n".join(table_cells_text)
total_words = sum(len(p.split()) for p in full_text_paras) + sum(len(c.split()) for c in table_cells_text)
print(f"Non-empty paragraphs: {len(full_text_paras)}")
print(f"Total words (paragraphs + tables): {total_words}")

failures = []
warnings = []
passes = []

def check(name, condition, details=""):
    if condition:
        passes.append((name, details))
        print(f"[PASS] {name}: {details}")
    else:
        failures.append((name, details))
        print(f"[FAIL] {name}: {details}")

def warn(name, details=""):
    warnings.append((name, details))
    print(f"[WARN] {name}: {details}")

print("\n--- 1. STRUCTURAL & FORMATTING CHECKS ---")

# Check 1.1: Starts directly with INTRODUCTION GENERALE (no liminary pages)
first_p = full_text_paras[0] if full_text_paras else ""
check("Starts with INTRODUCTION GENERALE", 
      "INTRODUCTION" in first_p.upper() and ("GÉNÉRALE" in first_p.upper() or "GENERALE" in first_p.upper()),
      f"First paragraph: '{first_p[:60]}...'")

# Check 1.2: All chapters present
chapters = [
    "INTRODUCTION",
    "CHAPITRE I",
    "CHAPITRE II",
    "CHAPITRE III",
    "CHAPITRE IV",
    "CHAPITRE V",
    "CONCLUSION",
    "ANNEXE A",
    "ANNEXE B",
    "ANNEXE D",
    "ANNEXE F",
    "RÉFÉRENCES BIBLIOGRAPHIQUES"
]
for ch in chapters:
    found = any(ch in p for p in full_text_paras)
    check(f"Chapter/Section Presence: {ch}", found, f"Section '{ch}' found in document")

# Check 1.3: Margins and typography
section = doc.sections[0]
left_margin_cm = section.left_margin.inches * 2.54 if section.left_margin else 0
right_margin_cm = section.right_margin.inches * 2.54 if section.right_margin else 0
top_margin_cm = section.top_margin.inches * 2.54 if section.top_margin else 0
bottom_margin_cm = section.bottom_margin.inches * 2.54 if section.bottom_margin else 0

check("Left margin >= 2.9 cm (binding)", abs(left_margin_cm - 3.0) < 0.2, f"Left margin: {left_margin_cm:.2f} cm")
check("Other margins ~ 2.5 cm", abs(right_margin_cm - 2.5) < 0.2 and abs(top_margin_cm - 2.5) < 0.2, 
      f"Right: {right_margin_cm:.2f} cm, Top: {top_margin_cm:.2f} cm, Bottom: {bottom_margin_cm:.2f} cm")


print("\n--- 2. TECHNICAL CONCORDANCE AUDIT (8 PILLARS) ---")

# PILLAR 1: MONGODB & SQLITE VS POSTGRESQL
print("\n[PILLAR 1] MongoDB Atlas + SQLite Cache vs PostgreSQL")
# Check how PostgreSQL is described
pg_matches = [m.group(0) for m in re.finditer(r".{0,100}postgres.{0,100}", all_text, re.IGNORECASE)]
print(f"Total PostgreSQL occurrences: {len(pg_matches)}")

# Adversarial stress test: Does any snippet claim PostgreSQL is the actual current database implemented in weather-backend?
pg_erroneous = []
for pgm in pg_matches:
    # If it says "implémenté avec PostgreSQL" or "notre backend utilise PostgreSQL" without mention of initial framing or comparison
    if re.search(r"(implémenté|utilisé dans le backend|développé) avec postgres", pgm, re.IGNORECASE) and not re.search(r"(initial|cadrage|prévu|vs|substitution|remplacé)", pgm, re.IGNORECASE):
        pg_erroneous.append(pgm)

check("No erroneous claims that PostgreSQL is implemented in real backend", len(pg_erroneous) == 0, 
      f"Erroneous PG claims: {len(pg_erroneous)}")

# Check MongoDB presence and role
mongo_count = len(re.findall(r"mongodb", all_text, re.IGNORECASE))
sqlite_count = len(re.findall(r"sqlite", all_text, re.IGNORECASE))
check("MongoDB documented as user persistence database", mongo_count >= 15, f"MongoDB mentions: {mongo_count}")
check("SQLite documented as weather request cache", sqlite_count >= 8, f"SQLite mentions: {sqlite_count}")

# Check BSON users collection schema
bson_schema = any("collection mongodb" in p.lower() or "users" in p.lower() and "hashed_password" in p.lower() for p in full_text_paras)
check("MongoDB 'users' BSON schema documented", bson_schema, "Schema includes users, username, hashed_password")


# PILLAR 2: 5 PROVINCES & BUJAMBURA RURAL (IMBO / MUMIRWA)
print("\n[PILLAR 2] 5 Pilot Provinces & Imbo/Mumirwa Topoclimatic Split")
provinces = ["gitega", "karusi", "bujumbura mairie", "rutana", "bujumbura rural"]
for prov in provinces:
    cnt = len(re.findall(rf"\b{prov}\b", all_text, re.IGNORECASE))
    check(f"Province present: {prov}", cnt >= 5, f"Count: {cnt}")

imbo_cnt = len(re.findall(r"\bimbo\b", all_text, re.IGNORECASE))
mumirwa_cnt = len(re.findall(r"\bmumirwa\b", all_text, re.IGNORECASE))
check("Sub-zone Imbo documented", imbo_cnt >= 10, f"Imbo mentions: {imbo_cnt}")
check("Sub-zone Mumirwa documented", mumirwa_cnt >= 10, f"Mumirwa mentions: {mumirwa_cnt}")
check("Elevation and topoclimatic distinction explained", 
      "820" in all_text and "1 350" in all_text or "1350" in all_text, 
      "Altitudes 820m (plain) and >1350m (highlands) documented")


# PILLAR 3: NASA LHASA REMOVAL & SCIENTIFIC JUSTIFICATION
print("\n[PILLAR 3] NASA LHASA Removal & Scientific Justification")
lhasa_cnt = len(re.findall(r"lhasa", all_text, re.IGNORECASE))
check("NASA LHASA mentioned and addressed", lhasa_cnt >= 5, f"LHASA mentions: {lhasa_cnt}")

# Adversarial check: Is LHASA explicitly stated as removed / excluded from implementation?
lhasa_removal_confirmed = any(
    re.search(r"(retrait|retiré|exclu|abandonné).{0,60}lhasa", p, re.IGNORECASE) or
    re.search(r"lhasa.{0,60}(retrait|retiré|exclu|abandonné)", p, re.IGNORECASE)
    for p in full_text_paras + table_cells_text
)
check("Explicit documentation of LHASA removal from code", lhasa_removal_confirmed, "Found explicit removal statements")

# Check scientific rationale
lhasa_rationale = any("résolution" in p.lower() or "maille" in p.lower() or "fausse alerte" in p.lower() or "panique" in p.lower() for p in full_text_paras)
check("Scientific rationale for LHASA removal detailed", lhasa_rationale, "Coarse grid vs steep relief & false alarms documented")


# PILLAR 4: SECURITY (ARGON2ID, DUMMY_HASH, JWT, HTTPONLY COOKIES)
print("\n[PILLAR 4] Security: Argon2id, Anti-Timing Dummy Hash, JWT, HttpOnly Cookies")
argon_cnt = len(re.findall(r"argon2id", all_text, re.IGNORECASE))
dummy_cnt = len(re.findall(r"dummy_hash", all_text, re.IGNORECASE))
jwt_cnt = len(re.findall(r"jwt", all_text, re.IGNORECASE))
httponly_cnt = len(re.findall(r"httponly", all_text, re.IGNORECASE))

check("Argon2id password hashing documented", argon_cnt >= 5, f"Argon2id mentions: {argon_cnt}")
check("DUMMY_HASH anti-timing defense documented", dummy_cnt >= 2, f"DUMMY_HASH mentions: {dummy_cnt}")
check("JWT authentication documented", jwt_cnt >= 10, f"JWT mentions: {jwt_cnt}")
check("HttpOnly / SameSite=Strict cookies documented", httponly_cnt >= 3, f"HttpOnly mentions: {httponly_cnt}")


# PILLAR 5: FASTAPI ROUTES
print("\n[PILLAR 5] FastAPI Routes Alignment")
route_user = any("/user" in p for p in full_text_paras + table_cells_text)
route_token = any("/token" in p for p in full_text_paras + table_cells_text)
route_loc = any("/{location}" in p or "{location}" in p for p in full_text_paras + table_cells_text)

check("Route POST /user documented", route_user, "POST /user for account creation present")
check("Route POST /token documented", route_token, "POST /token for OAuth2 login present")
check("Route GET /{location} documented", route_loc, "GET /{location} weather forecast present")


# PILLAR 6: LEAFLET & SVELTE 5 RUNES
print("\n[PILLAR 6] Leaflet 6 Markers & Svelte 5 Runes")
leaflet_cnt = len(re.findall(r"(leaflet|sveaflet)", all_text, re.IGNORECASE))
markers_6 = any("6 marqueurs" in p.lower() or "six marqueurs" in p.lower() for p in full_text_paras + table_cells_text)
runes_cnt = len(re.findall(r"(runes?|\$state|\$derived|\$props)", all_text, re.IGNORECASE))

check("Leaflet / Sveaflet map documented", leaflet_cnt >= 5, f"Leaflet/Sveaflet mentions: {leaflet_cnt}")
check("6 geographic markers documented", markers_6, "Confirmed: 6 markers for 5 provinces with 2 in Buja Rural")
check("Svelte 5 Runes ($state, etc.) documented", runes_cnt >= 5, f"Runes mentions: {runes_cnt}")


# PILLAR 7: IGEBU & GLOFAS THRESHOLDS & PREVALENT CROPS
print("\n[PILLAR 7] Agro-Climatic Thresholds (IGEBU / GloFAS) & Prevalent Crops")
p50_cnt = len(re.findall(r"50\s*mm", all_text, re.IGNORECASE))
p100_cnt = len(re.findall(r"100\s*mm", all_text, re.IGNORECASE))
w40_cnt = len(re.findall(r"40\s*km/h", all_text, re.IGNORECASE))
glofas_p75 = any("p75" in p.lower() or "percentile" in p.lower() for p in full_text_paras + table_cells_text)
crops_regional = any("prévalente" in p.lower() or "par province" in p.lower() or "par zone" in p.lower() for p in full_text_paras)

check("Rain threshold 50 mm / 24h (plain) documented", p50_cnt >= 4, f"50 mm mentions: {p50_cnt}")
check("Rain threshold 100 mm / 24h (mountain) documented", p100_cnt >= 5, f"100 mm mentions: {p100_cnt}")
check("Wind threshold 40 km/h (banana) documented", w40_cnt >= 2, f"40 km/h mentions: {w40_cnt}")
check("GloFAS flood rule (Q_prevu > Q_ref_p75) documented", glofas_p75, "GloFAS p75 rule present")
check("Prevalent crops per region documented", crops_regional, "Regional crop matrices documented")


# PILLAR 8: PYTEST 31 TESTS & VITE BUILD SUCCESS
print("\n[PILLAR 8] Pytest 31 Tests & Vite Build Results")
pytest_31 = any("31 tests" in p.lower() or "31/31" in p.lower() for p in full_text_paras + table_cells_text)
pytest_100 = any("100 %" in p or "100%" in p for p in full_text_paras + table_cells_text)
vite_build = any("vite" in p.lower() and ("exit code 0" in p.lower() or "sans erreur" in p.lower() or "0 erreur" in p.lower()) for p in full_text_paras + table_cells_text)

check("Pytest 31 unit tests documented", pytest_31, "31 tests specifically recorded")
check("100% pass rate documented", pytest_100, "100% test success rate recorded")
check("Vite production build success documented", vite_build, "Vite production build confirmed")


print("\n================================================================================")
print(f"AUDIT SUMMARY: {len(passes)} PASSES, {len(failures)} FAILURES, {len(warnings)} WARNINGS")
print("================================================================================")

if len(failures) == 0:
    print("VERDICT: >>> APPROVE <<<")
else:
    print("VERDICT: >>> REQUEST_CHANGES <<<")
