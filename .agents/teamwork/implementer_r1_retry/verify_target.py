import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
doc = docx.Document(target_path)

print("================================================================================")
print("     INDEPENDENT CONCORDANCE & INTEGRITY AUDIT — FINAL DELIVERABLE              ")
print("================================================================================")

passes = 0
fails = 0

def check(name, condition, detail=""):
    global passes, fails
    if condition:
        passes += 1
        print(f"  [PASS] {name}: {detail}")
    else:
        fails += 1
        print(f"  [FAIL] {name} -> {detail}")

# 1. Sections and Pagination
check("Section Count", len(doc.sections) == 2, f"Found {len(doc.sections)} sections (expected 2)")

sec0 = doc.sections[0]
sec1 = doc.sections[1]

# Margins
check("Sec0 Left Margin (Reliure)", abs(sec0.left_margin.cm - 3.0) < 0.05, f"{sec0.left_margin.cm:.2f} cm")
check("Sec0 Right Margin", abs(sec0.right_margin.cm - 2.5) < 0.05, f"{sec0.right_margin.cm:.2f} cm")
check("Sec0 Top Margin", abs(sec0.top_margin.cm - 2.5) < 0.05, f"{sec0.top_margin.cm:.2f} cm")
check("Sec0 Bottom Margin", abs(sec0.bottom_margin.cm - 2.5) < 0.05, f"{sec0.bottom_margin.cm:.2f} cm")

check("Sec1 Left Margin (Reliure)", abs(sec1.left_margin.cm - 3.0) < 0.05, f"{sec1.left_margin.cm:.2f} cm")
check("Sec1 Right Margin", abs(sec1.right_margin.cm - 2.5) < 0.05, f"{sec1.right_margin.cm:.2f} cm")
check("Sec1 Top Margin", abs(sec1.top_margin.cm - 2.5) < 0.05, f"{sec1.top_margin.cm:.2f} cm")
check("Sec1 Bottom Margin", abs(sec1.bottom_margin.cm - 2.5) < 0.05, f"{sec1.bottom_margin.cm:.2f} cm")

# Page number formats in sectPr
pgNum0 = sec0._sectPr.find(docx.oxml.ns.qn('w:pgNumType'))
fmt0 = pgNum0.get(docx.oxml.ns.qn('w:fmt')) if pgNum0 is not None else None
start0 = pgNum0.get(docx.oxml.ns.qn('w:start')) if pgNum0 is not None else None
check("Sec0 Page Num Format", fmt0 == 'lowerRoman' and start0 == '1', f"fmt={fmt0}, start={start0}")

pgNum1 = sec1._sectPr.find(docx.oxml.ns.qn('w:pgNumType'))
fmt1 = pgNum1.get(docx.oxml.ns.qn('w:fmt')) if pgNum1 is not None else None
start1 = pgNum1.get(docx.oxml.ns.qn('w:start')) if pgNum1 is not None else None
check("Sec1 Page Num Format", fmt1 == 'decimal' and start1 == '1', f"fmt={fmt1}, start={start1}")

# Footers centered
check("Sec0 Footer Field", "PAGE" in sec0.footer.paragraphs[0]._element.xml, "Dynamic PAGE field present in sec0 footer")
check("Sec1 Footer Field", "PAGE" in sec1.footer.paragraphs[0]._element.xml, "Dynamic PAGE field present in sec1 footer")

# 2. Preliminary Pages Content Checks
p_idx_sec1_start = None
for idx, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        p_idx_sec1_start = idx
        break

check("Body Starts with INTRODUCTION GÉNÉRALE", p_idx_sec1_start is not None, f"at index {p_idx_sec1_start}")

prelim_text = "\n".join(p.text for p in doc.paragraphs[:p_idx_sec1_start])

# Page de garde checks
cover_requirements = [
    "RÉPUBLIQUE DU BURUNDI",
    "MINISTÈRE DE L'ÉDUCATION NATIONALE ET DE LA RECHERCHE SCIENTIFIQUE",
    "UNIVERSITÉ POLYTECHNIQUE DE GITEGA",
    "FACULTÉ DES TECHNOLOGIES DE L'INFORMATION ET DE LA COMMUNICATION",
    "GÉNIE LOGICIEL",
    "PROJET II",
    "SYSTÈME DE VEILLE MÉTÉO ET CLIMATIQUE AU BURUNDI",
    "Présenté et soutenu par",
    "Sous la direction de",
    "Année Académique"
]
for req in cover_requirements:
    check(f"Page de garde : {req}", req.upper() in prelim_text.upper(), "Present in cover page")

# Table des matières checks
toc_checks = [
    "TABLE DES MATIÈRES",
    "INTRODUCTION GÉNÉRALE",
    "CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC",
    "CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART",
    "CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE",
    "CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION",
    "CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION",
    "CONCLUSION GÉNÉRALE ET PERSPECTIVES",
    "RÉFÉRENCES BIBLIOGRAPHIQUES",
    "TABLE DES ANNEXES",
    "ANNEXE A",
    "ANNEXE B",
    "ANNEXE D"
]
for tc in toc_checks:
    check(f"TOC/Annexes : {tc}", tc.upper() in prelim_text.upper(), "Present in TOC")

