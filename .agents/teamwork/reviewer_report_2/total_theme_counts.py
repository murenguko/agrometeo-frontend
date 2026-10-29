import docx
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

themes = {
    "1. MongoDB / NoSQL vs Postgres": [r"MongoDB", r"NoSQL", r"PostgreSQL"],
    "2. NASA LHASA / Glissements retrait": [r"LHASA", r"glissement"],
    "3. Cultures régionales ISABU": [r"CULTURES_PAR_ZONE", r"cultures prévalentes", r"ISABU", r"cultures"],
    "4. 5 provinces / sous-zones (Imbo/Mumirwa)": [r"Bujumbura Rural", r"Mumirwa", r"Imbo", r"Karusi", r"Rutana", r"Gitega"],
    "5. Authentification (Argon2id, JWT, DUMMY_HASH)": [r"Argon2id", r"DUMMY_HASH", r"JWT", r"OAuth2", r"authentification"]
}

total_counts = {k: 0 for k in themes}

# Check paragraphs
for p in doc.paragraphs:
    for k, pats in themes.items():
        for pat in pats:
            total_counts[k] += len(re.findall(pat, p.text, re.IGNORECASE))

# Check tables
for t in doc.tables:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for k, pats in themes.items():
                    for pat in pats:
                        total_counts[k] += len(re.findall(pat, p.text, re.IGNORECASE))

print("=== TOTAL OCCURRENCES IN ENTIRE DOCUMENT (TEXT + TABLES) ===")
for k, count in total_counts.items():
    print(f"  * {k}: {count} occurrences")
