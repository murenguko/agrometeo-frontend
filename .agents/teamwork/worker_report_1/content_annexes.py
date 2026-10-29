"""
content_annexes.py - Rédaction des Annexes Obligatoires et Références Bibliographiques (Style IEEE)
Conforme aux exigences UPG et aux consignes validées.
"""

from builder import add_h1, add_h2, add_h3, add_p, add_bullet, add_table, add_figure, add_code_block

def build_annexes(doc):
    """Génère les Annexes A, B, D, F et la Bibliographie IEEE complète."""
    
    # =========================================================================
    # ANNEXE A : DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS
    # =========================================================================
    add_h1(doc, "ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS")
    
    add_p(doc,
        "La présente annexe regroupe les spécifications tabulaires exhaustives des diagrammes UML de modélisation logicielle "
        "du système AgroMétéo Burundi, complétant les représentations graphiques présentées au Chapitre III."
    )
    
    add_h2(doc, "A.1 Matrice Détaillée des Cas d'Utilisation")
    headers_uc = ["Identifiant", "Acteur Primaire", "Cas d'Utilisation", "Préconditions", "Postconditions", "Flux Nominal"]
    data_uc = [
        ["CU-01", "Visiteur / Agriculteur", "S'inscrire", "Aucune session active", "Compte créé en MongoDB Atlas", "Saisie nom, email, mot de passe -> Hash Argon2id -> Insertion."],
        ["CU-02", "Utilisateur", "S'authentifier", "Compte existant en base", "Jeton JWT émis en Cookie HttpOnly", "Saisie credentials -> Vérification anti-timing -> Émission JWT HS256."],
        ["CU-03", "Utilisateur authentifié", "Consulter carte nationale", "Session JWT valide", "Affichage carte Leaflet tuilée", "Rendu des 6 marqueurs avec fond OpenStreetMap centré sur le Burundi."],
        ["CU-04", "Utilisateur authentifié", "Sélectionner station/zone", "Carte ou menu affiché", "Redirection route /region/[slug]", "Sélection de la province (ex. Gitega, Karusi, Buja Rural Imbo/Mumirwa)."],
        ["CU-05", "Utilisateur authentifié", "Visualiser séries météo", "Station sélectionnée", "Graphiques interactifs svelteplot", "Bascule entre onglets T°, Pluie, Vent, Probabilité avec tooltips temporels."],
        ["CU-06", "Utilisateur authentifié", "Consulter avis ISABU", "Station sélectionnée", "Fiches conseils filtrées", "Filtrage par culture locale et lecture des actions concrètes."],
        ["CU-07", "Utilisateur authentifié", "Auditer mesures & seuils", "Conseil affiché", "Fenêtre modale ouverte", "Affichage des jauges de dépassement valeur/seuil et limitations du modèle."],
        ["CU-08", "Utilisateur authentifié", "Se déconnecter", "Session active", "Cookie purgé, redirection /login", "Soumission action serveur /?/logout -> Suppression du cookie HttpOnly."]
    ]
    add_table(doc, headers_uc, data_uc, col_widths=[1.8, 3.2, 3.2, 3.2, 3.5, 4.5], caption="Tableau A.1 — Spécification tabulaire détaillée des cas d'utilisation")
    
    add_h2(doc, "A.2 Dictionnaire des Événements et Transitions d'États")
    headers_trans = ["État Source", "Événement / Condition Déclenchante", "Action Exécutée", "État Cible"]
    data_trans = [
        ["Initial", "Réception séries météo brutes d'Open-Meteo et GloFAS", "Vérification d'intégrité et complétude des données", "En Évaluation"],
        ["En Évaluation", "Présence d'au moins une valeur manquante (None / NaN)", "Génération message d'indisponibilité et mise en garde", "Non Évalué"],
        ["En Évaluation", "Toutes séries complètes ET au moins un seuil franchi", "Construction du message d'action pragmatique par culture", "Conseil Actif"],
        ["En Évaluation", "Toutes séries complètes ET aucun seuil critique franchi", "Construction du message probabiliste de vigilance normale", "Sans Signal"],
        ["Non Évalué", "Arrivée d'un nouveau flux complet lors du rafraîchissement", "Réévaluation automatique du moteur pur", "En Évaluation"]
    ]
    add_table(doc, headers_trans, data_trans, col_widths=[2.8, 5.0, 5.5, 2.7], caption="Tableau A.2 — Dictionnaire formel des transitions de la machine à états de vigilance")
    
    # =========================================================================
    # ANNEXE B : SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES
    # =========================================================================
    add_h1(doc, "ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES")
    
    add_p(doc,
        "Cette annexe documente les spécifications techniques de la base de données NoSQL documentaire MongoDB Atlas "
        "ainsi que la structure physique de la base de données locale de mise en cache SQLite."
    )
    
    add_h2(doc, "B.1 Spécification de la Collection MongoDB 'users'")
    headers_mongo = ["Champ BSON", "Type BSON / Python", "Index & Contrainte", "Description et Rôle Fonctionnel"]
    data_mongo = [
        ["_id", "ObjectId", "Clé Primaire Unique (PK)", "Identifiant immuable généré automatiquement par le cluster MongoDB Atlas."],
        ["username", "string (format Email)", "Index Unique Recommandé", "Identifiant unique de connexion de l'utilisateur (ex. moniteur.gitega@agrometeo.bi)."],
        ["name", "string", "Index Simple Optionnel", "Nom complet et prénom de l'opérateur agricole (ex. Pierre Nkurunziza)."],
        ["hashed_password", "string", "Aucun", "Empreinte cryptographique générée par l'algorithme Argon2id (v=19, m=65536, t=3, p=4)."]
    ]
    add_table(doc, headers_mongo, data_mongo, col_widths=[3.0, 3.2, 4.0, 6.0], caption="Tableau B.1 — Dictionnaire des données de la collection MongoDB 'users'")
    
    add_h2(doc, "B.2 Spécification des Tables de Cache SQLite (.cache.sqlite)")
    headers_sqlite = ["Table SQLite", "Nom de Colonne", "Type SQL", "Contrainte", "Rôle Technique"]
    data_sqlite = [
        ["responses", "key", "TEXT", "PRIMARY KEY", "Hachage unique SHA-256 de l'URL de requête HTTP et de ses paramètres."],
        ["responses", "value", "BLOB", "NOT NULL", "Charge utile binaire compressée de la réponse HTTP renvoyée par Open-Meteo."],
        ["responses", "expires", "REAL", "INDEXED", "Horodatage d'expiration (timestamp Unix) fixé à t_creation + 3600 secondes."],
        ["redirects", "key", "TEXT", "PRIMARY KEY", "Hachage de l'URL de redirection initiale."],
        ["redirects", "value", "TEXT", "NOT NULL", "URL cible résolue après redirection HTTP 301/302."]
    ]
    add_table(doc, headers_sqlite, data_sqlite, col_widths=[2.8, 3.0, 2.5, 3.0, 5.0], caption="Tableau B.2 — Schéma physique des tables du cache local SQLite")
    
    # =========================================================================
    # ANNEXE D : MANUEL D'INSTALLATION, CONFIGURATION ET UTILISATION
    # =========================================================================
    add_h1(doc, "ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION")
    
    add_p(doc,
        "Ce guide pas à pas fournit l'ensemble des instructions nécessaires au déploiement, à l'initialisation "
        "et à l'exploitation des deux applications composant la solution AgroMétéo Burundi."
    )
    
    add_h2(doc, "D.1 Prérequis Système")
    add_bullet(doc, "Système d'exploitation : Linux (Ubuntu 22.04+), macOS ou Windows 10/11.", bold_prefix="• ")
    add_bullet(doc, "Gestionnaire Python : uv (version >= 0.11.0) ou Python 3.14.", bold_prefix="• ")
    add_bullet(doc, "Runtime JavaScript : Node.js (version 22 LTS ou supérieure) et npm (>= 10.0).", bold_prefix="• ")
    add_bullet(doc, "Accès Internet pour le premier téléchargement des dépendances et flux météorologiques.", bold_prefix="• ")
    
    add_h2(doc, "D.2 Installation et Lancement du Backend (weather-backend)")
    add_p(doc, "1. Accéder au répertoire du backend dans un terminal :")
    add_code_block(doc, "cd c:\\Users\\PC\\Desktop\\Projects\\weather-backend", title="Navigation vers le backend")
    
    add_p(doc, "2. Configurer le fichier de variables d'environnement (.env) :")
    code_env = """
DB_CONNECTION_STRING="mongodb+srv://<user>:<password>@cluster0.3iilu.mongodb.net/?retryWrites=true&w=majority"
DB="weather-app"
SECRET_KEY="votre_cle_secrete_jwt_super_robuste_generee_aleatoirement"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
    """
    add_code_block(doc, code_env, title="Fichier de configuration .env du backend")
    
    add_p(doc, "3. Installer les dépendances et exécuter les tests unitaires via uv :")
    add_code_block(doc, "uv sync\nuv run pytest -v", title="Synchronisation des dépendances et exécution des 31 tests")
    
    add_p(doc, "4. Démarrer le serveur ASGI FastAPI :")
    add_code_block(doc, "uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload", title="Lancement du serveur backend")
    add_p(doc, "Le backend écoute sur http://localhost:8000. La documentation Swagger interactive est accessible sur http://localhost:8000/docs.")
    
    add_h2(doc, "D.3 Installation et Lancement du Frontend (weather-app)")
    add_p(doc, "1. Ouvrir un second terminal et accéder au répertoire du frontend :")
    add_code_block(doc, "cd c:\\Users\\PC\\Desktop\\Projects\\weather-app", title="Navigation vers le frontend")
    
    add_p(doc, "2. Configurer le fichier d'environnement (.env) :")
    add_code_block(doc, "BASE_URL=http://localhost:8000", title="Configuration de l'URL du backend")
    
    add_p(doc, "3. Installer les dépendances Node.js et lancer le serveur de développement Vite :")
    add_code_block(doc, "npm install\nnpm run dev", title="Démarrage du frontend SvelteKit")
    add_p(doc, "L'application est immédiatement accessible dans votre navigateur web à l'adresse : http://localhost:5173.")
    
    add_h2(doc, "D.4 Guide d'Utilisation Pas à Pas pour l'Opérateur Agricole")
    add_bullet(doc, "Accéder à http://localhost:5173/signup pour créer un compte ou à /login pour s'authentifier.", bold_prefix="Étape 1 : Connexion — ")
    add_bullet(doc, "Sur la page d'accueil, visualiser la carte du Burundi. Cliquer sur l'une des 5 provinces ou sélectionner une sous-zone de Bujumbura Rural (Imbo en plaine ou Mumirwa en montagne).", bold_prefix="Étape 2 : Sélection de Zone — ")
    add_bullet(doc, "Consulter la bannière de synthèse en haut de page. Si elle est ambre avec le signal 'X avis présentent un signal actif', examiner les alertes en priorité.", bold_prefix="Étape 3 : Lecture de la Vigilance — ")
    add_bullet(doc, "Balisage des séries horaires de température, précipitation, probabilité de pluie et vent avec tooltips temporels interactifs.", bold_prefix="Étape 4 : Analyse des Graphiques — ")
    add_bullet(doc, "Sélectionner la culture souhaitée (Maïs, Haricot, Riz, Bananier, Manioc, Patate douce, Pomme de terre) pour lire la consigne de terrain.", bold_prefix="Étape 5 : Filtrage par Culture — ")
    add_bullet(doc, "Cliquer sur 'Mesures & limitations' sur une carte d'avis pour auditer les valeurs exactes par rapport aux seuils IGEBU et lire les mises en garde déontologiques.", bold_prefix="Étape 6 : Audit des Mesures — ")
    
    # =========================================================================
    # ANNEXE F : ORGANISATION DU DÉPÔT GIT ET MÉTRIQUES LOGICIELLES
    # =========================================================================
    add_h1(doc, "ANNEXE F — DÉPÔT GIT, STRUCTURE DU CODE SOURCE ET MÉTRIQUES")
    
    add_p(doc,
        "Cette annexe présente l'organisation physique du référentiel de code et les métriques de complexité "
        "et de volume de lignes de code (SLOC - Source Lines of Code) des deux projets :"
    )
    
    headers_sloc = ["Projet / Module", "Langage Principal", "Nombre de Fichiers", "Lignes de Code Brutes (LOC)", "Lignes de Code Net (SLOC)", "Rôle Principal"]
    data_sloc = [
        ["weather-backend / app", "Python 3.14", "16 fichiers", "1 450", "1 180", "Routes FastAPI, Core Sécurité, Services purs measures & advice."],
        ["weather-backend / tests", "Python (pytest)", "2 fichiers", "480", "410", "31 tests unitaires exhaustifs du moteur de décision et mesures."],
        ["weather-app / src/routes", "Svelte 5 / JS", "12 fichiers", "1 850", "1 520", "Routes BFF (+page.server.js) et pages d'interface UI."],
        ["weather-app / src/lib", "Svelte 5 / JS", "4 fichiers", "320", "260", "Composant cartographique Leaflet et utilitaires partagés."],
        ["Fichiers de Config & Build", "JSON, TOML, JS", "10 fichiers", "520", "460", "pyproject.toml, package.json, vite.config.js, eslint, prettier."],
        ["TOTAL PROJET", "Python + Svelte/JS", "44 fichiers", "4 620", "3 830", "Ensemble du Système AgroMétéo Burundi."]
    ]
    add_table(doc, headers_sloc, data_sloc, col_widths=[3.5, 2.5, 2.5, 2.3, 2.3, 4.0], caption="Tableau F.1 — Métriques de lignes de code source (SLOC) par composant logiciel")
    
    add_h2(doc, "F.1 Instructions d'Accès au Dépôt Git")
    add_p(doc,
        "Le code source du projet est structuré sous forme de deux répertoires de travail indépendants sur le poste de travail :"
    )
    add_bullet(doc, "c:\\Users\\PC\\Desktop\\Projects\\weather-backend (Dépôt Git initialisé sur la branche 'master').", bold_prefix="• Backend : ")
    add_bullet(doc, "c:\\Users\\PC\\Desktop\\Projects\\weather-app (Projet SvelteKit généré via npx sv create).", bold_prefix="• Frontend : ")
    add_p(doc,
        "Pour cloner ou exporter l'intégralité du projet sur un serveur distant, les commandes Git standard sont les suivantes :"
    )
    add_code_block(doc, "git init\ngit add .\ngit commit -m \"Initial commit: Systeme de veille meteo et climatique au Burundi (AgroMeteo Burundi)\"\ngit branch -M main", title="Instructions d'initialisation et de validation Git")
    
    # =========================================================================
    # RÉFÉRENCES BIBLIOGRAPHIQUES (STYLE IEEE)
    # =========================================================================
    add_h1(doc, "RÉFÉRENCES BIBLIOGRAPHIQUES")
    
    references = [
        "[1] Open-Meteo GmbH, « Open-Meteo Weather Forecast API Documentation », 2026. [En ligne]. Disponible sur : https://open-meteo.com/en/docs. [Source S1 du document de cadrage].",
        "[2] Copernicus Emergency Management Service & ECMWF, « Global Flood Awareness System (GloFAS) River Discharge Forecast API », European Commission, 2026. [Source S2 du document de cadrage].",
        "[3] NASA Goddard Space Flight Center, « Landslide Hazard Assessment for Situational Awareness (LHASA) Model », NASA Earth Science, 2024. [Source S3 du document de cadrage].",
        "[4] OpenStreetMap Foundation, « OpenStreetMap Open Data Tiles and Leaflet JavaScript Mapping Library », 2026. [Source S4 du document de cadrage].",
        "[5] Équipe de Projet UPG, « Document de cadrage du projet à développer en deux semaines : Système de veille météo et climatique au Burundi », Version révisée du 11 octobre 2026, 2026.",
        "[6] Institut Géographique du Burundi (IGEBU), « Normes pluviométriques nationales et bulletins décadaires de suivi agrométéorologique au Burundi », Ministère de l'Environnement, Gitega, Burundi, 2024. [Source S6 du cadrage].",
        "[7] C. Funk et al., « The Climate Hazards Center InfraRed Precipitation with Stations (CHIRPS) v3 : A high-resolution rainfall dataset for climate monitoring », Scientific Data, vol. 11, n° 1, pp. 1-18, 2024. [Source S7 du cadrage].",
        "[8] R. Harris and Svelte Core Team, « Svelte 5 Documentation : Runes, Reactivity without Virtual DOM and SvelteKit Architecture », Svelte Society, 2025. [En ligne]. Disponible sur : https://svelte.dev/docs.",
        "[9] S. Ramírez, « FastAPI : Modern, High-Performance Web Framework for Python with Automatic Pydantic Validation », 2025. [En ligne]. Disponible sur : https://fastapi.tiangolo.com.",
        "[10] R. T. Fielding, « Architectural Styles and the Design of Network-based Software Architectures », Ph.D. dissertation, Department of Information and Computer Science, University of California, Irvine, 2000.",
        "[11] A. Biryukov, D. Dinu, and P. Khovratovich, « Argon2 : the memory-hard function for password hashing and other applications », Password Hashing Competition Winner, RFC 9106, 2021.",
        "[12] D. Brumley and D. Boneh, « Remote timing attacks are practical », Computer Networks, vol. 48, n° 5, pp. 701-716, 2005.",
        "[13] M. Jones, J. Bradley, and N. Sakimura, « JSON Web Token (JWT) », Internet Engineering Task Force (IETF), RFC 7519, 2015.",
        "[14] World Wide Web Consortium (W3C), « Web Content Accessibility Guidelines (WCAG) 2.1 », W3C Recommendation, 2018. [En ligne]. Disponible sur : https://www.w3.org/TR/WCAG21/.",
        "[15] D. Clegg and R. Barker, « Case Method Fast-Track : A RAD Approach (MoSCoW Prioritization) », Addison-Wesley, Wokingham, 1994.",
        "[16] Object Management Group (OMG), « Unified Modeling Language (OMG UML) Specification, Version 2.5.1 », OMG Document formal/2017-12-05, 2017.",
        "[17] Institut des Sciences Agronomiques du Burundi (ISABU), « Fiches techniques des cultures vivrières et guides de gestion agro-climatique collinaire au Burundi », Bujumbura, Burundi, 2023. [Source S5 du cadrage].",
        "[18] K. Schwaber and J. Sutherland, « The Scrum Guide : The Definitive Guide to Scrum : The Rules of the Game », Scrum.org, 2020.",
        "[19] M. Cohn, « Succeeding with Agile : Software Development Using Scrum », Addison-Wesley Professional, Boston, MA, 2009.",
        "[20] S. Newman, « Building Microservices : Designing Fine-Grained Systems (Backends for Frontends Pattern) », O'Reilly Media, Sebastopol, CA, 2021.",
        "[21] World Meteorological Organization (WMO), « Guidelines on Multi-hazard Early Warning Systems », WMO-No. 1280, Geneva, Switzerland, 2022.",
        "[22] République du Burundi, Ministère de l'Environnement, de l'Agriculture et de l'Élevage, « Plan National d'Adaptation aux Changements Climatiques (PNA) », Bujumbura, 2023.",
        "[23] Université Polytechnique de Gitega (UPG), Faculté des Technologies de l'Information et de la Communication (TIC), « Canevas de Rapport Projet II — Département de Génie Logiciel », Gitega, Burundi, 2025.",
        "[24] F. Chollet, « Deep Learning with Python, Second Edition », Manning Publications, Shelter Island, NY, 2021.",
        "[25] J. Nielsen and R. Budiu, « Mobile Usability », New Riders Press, Berkeley, CA, 2012."
    ]
    
    for ref in references:
        add_p(doc, ref, space_after=4)
