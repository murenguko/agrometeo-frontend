import os
import sys
import zipfile
import re
import json
import xml.etree.ElementTree as ET
import docx
from docx.shared import Pt, Inches
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
ANALYSIS_JSON = r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\implementer_r1_retry\doc_analysis.json"
GEN_REPORT_PY = r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\worker_report_1\generate_report.py"

print("=" * 80)
print("INDEPENDENT VICTORY AUDITOR (SENTINEL AUDITOR 2)")
print("Deliverable:", DOCX_PATH)
print("=" * 80)

audit_log = []
failures = []

def record(phase, test_id, description, passed, details=""):
    status = "PASS" if passed else "FAIL"
    entry = {
        "phase": phase,
        "test_id": test_id,
        "description": description,
        "status": status,
        "details": details
    }
    audit_log.append(entry)
    if not passed:
        failures.append(entry)
    print(f"[{status}] [{phase}] {test_id} - {description}: {details}")

# ==============================================================================
# PHASE A — TIMELINE & PROVENANCE AUDIT
# ==============================================================================
print("\n>>> PHASE A: TIMELINE & PROVENANCE AUDIT")

# A1: Physical existence and non-zero size
if os.path.exists(DOCX_PATH):
    size_bytes = os.path.getsize(DOCX_PATH)
    record("Phase A", "A1_EXISTS", "Deliverable file exists on disk", size_bytes > 50000, f"Size = {size_bytes} bytes")
else:
    record("Phase A", "A1_EXISTS", "Deliverable file exists on disk", False, "File not found")

# A2: Zip container integrity
try:
    with zipfile.ZipFile(DOCX_PATH, 'r') as zf:
        corrupt = zf.testzip()
        entries = zf.namelist()
        record("Phase A", "A2_ZIP_INTEGRITY", "OpenXML ZIP container is valid", corrupt is None, f"{len(entries)} zip entries found")
except Exception as e:
    record("Phase A", "A2_ZIP_INTEGRITY", "OpenXML ZIP container is valid", False, str(e))

# A3: generate_report.py execution provenance
if os.path.exists(GEN_REPORT_PY):
    gen_mtime = os.path.getmtime(GEN_REPORT_PY)
    docx_mtime = os.path.getmtime(DOCX_PATH)
    # The current task started after 14:49:55Z on 2026-10-29.
    # gen_report was last modified around 11:29:24. It must not be modified or executed in this run.
    record("Phase A", "A3_GEN_REPORT_NOT_TOUCHED", "generate_report.py was not modified during this run",
           gen_mtime < docx_mtime, f"gen_mtime={gen_mtime}, docx_mtime={docx_mtime}")
else:
    record("Phase A", "A3_GEN_REPORT_NOT_TOUCHED", "generate_report.py not found in active workspace", True, "N/A")

# ==============================================================================
# PHASE B — INTEGRITY & FORENSICS AUDIT
# ==============================================================================
print("\n>>> PHASE B: INTEGRITY & FORENSICS AUDIT")

doc = docx.Document(DOCX_PATH)
full_text = "\n".join(p.text for p in doc.paragraphs)

# B1: Prohibited placeholder tokens
prohibited_patterns = [
    r'\bTODO\b', r'\bFIXME\b', r'\bXXX\b', r'\[TBD\]', r'\bTBD\b',
    r'lorem ipsum', r'dolor sit amet', r'dummy text', r'\[insérer',
    r'\[à compléter\]', r'texte d\'attente'
]
found_tokens = []
for pat in prohibited_patterns:
    matches = re.findall(pat, full_text, flags=re.IGNORECASE)
    if matches:
        found_tokens.append(f"{pat} ({len(matches)} matches)")

record("Phase B", "B1_NO_PLACEHOLDERS", "No dummy/placeholder tokens in document", len(found_tokens) == 0,
       f"Found: {', '.join(found_tokens)}" if found_tokens else "Clean (0 occurrences)")

# B2: Locate boundary between Preliminary Pages and Body
intro_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        intro_idx = i
        break

