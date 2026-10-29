import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import shutil
import os
import json

TARGET_FILE = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
BACKUP_FILE = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx.pre_fix"

# 1. Backup target
if not os.path.exists(BACKUP_FILE):
    shutil.copyfile(TARGET_FILE, BACKUP_FILE)
    print(f"Created backup at {BACKUP_FILE}")

# 2. Open document
doc = docx.Document(TARGET_FILE)

# Find INTRODUCTION GÉNÉRALE
p_intro_idx = None
for idx, p in enumerate(doc.paragraphs):
    if p.text.strip() == "INTRODUCTION GÉNÉRALE":
        p_intro_idx = idx
        break

if p_intro_idx is None:
    raise ValueError("Could not find 'INTRODUCTION GÉNÉRALE' in document!")

print(f"Found 'INTRODUCTION GÉNÉRALE' at paragraph index {p_intro_idx}")

# Delete all preliminary paragraphs before p_intro
for idx in range(p_intro_idx - 1, -1, -1):
    p = doc.paragraphs[idx]
    p._element.getparent().remove(p._element)

print("Removed old preliminary paragraphs.")

# Re-reference p0 (which is now INTRODUCTION GÉNÉRALE at index 0)
p0 = doc.paragraphs[0]
assert p0.text.strip() == "INTRODUCTION GÉNÉRALE"

def format_p(p, font_name="Times New Roman", font_size=12, bold=False, italic=False, 
             alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.5, color=None):
    p.paragraph_format.alignment = alignment
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    for r in p.runs:
        r.font.name = font_name
        r.font.size = Pt(font_size)
        r.bold = bold
        r.italic = italic
        if color:
            r.font.color.rgb = color
    return p

def add_p_before(ref_p, text="", font_name="Times New Roman", font_size=12, bold=False, italic=False,
                 alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.5, color=None):
    new_p = ref_p.insert_paragraph_before(text)
    format_p(new_p, font_name, font_size, bold, italic, alignment, space_before, space_after, line_spacing, color)
    return new_p

def add_toc_line_before(ref_p, title, page_str, level=1, is_bold=False):
    new_p = ref_p.insert_paragraph_before()
    new_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    new_p.paragraph_format.line_spacing = 1.15
    new_p.paragraph_format.space_before = Pt(2 if level == 1 else 0.5)
    new_p.paragraph_format.space_after = Pt(2 if level == 1 else 0.5)
    
    if level == 2:
        new_p.paragraph_format.left_indent = Inches(0.25)
    elif level == 3:
        new_p.paragraph_format.left_indent = Inches(0.5)
        
    pPr = new_p._element.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'right')
    tab.set(qn('w:leader'), 'dot')
    tab.set(qn('w:pos'), '9070')
    tabs.append(tab)
    pPr.append(tabs)
    
    r1 = new_p.add_run(title)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11 if level > 1 else 12)
    r1.bold = is_bold
    
    r2 = new_p.add_run(f"\t{page_str}")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11 if level > 1 else 12)
    r2.bold = is_bold
    return new_p

# ==============================================================================
# PAGE 1 : PAGE DE GARDE
# ==============================================================================
add_p_before(p0, "RÉPUBLIQUE DU BURUNDI", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, line_spacing=1.15)
add_p_before(p0, "MINISTÈRE DE L'ÉDUCATION NATIONALE ET DE LA RECHERCHE SCIENTIFIQUE", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, line_spacing=1.15)
add_p_before(p0, "UNIVERSITÉ POLYTECHNIQUE DE GITEGA (UPG)", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2, line_spacing=1.15)
add_p_before(p0, "FACULTÉ DES TECHNOLOGIES DE L'INFORMATION ET DE LA COMMUNICATION", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2, line_spacing=1.15)
add_p_before(p0, "DÉPARTEMENT DE GÉNIE LOGICIEL", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=20, line_spacing=1.15)

add_p_before(p0, "PROJET II — GÉNIE LOGICIEL", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4, line_spacing=1.15)
add_p_before(p0, "RAPPORT DE PROJET DE FIN D'ÉTUDES", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=24, line_spacing=1.15)

