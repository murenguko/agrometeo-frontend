import win32com.client as win32
import json

word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False
try:
    doc = word.Documents.Open(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx', ReadOnly=True)
    sec2 = doc.Sections(2)
    
    sec2_paras = []
    for p in sec2.Range.Paragraphs:
        t = p.Range.Text.strip()
        if t:
            page_in_sec = p.Range.Information(1) # wdActiveEndAdjustedPageNumber
            sec2_paras.append((t, page_in_sec))
            
    print(f"Total non-empty paragraphs in sec2: {len(sec2_paras)}")
    
    headings_to_find = [
        "INTRODUCTION GÉNÉRALE",
        "1. Contexte Général et Justification",
        "2. Problématique de Recherche et d'Ingénierie",
        "3. Questions Spécifiques de Recherche et d'Ingénierie",
        "4. Objectif Général du Projet",
        "5. Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)",
        "6. Structure Globale du Rapport",
        
        "CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC",
        "1. Présentation du Cadre d'Étude et Périmètre des Zones Pilotes",
        "2. Expression et Analyse du Besoin des Parties Prenantes",
        "3. Modélisation des Personas et Parcours Utilisateurs",
        "4. Contraintes Globales d'Ingénierie",
        "5. Étude de Faisabilité Multidimensionnelle",
        "6. Synthèse du Diagnostic",
        
        "CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART",
        "1. Architecture Client-Serveur",
        "2. Framwework Front-End",
        "3. Framework Back-End",
        "4. Persistance des Données : MongoDB Atlas & Cache SQLite vs PostgreSQL",
        "5. API REST, Protocoles et Formats d'Échange",
        "6. Architecture de Sécurité et d'Authentification Avancée",
        "6.1 Hachage Cryptographique des Mots de Passe via Argon2id",
        "6.2 Neutralisation des Attaques Temporelles (Side-Channel Timing Attacks)",
        "6.3 Jetons JSON Web Tokens (JWT) et Transport Sécurisé par Cookies HttpOnly",
        "7. Responsive Design et Accessibilité Numérique (WCAG 2.1)",
        "8. Synthèse de l'État de l'Art et Choix Retenus",
        
        "CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE",
        "1. Spécification des Exigences Fonctionnelles (EF-01 à EF-20)",
        "2. Spécification des Exigences Non-Fonctionnelles (ENF-01 à ENF-10)",
        "3. Architecture Applicative Globale et Séparation BFF",
        "4. Modélisation UML Complète du Système",
        "4.1 Diagramme de Cas d'Utilisation (Use Case Diagram)",
        "4.2 Diagramme de Classes Métier (Class Diagram)",
        "4.3 Diagramme de Composants (Component Diagram)",
        "4.4 Diagrammes de Séquence (Sequence Diagrams)",
        "5. Modélisation des Données et Schémas Physiques",
        "5.1 Schéma de la Collection MongoDB 'users'",
        "5.2 Schéma de la Table de Cache SQLite (.cache.sqlite)",
        "6. Moteur de Règles Métier et Formalisation Algorithmique",
        "6.1 Formalisation Mathématique des Règles Métier",
        "6.2 Matrice ISABU des Cultures Prévalentes par Région",
        "7. Planification Agile Scrum sur Deux Semaines (W1–W2)",
        "8. Synthèse de la Conception",
        
        "CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION",
        "1. Environnement de Développement et Outillage Technique",
        "2. Implémentation du Backend `weather-backend`",
        "2.1 Implémentation des Contrôleurs et Routes FastAPI",
        "2.2 Client Réseau Résilient et Mise en Cache SQLite (app/services/weather.py)",
        "2.3 Moteur d'Agrégation Temporelle (app/services/measures.py)",
        "2.4 Moteur Décisionnel et Éthique des Messages (app/services/advice.py)",
        "3. Implémentation du Frontend SvelteKit `weather-app`",
        "3.1 Composant Cartographique Interactif (src/lib/components/Leaflet.svelte)",
        "3.2 Visualisation Vectorielle Temporelle (svelteplot) et Filtrage des Avis",
        "3.3 Modale d'Inspection des Mesures et Limitations",
        "4. Gestion de Version Git, Dépendances et Documentation",
        "5. Synthèse de la Réalisation",
        
        "CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION",
        "1. Méthodologie d'Assurance Qualité et Stratégie de Test",
        "2. Revue Exhaustive des Tests Automatisés Backend (pytest)",
        "3. Tests et Validation du Frontend SvelteKit",
        "4. Tests d'Interface, Compatibilité Responsive et Accessibilité (WCAG 2.1)",
        "5. Évaluation de l'Utilisabilité et des Performances",
        "7. Synthèse de l'Évaluation",
        
        "CONCLUSION GÉNÉRALE ET PERSPECTIVES",
        "1. Bilan Synthétique au Regard de la Problématique et des Objectifs",
        "2. Limites Actuelles du Prototype",
        "3. Perspectives d'Évolution",
        
        "ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS",
        "A.1 Matrice Détaillée des Cas d'Utilisation",
        "A.2 Dictionnaire des Événements et Transitions d'États",
        "ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES",
        "B.1 Spécification de la Collection MongoDB 'users'",
        "B.2 Spécification des Tables de Cache SQLite (.cache.sqlite)",
        "ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION",
        "RÉFÉRENCES BIBLIOGRAPHIQUES"
    ]
    
    results = {}
    for h in headings_to_find:
        page = None
        for t, p in sec2_paras:
            if t == h or t.startswith(h) or h == t.strip():
                page = p
                break
        if page is None:
            # Fallback for minor variations
            for t, p in sec2_paras:
                if h in t:
                    page = p
                    break
        results[h] = page
        print(f"[{page:2d}] {h}")
        
    with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\headings_pages.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    doc.Close(False)
finally:
    word.Quit()
