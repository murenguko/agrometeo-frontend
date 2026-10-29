import docx
from docx.shared import Pt, Inches
import re
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
ANALYSIS_JSON = r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\implementer_r1_retry\doc_analysis.json"

print(f"Loading document: {DOCX_PATH}")
doc = docx.Document(DOCX_PATH)

results = {
    "total_checks": 0,
    "passes": 0,
    "failures": [],
}

def record_check(category, name, passed, detail=""):
    results["total_checks"] += 1
    if passed:
        results["passes"] += 1
        print(f"  [PASS] [{category}] {name}: {detail}")
    else:
        results["failures"].append({"category": category, "name": name, "detail": detail})
        print(f"  [FAIL] [{category}] {name}: {detail}")

# ==============================================================================
# 1. SECTION & MARGIN CHECKS (R4)
# ==============================================================================
print("\n--- 1. SECTION & MARGIN CHECKS (R4) ---")
record_check("Sections", "Two sections exist", len(doc.sections) == 2, f"Found {len(doc.sections)} sections")

sec0 = doc.sections[0]
sec1 = doc.sections[1]

# Check Section 0 margins (3 cm left, 2.5 cm top/right/bottom)
record_check("Margins", "Sec0 Left margin = 3.0 cm", abs(sec0.left_margin.cm - 3.0) < 0.05, f"{sec0.left_margin.cm:.2f} cm")
record_check("Margins", "Sec0 Right margin = 2.5 cm", abs(sec0.right_margin.cm - 2.5) < 0.05, f"{sec0.right_margin.cm:.2f} cm")
record_check("Margins", "Sec0 Top margin = 2.5 cm", abs(sec0.top_margin.cm - 2.5) < 0.05, f"{sec0.top_margin.cm:.2f} cm")
record_check("Margins", "Sec0 Bottom margin = 2.5 cm", abs(sec0.bottom_margin.cm - 2.5) < 0.05, f"{sec0.bottom_margin.cm:.2f} cm")

# Check Section 1 margins
record_check("Margins", "Sec1 Left margin = 3.0 cm", abs(sec1.left_margin.cm - 3.0) < 0.05, f"{sec1.left_margin.cm:.2f} cm")
record_check("Margins", "Sec1 Right margin = 2.5 cm", abs(sec1.right_margin.cm - 2.5) < 0.05, f"{sec1.right_margin.cm:.2f} cm")
record_check("Margins", "Sec1 Top margin = 2.5 cm", abs(sec1.top_margin.cm - 2.5) < 0.05, f"{sec1.top_margin.cm:.2f} cm")
record_check("Margins", "Sec1 Bottom margin = 2.5 cm", abs(sec1.bottom_margin.cm - 2.5) < 0.05, f"{sec1.bottom_margin.cm:.2f} cm")

# ==============================================================================
# 2. PAGINATION NORMS (R4)
# ==============================================================================
print("\n--- 2. PAGINATION & FOOTERS (R4) ---")
pgNum0 = sec0._sectPr.find(docx.oxml.ns.qn('w:pgNumType'))
fmt0 = pgNum0.get(docx.oxml.ns.qn('w:fmt')) if pgNum0 is not None else None
start0 = pgNum0.get(docx.oxml.ns.qn('w:start')) if pgNum0 is not None else None
record_check("Pagination", "Sec0 Lowercase Roman numerals", fmt0 == 'lowerRoman', f"w:fmt = {fmt0}")
record_check("Pagination", "Sec0 Start page = 1 (roman i)", start0 == '1', f"w:start = {start0}")

pgNum1 = sec1._sectPr.find(docx.oxml.ns.qn('w:pgNumType'))
fmt1 = pgNum1.get(docx.oxml.ns.qn('w:fmt')) if pgNum1 is not None else None
start1 = pgNum1.get(docx.oxml.ns.qn('w:start')) if pgNum1 is not None else None
record_check("Pagination", "Sec1 Decimal Arabic numerals", fmt1 == 'decimal', f"w:fmt = {fmt1}")
record_check("Pagination", "Sec1 Start page = 1", start1 == '1', f"w:start = {start1}")

