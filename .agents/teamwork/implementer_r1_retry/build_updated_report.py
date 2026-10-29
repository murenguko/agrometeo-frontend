import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import shutil
import re

INPUT_FILE = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx.bak"
OUTPUT_FILE = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"

# Make sure we read from pristine backup and write to target
shutil.copyfile(INPUT_FILE, OUTPUT_FILE)
doc = docx.Document(OUTPUT_FILE)

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
    new_p.paragraph_format.line_spacing = 1.3
    new_p.paragraph_format.space_before = Pt(3 if level == 1 else 1)
    new_p.paragraph_format.space_after = Pt(3 if level == 1 else 1)
    
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
# PAGE 2 : TABLE DES MATIÈRES ET TABLE DES ANNEXES
# ==============================================================================
add_p_before(p0, "TABLE DES MATIÈRES", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)

toc_items = [
    ("INTRODUCTION GÉNÉRALE", "1", 1, True),
    ("1. Contexte Général et Justification", "1", 2, False),
    ("2. Problématique de Recherche et d'Ingénierie", "2", 2, False),
    ("3. Questions Spécifiques de Recherche et d'Ingénierie", "3", 2, False),
    ("4. Objectif Général du Projet", "3", 2, False),
    ("5. Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)", "4", 2, False),
    ("6. Structure Globale du Rapport", "5", 2, False),
    
    ("CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC", "6", 1, True),
    ("1. Présentation du Cadre d'Étude et Périmètre des Zones Pilotes", "6", 2, False),
    ("2. Expression et Analyse du Besoin des Parties Prenantes", "9", 2, False),
    ("3. Modélisation des Personas et Parcours Utilisateurs", "10", 2, False),
    ("4. Contraintes Globales d'Ingénierie", "12", 2, False),
    ("5. Étude de Faisabilité Multidimensionnelle", "13", 2, False),
    ("6. Synthèse du Diagnostic", "14", 2, False),
    
    ("CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART", "15", 1, True),
    ("1. Architecture Client-Serveur", "15", 2, False),
    ("2. Framework Front-End", "16", 2, False),
    ("3. Framework Back-End", "17", 2, False),
    ("4. Persistance des Données : MongoDB Atlas & Cache SQLite vs PostgreSQL", "18", 2, False),
    ("5. API REST, Protocoles et Formats d'Échange", "19", 2, False),
    ("6. Architecture de Sécurité et d'Authentification Avancée", "20", 2, False),
    ("6.1 Hachage Cryptographique des Mots de Passe via Argon2id", "20", 3, False),
    ("6.2 Neutralisation des Attaques Temporelles (Side-Channel Timing Attacks)", "21", 3, False),
    ("6.3 Jetons JSON Web Tokens (JWT) et Transport Sécurisé par Cookies HttpOnly", "22", 3, False),
    ("7. Responsive Design et Accessibilité Numérique (WCAG 2.1)", "23", 2, False),
    ("8. Synthèse de l'État de l'Art et Choix Retenus", "24", 2, False),
    
    ("CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE", "25", 1, True),
    ("1. Spécification des Exigences Fonctionnelles (EF-01 à EF-20)", "25", 2, False),
    ("2. Spécification des Exigences Non-Fonctionnelles (ENF-01 à ENF-10)", "27", 2, False),
    ("3. Architecture Applicative Globale et Séparation BFF", "28", 2, False),
    ("4. Modélisation UML Complète du Système", "29", 2, False),
    ("4.1 Diagramme de Cas d'Utilisation (Use Case Diagram)", "29", 3, False),
    ("4.2 Diagramme de Classes Métier (Class Diagram)", "30", 3, False),
    ("4.3 Diagramme de Composants (Component Diagram)", "31", 3, False),
    ("4.4 Diagrammes de Séquence (Sequence Diagrams)", "32", 3, False),
    ("5. Modélisation des Données et Schémas Physiques", "33", 2, False),
    ("5.1 Schéma de la Collection MongoDB 'users'", "33", 3, False),
    ("5.2 Schéma de la Table de Cache SQLite (.cache.sqlite)", "34", 3, False),
    ("6. Moteur de Règles Métier et Formalisation Algorithmique", "35", 2, False),
    ("6.1 Formalisation Mathématique des Règles Métier", "35", 3, False),
    ("6.2 Matrice ISABU des Cultures Prévalentes par Région", "38", 3, False),
    ("7. Planification Agile Scrum sur Deux Semaines (W1–W2)", "39", 2, False),
    ("8. Synthèse de la Conception", "40", 2, False),
    
    ("CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION", "41", 1, True),
    ("1. Environnement de Développement et Outillage Technique", "41", 2, False),
    ("2. Implémentation du Backend `weather-backend`", "42", 2, False),
    ("2.1 Implémentation des Contrôleurs et Routes FastAPI", "42", 3, False),
    ("2.2 Client Réseau Résilient et Mise en Cache SQLite (app/services/weather.py)", "43", 3, False),
    ("2.3 Moteur d'Agrégation Temporelle (app/services/measures.py)", "44", 3, False),
    ("2.4 Moteur Décisionnel et Éthique des Messages (app/services/advice.py)", "45", 3, False),
    ("3. Implémentation du Frontend SvelteKit `weather-app`", "46", 2, False),
    ("3.1 Composant Cartographique Interactif (src/lib/components/Leaflet.svelte)", "47", 3, False),
    ("3.2 Visualisation Vectorielle Temporelle (svelteplot) et Filtrage des Avis", "48", 3, False),
    ("3.3 Modale d'Inspection des Mesures et Limitations", "49", 3, False),
    ("4. Gestion de Version Git, Dépendances et Documentation", "49", 2, False),
    ("5. Synthèse de la Réalisation", "50", 2, False),
    
    ("CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION", "51", 1, True),
    ("1. Méthodologie d'Assurance Qualité et Stratégie de Test", "51", 2, False),
    ("2. Revue Exhaustive des Tests Automatisés Backend (pytest)", "52", 2, False),
    ("3. Tests et Validation du Frontend SvelteKit", "55", 2, False),
    ("4. Tests d'Interface, Compatibilité Responsive et Accessibilité (WCAG 2.1)", "56", 2, False),
    ("5. Évaluation de l'Utilisabilité et des Performances", "57", 2, False),
    ("7. Synthèse de l'Évaluation", "58", 2, False),
    
    ("CONCLUSION GÉNÉRALE ET PERSPECTIVES", "59", 1, True),
    ("1. Bilan Synthétique au Regard de la Problématique et des Objectifs", "59", 2, False),
    ("2. Limites Actuelles du Prototype", "60", 2, False),
    ("3. Perspectives d'Évolution", "61", 2, False),
    
    ("RÉFÉRENCES BIBLIOGRAPHIQUES", "67", 1, True),
]

