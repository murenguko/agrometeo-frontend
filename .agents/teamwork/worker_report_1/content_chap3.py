"""
content_chap3.py - Rédaction du Chapitre III : Conception de la Solution Cible
Conforme aux exigences UPG et intégrant la modélisation UML complète, les exigences EF/ENF et le moteur de règles.
"""

from builder import add_h1, add_h2, add_h3, add_p, add_bullet, add_table, add_figure, add_callout, add_code_block

def build_chap3(doc):
    """Génère le Chapitre III complet : Conception de la Solution Cible."""
    add_h1(doc, "CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE")
    
    # --- 1. Exigences fonctionnelles détaillées ---
    add_h2(doc, "1. Spécification des Exigences Fonctionnelles (EF-01 à EF-20)")
    
    add_p(doc,
        "La phase de conception débute par la formalisation rigoureuse des besoins en spécifications fonctionnelles "
        "numérotées et hiérarchisées selon la méthode de priorisation MoSCoW (Must have, Should have, Could have, Won't have) [15]. "
        "Chaque exigence est confrontée à son statut d'implémentation effectif dans la base de code :"
    )
    
    headers_ef = ["Code EF", "Intitulé de l'Exigence", "Description Fonctionnelle Détaillée", "Priorité MoSCoW", "Statut dans l'Implémentation"]
    data_ef = [
        ["EF-01", "Inscription Utilisateur", "Permettre la création d'un compte avec nom, email unique et mot de passe sécurisé haché en base.", "Must have", "Implémenté (POST /user, Argon2id)"],
        ["EF-02", "Authentification OAuth2 / JWT", "Authentifier l'utilisateur via mot de passe et délivrer un jeton Bearer JWT valide 30 minutes.", "Must have", "Implémenté (POST /token, pyjwt HS256)"],
        ["EF-03", "Protection des Routes Météo", "Interdire formellement l'accès aux données météo sans jeton JWT valide (HTTP 401).", "Must have", "Implémenté (Depends get_current_user)"],
        ["EF-04", "Visualisation Cartographique", "Afficher une carte Leaflet interactive tuilée OSM centrée sur le Burundi avec les stations géolocalisées.", "Must have", "Implémenté (Leaflet.svelte / Sveaflet)"],
        ["EF-05", "Sélection Territoriale", "Permettre la sélection d'une province via clic sur marqueur cartographique ou panneau latéral.", "Must have", "Implémenté (Routes dynamiques /region/[slug])"],
        ["EF-06", "Scission Topographique Buja Rural", "Subdiviser Bujumbura Rural en sous-zone de plaine (Imbo) et de montagne (Mumirwa).", "Must have", "Implémenté (app/config.py, sous-menus UI)"],
        ["EF-07", "Collecte Météo Horaires 7j", "Ingérer automatiquement les prévisions de T°, pluie, vent et probabilité sur 7 jours via Open-Meteo.", "Must have", "Implémenté (Client Open-Meteo binaire)"],
        ["EF-08", "Ingestion Historique Passé 7j", "Récupérer les estimations des 7 derniers jours écoulés pour évaluer la saturation hydrique préalable.", "Must have", "Implémenté (past_days=7, measures.py)"],
        ["EF-09", "Surveillance Hydrologique GloFAS", "Interroger les débits prévus à 7 jours sur la maille hydrographique Copernicus associée à la zone.", "Must have", "Implémenté (flood-api.open-meteo.com)"],
        ["EF-10", "Calcul Seuil Anormal p75", "Calculer le 75e percentile des débits des 31 derniers jours pour déterminer un seuil d'anomalie dynamique.", "Should have", "Implémenté (get_flood_past_data)"],
        ["EF-11", "Alerte Pluie Critique 24h", "Déclencher un conseil d'action si la pluie 24h franchit 50 mm (plaine) ou 100 mm (montagne).", "Must have", "Implémenté (Seuils IGEBU, advice.py)"],
        ["EF-12", "Alerte Pluie Prolongée 72h", "Déclencher un conseil d'engorgement des sols si la pluie 72h franchit 60 mm (plaine) ou 90 mm (montagne).", "Must have", "Implémenté (Seuils IGEBU, advice.py)"],
        ["EF-13", "Alerte Sols Saturés 7j Passés", "Déclencher une alerte pour tubercules et haricot si les 7 jours passés cumulent ≥ 50 mm de pluie.", "Should have", "Implémenté (Règle humidité des sols)"],
        ["EF-14", "Alerte Vent Violent & Rafales", "Alerter les producteurs de bananes et de maïs dès que les rafales prévues atteignent ≥ 40 km/h.", "Must have", "Implémenté (advice.py, seuil 40 km/h)"],
        ["EF-15", "Alerte Crue Rizicole", "Générer un conseil d'inspection des diguettes rizicoles si le débit prévu dépasse le percentile p75.", "Must have", "Implémenté (advice.py, focus riz bas-fond)"],
        ["EF-16", "Détection Période Sèche", "Identifier les séquences sèches critiques d'au moins 5 jours consécutifs avec pluie < 2 mm.", "Should have", "Implémenté (advice.py, règle sécheresse)"],
        ["EF-17", "Cultures Prévalentes Régionales", "Filtrer dynamiquement les avis selon la matrice agro-écologique ISABU propre à la province.", "Must have", "Implémenté (CULTURES_PAR_ZONE dans backend)"],
        ["EF-18", "Traçabilité des Mesures & Seuils", "Afficher dans une modale la valeur exacte, le seuil comparatif, la source et les limitations du modèle.", "Must have", "Implémenté (Modale Mesures & Limitations)"],
        ["EF-19", "Modèle Glissements NASA LHASA", "Croiser la carte de susceptibilité globale aux glissements avec les précipitations satellitaires.", "Could have", "Retiré du périmètre (Justifié au Chapitre V)"],
        ["EF-20", "Précipitations Historiques CHIRPS", "Intégrer les séries longues CHIRPS v3 pour le calcul des déciles historiques centennaux.", "Could have", "Remplacé (Réanalyses Open-Meteo past_days=7)"]
    ]
    add_table(doc, headers_ef, data_ef, col_widths=[1.8, 3.2, 5.7, 2.5, 3.8], caption="Tableau 3.1 — Spécification formelle des exigences fonctionnelles (EF-01 à EF-20)")
    
    # --- 2. Exigences non fonctionnelles détaillées ---
    add_h2(doc, "2. Spécification des Exigences Non-Fonctionnelles (ENF-01 à ENF-10)")
    
    add_p(doc,
        "Les exigences non fonctionnelles établissent les critères qualitatifs de performance, robustesse, sécurité "
        "et ergonomie indispensables à l'acceptabilité opérationnelle du système :"
    )
    
    headers_enf = ["Code ENF", "Dimension Qualité", "Exigence Formelle et Spécification", "Critère d'Acceptation & Métrique Mesurable"]
    data_enf = [
        ["ENF-01", "Performance & Latence", "Temps de réponse minimal lors des requêtes d'affichage d'un bulletin météorologique.", "Temps de réponse API < 50 ms lorsque la zone est en cache SQLite ; < 1,5 s en rafraîchissement externe."],
        ["ENF-02", "Disponibilité & Cache", "Capacité à servir les données météorologiques même lors d'une interruption transitoire du réseau.", "Mise en cache HTTP locale SQLite de 3 600 s (1 heure) ; 5 relances automatiques avec backoff exponentiel."],
        ["ENF-03", "Résistance Cryptographique", "Protection maximale des mots de passe utilisateurs contre les attaques par force brute distribuée.", "Algorithme Argon2id (m=65536 Ko, t=3, p=4) avec coût mémoire incompressible de 64 Mo par hash."],
        ["ENF-04", "Sécurité Anti-Timing", "Impossibilité de déduire l'existence d'une adresse email par chronométrage réseau lors de la connexion.", "Égalisation du temps de calcul serveur par exécution d'un DUMMY_HASH en cas d'identifiant introuvable."],
        ["ENF-05", "Intégrité Mathématique", "Interdiction stricte d'interpoler des valeurs ou de masquer des séries temporelles incomplètes.", "Toute lacune ou valeur NaN produit la valeur None et positionne immédiatement le statut 'non_evalue'."],
        ["ENF-06", "Déontologie Institutionnelle", "Respect absolu du monopole régalien des autorités de sécurité civile du Burundi.", "Bannissement total des expressions 'inondation certaine' et 'évacuation' dans l'ensemble des modules d'avis."],
        ["ENF-07", "Compacité & Bas Débit", "Optimisation du volume de données transféré pour s'adapter aux réseaux 3G ruraux limités.", "Poids total du bundle JavaScript client initial généré par Vite < 250 Ko (gzippé < 100 Ko)."],
        ["ENF-08", "Accessibilité Numérique", "Lisibilité et manipulabilité aisée en plein soleil sur le terrain par des moniteurs agricoles.", "Conformité WCAG 2.1 AA : contraste textuel > 7:1 sur fond sombre, cibles tactiles minimales de 44 × 44 px."],
        ["ENF-09", "Testabilité Unitaire Pure", "Découplage absolu entre la logique de décision agricole et les infrastructures d'E/S réseau.", "100% des fonctions des modules measures.py et advice.py testables unitairement sans mock réseau complexe."],
        ["ENF-10", "Conformité aux Standards", "Respect rigoureux des standards ouverts du web et du génie logiciel contemporain.", "Spécification OpenAPI 3.0 auto-générée, validation Pydantic stricte, conformité ECMAScript / ESLint 10."]
    ]
    add_table(doc, headers_enf, data_enf, col_widths=[2.0, 3.2, 6.0, 5.8], caption="Tableau 3.2 — Spécification formelle des exigences non fonctionnelles (ENF-01 à ENF-10)")
    
    # --- 3. Architecture applicative globale ---
    add_h2(doc, "3. Architecture Applicative Globale et Séparation BFF")
    
    add_p(doc,
        "La solution cible est organisée selon une architecture en couches découpée en trois tiers fonctionnels distincts, "
        "articulée autour du patron Backend-For-Frontend (BFF) :"
    )
    
    figure_3_1 = """
                     ARCHITECTURE EN COUCHES ET FLUX DE DONNÉES APPLICATIFS
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ COUCHE PRÉSENTATION & CLIENT WEB (Svelte 5 / Runes)                         │
  │ • Navigation & Layout (+layout.svelte)      • Formulaires (/login, /signup) │
  │ • Hub Cartographique Leaflet.svelte         • Dashboard /region/[slug]      │
  │ • Visualisation SVG svelteplot              • Modale Mesures & Limitations  │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ Requêtes HTTP internes + Cookie HttpOnly JWT
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ COUCHE BACKEND-FOR-FRONTEND (SvelteKit Server Runtime)                      │
  │ • Garde de navigation serveur (+layout.server.js)                           │
  │ • Actions de connexion/déconnexion (/login, /signup, +page.server.js)       │
  │ • Chargement serveur des bulletins régionaux (/region/[slug]/+page.server.js)│
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ Protocole REST API (Header: Bearer <JWT>)
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ COUCHE LOGIQUE MÉTIER & SERVICES (FastAPI / Python 3.14)                    │
  │ • Contrôleurs d'API (routes/weather.py, routes/token.py, routes/user.py)    │
  │ • Sécurité & Chiffrement (core/security.py : Argon2id, HS256, DUMMY_HASH)   │
  │ • Moteur d'Agrégation Temporelle (services/measures.py)                    │
  │ • Moteur de Règles Décisionnelles Agricoles (services/advice.py)             │
  │ • Connecteur & Cache HTTP Résilient (services/weather.py)                   │
  └───────────────────┬─────────────────────────────────────┬───────────────────┘
                      │                                     │
                      ▼                                     ▼
  ┌───────────────────────────────────────┐ ┌───────────────────────────────────┐
  │ PERSISTANCE INTERNE                   │ │ FLUX EXTERNES MÉTÉO & CRUES       │
  │ • MongoDB Atlas (Collection 'users')  │ │ • Open-Meteo Weather API          │
  │ • Cache SQLite local (.cache.sqlite)  │ │ • GloFAS Open-Meteo Flood API     │
  └───────────────────────────────────────┘ └───────────────────────────────────┘
    """
    add_figure(doc, figure_3_1, caption="Figure 3.1 — Architecture logicielle globale en couches et interconnexions de données")
    
    # --- 4. Modélisation UML complète ---
    add_h2(doc, "4. Modélisation UML Complète du Système")
    
    add_p(doc,
        "La modélisation de la solution cible est formalisée conformément aux standards de l'Unified Modeling Language (UML 2.5) [16]. "
        "Elle couvre les vues fonctionnelle, statique, dynamique et d'implémentation physique."
    )
    
    add_h3(doc, "4.1 Diagramme de Cas d'Utilisation (Use Case Diagram)")
    add_p(doc,
        "Le diagramme de cas d'utilisation capture les interactions entre les acteurs externes (l'Encadreur Agricole / Moniteur DPAE, "
        "le Gestionnaire de Coopérative, et le Système Météorologique Tiers) et les fonctionnalités du système :"
    )
    
    figure_3_2 = """
                       DIAGRAMME DE CAS D'UTILISATION (UML)
                                  ┌───────────────────────────────────────────────┐
                                  │            AGROMÉTÉO BURUNDI                  │
                                  │                                               │
                                  │   ( S'inscrire sur la plateforme )            │
                                  │                 ▲                             │
                                  │                 │ <<include>>                 │
    웃                            │   ( S'authentifier via OAuth2 / JWT )         │
  Utilisateur Agricole /          │                 ▲                             │
  Moniteur DPAE                   │                 │ <<extend>>                  │
    │                             │   ( Consulter la carte interactive du Burundi)│
    ├───(Consulter Carte)─────────┤                 │                             │
    │                             │   ( Sélectionner une province pilote )        │
    ├───(Sélectionner Région)─────┤                 │                             │
    │                             │   ( Choisir sous-zone Imbo ou Mumirwa )       │
    ├───(Visualiser Météo)────────┤                 │                             │
    │                             │   ( Consulter les courbes météo svelteplot )  │
    ├───(Lire Avis ISABU)─────────┤                 │                             │
    │                             │   ( Filtrer les conseils par culture vivrière)│
    └───(Inspecter Mesures)───────┤                 │                             │
                                  │   ( Auditer les mesures et limitations modale)│
                                  │                 │                             │
                                  │   ( Se déconnecter )                          │
                                  │                                               │
    웃                            │   ( Interroger les prévisions Open-Meteo )    │
  Fournisseur Météo Externe ──────┼─────────────────┼─────────────────────────────┤
  (Open-Meteo / GloFAS)           │   ( Collecter les débits fluviaux GloFAS )    │
                                  └───────────────────────────────────────────────┘
    """
    add_figure(doc, figure_3_2, caption="Figure 3.2 — Diagramme de cas d'utilisation du système AgroMétéo Burundi")
    
    add_h3(doc, "4.2 Diagramme de Classes Métier (Class Diagram)")
    add_p(doc,
        "Le diagramme de classes illustre les structures de données, les schémas de transfert Pydantic et la séparation "
        "entre les modèles de persistance et les composants de logique pure :"
    )
    
    figure_3_3 = """
                        DIAGRAMME DE CLASSES MÉTIER (UML)
  ┌─────────────────────────┐               ┌─────────────────────────────────┐
  │       <<Schema>>        │               │           <<Service>>           │
  │          User           │               │          SecurityManager        │
  ├─────────────────────────┤               ├─────────────────────────────────┤
  │ + username: str (Email) │               │ - secret_key: str               │
  │ + name: str             │               │ - algorithm: str = "HS256"      │
  └─────────────────────────┘               ├─────────────────────────────────┤
               ▲                            │ + verify_password(...) : bool   │
               │ hérite                     │ + get_password_hash(...) : str  │
  ┌─────────────────────────┐               │ + authenticate_user(...) : User │
  │       <<Document>>      │               │ + create_access_token(...) : str│
  │        UserInDB         │               │ + get_current_user(...) : User  │
  ├─────────────────────────┤               └─────────────────────────────────┘
  │ + hashed_password: str  │
  └─────────────────────────┘
               ▲
               │ persiste dans
  ┌─────────────────────────┐               ┌─────────────────────────────────┐
  │       <<Database>>      │               │           <<Service>>           │
  │     MongoDB 'users'     │               │          MeasuresEngine         │
  └─────────────────────────┘               ├─────────────────────────────────┤
                                            │ + extraire_mesures(...) : dict  │
  ┌─────────────────────────┐               │ - _fenetre_complete(...) : bool │
  │       <<Service>>       │               │ - _somme_pluie(...) : float     │
  │       AdviceEngine      │               │ - _max_rafales(...) : float     │
  ├─────────────────────────┤               └─────────────────────────────────┘
  │ + seuils: Seuils        │                                ▲
  ├─────────────────────────┤                                │ transmet dict mesures
  │ + generer_conseil(...)  │                                │
  │ + generer_conseils(...) │─────────────── évalue ─────────┘
  └─────────────────────────┘
               │ génère
               ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │                               <<DataStructure>>                           │
  │                                ConseilAgricole                            │
  ├───────────────────────────────────────────────────────────────────────────┤
  │ + culture: str                   + statut: StatutConseil ("actif", etc.)  │
  │ + zone: str                      + sous_zone: Optional[str]               │
  │ + date_evaluation: str (ISO)     + validite: str ("24h", "72h", "7j")     │
  │ + message: str (Action terrain)  + regles_declenchees: List[str]          │
  │ + mesures_utilisees: dict        + limitations: List[str]                 │
  └───────────────────────────────────────────────────────────────────────────┘
    """
    add_figure(doc, figure_3_3, caption="Figure 3.3 — Diagramme de classes métier du backend AgroMétéo Burundi")
    
    headers_classes = ["Entité / Classe", "Couche Logicielle", "Responsabilité & Fonctions Principales", "Attributs Majeurs"]
    data_classes = [
        ["User & UserInDB", "Schemas (app/schemas/user.py)", "Représentation typée du profil utilisateur et encapsulation du mot de passe haché.", "username (email), name, hashed_password (Argon2id)"],
        ["SecurityManager", "Core (app/core/security.py)", "Hachage, vérification anti-timing, émission et validation des jetons d'accès JWT.", "SECRET_KEY, ALGORITHM (HS256), ACCESS_TOKEN_EXPIRE_MINUTES (30)"],
        ["MeasuresEngine", "Service (app/services/measures.py)", "Alignement temporel sur t0, extraction vectorielle des cumuls 24h/72h/7j et rafales.", "extraire_mesures(), _somme_pluie(), _fenetre_complete()"],
        ["AdviceEngine", "Service (app/services/advice.py)", "Évaluation fonctionnelle pure des seuils IGEBU et règles ISABU par culture vivrière.", "generer_conseil(), generer_conseils(), CULTURES_PAR_ZONE"],
        ["ConseilAgricole", "Structure Domaine", "Encapsulation complète de la directive d'action agricole et des métadonnées de traçabilité.", "culture, zone, statut, validite, message, limitations"]
    ]
    add_table(doc, headers_classes, data_classes, col_widths=[3.0, 3.5, 6.0, 4.5], caption="Tableau 3.3 — Description des classes et modules logiciels métier")
    
    add_h3(doc, "4.3 Diagramme de Composants (Component Diagram)")
    add_p(doc,
        "Le diagramme de composants matérialise les frontières physiques et modulaires entre les packages logiciels :"
    )
    
    figure_3_4 = """
                     DIAGRAMME DE COMPOSANTS LOGICIELS (UML)
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ <<Frontend Component>> : SvelteKit Client (Navigateur Web)                  │
  │  [ Leaflet.svelte (Sveaflet 0.1.5) ]   [ SveltePlot (Graphiques SVG) ]       │
  │  [ Dashboard (+page.svelte) ]          [ Modale Mesures & Limitations ]     │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ JSON / HTML SSR (Port 5173 / 3000)
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ <<BFF Component>> : SvelteKit Server Runtime (+page.server.js)              │
  │  [ Auth Guard (+layout.server.js) ]    [ Session Cookie Manager (HttpOnly) ]│
  │  [ Data Fetcher (region/[slug]) ]      [ Form Action Handlers ]             │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ REST API / Bearer Token (Port 8000)
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ <<Backend Component>> : FastAPI Application Core                            │
  │  [ Router: weather.py ]   [ Router: token.py ]   [ Router: user.py ]         │
  │  [ Core: security.py ]    [ Core: db.py ]        [ Config: config.py ]       │
  │  [ Service: measures.py ] [ Service: advice.py ] [ Service: weather.py ]     │
  └───────────────────┬─────────────────────────────────────┬───────────────────┘
                      │ Driver PyMongo                      │ Client FlatBuffers
                      ▼                                     ▼
  ┌───────────────────────────────────────┐ ┌───────────────────────────────────┐
  │ <<Data Storage>>                      │ │ <<External Web Services>>         │
  │ [ MongoDB Atlas Cloud ('users') ]     │ │ [ Open-Meteo Weather Forecast ]   │
  │ [ SQLite Local Cache (.cache.sqlite) ]│ │ [ GloFAS Flood API (Copernicus) ] │
  └───────────────────────────────────────┘ └───────────────────────────────────┘
    """
    add_figure(doc, figure_3_4, caption="Figure 3.4 — Diagramme de composants logiciels du système")
    
    add_h3(doc, "4.4 Diagrammes de Séquence (Sequence Diagrams)")
    add_p(doc,
        "Les diagrammes de séquence détaillent la chronologie des messages échangés lors des deux cas d'usage majeurs du système."
    )
    
    add_h3(doc, "Séquence 1 : Authentification Sécurisée et Émission du Cookie de Session")
    figure_3_5 = """
                 DIAGRAMME DE SÉQUENCE : AUTHENTIFICATION UTILISATEUR
  Utilisateur        Client SvelteKit         BFF Server             Backend FastAPI         MongoDB Atlas
      │                     │                     │                         │                      │
      ├── 1. POST /login ──>│                     │                         │                      │
      │   (username, pwd)   ├── 2. Form Submit ──>│                         │                      │
      │                     │   (action /login)   ├── 3. POST /token ──────>│                      │
      │                     │                     │   (x-www-form-urlencoded)│                      │
      │                     │                     │                         ├── 4. get_user() ────>│
      │                     │                     │                         │<── user document ────┤
      │                     │                     │                         │                      │
      │                     │                     │                         ├── 5. verify_password()
      │                     │                     │                         │   (ou DUMMY_HASH)    │
      │                     │                     │                         │                      │
      │                     │                     │                         ├── 6. encode JWT HS256│
      │                     │                     │<── 7. {access_token} ───┤   (expire 30 min)    │
      │                     │                     │                         │                      │
      │                     │                     ├── 8. cookies.set() ─────┤                      │
      │                     │                     │   (HttpOnly, Strict)    │                      │
      │                     │<── 9. Redirect 303 ─┤                         │                      │
      │<── 10. Affiche Home─┤    vers / d'accueil │                         │                      │
    """
    add_figure(doc, figure_3_5, caption="Figure 3.5 — Diagramme de séquence de l'authentification OAuth2 / JWT")
    
    add_h3(doc, "Séquence 2 : Consultation d'un Bulletin Régional et Évaluation du Moteur Pur")
    figure_3_6 = """
             DIAGRAMME DE SÉQUENCE : CONSULTATION MÉTÉO ET AVIS ISABU
  Utilisateur        Client SvelteKit         BFF Server             Backend FastAPI       Open-Meteo & GloFAS
      │                     │                     │                         │                      │
      ├── 1. Clic Région ──>│                     │                         │                      │
      │   (/region/gitega)  ├── 2. load() ───────>│                         │                      │
      │                     │   (Cookie inclus)   │                         │                      │
      │                     │                     ├── 3. GET /gitega ──────>│                      │
      │                     │                     │   (Bearer <JWT>)        ├── 4. Vérifie JWT     │
      │                     │                     │                         │                      │
      │                     │                     │                         ├── 5. Check Cache ────┐
      │                     │                     │                         │   .cache.sqlite      │
      │                     │                     │                         │<── HIT / MISS ───────┘
      │                     │                     │                         │                      │
      │                     │                     │                         ├── 6. (Si MISS) Fetch>│
      │                     │                     │                         │<── FlatBuffers Data ─┤
      │                     │                     │                         │                      │
      │                     │                     │                         ├── 7. extraire_mesures()
      │                     │                     │                         │   (measures.py)      │
      │                     │                     │                         ├── 8. generer_conseils()
      │                     │                     │                         │   (advice.py)        │
      │                     │                     │<── 9. JSON Unifié ──────┤                      │
      │                     │                     │    (Météo + Conseils)   │                      │
      │                     │<── 10. Rendu Page ──┤                         │                      │
      │<── 11. Affichage ───┤    (Leaflet, Plot,  │                         │                      │
      │    Courbes & Avis   │     Cartes Conseils)│                         │                      │
    """
    add_figure(doc, figure_3_6, caption="Figure 3.6 — Diagramme de séquence de la consultation d'un bulletin agro-météorologique")
    
    add_h3(doc, "4.5 Diagramme d'États-Transitions des Avis de Vigilance (State Machine Diagram)")
    add_p(doc,
        "Chaque conseil agro-climatique évolue selon une machine à états finis déterministe garantissant une intégrité "
        "déontologique absolue face aux imprévus de données :"
    )
    
    figure_3_7 = """
               DIAGRAMME D'ÉTATS-TRANSITIONS DES AVIS DE VIGILANCE
       ┌────────────────┐
       │   INITIAL      │
       └───────┬────────┘
               │ Réception des séries temporelles (Open-Meteo & GloFAS)
               ▼
       ┌────────────────────────────────────────────────────────┐
       │             ÉVALUATION DES DONNÉES ENTRANTES           │
       └───────┬────────────────────────────────────────┬───────┘
               │ Donnée indispensable manquante         │ Toutes données requises
               │ (NaN, None, série tronquée)            │ complètes et valides
               ▼                                        ▼
    ┌───────────────────────────┐            ┌────────────────────────────────────┐
    │     ÉTAT : NON_ÉVALUÉ     │            │    ÉVALUATION DES RÈGLES MÉTIER    │
    │ « Données indisponibles.  │            │ (Seuils IGEBU, Vent, Débit p75)    │
    │ L'absence de données n'est│            └──────────┬──────────────────┬──────┘
    │ pas une absence de danger»│                       │                  │
    └───────────────────────────┘       Au moins 1 seuil│                  │ Aucun seuil
                                        critique franchi│                  │ franchi
                                                        ▼                  ▼
                                            ┌───────────────────┐  ┌────────────────────┐
                                            │ÉTAT: CONSEIL_ACTIF│  │ÉTAT: SANS_SIGNAL   │
                                            │Bannière ambre     │  │Bannière verte      │
                                            │Directive d'action │  │Rappel probabiliste │
                                            │immédiate terrain  │  │Vérification locale │
                                            └───────────────────┘  └────────────────────┘
    """
    add_figure(doc, figure_3_7, caption="Figure 3.7 — Diagramme d'états-transitions du moteur de vigilance agricole")
    
    add_h3(doc, "4.6 Diagramme de Déploiement Physique (Deployment Diagram)")
    add_p(doc,
        "Le diagramme de déploiement spécifie l'allocation des artefacts logiciels sur les nœuds matériels d'exécution :"
    )
    
    figure_3_8 = """
                     DIAGRAMME DE DÉPLOIEMENT PHYSIQUE DU SYSTÈME
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ NŒUD CLIENT : Terminal Mobile / PC Agricole                                 │
  │ • Navigateur Web moderne (Chrome Mobile, Firefox, Safari)                   │
  │ • Exécution Client Svelte 5 (Runes, Sveaflet, SVG SveltePlot)               │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ HTTPS / TCP 443
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ NŒUD SERVEUR FRONTEND : Runtime Node.js 22                                  │
  │ • Serveur d'Application SvelteKit (Port 5173 / 3000)                        │
  │ • Adaptateur @sveltejs/adapter-auto                                         │
  │ • Gestionnaire de sessions cookies HttpOnly                                 │
  └──────────────────────────────────────┬──────────────────────────────────────┘
                                         │ HTTP / Réseau Privé Local (Port 8000)
                                         ▼
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ NŒUD SERVEUR BACKEND : Serveur d'Application Python 3.14                    │
  │ • Moteur ASGI Uvicorn (uvicorn app.main:app)                                │
  │ • Framework FastAPI v0.159.1                                                │
  │ • Cache HTTP local SQLite (.cache.sqlite) sur système de fichiers NVMe      │
  └───────────────────┬─────────────────────────────────────┬───────────────────┘
                      │ TLS / Port 27017                    │ HTTPS / Port 443
                      ▼                                     ▼
  ┌───────────────────────────────────────┐ ┌───────────────────────────────────┐
  │ CLOUD DATABASE : MongoDB Atlas M0     │ │ CLOUD APIS TIERS : Open-Meteo     │
  │ • Cluster cluster0.3iilu.mongodb.net  │ │ • api.open-meteo.com/v1/forecast  │
  │ • Base 'weather-app', Coll. 'users'   │ │ • flood-api.open-meteo.com/v1/flood│
  └───────────────────────────────────────┘ └───────────────────────────────────┘
    """
    add_figure(doc, figure_3_8, caption="Figure 3.8 — Diagramme de déploiement physique de l'architecture distribuée")
    
    # --- 5. Modélisation des données ---
    add_h2(doc, "5. Modélisation des Données et Schémas Physiques")
    
    add_p(doc,
        "La persistance des données au sein du système repose sur une stricte séparation entre les données d'identité "
        "et les séries temporelles transitoires :"
    )
    
    add_h3(doc, "5.1 Schéma de la Collection MongoDB 'users'")
    add_p(doc,
        "Les comptes utilisateurs sont stockés sous forme de documents BSON structurés dans la base 'weather-app' :"
    )
    
    code_schema_user = """
{
  "_id": ObjectId("672100000000000000000001"),
  "username": "moniteur.gitega@agrometeo.bi",
  "name": "Pierre Nkurunziza",
  "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$SD/Y0VojbYzgQOFpkuoOwg$5ZvE2F8bvlXvm4fC7QfwBSkKzA5TXBbR1X1ktwP45Yc"
}
    """
    add_code_block(doc, code_schema_user, title="Schéma documentaire BSON — Collection MongoDB 'users'")
    
    add_h3(doc, "5.2 Schéma de la Table de Cache SQLite (.cache.sqlite)")
    add_p(doc,
        "La bibliothèque `requests-cache` gère un fichier SQLite local `.cache.sqlite` contenant deux tables internes : "
        "`responses` (stockant la charge utile binaire compressée de la réponse HTTP, les en-têtes et la date d'expiration) "
        "et `redirects` (résolution des redirections d'URL). Le TTL configuré à 3 600 secondes garantit que toute requête "
        "identique émise au cours de l'heure est servie directement depuis le disque local en moins de 5 millisecondes."
    )
    
    # --- 6. Moteur de règles métier agro-climatiques ---
    add_h2(doc, "6. Moteur de Règles Métier et Formalisation Algorithmique")
    
    add_p(doc,
        "Le cœur décisionnel du projet est implanté de façon pure dans `app/services/measures.py` et `app/services/advice.py`. "
        "Il traduit avec rigueur les seuils de vigilance officiels de l'IGEBU [17] et les directives culturales de l'ISABU [18]."
    )
    
    add_h3(doc, "6.1 Formalisation Mathématique des Règles Métier")
    
    add_p(doc,
        "1. Règle de Pluie Critique sur 24 heures (Toutes cultures, avec conseil renforcé pour le Maïs) :\n"
        "Soit P_24h le cumul horaire des précipitations prévu sur l'intervalle temporel ouvert à gauche (t0, t0 + 24h] :\n"
        "P_24h = Somme de i=1 à 24 de p(t0 + i heures)\n"
        "La condition de déclenchement s'énonce :\n"
        "P_24h >= S_24h où S_24h = 50.0 mm si Zone = Plaine, et S_24h = 100.0 mm si Zone = Montagne.\n"
        "Directive pour le Maïs : « Si vous faites sécher du maïs en plein air, prévoyez de le mettre à l'abri ou de le couvrir avant les pluies annoncées. Vérifiez les fossés et les accès autour des aires de séchage. »"
    )
    
    add_p(doc,
        "2. Règle de Pluie Prolongée sur 72 heures (Haricot, Manioc, Patate douce, Pomme de terre) :\n"
        "Soit P_72h = Somme de i=1 à 72 de p(t0 + i heures).\n"
        "La condition de déclenchement s'énonce :\n"
        "P_72h >= S_72h où S_72h = 60.0 mm si Plaine, et S_72h = 90.0 mm si Montagne.\n"
        "Directive opérationnelle : « Après des pluies prolongées, vérifiez l'apparition de rigoles ou de ravinements et l'évacuation de l'eau autour des parcelles. » (Ajout spécifique pour la patate douce : « Vérifiez aussi l'état des buttes. »)"
    )
    
    add_p(doc,
        "3. Règle de Saturation Hydrique des Sols sur les 7 Jours Écoulés :\n"
        "Soit P_7j_passes = Somme de j=1 à 168 de p(t0 - j heures).\n"
        "Condition de déclenchement : P_7j_passes >= 50.0 mm.\n"
        "Rôle agronomique : avertir que la réserve utile du sol est saturée et que toute nouvelle pluie entraînera une asphyxie racinaire."
    )
    
    add_p(doc,
        "4. Règle de Vent Violent et Rafales (Bananier et Maïs) :\n"
        "Soit V_rafales = Max de i=1 à 24 de vent_rafale(t0 + i heures).\n"
        "Condition de déclenchement : V_rafales >= 40.0 km/h.\n"
        "Directive pour le Bananier : « Vérifiez les plants exposés au vent. Si des brise-vent existent, contrôlez leur état ; les régimes proches de la maturité peuvent être plus vulnérables à la chute. »"
    )
    
    add_p(doc,
        "5. Règle de Crue Hydrologique et Débit Anormal pour le Riz de Bas-fond :\n"
        "Soit Q_prevu le débit maximal prévu sur 7 jours via GloFAS, et Q_ref_p75 le 75e percentile des débits des 31 derniers jours.\n"
        "Condition de déclenchement : Q_prevu > Q_ref_p75.\n"
        "Directive opérationnelle : « Le débit prévu est inhabituel pour ce point à cette période. Vérifiez les diguettes, les canaux et les accès du bas-fond. Une pluie normale n'est pas un problème pour le riz, mais un débit inhabituel justifie une vérification locale. »"
    )
    
    add_p(doc,
        "6. Règle de Période Sèche Prolongée (Toutes cultures) :\n"
        "Soit N_jours_secs le nombre de jours consécutifs où la pluie sur 24h est inférieure à 2.0 mm.\n"
        "Condition de déclenchement : N_jours_secs >= 5 jours.\n"
        "Directive : « Période sèche annoncée : surveillez l'état des cultures et vérifiez localement la disponibilité en eau. »"
    )
    
    add_h3(doc, "6.2 Matrice ISABU des Cultures Prévalentes par Région")
    add_p(doc,
        "L'application adapte dynamiquement les avis en fonction du catalogue des cultures dominantes de la zone :"
    )
    add_bullet(doc, "Bujumbura Mairie : riz, maïs, manioc, bananier.", bold_prefix="• ")
    add_bullet(doc, "Bujumbura Rural (Imbo) : riz, maïs, manioc, bananier.", bold_prefix="• ")
    add_bullet(doc, "Bujumbura Rural (Mumirwa) : bananier, maïs, haricot, manioc, pomme de terre.", bold_prefix="• ")
    add_bullet(doc, "Gitega : maïs, haricot, bananier, riz, patate douce, pomme de terre.", bold_prefix="• ")
    add_bullet(doc, "Karusi : maïs, haricot, bananier, manioc, patate douce.", bold_prefix="• ")
    add_bullet(doc, "Rutana : riz, maïs, haricot, manioc, bananier.", bold_prefix="• ")
    
    # --- 7. Planification Scrum Agile ---
    add_h2(doc, "7. Planification Agile Scrum sur Deux Semaines (W1–W2)")
    
    add_p(doc,
        "Le projet a été exécuté selon la méthode Agile Scrum condensée sur un cycle ferme de dix jours ouvrés (deux semaines) [19] :"
    )
    
    headers_scrum = ["Jour Ouvré", "Phase / Sprint", "Objectifs et Livrables Techniques", "Statut de Clôture"]
    data_scrum = [
        ["J1 - J2", "Sprint 1 : Exploration & Cadrage", "Validation des coordonnées GPS des 5 zones, test des points GloFAS, formalisation des seuils IGEBU (50/100 mm).", "Validé à 100%"],
        ["J3 - J5", "Sprint 2 : Backend Pur & Sécurité", "Développement de measures.py et advice.py, client HTTP avec cache SQLite, auth Argon2id / JWT et tests pytest.", "Validé à 100% (31/31 tests)"],
        ["J6 - J7", "Sprint 3 : Frontend SvelteKit", "Architecture des routes (/login, /signup, /region/[slug]), intégration Sveaflet/Leaflet et graphiques svelteplot.", "Validé à 100%"],
        ["J8 - J9", "Sprint 4 : Intégration & Validation", "Connexion API BFF, gestion des cookies HttpOnly, tests d'affichage mobile responsive et validation du build Vite.", "Validé à 100% (Build exit 0)"],
        ["J10", "Sprint 5 : Synthèse & Documentation", "Rédaction du rapport académique UPG, matrices d'évaluation comparative et préparation des livrables.", "Validé à 100%"]
    ]
    add_table(doc, headers_scrum, data_scrum, col_widths=[2.0, 4.0, 8.0, 3.0], caption="Tableau 3.4 — Planification Scrum et exécution des sprints sur 10 jours ouvrés")
    
    # --- 8. Synthèse de la conception ---
    add_h2(doc, "8. Synthèse de la Conception")
    add_p(doc,
        "La conception de la solution AgroMétéo Burundi aboutit à une architecture modulaire hautement formalisée. "
        "Grâce à des exigences clairement quantifiées (EF et ENF), une modélisation UML exhaustive, des schémas de données légers "
        "et un moteur de règles fonctionnel pur d'une rigueur absolue, le système dispose d'une assise solide pour la réalisation "
        "technique détaillée au chapitre suivant."
    )