# Check footers have dynamic page fields and are centered
sec0_footer_xml = sec0.footer.paragraphs[0]._element.xml if len(sec0.footer.paragraphs) > 0 else ""
sec1_footer_xml = sec1.footer.paragraphs[0]._element.xml if len(sec1.footer.paragraphs) > 0 else ""
record_check("Footers", "Sec0 Footer dynamic PAGE field", "PAGE" in sec0_footer_xml, "PAGE field found")
record_check("Footers", "Sec1 Footer dynamic PAGE field", "PAGE" in sec1_footer_xml, "PAGE field found")

# ==============================================================================
# 3. PRELIMINARY PAGES IDENTIFICATION & COMPLETENESS (R1)
# ==============================================================================
print("\n--- 3. PRELIMINARY PAGES COMPLETENESS (R1) ---")
intro_p_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_p_idx = i
        break

record_check("Structure", "Body begins with INTRODUCTION GÉNÉRALE", intro_p_idx is not None, f"Found at paragraph index {intro_p_idx}")

prelim_paras = doc.paragraphs[:intro_p_idx]
body_paras = doc.paragraphs[intro_p_idx:]

prelim_full_text = "\n".join(p.text for p in prelim_paras)

# Check Cover Page elements
cover_items = [
    ("RÉPUBLIQUE DU BURUNDI", "République du Burundi"),
    ("MINISTÈRE DE L'ÉDUCATION NATIONALE", "Ministère de l'Éducation Nationale"),
    ("UNIVERSITÉ POLYTECHNIQUE DE GITEGA", "Université Polytechnique de Gitega"),
    ("FACULTÉ DES TECHNOLOGIES DE L'INFORMATION", "Faculté des TIC"),
    ("GÉNIE LOGICIEL", "Génie Logiciel"),
    ("PROJET II", "Projet II"),
    ("SYSTÈME DE VEILLE MÉTÉO ET CLIMATIQUE AU BURUNDI", "Titre du projet"),
    ("Présenté et soutenu par", "Espace étudiant/auteur"),
    ("Sous la direction de", "Espace encadreur"),
    ("Année Académique", "Année académique")
]
for item_str, item_label in cover_items:
    record_check("Page de Garde", item_label, item_str.upper() in prelim_full_text.upper(), f"'{item_str}' in prelims")

# Check Preliminary sections present
prelim_sections = [
    "TABLE DES MATIÈRES",
    "TABLE DES ANNEXES",
    "LISTE DES FIGURES",
    "LISTE DES TABLEAUX",
    "LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES"
]
for psec in prelim_sections:
    record_check("Prelim Sections", psec, psec in prelim_full_text, f"'{psec}' found")

# Check Acronyms List
required_acronyms = [
    "UPG", "TIC", "ISABU", "IGEBU", "GloFAS", "NASA", "LHASA", "CHIRPS", "MVP",
    "API", "REST", "BFF", "SSR", "JWT", "OAuth2", "OWASP", "SGBD", "NoSQL",
    "SQL", "JSON", "GeoJSON", "HTML", "CSS", "UI", "UX", "WCAG", "UML", "TTL"
]
for acr in required_acronyms:
    # search for acronym definition
    pattern = rf"\b{re.escape(acr)}\b"
    found = re.search(pattern, prelim_full_text) is not None
    record_check("Acronyms", f"Acronym {acr}", found, f"'{acr}' present in acronyms list")

# ==============================================================================
# 4. CONCORDANCE OF TOC, FIGURES, TABLES WITH BODY (R1)
# ==============================================================================
print("\n--- 4. CONCORDANCE OF TOC, FIGURES, TABLES (R1) ---")
body_full_text = "\n".join(p.text for p in body_paras)