record("Phase B", "B2_BODY_START", "Body starts with INTRODUCTION GÉNÉRALE", intro_idx is not None and intro_idx > 0,
       f"INTRODUCTION GÉNÉRALE found at paragraph index {intro_idx}")

prelim_paras = doc.paragraphs[:intro_idx] if intro_idx else []
body_paras = doc.paragraphs[intro_idx:] if intro_idx else []
prelim_text = "\n".join(p.text for p in prelim_paras)
body_text = "\n".join(p.text for p in body_paras)

# B3: Preservation of User-Edited Body
# Check against doc_analysis.json
if os.path.exists(ANALYSIS_JSON):
    with open(ANALYSIS_JSON, "r", encoding="utf-8") as f:
        orig = json.load(f)
    
    # Check tables count
    orig_tables = orig.get("total_tables", 0)
    current_tables = len(doc.tables)
    record("Phase B", "B3_TABLES_PRESERVED", "All tables preserved", orig_tables == current_tables == 16,
           f"Original: {orig_tables}, Current: {current_tables}")

    # Check body paragraphs from INTRODUCTION GÉNÉRALE up to RÉFÉRENCES BIBLIOGRAPHIQUES
    orig_paras_count = orig.get("total_paragraphs", 0) # was 499
    # In original doc: paragraph 0 was INTRODUCTION GÉNÉRALE, paragraph 473 was RÉFÉRENCES BIBLIOGRAPHIQUES
    # 474 paragraphs in body prior to bibliography
    biblio_idx = None
    for i, p in enumerate(body_paras):
        if p.text.strip() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
            biblio_idx = i
            break
    
    record("Phase B", "B4_BIBLIO_LOCATION", "RÉFÉRENCES BIBLIOGRAPHIQUES found in body", biblio_idx is not None,
           f"RÉFÉRENCES BIBLIOGRAPHIQUES found at body paragraph {biblio_idx}")

    # Compare body paragraphs count
    record("Phase B", "B5_BODY_PARAS_COUNT", "Body paragraphs count prior to bibliography matches original",
           biblio_idx == 473 or biblio_idx == 474, f"Found {biblio_idx} paragraphs before references")

    # Check key chapters preserved in body text
    key_sections = [
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
        "ANNEXE F — DÉPÔT GIT, STRUCTURE DU CODE SOURCE ET MÉTRIQUES"
    ]
    missing_sections = [s for s in key_sections if s not in body_text]
    record("Phase B", "B6_KEY_SECTIONS_INTACT", "All major chapters and annexes preserved verbatim",
           len(missing_sections) == 0, f"Missing: {missing_sections}" if missing_sections else "All 11 sections intact")
else:
    record("Phase B", "B3_TABLES_PRESERVED", "All tables preserved", len(doc.tables) == 16, f"{len(doc.tables)} tables")

# ==============================================================================
# PHASE C — INDEPENDENT REQUIREMENT & TEST VERIFICATION
# ==============================================================================
print("\n>>> PHASE C: INDEPENDENT REQUIREMENT & TEST VERIFICATION")

# --- R1: PRELIMINARY PAGES COMPLETENESS ---
# C1: Page de garde
cover_requirements = [
    ("République du Burundi", r"RÉPUBLIQUE DU BURUNDI"),
    ("Ministère de l'Éducation", r"MINISTÈRE DE L'ÉDUCATION NATIONALE"),
    ("Université Polytechnique de Gitega", r"UNIVERSITÉ POLYTECHNIQUE DE GITEGA"),
    ("Faculté des TIC", r"FACULTÉ DES TECHNOLOGIES DE L'INFORMATION ET DE LA COMMUNICATION"),
    ("Projet II - Génie Logiciel", r"PROJET II\s*[-–—]\s*GÉNIE LOGICIEL"),
    ("Titre du projet", r"SYSTÈME DE VEILLE MÉTÉO ET CLIMATIQUE AU BURUNDI"),
    ("Espace étudiant", r"Présenté et soutenu par"),
    ("Espace encadreur", r"Sous la direction de"),
    ("Année académique", r"Année [Aa]cadémique")
]
for name, pat in cover_requirements:
    match = re.search(pat, prelim_text, re.IGNORECASE)
    record("Phase C", f"C1_COVER_{name[:12]}", f"Page de garde: {name}", match is not None,
           f"Matched: '{match.group(0)}'" if match else "Not found")

