import re

with open(r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\challenger_report_2\extracted_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

out = []
def p(s):
    out.append(s)

p("=== CHECK 1: POSTGRESQL CLAIMS ===")
pg_matches = [m.group(0) for m in re.finditer(r".{0,120}postgres.{0,120}", text, re.IGNORECASE)]
p(f"Total PostgreSQL matches: {len(pg_matches)}")
for i, m in enumerate(pg_matches):
    p(f"PG [{i+1}]: {m.strip()}\n")

p("\n=== CHECK 2: MONGODB & SQLITE CLAIMS ===")
mongo_sqlite_mentions = [m.group(0) for m in re.finditer(r".{0,120}(mongodb|sqlite).{0,120}", text, re.IGNORECASE)]
p(f"Total Mongo/SQLite snippets: {len(mongo_sqlite_mentions)}")
for i, m in enumerate(mongo_sqlite_mentions[:10]):
    p(f"DB [{i+1}]: {m.strip()}\n")

p("\n=== CHECK 3: PROVINCES & IMBO / MUMIRWA ===")
prov_snippets = [m.group(0) for m in re.finditer(r".{0,120}(5\s*provinces|buja_rural_imbo|buja_rural_mumirwa|plaine de l'imbo|mumirwa).{0,120}", text, re.IGNORECASE)]
p(f"Total Province snippets: {len(prov_snippets)}")
for i, m in enumerate(prov_snippets[:10]):
    p(f"PROV [{i+1}]: {m.strip()}\n")

p("\n=== CHECK 4: NASA LHASA RETRAIT ===")
lhasa_snippets = [m.group(0) for m in re.finditer(r".{0,120}(lhasa|glissement).{0,120}", text, re.IGNORECASE)]
p(f"Total LHASA snippets: {len(lhasa_snippets)}")
for i, m in enumerate(lhasa_snippets[:12]):
    p(f"LHASA [{i+1}]: {m.strip()}\n")

p("\n=== CHECK 5: ARGON2ID, DUMMY HASH, JWT, COOKIES ===")
sec_snippets = [m.group(0) for m in re.finditer(r".{0,120}(argon2|dummy|timing|httponly|access_token).{0,120}", text, re.IGNORECASE)]
p(f"Total Security snippets: {len(sec_snippets)}")
for i, m in enumerate(sec_snippets[:12]):
    p(f"SEC [{i+1}]: {m.strip()}\n")

p("\n=== CHECK 6: FASTAPI ROUTES ===")
route_snippets = [m.group(0) for m in re.finditer(r".{0,120}(/user|/token|/\{location\}).{0,120}", text, re.IGNORECASE)]
p(f"Total Route snippets: {len(route_snippets)}")
for i, m in enumerate(route_snippets[:10]):
    p(f"ROUTE [{i+1}]: {m.strip()}\n")

p("\n=== CHECK 7: LEAFLET 6 MARQUEURS & SVELTE 5 ===")
front_snippets = [m.group(0) for m in re.finditer(r".{0,120}(6\s*marqueurs|sveaflet|svelte\s*5|runes|\$state).{0,120}", text, re.IGNORECASE)]
p(f"Total Frontend snippets: {len(front_snippets)}")
for i, m in enumerate(front_snippets[:10]):
    p(f"FRONT [{i+1}]: {m.strip()}\n")

p("\n=== CHECK 8: SEUILS IGEBU & GLOFAS & PYTEST 31 TESTS ===")
test_snippets = [m.group(0) for m in re.finditer(r".{0,120}(31\s*tests|50\s*mm|100\s*mm|40\s*km/h|p75).{0,120}", text, re.IGNORECASE)]
p(f"Total Test & Seuil snippets: {len(test_snippets)}")
for i, m in enumerate(test_snippets[:12]):
    p(f"TEST/SEUIL [{i+1}]: {m.strip()}\n")

with open(r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\challenger_report_2\test_concordance_utf8.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("Saved test_concordance_utf8.txt")