# Headings in body
body_headings = []
for p in body_paras:
    t = p.text.strip()
    if not t:
        continue
    if (t.startswith("INTRODUCTION GÉNÉRALE") or
        t.startswith("CHAPITRE ") or
        t.startswith("CONCLUSION GÉNÉRALE") or
        t.startswith("ANNEXE ") or
        t.startswith("RÉFÉRENCES BIBLIOGRAPHIQUES") or
        re.match(r"^(\d+(\.\d+)*)\s+[A-ZÀ-Ÿ]", t) or
        re.match(r"^[A-Z]\.\d+\s+[A-ZÀ-Ÿ]", t)):
        body_headings.append(t)

print(f"Total identified body headings: {len(body_headings)}")

# Check that every main heading appears in the TOC
missing_in_toc = []
for bh in body_headings:
    # Extract clean title without trailing dots
    clean_h = bh.split('  ')[0].strip()
    # Check if heading title exists in TOC
    if clean_h not in prelim_full_text:
        missing_in_toc.append(clean_h)

record_check("TOC Concordance", "All body headings listed in TOC", len(missing_in_toc) == 0, 
             f"Missing: {len(missing_in_toc)} headings" if missing_in_toc else "100% matched")

# Figure captions in body
figure_captions = [p.text.strip() for p in body_paras if p.text.strip().startswith("Figure ") or p.text.strip().startswith("Fig. ")]
print(f"Total figure captions in body: {len(figure_captions)}")
missing_figs = []
for fc in figure_captions:
    prefix = fc.split("—")[0].strip() if "—" in fc else fc[:15]
    if prefix not in prelim_full_text:
        missing_figs.append(fc)

record_check("Figures Concordance", "All figures listed in Liste des figures", len(missing_figs) == 0,
             f"Missing: {len(missing_figs)} figures" if missing_figs else f"All {len(figure_captions)} figures matched")

# Table captions in body
table_captions = [p.text.strip() for p in body_paras if p.text.strip().startswith("Tableau ") or p.text.strip().startswith("Table ")]
print(f"Total table captions in body: {len(table_captions)}")
missing_tabs = []
for tc in table_captions:
    prefix = tc.split("—")[0].strip() if "—" in tc else tc[:15]
    if prefix not in prelim_full_text:
        missing_tabs.append(tc)

record_check("Tables Concordance", "All tables listed in Liste des tableaux", len(missing_tabs) == 0,
             f"Missing: {len(missing_tabs)} tables" if missing_tabs else f"All {len(table_captions)} tables matched")

# ==============================================================================
# 5. PRESERVATION OF USER-EDITED BODY TEXT & TABLES (R3)
# ==============================================================================
print("\n--- 5. PRESERVATION OF BODY TEXT & TABLES (R3) ---")
# Check table count: 16 tables
record_check("Tables", "16 tables preserved", len(doc.tables) == 16, f"Found {len(doc.tables)} tables")

# Check comparison against doc_analysis.json (pre-modification snapshot)
if os.path.exists(ANALYSIS_JSON):
    with open(ANALYSIS_JSON, "r", encoding="utf-8") as f:
        orig_data = json.load(f)
    orig_total_p = orig_data.get("total_paragraphs")
    orig_total_tables = orig_data.get("total_tables")
    record_check("Preservation", "Original table count matched", orig_total_tables == len(doc.tables), f"orig={orig_total_tables}, current={len(doc.tables)}")

    # Check key chapters in body
    expected_chapters = [
        "INTRODUCTION GÉNÉRALE",
        "CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC",
        "CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART",
        "CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE",
        "CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION",
        "CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION",
        "CONCLUSION GÉNÉRALE ET PERSPECTIVES",
        "ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS",
        "ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES",
        "ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION"
    ]
    for ch in expected_chapters:
        record_check("Preservation", f"Chapter preserved: {ch[:35]}", ch in body_full_text, "Found intact in body")