for title, page_str, level, is_bold in toc_items:
    add_toc_line_before(p0, title, page_str, level, is_bold)

# TABLE DES ANNEXES
add_p_before(p0, "TABLE DES ANNEXES", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=10)

annex_items = [
    ("ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS", "62", 1, True),
    ("A.1 Matrice Détaillée des Cas d'Utilisation", "62", 2, False),
    ("A.2 Dictionnaire des Événements et Transitions d'États", "63", 2, False),
    ("ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES", "64", 1, True),
    ("B.1 Spécification de la Collection MongoDB 'users'", "64", 2, False),
    ("B.2 Spécification des Tables de Cache SQLite (.cache.sqlite)", "65", 2, False),
    ("ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION", "66", 1, True),
]

p_end_page2 = None
for title, page_str, level, is_bold in annex_items:
    p_end_page2 = add_toc_line_before(p0, title, page_str, level, is_bold)

p_end_page2.runs[-1].add_break(WD_BREAK.PAGE)

# ==============================================================================
# PAGE 3 : LISTE DES FIGURES ET LISTE DES TABLEAUX
# ==============================================================================
add_p_before(p0, "LISTE DES FIGURES", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=12)

figures_list = [
    ("Figure 1.2 — Diagramme de flux du parcours utilisateur complet", "12"),
    ("Figure 2.1 — Diagramme architectural du patron Backend-For-Frontend (BFF)", "16"),
    ("Figure 3.1 — Architecture logicielle globale en couches et interconnexions de données", "28"),
    ("Figure 3.2 — Diagramme de cas d'utilisation du système AgroMétéo Burundi", "29"),
    ("Figure 3.3 — Diagramme de classes métier du backend AgroMétéo Burundi", "30"),
    ("Figure 3.4 — Diagramme de composants logiciels du système", "31"),
    ("Figure 3.5 — Diagramme de séquence de l'authentification OAuth2 / JWT", "32"),
    ("Figure 3.6 — Diagramme de séquence de la consultation d'un bulletin agro-météorologique", "32"),
    ("Figure 4.1 — Structure modulaire de la base de code du backend FastAPI", "42"),
    ("Figure 4.2 — Structure modulaire du frontend SvelteKit", "47"),
]

