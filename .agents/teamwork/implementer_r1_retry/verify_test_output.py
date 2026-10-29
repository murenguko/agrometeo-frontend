import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

orig_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx.bak"
new_path = r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\implementer_r1_retry\test_output.docx"

doc_orig = docx.Document(orig_path)
doc_new = docx.Document(new_path)

print("================================================================================")
print("              COMPREHENSIVE DEEP VERIFICATION OF TEST OUTPUT                    ")
print("================================================================================")

passes = 0
fails = 0

def assert_check(name, condition, detail=""):
    global passes, fails
    if condition:
        passes += 1
        print(f"  [PASS] {name}: {detail}")
    else:
        fails += 1
        print(f"  [FAIL] {name} -> {detail}")

# 1. Sections and Pagination
assert_check("Section Count", len(doc_new.sections) == 2, f"Found {len(doc_new.sections)} sections (expected 2)")

sec0 = doc_new.sections[0]
sec1 = doc_new.sections[1]

# Margins
assert_check("Sec0 Left Margin (Reliure)", abs(sec0.left_margin.cm - 3.0) < 0.05, f"{sec0.left_margin.cm:.2f} cm")
assert_check("Sec0 Right Margin", abs(sec0.right_margin.cm - 2.5) < 0.05, f"{sec0.right_margin.cm:.2f} cm")
assert_check("Sec0 Top Margin", abs(sec0.top_margin.cm - 2.5) < 0.05, f"{sec0.top_margin.cm:.2f} cm")
assert_check("Sec0 Bottom Margin", abs(sec0.bottom_margin.cm - 2.5) < 0.05, f"{sec0.bottom_margin.cm:.2f} cm")

assert_check("Sec1 Left Margin (Reliure)", abs(sec1.left_margin.cm - 3.0) < 0.05, f"{sec1.left_margin.cm:.2f} cm")
assert_check("Sec1 Right Margin", abs(sec1.right_margin.cm - 2.5) < 0.05, f"{sec1.right_margin.cm:.2f} cm")
assert_check("Sec1 Top Margin", abs(sec1.top_margin.cm - 2.5) < 0.05, f"{sec1.top_margin.cm:.2f} cm")
assert_check("Sec1 Bottom Margin", abs(sec1.bottom_margin.cm - 2.5) < 0.05, f"{sec1.bottom_margin.cm:.2f} cm")

# Page number formats in sectPr
pgNum0 = sec0._sectPr.find(docx.oxml.ns.qn('w:pgNumType'))
fmt0 = pgNum0.get(docx.oxml.ns.qn('w:fmt')) if pgNum0 is not None else None
start0 = pgNum0.get(docx.oxml.ns.qn('w:start')) if pgNum0 is not None else None
assert_check("Sec0 Page Num Format", fmt0 == 'lowerRoman' and start0 == '1', f"fmt={fmt0}, start={start0}")

pgNum1 = sec1._sectPr.find(docx.oxml.ns.qn('w:pgNumType'))
fmt1 = pgNum1.get(docx.oxml.ns.qn('w:fmt')) if pgNum1 is not None else None
start1 = pgNum1.get(docx.oxml.ns.qn('w:start')) if pgNum1 is not None else None
assert_check("Sec1 Page Num Format", fmt1 == 'decimal' and start1 == '1', f"fmt={fmt1}, start={start1}")

# Footers centered
f0_text = sec0.footer.paragraphs[0].text
assert_check("Sec0 Footer Field", "PAGE" in sec0.footer.paragraphs[0]._element.xml, "Dynamic PAGE field present in sec0 footer")
assert_check("Sec1 Footer Field", "PAGE" in sec1.footer.paragraphs[0]._element.xml, "Dynamic PAGE field present in sec1 footer")