# C2: Preliminary sections headings
prelim_sections = [
    "TABLE DES MATIÈRES",
    "TABLE DES ANNEXES",
    "LISTE DES FIGURES",
    "LISTE DES TABLEAUX",
    "LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES"
]
for psec in prelim_sections:
    record("Phase C", f"C2_SEC_{psec[:10]}", f"Preliminary section: {psec}", psec in prelim_text,
           "Heading present" if psec in prelim_text else "Missing")

# C3: Required Acronyms
required_acronyms = [
    "UPG", "TIC", "ISABU", "IGEBU", "GloFAS", "NASA", "LHASA", "CHIRPS", "MVP",
    "API", "REST", "BFF", "SSR", "JWT", "OAuth2", "OWASP", "SGBD", "NoSQL",
    "SQL", "JSON", "GeoJSON", "HTML", "CSS", "UI", "UX", "WCAG", "UML", "TTL"
]
# Extract the acronym list text specifically
acr_start = prelim_text.find("LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES")
acr_text = prelim_text[acr_start:] if acr_start != -1 else prelim_text

missing_acronyms = []
for acr in required_acronyms:
    # Look for the acronym as a standalone word in the acronym section
    pat = rf"\b{re.escape(acr)}\b"
    if not re.search(pat, acr_text):
        missing_acronyms.append(acr)

record("Phase C", "C3_ACRONYMS", "All 28 required acronyms present in acronym list", len(missing_acronyms) == 0,
       f"Missing: {missing_acronyms}" if missing_acronyms else f"All {len(required_acronyms)} acronyms verified")

# C4: TOC concordance with body headings
# Collect body headings
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

toc_start = prelim_text.find("TABLE DES MATIÈRES")
toc_end = prelim_text.find("LISTE DES FIGURES") if prelim_text.find("LISTE DES FIGURES") != -1 else len(prelim_text)
toc_text = prelim_text[toc_start:toc_end] if toc_start != -1 else ""

missing_in_toc = []
for bh in body_headings:
    # clean heading text for matching
    clean_h = re.split(r'\s{2,}', bh)[0].strip()
    # Also strip trailing punctuation or dots
    clean_h = clean_h.rstrip('.')
    if clean_h not in toc_text:
        missing_in_toc.append(clean_h)

record("Phase C", "C4_TOC_CONCORDANCE", "All body headings listed in Table des matières",
       len(missing_in_toc) == 0,
       f"Missing {len(missing_in_toc)} headings: {missing_in_toc[:3]}" if missing_in_toc else f"All {len(body_headings)} headings concordant")

# C5: Figure captions concordance
body_figures = [p.text.strip() for p in body_paras if p.text.strip().startswith("Figure ") or p.text.strip().startswith("Fig. ")]
fig_start = prelim_text.find("LISTE DES FIGURES")
fig_end = prelim_text.find("LISTE DES TABLEAUX") if prelim_text.find("LISTE DES TABLEAUX") != -1 else len(prelim_text)
fig_text = prelim_text[fig_start:fig_end] if fig_start != -1 else ""

missing_figs = []
for bf in body_figures:
    prefix = bf.split("—")[0].strip() if "—" in bf else bf[:20]
    if prefix not in fig_text:
        missing_figs.append(bf)

record("Phase C", "C5_FIGURES_CONCORDANCE", "All figures listed in Liste des figures",
       len(missing_figs) == 0,
       f"Missing {len(missing_figs)} figures: {missing_figs}" if missing_figs else f"All {len(body_figures)} figures concordant")