for title, page_str in figures_list:
    add_toc_line_before(p0, title, page_str, level=1, is_bold=False)

add_p_before(p0, "LISTE DES TABLEAUX", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=12)

tables_list = [
    ("Tableau 0.1 — Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)", "4"),
    ("Tableau 1.1 — Caractérisation géographique et agro-climatique des zones pilotes d'étude", "7"),
    ("Tableau 1.2 — Matrice des besoins exprimés par typologie d'utilisateurs", "10"),
    ("Tableau 3.1 — Spécification formelle des exigences fonctionnelles (EF-01 à EF-20)", "25"),
    ("Tableau 3.2 — Spécification formelle des exigences non fonctionnelles (ENF-01 à ENF-10)", "27"),
    ("Tableau 3.3 — Description des classes et modules logiciels métier", "30"),
    ("Tableau 3.4 — Planification Scrum et exécution des sprints sur 10 jours ouvrés", "39"),
    ("Tableau 4.1 — Matrice de l'environnement technologique et outillage de développement", "41"),
    ("Tableau 5.1 — Registre exhaustif des 31 tests unitaires validés sous pytest (100% succès)", "53"),
    ("Tableau A.1 — Spécification tabulaire détaillée des cas d'utilisation", "62"),
    ("Tableau A.2 — Dictionnaire formel des transitions de la machine à états de vigilance", "63"),
    ("Tableau B.1 — Dictionnaire des données de la collection MongoDB 'users'", "64"),
    ("Tableau B.2 — Schéma physique des tables du cache local SQLite", "65"),
]

p_end_page3 = None
for title, page_str in tables_list:
    p_end_page3 = add_toc_line_before(p0, title, page_str, level=1, is_bold=False)

p_end_page3.runs[-1].add_break(WD_BREAK.PAGE)