add_p_before(p0, "Thème :", font_size=12, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4, line_spacing=1.15)
add_p_before(p0, "SYSTÈME DE VEILLE MÉTÉO ET CLIMATIQUE AU BURUNDI", font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8, line_spacing=1.2)
add_p_before(p0, "Plateforme décisionnelle agro-climatique collinaire basée sur SvelteKit, FastAPI, MongoDB Atlas et les flux ouverts Open-Meteo & GloFAS", 
             font_size=11, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=36, line_spacing=1.2)

add_p_before(p0, "Présenté et soutenu par :", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=2, line_spacing=1.15)
add_p_before(p0, "[Nom et Prénom de l'Étudiant / Candidat]\nÉtudiant en Génie Logiciel (Projet II)", font_size=11, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=16, line_spacing=1.15)

add_p_before(p0, "Sous la direction de :", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=2, line_spacing=1.15)
add_p_before(p0, "[Nom et Titre de l'Encadreur]\nEncadreur Pédagogique et Scientifique", font_size=11, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=30, line_spacing=1.15)

add_p_before(p0, "Année Académique : 2025 – 2026", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2, line_spacing=1.15)
p_end_page1 = add_p_before(p0, "Gitega, Burundi — Octobre 2026", font_size=11, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10, line_spacing=1.15)
p_end_page1.runs[-1].add_break(WD_BREAK.PAGE)

# ==============================================================================
# PAGE 2 & 3 : TABLE DES MATIÈRES ET TABLE DES ANNEXES
# Exact Word section page numbers verified via win32com layout engine
# ==============================================================================
add_p_before(p0, "TABLE DES MATIÈRES", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=10)