# C6: Table captions concordance
body_tables = [p.text.strip() for p in body_paras if p.text.strip().startswith("Tableau ") or p.text.strip().startswith("Table ")]
tab_start = prelim_text.find("LISTE DES TABLEAUX")
tab_end = prelim_text.find("LISTE DES SIGLES") if prelim_text.find("LISTE DES SIGLES") != -1 else len(prelim_text)
tab_text = prelim_text[tab_start:tab_end] if tab_start != -1 else ""

missing_tabs = []
for bt in body_tables:
    prefix = bt.split("—")[0].strip() if "—" in bt else bt[:20]
    if prefix not in tab_text:
        missing_tabs.append(bt)

record("Phase C", "C6_TABLES_CONCORDANCE", "All tables listed in Liste des tableaux",
       len(missing_tabs) == 0,
       f"Missing {len(missing_tabs)} tables: {missing_tabs}" if missing_tabs else f"All {len(body_tables)} tables concordant")

# --- R2: REVISED BIBLIOGRAPHY & CITATIONS ---
# Extract bibliography paragraphs
biblio_paras = []
in_bib = False
for p in body_paras:
    if p.text.strip() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        in_bib = True
        continue
    if in_bib and p.text.strip():
        biblio_paras.append(p)

record("Phase C", "C7_BIBLIO_COUNT", "Bibliography has 30 references", len(biblio_paras) == 30,
       f"Found {len(biblio_paras)} reference entries")

# Check IEEE format and completeness
ieee_conforming = 0
for bp in biblio_paras:
    t = bp.text.strip()
    # Check [N] author, title, source, year
    if re.match(r'^\[\d+\]', t) and any(y in t for y in ["199", "200", "201", "202"]):
        ieee_conforming += 1

record("Phase C", "C8_BIBLIO_IEEE_FORMAT", "Standardized IEEE format for bibliography",
       ieee_conforming == len(biblio_paras) == 30, f"{ieee_conforming}/30 conform to IEEE pattern")

# Check citations in body text
citations_in_body = set(re.findall(r'\[(\d+)\]', body_text))
all_cited = all(str(i) in citations_in_body for i in range(1, 31))
record("Phase C", "C9_CITATIONS_REFERENCED", "All references [1] to [30] cited in body",
       all_cited, f"Total distinct citations found: {len(citations_in_body)} / 30")

# Check coverage of key technologies and institutions
key_techs = ["Open-Meteo", "GloFAS", "LHASA", "MongoDB", "FastAPI", "SvelteKit", "ISABU", "IGEBU", "OWASP"]
biblio_full = "\n".join(bp.text for bp in biblio_paras)
missing_techs = [tech for tech in key_techs if tech.lower() not in biblio_full.lower()]
record("Phase C", "C10_BIBLIO_TECH_ALIGNMENT", "Bibliography covers key technologies & institutions",
       len(missing_techs) == 0, f"Missing: {missing_techs}" if missing_techs else f"All {len(key_techs)} covered")

# --- R4: UPG LAYOUT NORMS & TYPOGRAPHY ---
# C11: Section count and margins
record("Phase C", "C11_SECTIONS_COUNT", "Document has exactly 2 sections (prelims & body)",
       len(doc.sections) == 2, f"Found {len(doc.sections)} sections")

sec0 = doc.sections[0]
sec1 = doc.sections[1]

# Margins: Left 3.0 cm, Others 2.5 cm
m0_ok = (abs(sec0.left_margin.cm - 3.0) < 0.05 and
         abs(sec0.right_margin.cm - 2.5) < 0.05 and
         abs(sec0.top_margin.cm - 2.5) < 0.05 and
         abs(sec0.bottom_margin.cm - 2.5) < 0.05)
record("Phase C", "C12_SEC0_MARGINS", "Section 0 margins (Left 3.0cm, Right/Top/Bottom 2.5cm)",
       m0_ok, f"L={sec0.left_margin.cm:.2f}, R={sec0.right_margin.cm:.2f}, T={sec0.top_margin.cm:.2f}, B={sec0.bottom_margin.cm:.2f}")