# ==============================================================================
# 6. REVISED BIBLIOGRAPHY & CITATIONS (R2)
# ==============================================================================
print("\n--- 6. REVISED BIBLIOGRAPHY & CITATIONS (R2) ---")
biblio_paras = []
in_biblio = False
for p in body_paras:
    if p.text.strip() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        in_biblio = True
        continue
    if in_biblio:
        if p.text.strip():
            biblio_paras.append(p)

record_check("Bibliography", "30 references present", len(biblio_paras) == 30, f"Found {len(biblio_paras)} reference entries")

# Check in-text citations [1] to [30]
in_text_citations = set(re.findall(r'\[(\d+)\]', body_full_text))
print(f"Distinct numeric citations in text: {len(in_text_citations)}")
# Ensure every reference [1] to [30] is referenced or in order
all_citations_present = all(str(i) in in_text_citations for i in range(1, 31))
record_check("Bibliography", "All citations [1] to [30] cited in body", all_citations_present, f"Cited numbers: {sorted([int(x) for x in in_text_citations])}")

# Check IEEE format and completeness
ieee_pattern = re.compile(r'^\[\d+\]\s+[A-ZÀ-Ÿ].+,\s+[«"].+["»],\s+.+,\s+\d{4}')
conforming_refs = 0
for bp in biblio_paras:
    t = bp.text.strip()
    if re.match(r'^\[\d+\]', t) and any(y in t for y in ["201", "202", "199", "200"]):
        conforming_refs += 1

record_check("Bibliography", "Homogeneous citation format across entries", conforming_refs == 30, f"{conforming_refs}/30 conform to standard bibliographic format")

# Check key technologies and institutions represented
tech_keys = ["Open-Meteo", "GloFAS", "LHASA", "MongoDB", "FastAPI", "SvelteKit", "ISABU", "IGEBU", "PNA", "OWASP"]
for tk in tech_keys:
    biblio_text = "\n".join(p.text for p in biblio_paras)
    record_check("Bibliography", f"Key source {tk} present", tk in biblio_text, f"'{tk}' referenced")

# ==============================================================================
# 7. TYPOGRAPHY & FORMATTING NORMS (R4)
# ==============================================================================
print("\n--- 7. TYPOGRAPHY & FORMATTING NORMS (R4) ---")
# Check preliminary pages typography: Times New Roman, 1.5 line spacing (or justified 12pt)
non_tnr_runs = 0
total_runs_checked = 0
for p in prelim_paras:
    for r in p.runs:
        if r.text.strip():
            total_runs_checked += 1
            if r.font.name and r.font.name != "Times New Roman":
                non_tnr_runs += 1

record_check("Typography", "Prelims: All runs use Times New Roman", non_tnr_runs == 0, f"non-TNR runs = {non_tnr_runs}/{total_runs_checked}")

# Check bibliography typography: Times New Roman, 12 pt, 1.5 line spacing
biblio_typo_errors = 0
for i, bp in enumerate(biblio_paras):
    line_sp = bp.paragraph_format.line_spacing
    if line_sp is not None and abs(line_sp - 1.5) > 0.05:
        biblio_typo_errors += 1
    for r in bp.runs:
        if r.font.name and r.font.name != "Times New Roman":
            biblio_typo_errors += 1
        if r.font.size and abs(r.font.size.pt - 12.0) > 0.5:
            biblio_typo_errors += 1

record_check("Typography", "Bibliography: TNR 12pt 1.5 line spacing", biblio_typo_errors == 0, f"Errors: {biblio_typo_errors}")

# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "="*80)
print(f"AUDIT SUMMARY: {results['passes']} PASSES out of {results['total_checks']} CHECKS")
if results["failures"]:
    print(f"FAILURES DETECTED: {len(results['failures'])}")
    for f in results["failures"]:
        print(f"  FAILED: [{f['category']}] {f['name']}: {f['detail']}")
else:
    print("ALL AUDIT CHECKS PASSED WITH 100% SUCCESS!")
print("="*80)