toc_items = [
    ("INTRODUCTION GÉNÉRALE", "1", 1, True),
    ("1. Contexte Général et Justification", "1", 2, False),
    ("2. Problématique de Recherche et d'Ingénierie", "2", 2, False),
    ("3. Questions Spécifiques de Recherche et d'Ingénierie", "3", 2, False),
    ("4. Objectif Général du Projet", "4", 2, False),
    ("5. Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)", "4", 2, False),
    ("6. Structure Globale du Rapport", "5", 2, False),
    
    ("CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC", "7", 1, True),
    ("1. Présentation du Cadre d'Étude et Périmètre des Zones Pilotes", "7", 2, False),
    ("2. Expression et Analyse du Besoin des Parties Prenantes", "10", 2, False),
    ("3. Modélisation des Personas et Parcours Utilisateurs", "10", 2, False),
    ("4. Contraintes Globales d'Ingénierie", "12", 2, False),
    ("5. Étude de Faisabilité Multidimensionnelle", "13", 2, False),
    ("6. Synthèse du Diagnostic", "14", 2, False),
    
    ("CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART", "15", 1, True),
    ("1. Architecture Client-Serveur", "15", 2, False),
    ("2. Framwework Front-End", "17", 2, False),
    ("3. Framework Back-End", "17", 2, False),
    ("4. Persistance des Données : MongoDB Atlas & Cache SQLite vs PostgreSQL", "18", 2, False),
    ("5. API REST, Protocoles et Formats d'Échange", "18", 2, False),
    ("6. Architecture de Sécurité et d'Authentification Avancée", "19", 2, False),
    ("6.1 Hachage Cryptographique des Mots de Passe via Argon2id", "19", 3, False),
    ("6.2 Neutralisation des Attaques Temporelles (Side-Channel Timing Attacks)", "19", 3, False),
    ("6.3 Jetons JSON Web Tokens (JWT) et Transport Sécurisé par Cookies HttpOnly", "20", 3, False),
    ("7. Responsive Design et Accessibilité Numérique (WCAG 2.1)", "20", 2, False),
    ("8. Synthèse de l'État de l'Art et Choix Retenus", "21", 2, False),
    
    ("CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE", "22", 1, True),
    ("1. Spécification des Exigences Fonctionnelles (EF-01 à EF-20)", "22", 2, False),
    ("2. Spécification des Exigences Non-Fonctionnelles (ENF-01 à ENF-10)", "24", 2, False),
    ("3. Architecture Applicative Globale et Séparation BFF", "26", 2, False),
    ("4. Modélisation UML Complète du Système", "27", 2, False),
    ("4.1 Diagramme de Cas d'Utilisation (Use Case Diagram)", "27", 3, False),
    ("4.2 Diagramme de Classes Métier (Class Diagram)", "29", 3, False),
    ("4.3 Diagramme de Composants (Component Diagram)", "30", 3, False),
    ("4.4 Diagrammes de Séquence (Sequence Diagrams)", "31", 3, False),
    ("5. Modélisation des Données et Schémas Physiques", "33", 2, False),
    ("5.1 Schéma de la Collection MongoDB 'users'", "33", 3, False),
    ("5.2 Schéma de la Table de Cache SQLite (.cache.sqlite)", "34", 3, False),
    ("6. Moteur de Règles Métier et Formalisation Algorithmique", "34", 2, False),
    ("6.1 Formalisation Mathématique des Règles Métier", "34", 3, False),
    ("6.2 Matrice ISABU des Cultures Prévalentes par Région", "36", 3, False),
    ("7. Planification Agile Scrum sur Deux Semaines (W1–W2)", "36", 2, False),
    ("8. Synthèse de la Conception", "37", 2, False),
    
    ("CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION", "38", 1, True),
    ("1. Environnement de Développement et Outillage Technique", "38", 2, False),
    ("2. Implémentation du Backend `weather-backend`", "39", 2, False),
    ("2.1 Implémentation des Contrôleurs et Routes FastAPI", "40", 3, False),
    ("2.2 Client Réseau Résilient et Mise en Cache SQLite (app/services/weather.py)", "40", 3, False),
    ("2.3 Moteur d'Agrégation Temporelle (app/services/measures.py)", "41", 3, False),
    ("2.4 Moteur Décisionnel et Éthique des Messages (app/services/advice.py)", "41", 3, False),
    ("3. Implémentation du Frontend SvelteKit `weather-app`", "42", 2, False),
    ("3.1 Composant Cartographique Interactif (src/lib/components/Leaflet.svelte)", "43", 3, False),
    ("3.2 Visualisation Vectorielle Temporelle (svelteplot) et Filtrage des Avis", "44", 3, False),
    ("3.3 Modale d'Inspection des Mesures et Limitations", "44", 3, False),
    ("4. Gestion de Version Git, Dépendances et Documentation", "44", 2, False),
    ("5. Synthèse de la Réalisation", "44", 2, False),
    
    ("CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION", "45", 1, True),
    ("1. Méthodologie d'Assurance Qualité et Stratégie de Test", "45", 2, False),
    ("2. Revue Exhaustive des Tests Automatisés Backend (pytest)", "46", 2, False),
    ("3. Tests et Validation du Frontend SvelteKit", "49", 2, False),
    ("4. Tests d'Interface, Compatibilité Responsive et Accessibilité (WCAG 2.1)", "49", 2, False),
    ("5. Évaluation de l'Utilisabilité et des Performances", "50", 2, False),
    ("7. Synthèse de l'Évaluation", "50", 2, False),
    
    ("CONCLUSION GÉNÉRALE ET PERSPECTIVES", "51", 1, True),
    ("1. Bilan Synthétique au Regard de la Problématique et des Objectifs", "51", 2, False),
    ("2. Limites Actuelles du Prototype", "52", 2, False),
    ("3. Perspectives d'Évolution", "52", 2, False),
]

for title, page_str, level, is_bold in toc_items:
    add_toc_line_before(p0, title, page_str, level, is_bold)

# TABLE DES ANNEXES
p_annex_title = add_p_before(p0, "TABLE DES ANNEXES", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)
p_annex_title.paragraph_format.keep_with_next = True

annex_items = [
    ("ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS", "55", 1, True),
    ("A.1 Matrice Détaillée des Cas d'Utilisation", "55", 2, False),
    ("A.2 Dictionnaire des Événements et Transitions d'États", "56", 2, False),
    ("ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES", "57", 1, True),
    ("B.1 Spécification de la Collection MongoDB 'users'", "57", 2, False),
    ("B.2 Spécification des Tables de Cache SQLite (.cache.sqlite)", "57", 2, False),
    ("ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION", "58", 1, True),
]

for title, page_str, level, is_bold in annex_items:
    add_toc_line_before(p0, title, page_str, level, is_bold)

# Références bibliographiques entry placed in TOC at its exact sequential position (page 58)
p_end_page2 = add_toc_line_before(p0, "RÉFÉRENCES BIBLIOGRAPHIQUES", "58", level=1, is_bold=True)
p_end_page2.runs[-1].add_break(WD_BREAK.PAGE)

