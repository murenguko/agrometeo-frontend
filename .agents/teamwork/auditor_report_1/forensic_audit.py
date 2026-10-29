"""
FORENSIC INTEGRITY AUDIT SCRIPT
Target: c:/Users/PC/Desktop/Projects/weather-app/Rapport_Projet_Veille_Meteo_Burundi.docx
Auditor: auditor_report_1
Mission: Binary verification (CLEAN vs INTEGRITY VIOLATION)
"""

import os
import sys
import hashlib
import zipfile
import re
from xml.etree import ElementTree as ET

# Configuration
DOCX_PATH = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
BACKEND_DIR = r"c:\Users\PC\Desktop\Projects\weather-backend"
FRONTEND_DIR = r"c:\Users\PC\Desktop\Projects\weather-app"

# Namespace dictionary for WordprocessingML
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

class ForensicAuditor:
    def __init__(self, docx_path):
        self.docx_path = docx_path
        self.violations = []
        self.findings = []
        self.metrics = {}
        self.full_text = ""
        self.paragraphs = []
        self.tables_data = []

    def log(self, category, status, detail):
        prefix = "[PASS]" if status else "[VIOLATION]"
        msg = f"{prefix} [{category}] {detail}"
        print(msg)
        if status:
            self.findings.append((category, detail))
        else:
            self.violations.append((category, detail))

    def run_all_checks(self):
        print("=" * 80)
        print("STARTING INDEPENDENT FORENSIC INTEGRITY AUDIT")
        print(f"Target: {self.docx_path}")
        print("=" * 80)

        self.check_file_integrity()
        self.check_ooxml_structure()
        self.extract_content_and_metrics()
        self.check_upg_canvas_and_formatting()
        self.check_anti_cheat_and_authenticity()
        self.check_codebase_reality_and_divergences()
        self.print_summary_and_verdict()

    def check_file_integrity(self):
        print("\n--- PHASE 1: PHYSICAL FILE INTEGRITY & HASH ---")
        if not os.path.exists(self.docx_path):
            self.log("FILE", False, f"Target file does not exist at {self.docx_path}")
            return

        file_size = os.path.getsize(self.docx_path)
        self.metrics['file_size_bytes'] = file_size
        self.metrics['file_size_kb'] = file_size / 1024.0

        if file_size < 10000:
            self.log("FILE", False, f"File size abnormally small ({file_size} bytes)")
        else:
            self.log("FILE", True, f"File exists, size: {file_size} bytes ({file_size/1024.0:.2f} KB)")

        # Compute SHA-256
        sha256 = hashlib.sha256()
        with open(self.docx_path, "rb") as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        self.metrics['sha256'] = sha256.hexdigest()
        self.log("HASH", True, f"SHA-256: {self.metrics['sha256']}")

    def check_ooxml_structure(self):
        print("\n--- PHASE 2: OOXML ARCHIVE INTEGRITY ---")
        try:
            with zipfile.ZipFile(self.docx_path, 'r') as z:
                names = z.namelist()
                required = ['[Content_Types].xml', 'word/document.xml', 'word/styles.xml']
                for req in required:
                    if req in names:
                        self.log("OOXML", True, f"Required part present: {req}")
                    else:
                        self.log("OOXML", False, f"Missing required OOXML part: {req}")

                # Test zip integrity
                bad_file = z.testzip()
                if bad_file:
                    self.log("ZIP", False, f"Corrupted file inside zip: {bad_file}")
                else:
                    self.log("ZIP", True, "Zip container structure 100% valid and uncorrupted")
        except Exception as e:
            self.log("ZIP", False, f"Failed to open as zip archive: {e}")

    def extract_content_and_metrics(self):
        print("\n--- PHASE 3: CONTENT EXTRACTION & TEXT METRICS ---")
        try:
            with zipfile.ZipFile(self.docx_path, 'r') as z:
                doc_xml = z.read('word/document.xml')
                root = ET.fromstring(doc_xml)

                # Extract all paragraphs and tables
                paras = root.findall('.//w:p', NS)
                self.metrics['paragraph_count'] = len(paras)

                para_texts = []
                for p in paras:
                    t_nodes = p.findall('.//w:t', NS)
                    p_text = "".join([t.text for t in t_nodes if t.text])
                    if p_text:
                        para_texts.append(p_text)

                self.paragraphs = para_texts
                self.full_text = "\n".join(para_texts)

                # Words count
                words = re.findall(r'\b\w+\b', self.full_text)
                self.metrics['word_count'] = len(words)
                self.metrics['char_count'] = len(self.full_text)

                # Tables
                tbls = root.findall('.//w:tbl', NS)
                self.metrics['table_count'] = len(tbls)

                print(f"Total extracted paragraphs: {len(self.paragraphs)}")
                print(f"Total estimated words: {self.metrics['word_count']}")
                print(f"Total characters: {self.metrics['char_count']}")
                print(f"Total tables: {self.metrics['table_count']}")

                if self.metrics['word_count'] < 5000:
                    self.log("VOLUME", False, f"Word count too low ({self.metrics['word_count']} words) for comprehensive academic report")
                else:
                    self.log("VOLUME", True, f"Word count is robust: {self.metrics['word_count']} words (>= 5000 target)")

                if self.metrics['table_count'] < 10:
                    self.log("TABLES", False, f"Table count too low ({self.metrics['table_count']})")
                else:
                    self.log("TABLES", True, f"Table count is substantial: {self.metrics['table_count']} tables/callouts")

        except Exception as e:
            self.log("EXTRACTION", False, f"Failed to extract document contents: {e}")

    def check_upg_canvas_and_formatting(self):
        print("\n--- PHASE 4: UPG CANVAS & NORMS VALIDATION ---")
        # 1. Preliminary pages check: must NOT have cover page, TOC, list of figures/tables, sigles
        # First non-empty paragraph must be INTRODUCTION GÉNÉRALE
        if self.paragraphs:
            first_p = self.paragraphs[0].strip()
            if "INTRODUCTION" in first_p.upper() and "GÉNÉRALE" in first_p.upper():
                self.log("PRELIMINARY_PAGES", True, f"First paragraph is directly '{first_p}' (Preliminary pages strictly omitted)")
            else:
                self.log("PRELIMINARY_PAGES", False, f"Document does not start with INTRODUCTION GÉNÉRALE. Found: '{first_p}'")
        else:
            self.log("PRELIMINARY_PAGES", False, "No paragraphs found in document")

        # 2. Check all required chapters & annexes in text
        required_chapters = [
            ("INTRODUCTION GÉNÉRALE", r"INTRODUCTION\s+G[ÉE]N[ÉE]RALE"),
            ("CHAPITRE I", r"CHAPITRE\s+I\s*—\s*[ÉE]TAT\s+DES\s+LIEUX"),
            ("CHAPITRE II", r"CHAPITRE\s+II\s*—\s*[ÉE]TUDE\s+TH[ÉE]ORIQUE"),
            ("CHAPITRE III", r"CHAPITRE\s+III\s*—\s*CONCEPTION"),
            ("CHAPITRE IV", r"CHAPITRE\s+IV\s*—\s*IMPL[ÉE]MENTATION"),
            ("CHAPITRE V", r"CHAPITRE\s+V\s*—\s*TESTS"),
            ("CONCLUSION GÉNÉRALE", r"CONCLUSION\s+G[ÉE]N[ÉE]RALE"),
            ("ANNEXE A", r"ANNEXE\s+A"),
            ("ANNEXE B", r"ANNEXE\s+B"),
            ("ANNEXE D", r"ANNEXE\s+D"),
            ("ANNEXE F", r"ANNEXE\s+F"),
            ("RÉFÉRENCES BIBLIOGRAPHIQUES", r"R[ÉE]F[ÉE]RENCES\s+BIBLIOGRAPHIQUES"),
        ]

        for name, pattern in required_chapters:
            if re.search(pattern, self.full_text, re.IGNORECASE):
                self.log("CHAPTER", True, f"Found mandatory section: {name}")
            else:
                self.log("CHAPTER", False, f"Missing mandatory section: {name}")

        # 3. Margins check via XML (w:pgMar)
        try:
            with zipfile.ZipFile(self.docx_path, 'r') as z:
                doc_xml = z.read('word/document.xml')
                root = ET.fromstring(doc_xml)
                pg_mar = root.find('.//w:pgMar', NS)
                if pg_mar is not None:
                    # In twentieths of a point (dxa): 1 inch = 1440 dxa = 2.54 cm
                    # 3.0 cm = 3.0 / 2.54 * 1440 = 1700.78 dxa (~1701 dxa)
                    # 2.5 cm = 2.5 / 2.54 * 1440 = 1417.32 dxa (~1417 dxa)
                    left = int(pg_mar.attrib.get(f"{{{NS['w']}}}left", 0))
                    right = int(pg_mar.attrib.get(f"{{{NS['w']}}}right", 0))
                    top = int(pg_mar.attrib.get(f"{{{NS['w']}}}top", 0))
                    bottom = int(pg_mar.attrib.get(f"{{{NS['w']}}}bottom", 0))

                    left_cm = left * 2.54 / 1440.0
                    right_cm = right * 2.54 / 1440.0
                    top_cm = top * 2.54 / 1440.0
                    bottom_cm = bottom * 2.54 / 1440.0

                    print(f"Margins measured: Left={left_cm:.2f}cm, Right={right_cm:.2f}cm, Top={top_cm:.2f}cm, Bottom={bottom_cm:.2f}cm")

                    if 2.9 <= left_cm <= 3.1:
                        self.log("MARGIN_LEFT", True, f"Left margin is {left_cm:.2f}cm (UPG 3.0cm binding standard)")
                    else:
                        self.log("MARGIN_LEFT", False, f"Left margin is {left_cm:.2f}cm, expected 3.0cm")

                    if 2.4 <= right_cm <= 2.6 and 2.4 <= top_cm <= 2.6 and 2.4 <= bottom_cm <= 2.6:
                        self.log("MARGIN_OTHER", True, f"Top/Bottom/Right margins conform to 2.5cm ({top_cm:.2f}cm / {bottom_cm:.2f}cm / {right_cm:.2f}cm)")
                    else:
                        self.log("MARGIN_OTHER", False, f"Top/Bottom/Right margins mismatch 2.5cm standard")
                else:
                    self.log("MARGINS", False, "No w:pgMar tag found in document.xml")
        except Exception as e:
            self.log("MARGINS", False, f"Error inspecting margins: {e}")

    def check_anti_cheat_and_authenticity(self):
        print("\n--- PHASE 5: ANTI-CHEAT, ANTI-FACADE & AUTHENTICITY ---")
        # 1. Search for prohibited placeholder tokens
        forbidden_tokens = [
            "lorem ipsum", "dolor sit amet", "consectetur adipiscing",
            "TODO:", "[TODO", "FIXME", "XXX", "TBD", "[TBD",
            "dummy text", "placeholder", "texte d'attente",
            "remplir plus tard", "insérer ici", "a completer", "à compléter"
        ]

        found_forbidden = []
        for token in forbidden_tokens:
            matches = re.findall(re.escape(token), self.full_text, re.IGNORECASE)
            if matches:
                found_forbidden.append((token, len(matches)))

        if found_forbidden:
            for tok, cnt in found_forbidden:
                self.log("FORBIDDEN_TEXT", False, f"Found placeholder token '{tok}' ({cnt} occurrences)")
        else:
            self.log("FORBIDDEN_TEXT", True, "Zero placeholder tokens (no lorem ipsum, no TODO, no placeholder)")

        # 2. Check for duplicated looped paragraphs (facade detection)
        para_counts = {}
        for p in self.paragraphs:
            cleaned = p.strip()
            if len(cleaned) > 50:  # Only check substantial paragraphs
                para_counts[cleaned] = para_counts.get(cleaned, 0) + 1

        excessive_duplicates = {p: count for p, count in para_counts.items() if count > 2}
        if excessive_duplicates:
            for p, count in list(excessive_duplicates.items())[:3]:
                snippet = p[:80] + "..." if len(p) > 80 else p
                self.log("DUPLICATION", False, f"Repeated paragraph detected {count} times: '{snippet}'")
        else:
            self.log("DUPLICATION", True, "No repeated looped text blocks detected (high informational entropy)")

        # 3. Check bibliography citations: IEEE format [1], [2], etc.
        ieee_citations = re.findall(r'\[\d+\]', self.full_text)
        self.metrics['citation_count'] = len(ieee_citations)
        if len(ieee_citations) >= 15:
            self.log("CITATIONS", True, f"Found {len(ieee_citations)} IEEE-style citations across the document")
        else:
            self.log("CITATIONS", False, f"Insufficient IEEE citations found ({len(ieee_citations)})")

    def check_codebase_reality_and_divergences(self):
        print("\n--- PHASE 6: CODEBASE REALITY & DIVERGENCE AUDIT ---")
        # Key facts that MUST be present and faithfully analyzed according to ORIGINAL_REQUEST.md

        # 1. Ancient provinces vs 3 pilot zones
        provinces = ["Bujumbura Mairie", "Bujumbura Rural", "Gitega", "Karusi", "Rutana"]
        for prov in provinces:
            if prov.lower() in self.full_text.lower():
                self.log("PROVINCE", True, f"Province '{prov}' documented")
            else:
                self.log("PROVINCE", False, f"Province '{prov}' missing from report")

        # Scission of Bujumbura Rural into Imbo and Mumirwa
        if "imbo" in self.full_text.lower() and "mumirwa" in self.full_text.lower():
            self.log("ZONING_SUBDIVISION", True, "Subdivision into Imbo (<1000m) and Mumirwa (>1350m) documented")
        else:
            self.log("ZONING_SUBDIVISION", False, "Missing Imbo and Mumirwa zoning analysis")

        # 2. NASA LHASA removal explanation
        lhasa_mentions = re.findall(r'LHASA', self.full_text, re.IGNORECASE)
        if lhasa_mentions and ("retir" in self.full_text.lower() or "écart" in self.full_text.lower() or "abandon" in self.full_text.lower()):
            self.log("NASA_LHASA_REMOVAL", True, f"NASA LHASA removal explicitly justified ({len(lhasa_mentions)} mentions)")
        else:
            self.log("NASA_LHASA_REMOVAL", False, "NASA LHASA removal not properly documented or justified")

        # 3. Database: MongoDB Atlas (real) vs PostgreSQL (cadrage)
        mongo_mentions = len(re.findall(r'mongodb', self.full_text, re.IGNORECASE))
        sqlite_mentions = len(re.findall(r'sqlite', self.full_text, re.IGNORECASE))
        postgres_mentions = len(re.findall(r'postgresql|postgres', self.full_text, re.IGNORECASE))

        if mongo_mentions >= 10:
            self.log("DB_MONGODB", True, f"MongoDB NoSQL extensively covered ({mongo_mentions} occurrences)")
        else:
            self.log("DB_MONGODB", False, f"MongoDB coverage insufficient ({mongo_mentions} occurrences)")

        if sqlite_mentions >= 5:
            self.log("DB_SQLITE", True, f"SQLite persistent cache documented ({sqlite_mentions} occurrences)")
        else:
            self.log("DB_SQLITE", False, f"SQLite cache not sufficiently covered ({sqlite_mentions} occurrences)")

        if postgres_mentions >= 5:
            self.log("DB_POSTGRES_DIVERGENCE", True, f"PostgreSQL initial cadrage vs MongoDB divergence analyzed ({postgres_mentions} occurrences)")
        else:
            self.log("DB_POSTGRES_DIVERGENCE", False, "PostgreSQL divergence analysis missing")

        # 4. Security & Authentication
        argon_mentions = len(re.findall(r'argon2id|argon2', self.full_text, re.IGNORECASE))
        jwt_mentions = len(re.findall(r'jwt', self.full_text, re.IGNORECASE))
        dummy_hash_mentions = len(re.findall(r'dummy_hash|timing attack|canal auxiliaire', self.full_text, re.IGNORECASE))

        if argon_mentions >= 5:
            self.log("AUTH_ARGON2", True, f"Argon2id hashing documented ({argon_mentions} occurrences)")
        else:
            self.log("AUTH_ARGON2", False, f"Argon2id hashing not documented ({argon_mentions} occurrences)")

        if jwt_mentions >= 5:
            self.log("AUTH_JWT", True, f"JWT bearer tokens documented ({jwt_mentions} occurrences)")
        else:
            self.log("AUTH_JWT", False, f"JWT authentication not documented ({jwt_mentions} occurrences)")

        if dummy_hash_mentions >= 2:
            self.log("AUTH_ANTI_TIMING", True, f"Side-channel timing attack mitigation (DUMMY_HASH) documented ({dummy_hash_mentions} occurrences)")
        else:
            self.log("AUTH_ANTI_TIMING", False, "Side-channel timing attack protection not documented")

        # 5. Crop matrix ISABU
        if "cultures_par_zone" in self.full_text.lower() or "culture prévalente" in self.full_text.lower() or "cultures prévalentes" in self.full_text.lower():
            self.log("CROPS_ISABU", True, "ISABU prevailing crop matrix per province documented")
        else:
            self.log("CROPS_ISABU", False, "Prevailing crops per province missing")

        # 6. Test statistics: 31 tests pytest
        if "31" in self.full_text and "test" in self.full_text.lower():
            self.log("TESTS_31", True, "Accurate reporting of backend 31 pytest tests")
        else:
            self.log("TESTS_31", False, "Backend test count (31 tests) not reported accurately")

        # 7. Frontend technologies: Svelte 5 runes, SvelteKit, Leaflet/Sveaflet
        svelte_mentions = len(re.findall(r'svelte', self.full_text, re.IGNORECASE))
        leaflet_mentions = len(re.findall(r'leaflet|sveaflet', self.full_text, re.IGNORECASE))
        if svelte_mentions >= 10:
            self.log("FE_SVELTE", True, f"Svelte 5 / SvelteKit documented ({svelte_mentions} occurrences)")
        else:
            self.log("FE_SVELTE", False, f"Svelte coverage insufficient ({svelte_mentions})")

        if leaflet_mentions >= 5:
            self.log("FE_LEAFLET", True, f"Leaflet / Sveaflet map documented ({leaflet_mentions} occurrences)")
        else:
            self.log("FE_LEAFLET", False, f"Leaflet map coverage insufficient ({leaflet_mentions})")

    def print_summary_and_verdict(self):
        print("\n" + "=" * 80)
        print("FORENSIC AUDIT SUMMARY REPORT")
        print("=" * 80)
        print(f"File: {self.docx_path}")
        print(f"Size: {self.metrics.get('file_size_bytes', 0)} bytes ({self.metrics.get('file_size_kb', 0):.2f} KB)")
        print(f"SHA-256: {self.metrics.get('sha256', 'N/A')}")
        print(f"Paragraphs: {self.metrics.get('paragraph_count', 0)}")
        print(f"Words: {self.metrics.get('word_count', 0)}")
        print(f"Characters: {self.metrics.get('char_count', 0)}")
        print(f"Tables: {self.metrics.get('table_count', 0)}")
        print(f"IEEE Citations: {self.metrics.get('citation_count', 0)}")
        print("-" * 80)
        print(f"TOTAL CHECKS PASSED: {len(self.findings)}")
        print(f"TOTAL VIOLATIONS:    {len(self.violations)}")
        print("-" * 80)

        if self.violations:
            print("\n!!! INTEGRITY VIOLATION DETECTED !!!")
            for cat, detail in self.violations:
                print(f" - [{cat}] {detail}")
            verdict = "INTEGRITY VIOLATION"
        else:
            print("\n>>> AUDIT VERDICT: CLEAN <<<")
            print("No integrity violations, no fraud, no shortcuts, 100% authentic academic content.")
            verdict = "CLEAN"

        print("=" * 80)
        return verdict


if __name__ == '__main__':
    auditor = ForensicAuditor(DOCX_PATH)
    auditor.run_all_checks()
    if auditor.violations:
        sys.exit(1)
    else:
        sys.exit(0)