# ==============================================================================
# PAGE 4 : LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES
# ==============================================================================
add_p_before(p0, "LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)

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
    p_sig = add_p_before(p0, font_size=11, space_before=1, space_after=2, line_spacing=1.25)
    r_ac = p_sig.add_run(f"{acronym} : ")
    r_ac.font.name = "Times New Roman"
    r_ac.font.size = Pt(11)
    r_ac.bold = True
    
    r_def = p_sig.add_run(definition)
    r_def.font.name = "Times New Roman"
    r_def.font.size = Pt(11)
    last_sigle_p = p_sig

pPr_last = last_sigle_p._element.get_or_add_pPr()
sectPr0 = OxmlElement('w:sectPr')

pgMar0 = OxmlElement('w:pgMar')
pgMar0.set(qn('w:top'), '1417')
pgMar0.set(qn('w:right'), '1417')
pgMar0.set(qn('w:bottom'), '1417')
pgMar0.set(qn('w:left'), '1701')
pgMar0.set(qn('w:header'), '720')
pgMar0.set(qn('w:footer'), '720')
sectPr0.append(pgMar0)

pgSz0 = OxmlElement('w:pgSz')
pgSz0.set(qn('w:w'), '12240')
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

doc.save(OUTPUT_FILE)
doc = docx.Document(OUTPUT_FILE)

sec0 = doc.sections[0]
sec1 = doc.sections[1]

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
    pgMar1.set(qn('w:top'), '1417')
    pgMar1.set(qn('w:bottom'), '1417')
    pgMar1.set(qn('w:right'), '1417')
    pgMar1.set(qn('w:left'), '1701')

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

# REVISE BIBLIOGRAPHY (RÉFÉRENCES BIBLIOGRAPHIQUES)
biblio_heading_idx = None
for idx in range(len(doc.paragraphs) - 1, -1, -1):
    p = doc.paragraphs[idx]
    if p.text.strip().upper() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        biblio_heading_idx = idx
        break

print(f"True Biblio heading found at paragraph index {biblio_heading_idx}: {doc.paragraphs[biblio_heading_idx].text}")

to_remove = doc.paragraphs[biblio_heading_idx + 1:]
print(f"Removing {len(to_remove)} old bibliography paragraphs...")
for p in to_remove:
    p._element.getparent().remove(p._element)

BIBLIO_ENTRIES = [
    "[1] République du Burundi, Ministère de l'Environnement, de l'Agriculture et de l'Élevage, « Plan National d'Adaptation aux Changements Climatiques du Burundi (PNA) », Bujumbura, Burundi, 2023.",
    "[2] Institut de Statistiques et d'Études Économiques du Burundi (ISTEEBU) & Banque Mondiale, « Rapport sur l'évaluation de la pauvreté et les indicateurs économiques et agricoles au Burundi », Bujumbura, Burundi, 2023.",
    "[3] World Meteorological Organization (WMO), « Guidelines on Multi-hazard Early Warning Systems and Climate Risk Assessment », WMO-No. 1280, Genève, Suisse, 2022.",
    "[4] Plateforme Nationale de Prévention des Risques et Gestion des Catastrophes & Direction Générale de la Protection Civile du Burundi, « Rapport d'évaluation des impacts des inondations et des aléas hydrométéorologiques dans la plaine de l'Imbo et le bassin du lac Tanganyika », Ministère de l'Intérieur, du Développement Communautaire et de la Sécurité Publique, Bujumbura, Burundi, 2024.",
    "[5] République du Burundi, « Décret n° 100/189 portant missions, organisation et fonctionnement de l'Institut Géographique du Burundi (IGEBU) et cadre légal des prévisions météorologiques », Bulletin Officiel du Burundi, Gitega, Burundi, 2019.",
    "[6] G. Coulouris, J. Dollimore, T. Kindberg, and G. Blair, « Distributed Systems : Concepts and Design », 5e éd., Boston, MA : Addison-Wesley, 2011.",
    "[7] S. Newman, « Building Microservices : Designing Fine-Grained Systems (Backends for Frontends Pattern) », 2e éd., Sebastopol, CA : O'Reilly Media, 2021.",
    "[8] R. Harris and Svelte Core Team, « Svelte 5 Documentation : Runes, Reactivity without Virtual DOM and SvelteKit Architecture », Svelte Society, 2025. [En ligne]. Disponible sur : https://svelte.dev/docs.",
    "[9] S. Ramírez, « FastAPI : Modern, High-Performance Web Framework for Python with Automatic Pydantic Validation », 2025. [En ligne]. Disponible sur : https://fastapi.tiangolo.com.",
    "[10] R. T. Fielding, « Architectural Styles and the Design of Network-based Software Architectures », Ph.D. dissertation, Department of Information and Computer Science, University of California, Irvine, CA, 2000.",
    "[11] A. Biryukov, D. Dinu, and P. Khovratovich, « Argon2 : the memory-hard function for password hashing and other applications », Internet Engineering Task Force (IETF), RFC 9106, 2021.",
    "[12] D. Brumley and D. Boneh, « Remote timing attacks are practical », Computer Networks, vol. 48, n° 5, pp. 701-716, 2005.",
    "[13] M. Jones, J. Bradley, and N. Sakimura, « JSON Web Token (JWT) », Internet Engineering Task Force (IETF), RFC 7519, 2015.",
    "[14] World Wide Web Consortium (W3C), « Web Content Accessibility Guidelines (WCAG) 2.1 », W3C Recommendation, 2018. [En ligne]. Disponible sur : https://www.w3.org/TR/WCAG21/.",
    "[15] D. Clegg and R. Barker, « Case Method Fast-Track : A RAD Approach (MoSCoW Prioritization) », Wokingham : Addison-Wesley, 1994.",
    "[16] Object Management Group (OMG), « Unified Modeling Language (OMG UML) Specification, Version 2.5.1 », OMG Document formal/2017-12-05, 2017.",
    "[17] Institut Géographique du Burundi (IGEBU), « Normes pluviométriques nationales, seuils critiques de précipitation et bulletins de suivi agro-météorologique au Burundi », Ministère de l'Environnement, Gitega, Burundi, 2024.",
    "[18] Institut des Sciences Agronomiques du Burundi (ISABU), « Fiches techniques des cultures vivrières et guides pratiques de gestion agro-climatique collinaire », Département de la Recherche Agronomique, Bujumbura, Burundi, 2023.",
    "[19] K. Schwaber and J. Sutherland, « The Scrum Guide : The Definitive Guide to Scrum : The Rules of the Game », Scrum.org, 2020.",
    "[20] M. Cohn, « Succeeding with Agile : Software Development Using Scrum », Boston, MA : Addison-Wesley Professional, 2009.",
    "[21] Open-Meteo GmbH, « Open-Meteo Weather Forecast API Documentation and High-Resolution Numerical Weather Data », 2026. [En ligne]. Disponible sur : https://open-meteo.com/en/docs.",
    "[22] Copernicus Emergency Management Service & ECMWF, « Global Flood Awareness System (GloFAS) River Discharge Forecast API and Reanalysis Data », European Commission, 2026.",
    "[23] NASA Goddard Space Flight Center, « Landslide Hazard Assessment for Situational Awareness (LHASA) Model Version 2.0 », NASA Earth Science Division, 2024.",
    "[24] OpenStreetMap Foundation, « OpenStreetMap Open Geodata and Leaflet Interactive Mobile-Friendly Mapping Library », 2026. [En ligne]. Disponible sur : https://www.openstreetmap.org et https://leafletjs.com.",
    "[25] C. Funk et al., « The Climate Hazards Center InfraRed Precipitation with Stations (CHIRPS) v3 : A high-resolution rainfall dataset for climate monitoring and agricultural drought tracking », Scientific Data, vol. 11, n° 1, pp. 1-18, 2024.",
    "[26] MongoDB Inc., « MongoDB Atlas Documentation : Fully Managed Cloud Database Architecture and BSON Document Model », 2026. [En ligne]. Disponible sur : https://www.mongodb.com/docs/atlas/ ; et D. Hipp, « SQLite Database Architecture and requests-cache HTTP Caching Engine », 2026.",
    "[27] Université Polytechnique de Gitega (UPG), Faculté des Technologies de l'Information et de la Communication (TIC), « Canevas de Rapport Projet II — Département de Génie Logiciel », Gitega, Burundi, 2025.",
    "[28] Équipe de Projet UPG, « Document de cadrage du projet à développer en deux semaines : Système de veille météo et climatique au Burundi », Version révisée du 11 octobre 2026, Université Polytechnique de Gitega, 2026.",
    "[29] Open Web Application Security Project (OWASP), « OWASP Top 10 Web Application Security Risks and Authentication Verification Standard », OWASP Foundation, 2025. [En ligne]. Disponible sur : https://owasp.org/www-project-top-ten/.",
    "[30] J. Nielsen and R. Budiu, « Mobile Usability : Principles and Patterns for Accessible Handheld Interfaces », Berkeley, CA : New Riders Press, 2012."
]

print(f"Appending {len(BIBLIO_ENTRIES)} harmonized IEEE references...")
for entry in BIBLIO_ENTRIES:
    p_b = doc.add_paragraph()
    format_p(p_b, font_name="Times New Roman", font_size=11, bold=False, italic=False,
             alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=4, line_spacing=1.3)
    p_b.paragraph_format.left_indent = Inches(0.3)
    p_b.paragraph_format.first_line_indent = Inches(-0.3)
    
    m = re.match(r"^(\[\d+\])\s*(.+)$", entry)
    if m:
        r_num = p_b.add_run(m.group(1) + " ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(11)
        r_num.bold = True
        
        r_txt = p_b.add_run(m.group(2))
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(11)
    else:
        r_txt = p_b.add_run(entry)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(11)

doc.save(OUTPUT_FILE)
print("Production transformation completed and saved to Rapport_Projet_Veille_Meteo_Burundi.docx!")