# ==============================================================================
# PAGE 4 : LISTE DES FIGURES ET LISTE DES TABLEAUX
# Exact Word section page numbers verified via win32com layout engine
# ==============================================================================
add_p_before(p0, "LISTE DES FIGURES", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=10)

figures_list = [
    ("Figure 1.2 — Diagramme de flux du parcours utilisateur complet", "12"),
    ("Figure 2.1 — Diagramme architectural du patron Backend-For-Frontend (BFF)", "16"),
    ("Figure 3.1 — Architecture logicielle globale en couches et interconnexions de données", "26"),
    ("Figure 3.2 — Diagramme de cas d'utilisation du système AgroMétéo Burundi", "29"),
    ("Figure 3.3 — Diagramme de classes métier du backend AgroMétéo Burundi", "29"),
    ("Figure 3.4 — Diagramme de composants logiciels du système", "31"),
    ("Figure 3.5 — Diagramme de séquence de l'authentification OAuth2 / JWT", "32"),
    ("Figure 3.6 — Diagramme de séquence de la consultation d'un bulletin agro-météorologique", "33"),
    ("Figure 4.1 — Structure modulaire de la base de code du backend FastAPI", "40"),
    ("Figure 4.2 — Structure modulaire du frontend SvelteKit", "43"),
]

for title, page_str in figures_list:
    add_toc_line_before(p0, title, page_str, level=1, is_bold=False)

add_p_before(p0, "LISTE DES TABLEAUX", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=10)

tables_list = [
    ("Tableau 0.1 — Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)", "4"),
    ("Tableau 1.1 — Caractérisation géographique et agro-climatique des zones pilotes d'étude", "8"),
    ("Tableau 1.2 — Matrice des besoins exprimés par typologie d'utilisateurs", "10"),
    ("Tableau 3.1 — Spécification formelle des exigences fonctionnelles (EF-01 à EF-20)", "22"),
    ("Tableau 3.2 — Spécification formelle des exigences non fonctionnelles (ENF-01 à ENF-10)", "24"),
    ("Tableau 3.3 — Description des classes et modules logiciels métier", "30"),
    ("Tableau 3.4 — Planification Scrum et exécution des sprints sur 10 jours ouvrés", "36"),
    ("Tableau 4.1 — Matrice de l'environnement technologique et outillage de développement", "38"),
    ("Tableau 5.1 — Registre exhaustif des 31 tests unitaires validés sous pytest (100% succès)", "46"),
    ("Tableau A.1 — Spécification tabulaire détaillée des cas d'utilisation", "55"),
    ("Tableau A.2 — Dictionnaire formel des transitions de la machine à états de vigilance", "56"),
    ("Tableau B.1 — Dictionnaire des données de la collection MongoDB 'users'", "57"),
    ("Tableau B.2 — Schéma physique des tables du cache local SQLite", "57"),
]

p_end_page3 = None
for title, page_str in tables_list:
    p_end_page3 = add_toc_line_before(p0, title, page_str, level=1, is_bold=False)

p_end_page3.runs[-1].add_break(WD_BREAK.PAGE)

