import docx
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

themes = {
    "1. MongoDB / NoSQL vs Postgres": [r"MongoDB", r"NoSQL", r"PostgreSQL"],
    "2. NASA LHASA / Glissements retrait": [r"LHASA", r"glissement"],
    "3. Cultures régionales ISABU": [r"CULTURES_PAR_ZONE", r"cultures prévalentes", r"ISABU"],
    "4. 5 provinces / sous-zones (Imbo/Mumirwa)": [r"Bujumbura Rural", r"Mumirwa", r"Imbo", r"Karusi", r"Rutana", r"Gitega"],
    "5. Authentification (Argon2id, JWT, DUMMY_HASH)": [r"Argon2id", r"DUMMY_HASH", r"JWT", r"OAuth2", r"authentification"]
}

# Determine chapter for each paragraph
current_chapter = "PRÉAMBULE"
chapter_paragraphs = {}

for p in doc.paragraphs:
    txt = p.text.strip()
    if not txt:
        continue
    for ch_name in [
        "INTRODUCTION GÉNÉRALE",
        "CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC",
        "CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART",
        "CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE",
        "CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION",
        "CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION",
        "CONCLUSION GÉNÉRALE ET PERSPECTIVES",
        "ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS",
        "ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES",
        "ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION",
        "ANNEXE F — DÉPÔT GIT, STRUCTURE DU CODE SOURCE ET MÉTRIQUES",
        "RÉFÉRENCES BIBLIOGRAPHIQUES"
    ]:
        if ch_name in txt:
            current_chapter = ch_name
            break
    if current_chapter not in chapter_paragraphs:
        chapter_paragraphs[current_chapter] = []
    chapter_paragraphs[current_chapter].append(txt)

print("=== THEME DISTRIBUTION ACROSS CHAPTERS ===")
for ch_name, paras in chapter_paragraphs.items():
    print(f"\n--- {ch_name} ({len(paras)} paras) ---")
    full_text = "\n".join(paras)
    for theme_name, regexes in themes.items():
        count = sum(len(re.findall(rx, full_text, re.IGNORECASE)) for rx in regexes)
        print(f"  * {theme_name}: {count} occurrences")