m1_ok = (abs(sec1.left_margin.cm - 3.0) < 0.05 and
         abs(sec1.right_margin.cm - 2.5) < 0.05 and
         abs(sec1.top_margin.cm - 2.5) < 0.05 and
         abs(sec1.bottom_margin.cm - 2.5) < 0.05)
record("Phase C", "C13_SEC1_MARGINS", "Section 1 margins (Left 3.0cm, Right/Top/Bottom 2.5cm)",
       m1_ok, f"L={sec1.left_margin.cm:.2f}, R={sec1.right_margin.cm:.2f}, T={sec1.top_margin.cm:.2f}, B={sec1.bottom_margin.cm:.2f}")

# C14: Pagination styles
pg0 = sec0._sectPr.find(qn('w:pgNumType'))
fmt0 = pg0.get(qn('w:fmt')) if pg0 is not None else None
start0 = pg0.get(qn('w:start')) if pg0 is not None else None
record("Phase C", "C14_SEC0_ROMAN_NUMERALS", "Section 0 uses lowerRoman starting at 1",
       fmt0 == 'lowerRoman' and start0 == '1', f"fmt={fmt0}, start={start0}")

pg1 = sec1._sectPr.find(qn('w:pgNumType'))
fmt1 = pg1.get(qn('w:fmt')) if pg1 is not None else None
start1 = pg1.get(qn('w:start')) if pg1 is not None else None
record("Phase C", "C15_SEC1_ARABIC_NUMERALS", "Section 1 uses decimal starting at 1",
       fmt1 == 'decimal' and start1 == '1', f"fmt={fmt1}, start={start1}")

# C16: Footers centered with dynamic PAGE field
f0_xml = sec0.footer.paragraphs[0]._element.xml if len(sec0.footer.paragraphs) > 0 else ""
f1_xml = sec1.footer.paragraphs[0]._element.xml if len(sec1.footer.paragraphs) > 0 else ""
record("Phase C", "C16_FOOTER_PAGE_FIELDS", "Both section footers have dynamic PAGE field",
       "PAGE" in f0_xml and "PAGE" in f1_xml, "Dynamic PAGE fields verified")

# C17: Typography checks
# Prelims: Times New Roman
non_tnr_prelim = 0
for p in prelim_paras:
    for r in p.runs:
        if r.text.strip() and r.font.name and r.font.name != "Times New Roman":
            non_tnr_prelim += 1

record("Phase C", "C17_PRELIM_FONT", "Prelims: All runs use Times New Roman",
       non_tnr_prelim == 0, f"Non-TNR runs = {non_tnr_prelim}")

# Bibliography: Times New Roman, 12pt, 1.5 line spacing
biblio_typo_issues = 0
for bp in biblio_paras:
    if bp.paragraph_format.line_spacing is not None and abs(bp.paragraph_format.line_spacing - 1.5) > 0.05:
        biblio_typo_issues += 1
    for r in bp.runs:
        if r.text.strip():
            if r.font.name and r.font.name != "Times New Roman":
                biblio_typo_issues += 1
            if r.font.size and abs(r.font.size.pt - 12.0) > 0.5:
                biblio_typo_issues += 1

record("Phase C", "C18_BIBLIO_TYPOGRAPHY", "Bibliography: TNR 12pt 1.5 line spacing",
       biblio_typo_issues == 0, f"Formatting issues = {biblio_typo_issues}")

# ==============================================================================
# AUDIT SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
total_tests = len(audit_log)
passed_tests = total_tests - len(failures)
print(f"TOTAL AUDIT ASSERTIONS: {total_tests}")
print(f"PASSED: {passed_tests}")
print(f"FAILED: {len(failures)}")
print("=" * 80)

if len(failures) > 0:
    print("\nFAILURES:")
    for f in failures:
        print(f"  - [{f['phase']}] {f['test_id']}: {f['description']} -> {f['details']}")
    print("\nOVERALL VERDICT: VICTORY REJECTED")
else:
    print("\nOVERALL VERDICT: VICTORY CONFIRMED")