# ==============================================================================
# PAGE 5 & 6 : LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES
# ==============================================================================
add_p_before(p0, "LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=10)

sigles = [
    ("API", "Application Programming Interface (Interface de Programmation d'Application)"),
    ("ASGI", "Asynchronous Server Gateway Interface (Interface de Passerelle Asynchrone)"),
    ("ASIC", "Application-Specific Integrated Circuit (Circuit Intégré Dédié)"),
    ("BFF", "Backend-For-Frontend (Patron d'Architecture Backend pour Frontend)"),
    ("BSON", "Binary JSON (Format Documentaire Binaire Sérialisé de MongoDB)"),
    ("CHIRPS", "Climate Hazards Group InfraRed Precipitation with Stations"),
    ("CORS", "Cross-Origin Resource Sharing (Partage de Ressources entre Origines Multiples)"),
    ("CSS", "Cascading Style Sheets (Feuilles de Style en Cascade)"),
    ("DOM", "Document Object Model (Modèle Objet de Document)"),
    ("DPAE", "Direction Provinciale de l'Agriculture et de l'Élevage (Burundi)"),
    ("DRF", "Django Rest Framework"),
    ("ECMWF", "European Centre for Medium-Range Weather Forecasts"),
    ("EF", "Exigence Fonctionnelle"),
    ("ENF", "Exigence Non-Fonctionnelle"),
    ("FCP", "First Contentful Paint (Temps d'Affichage du Premier Contenu)"),
    ("GeoJSON", "Geographic JavaScript Object Notation (Format Géospatial Ouvert)"),
    ("GFS", "Global Forecast System (Modèle Numérique Météorologique Global)"),
    ("GloFAS", "Global Flood Awareness System (Système Mondial d'Alerte aux Inondations)"),
    ("GPU", "Graphics Processing Unit (Processeur Graphique)"),
    ("HTML", "HyperText Markup Language (Langage de Balisage Hypertexte)"),
    ("HTTP", "HyperText Transfer Protocol (Protocole de Transfert Hypertexte)"),
    ("IEEE", "Institute of Electrical and Electronics Engineers"),
    ("IETF", "Internet Engineering Task Force"),
    ("IGEBU", "Institut Géographique du Burundi"),
    ("ISABU", "Institut des Sciences Agronomiques du Burundi"),
    ("ISO", "International Organization for Standardization"),
    ("JSON", "JavaScript Object Notation (Format d'Échange Textuel Léger)"),
    ("JWT", "JSON Web Token (Jeton d'Authentification Signé et Compact)"),
    ("LHASA", "Landslide Hazard Assessment for Situational Awareness (Modèle NASA)"),
    ("MoSCoW", "Must have, Should have, Could have, Won't have (Méthode de Priorisation)"),
    ("MVP", "Minimum Viable Product (Produit Minimum Viable)"),
    ("NASA", "National Aeronautics and Space Administration"),
    ("NetCDF", "Network Common Data Form (Format de Données Multidimensionnelles)"),
    ("NoSQL", "Not Only SQL (Bases de Données Non-Relationnelles Orientées Documents)"),
    ("OAuth2", "Open Authorization Framework version 2.0"),
    ("OMG", "Object Management Group"),
    ("OMM / WMO", "Organisation Météorologique Mondiale / World Meteorological Organization"),
    ("OS", "Objectif Spécifique"),
    ("OSM", "OpenStreetMap (Plateforme Cartographique Ouverte)"),
    ("OWASP", "Open Web Application Security Project (Projet de Sécurité Web)"),
    ("PIB", "Produit Intérieur Brut"),
    ("PNA", "Plan National d'Adaptation aux Changements Climatiques"),
    ("REST", "Representational State Transfer (Style d'Architecture Web Distribuée)"),
    ("RFC", "Request For Comments (Documents de Spécification et Normes IETF)"),
    ("SGBD", "Système de Gestion de Base de Données"),
    ("SMART", "Spécifique, Mesurable, Atteignable, Réaliste, Temporellement Défini"),
    ("SQL", "Structured Query Language (Langage de Requêtes Structurées)"),
    ("SSR", "Server-Side Rendering (Rendu Web Côté Serveur)"),
    ("TIC", "Technologies de l'Information et de la Communication"),
    ("TTL", "Time To Live (Durée de Rétention des Données en Cache)"),
    ("UI", "User Interface (Interface Utilisateur)"),
    ("UML", "Unified Modeling Language (Langage de Modélisation Unifié)"),
    ("UPG", "Université Polytechnique de Gitega"),
    ("URI / URL", "Uniform Resource Identifier / Uniform Resource Locator"),
    ("UX", "User Experience (Expérience Utilisateur)"),
    ("WCAG", "Web Content Accessibility Guidelines (Directives d'Accessibilité Web)"),
    ("W3C", "World Wide Web Consortium"),
    ("XSS", "Cross-Site Scripting (Vulnérabilité d'Injection de Script Client)"),
]

last_sigle_p = None
for acronym, definition in sigles:
    p_sig = add_p_before(p0, font_size=11, space_before=1, space_after=1.5, line_spacing=1.15)
    r_ac = p_sig.add_run(f"{acronym} : ")
    r_ac.font.name = "Times New Roman"
    r_ac.font.size = Pt(11)
    r_ac.bold = True
    
    r_def = p_sig.add_run(definition)
    r_def.font.name = "Times New Roman"
    r_def.font.size = Pt(11)
    last_sigle_p = p_sig

# Attach section break properties to the last preliminary paragraph
pPr_last = last_sigle_p._element.get_or_add_pPr()
sectPr0 = OxmlElement('w:sectPr')

pgMar0 = OxmlElement('w:pgMar')
pgMar0.set(qn('w:top'), '1417')      # 2.5 cm
pgMar0.set(qn('w:right'), '1417')    # 2.5 cm
pgMar0.set(qn('w:bottom'), '1417')   # 2.5 cm
pgMar0.set(qn('w:left'), '1701')     # 3.0 cm (reliure)
pgMar0.set(qn('w:header'), '720')
pgMar0.set(qn('w:footer'), '720')
sectPr0.append(pgMar0)

pgSz0 = OxmlElement('w:pgSz')
pgSz0.set(qn('w:w'), '12240')        # Letter / A4 standard
pgSz0.set(qn('w:h'), '15840')
sectPr0.append(pgSz0)

type0 = OxmlElement('w:type')
type0.set(qn('w:val'), 'nextPage')
sectPr0.append(type0)

pgNumType0 = OxmlElement('w:pgNumType')
pgNumType0.set(qn('w:fmt'), 'lowerRoman')
pgNumType0.set(qn('w:start'), '1')
sectPr0.append(pgNumType0)

pPr_last.append(sectPr0)

# Save and reload to ensure clean section object binding in python-docx
doc.save(TARGET_FILE)
doc = docx.Document(TARGET_FILE)

sec0 = doc.sections[0]
sec1 = doc.sections[1]

# Section 1 starts body: decoupler from Section 0
sec1.footer.is_linked_to_previous = False

sectPr1 = sec1._sectPr
pgNumType1 = sectPr1.find(qn('w:pgNumType'))
if pgNumType1 is None:
    pgNumType1 = OxmlElement('w:pgNumType')
    sectPr1.append(pgNumType1)
pgNumType1.set(qn('w:fmt'), 'decimal')
pgNumType1.set(qn('w:start'), '1')

pgMar1 = sectPr1.find(qn('w:pgMar'))
if pgMar1 is not None:
    pgMar1.set(qn('w:top'), '1417')     # 2.5 cm
    pgMar1.set(qn('w:bottom'), '1417')  # 2.5 cm
    pgMar1.set(qn('w:right'), '1417')   # 2.5 cm
    pgMar1.set(qn('w:left'), '1701')    # 3.0 cm (reliure)

# Footer for Section 0 (Preliminary Pages: Roman numerals centered)
footer0 = sec0.footer
f_p0 = footer0.paragraphs[0]
f_p0.text = ""
f_p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
f_p0.paragraph_format.line_spacing = 1.0
f_p0.paragraph_format.space_before = Pt(0)
f_p0.paragraph_format.space_after = Pt(0)

fld_xml0 = parse_xml(r'''
<w:pPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:pStyle w:val="Footer"/>
    <w:jc w:val="center"/>
</w:pPr>
''')
f_p0._element.append(fld_xml0)
r_begin = f_p0.add_run()
r_begin._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
r_instr = f_p0.add_run()
r_instr._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w')))
r_sep = f_p0.add_run()
r_sep._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))
r_txt = f_p0.add_run("i")
r_txt.font.name = "Times New Roman"
r_txt.font.size = Pt(10)
r_end = f_p0.add_run()
r_end._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))

# Footer for Section 1 (Body: Arabic numerals starting at 1 centered)
footer1 = sec1.footer
f_p1 = footer1.paragraphs[0]
f_p1.text = ""
f_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
f_p1.paragraph_format.line_spacing = 1.0
f_p1.paragraph_format.space_before = Pt(0)
f_p1.paragraph_format.space_after = Pt(0)

fld_xml1 = parse_xml(r'''
<w:pPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:pStyle w:val="Footer"/>
    <w:jc w:val="center"/>
</w:pPr>
''')
f_p1._element.append(fld_xml1)
r1_begin = f_p1.add_run()
r1_begin._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
r1_instr = f_p1.add_run()
r1_instr._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w')))
r1_sep = f_p1.add_run()
r1_sep._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))
r1_txt = f_p1.add_run("1")
r1_txt.font.name = "Times New Roman"
r1_txt.font.size = Pt(10)
r1_end = f_p1.add_run()
r1_end._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))

doc.save(TARGET_FILE)
print("Successfully regenerated target document with exact Word layout page numbers!")