# Figures checks
figures_checks = [
    "LISTE DES FIGURES",
    "Figure 1.2 — Diagramme de flux du parcours utilisateur complet",
    "Figure 2.1 — Diagramme architectural du patron Backend-For-Frontend (BFF)",
    "Figure 3.1 — Architecture logicielle globale en couches et interconnexions de données",
    "Figure 3.2 — Diagramme de cas d'utilisation du système AgroMétéo Burundi",
    "Figure 3.3 — Diagramme de classes métier du backend AgroMétéo Burundi",
    "Figure 3.4 — Diagramme de composants logiciels du système",
    "Figure 3.5 — Diagramme de séquence de l'authentification OAuth2 / JWT",
    "Figure 3.6 — Diagramme de séquence de la consultation d'un bulletin agro-météorologique",
    "Figure 4.1 — Structure modulaire de la base de code du backend FastAPI",
    "Figure 4.2 — Structure modulaire du frontend SvelteKit"
]
for fc in figures_checks:
    check(f"Figures List : {fc[:30]}", fc.upper() in prelim_text.upper(), "Present in figures list")

# Tables list checks
tables_checks = [
    "LISTE DES TABLEAUX",
    "Tableau 0.1",
    "Tableau 1.1",
    "Tableau 1.2",
    "Tableau 3.1",
    "Tableau 3.2",
    "Tableau 3.3",
    "Tableau 3.4",
    "Tableau 4.1",
    "Tableau 5.1",
    "Tableau A.1",
    "Tableau A.2",
    "Tableau B.1",
    "Tableau B.2"
]
for tbc in tables_checks:
    check(f"Tables List : {tbc}", tbc.upper() in prelim_text.upper(), "Present in tables list")

# Sigles checks
sigles_req = [
    "UPG", "TIC", "ISABU", "IGEBU", "GloFAS", "NASA", "LHASA", "CHIRPS", "MVP",
    "API", "REST", "BFF", "SSR", "JWT", "OAuth2", "OWASP", "SGBD", "NoSQL",
    "SQL", "JSON", "GeoJSON", "HTML", "CSS", "UI", "UX", "WCAG", "UML", "TTL"
]
for s in sigles_req:
    check(f"Sigle {s}", re.search(rf"\b{re.escape(s)}\b", prelim_text), f"Found {s} in sigles list")

# 3. Preservation of body chapters
print("\n--- Checking body chapters presence ---")
body_text = "\n".join(p.text for p in doc.paragraphs[p_idx_sec1_start:])
chapters_req = [
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
    "RÉFÉRENCES BIBLIOGRAPHIQUES"
]
for cr in chapters_req:
    check(f"Body Chapter: {cr[:30]}", cr in body_text, "Preserved in body")

check("Tables in Deliverable", len(doc.tables) == 16, f"16 tables preserved (found {len(doc.tables)})")

# 4. Bibliography Verification
print("\n--- Checking Bibliography ---")
biblio_paras = []
in_biblio = False
for p in doc.paragraphs[p_idx_sec1_start:]:
    if p.text.strip() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        in_biblio = True
        continue
    if in_biblio:
        biblio_paras.append(p.text)

check("Bibliography Entries Count", len(biblio_paras) == 30, f"Found {len(biblio_paras)} entries (expected 30)")

# Check concordance of in-text citations with biblio entries
check("Biblio [1] PNA Burundi", "[1]" in biblio_paras[0] and "Plan National d'Adaptation" in biblio_paras[0])
check("Biblio [2] ISTEEBU / Agriculture", "[2]" in biblio_paras[1] and "ISTEEBU" in biblio_paras[1])
check("Biblio [5] Décret IGEBU", "[5]" in biblio_paras[4] and "IGEBU" in biblio_paras[4])
check("Biblio [6] Distributed Systems", "[6]" in biblio_paras[5] and "Distributed Systems" in biblio_paras[5])
check("Biblio [7] Newman BFF", "[7]" in biblio_paras[6] and "Newman" in biblio_paras[6])
check("Biblio [10] Fielding REST", "[10]" in biblio_paras[9] and "Fielding" in biblio_paras[9])
check("Biblio [12] Brumley Timing Attacks", "[12]" in biblio_paras[11] and "Brumley" in biblio_paras[11])
check("Biblio [13] JWT RFC 7519", "[13]" in biblio_paras[12] and "RFC 7519" in biblio_paras[12])
check("Biblio [14] WCAG 2.1", "[14]" in biblio_paras[13] and "WCAG" in biblio_paras[13])
check("Biblio [15] MoSCoW Clegg", "[15]" in biblio_paras[14] and "MoSCoW" in biblio_paras[14])
check("Biblio [16] OMG UML", "[16]" in biblio_paras[15] and "UML" in biblio_paras[15])
check("Biblio [17] IGEBU Pluviométrie", "[17]" in biblio_paras[16] and "IGEBU" in biblio_paras[16])
check("Biblio [18] ISABU Fiches cultures", "[18]" in biblio_paras[17] and "ISABU" in biblio_paras[17])
check("Biblio [19] Scrum Guide", "[19]" in biblio_paras[18] and "Scrum" in biblio_paras[18])
check("Biblio [20] Mike Cohn Testing", "[20]" in biblio_paras[19] and "Cohn" in biblio_paras[19])
check("Biblio [21] Open-Meteo", "[21]" in biblio_paras[20] and "Open-Meteo" in biblio_paras[20])
check("Biblio [22] GloFAS", "[22]" in biblio_paras[21] and "GloFAS" in biblio_paras[21])
check("Biblio [23] NASA LHASA", "[23]" in biblio_paras[22] and "LHASA" in biblio_paras[22])
check("Biblio [26] MongoDB & SQLite", "[26]" in biblio_paras[25] and "MongoDB" in biblio_paras[25])

print(f"\nFINAL VERIFICATION SCORE: {passes} PASSES, {fails} FAILS")