# 2. Preliminary Pages Content Checks
all_sec0_paras = []
# Find where sec0 ends: paragraph with sectPr
p_idx_sec1_start = None
for idx, p in enumerate(doc_new.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        p_idx_sec1_start = idx
        break

assert_check("Body Starts with INTRODUCTION GÉNÉRALE", p_idx_sec1_start is not None, f"at index {p_idx_sec1_start}")

prelim_text = "\n".join(p.text for p in doc_new.paragraphs[:p_idx_sec1_start])

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
    assert_check(f"Page de garde : {req}", req.upper() in prelim_text.upper(), "Present in cover page")

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
    assert_check(f"TOC/Annexes : {tc}", tc.upper() in prelim_text.upper(), "Present in TOC")

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
    assert_check(f"Figures List : {fc[:30]}", fc.upper() in prelim_text.upper(), "Present in figures list")

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
    assert_check(f"Tables List : {tbc}", tbc.upper() in prelim_text.upper(), "Present in tables list")

# Sigles checks
sigles_req = [
    "UPG", "TIC", "ISABU", "IGEBU", "GloFAS", "NASA", "LHASA", "CHIRPS", "MVP",
    "API", "REST", "BFF", "SSR", "JWT", "OAuth2", "OWASP", "SGBD", "NoSQL",
    "SQL", "JSON", "GeoJSON", "HTML", "CSS", "UI", "UX", "WCAG", "UML", "TTL"
]
for s in sigles_req:
    assert_check(f"Sigle {s}", re.search(rf"\b{re.escape(s)}\b", prelim_text), f"Found {s} in sigles list")

# 3. Preservation of body text
print("\n--- Checking preservation of body text ---")
# The original document had 473 paragraphs from P[0] to P[472] (before biblio heading P[473])
orig_body_paras = [p.text for p in doc_orig.paragraphs[:473]]
new_body_paras = [p.text for p in doc_new.paragraphs[p_idx_sec1_start : p_idx_sec1_start + 473]]

assert_check("Body Paragraphs Count Identical", len(orig_body_paras) == len(new_body_paras), 
             f"Original={len(orig_body_paras)}, New={len(new_body_paras)}")

diffs = []
for i in range(len(orig_body_paras)):
    if orig_body_paras[i] != new_body_paras[i]:
        diffs.append((i, orig_body_paras[i][:40], new_body_paras[i][:40]))

assert_check("Body Paragraphs Text 100% Identical", len(diffs) == 0, f"Diffs count: {len(diffs)}")
if diffs:
    for d in diffs[:5]:
        print(f"   Diff at relative index {d[0]}: orig='{d[1]}' vs new='{d[2]}'")

# Check tables preservation
assert_check("Tables Count Identical", len(doc_orig.tables) == len(doc_new.tables), 
             f"Original={len(doc_orig.tables)}, New={len(doc_new.tables)}")

table_diffs = []
for t_idx in range(len(doc_orig.tables)):
    t_orig = doc_orig.tables[t_idx]
    t_new = doc_new.tables[t_idx]
    if len(t_orig.rows) != len(t_new.rows) or len(t_orig.columns) != len(t_new.columns):
        table_diffs.append((t_idx, "dimension mismatch"))
    else:
        for r_idx in range(len(t_orig.rows)):
            for c_idx in range(len(t_orig.columns)):
                if t_orig.cell(r_idx, c_idx).text != t_new.cell(r_idx, c_idx).text:
                    table_diffs.append((t_idx, f"cell ({r_idx},{c_idx}) mismatch"))
                    break

assert_check("All 16 Tables Content 100% Identical", len(table_diffs) == 0, f"Table diffs count: {len(table_diffs)}")

# 4. Bibliography Verification
print("\n--- Checking Bibliography ---")
new_biblio_paras = [p.text for p in doc_new.paragraphs[p_idx_sec1_start + 474:]]
assert_check("Bibliography Entries Count", len(new_biblio_paras) == 30, f"Found {len(new_biblio_paras)} entries (expected 30)")

# Check concordance of in-text citations with biblio entries
biblio_text = "\n".join(new_biblio_paras)
assert_check("Biblio [1] PNA Burundi", "[1]" in new_biblio_paras[0] and "Plan National d'Adaptation" in new_biblio_paras[0])
assert_check("Biblio [2] ISTEEBU / Agriculture", "[2]" in new_biblio_paras[1] and "ISTEEBU" in new_biblio_paras[1])
assert_check("Biblio [5] Décret IGEBU", "[5]" in new_biblio_paras[4] and "IGEBU" in new_biblio_paras[4])
assert_check("Biblio [6] Distributed Systems", "[6]" in new_biblio_paras[5] and "Distributed Systems" in new_biblio_paras[5])
assert_check("Biblio [7] Newman BFF", "[7]" in new_biblio_paras[6] and "Newman" in new_biblio_paras[6])
assert_check("Biblio [10] Fielding REST", "[10]" in new_biblio_paras[9] and "Fielding" in new_biblio_paras[9])
assert_check("Biblio [12] Brumley Timing Attacks", "[12]" in new_biblio_paras[11] and "Brumley" in new_biblio_paras[11])
assert_check("Biblio [13] JWT RFC 7519", "[13]" in new_biblio_paras[12] and "RFC 7519" in new_biblio_paras[12])
assert_check("Biblio [14] WCAG 2.1", "[14]" in new_biblio_paras[13] and "WCAG" in new_biblio_paras[13])
assert_check("Biblio [15] MoSCoW Clegg", "[15]" in new_biblio_paras[14] and "MoSCoW" in new_biblio_paras[14])
assert_check("Biblio [16] OMG UML", "[16]" in new_biblio_paras[15] and "UML" in new_biblio_paras[15])
assert_check("Biblio [17] IGEBU Pluviométrie", "[17]" in new_biblio_paras[16] and "IGEBU" in new_biblio_paras[16])
assert_check("Biblio [18] ISABU Fiches cultures", "[18]" in new_biblio_paras[17] and "ISABU" in new_biblio_paras[17])
assert_check("Biblio [19] Scrum Guide", "[19]" in new_biblio_paras[18] and "Scrum" in new_biblio_paras[18])
assert_check("Biblio [20] Mike Cohn Testing", "[20]" in new_biblio_paras[19] and "Cohn" in new_biblio_paras[19])
assert_check("Biblio [21] Open-Meteo", "[21]" in new_biblio_paras[20] and "Open-Meteo" in new_biblio_paras[20])
assert_check("Biblio [22] GloFAS", "[22]" in new_biblio_paras[21] and "GloFAS" in new_biblio_paras[21])
assert_check("Biblio [23] NASA LHASA", "[23]" in new_biblio_paras[22] and "LHASA" in new_biblio_paras[22])
assert_check("Biblio [26] MongoDB & SQLite", "[26]" in new_biblio_paras[25] and "MongoDB" in new_biblio_paras[25])

print(f"\nFINAL VERIFICATION SCORE: {passes} PASSES, {fails} FAILS")
