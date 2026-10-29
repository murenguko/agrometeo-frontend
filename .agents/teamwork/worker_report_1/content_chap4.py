"""
content_chap4.py - Rédaction du Chapitre IV : Implémentation et Réalisation
Conforme aux exigences UPG et détaillant minutieusement le code réel de weather-backend et weather-app.
"""

from builder import add_h1, add_h2, add_h3, add_p, add_bullet, add_table, add_figure, add_code_block

def build_chap4(doc):
    """Génère le Chapitre IV complet : Implémentation et Réalisation."""
    add_h1(doc, "CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION")
    
    # --- 1. Environnement de développement et outillage ---
    add_h2(doc, "1. Environnement de Développement et Outillage Technique")
    
    add_p(doc,
        "La concrétisation logicielle du projet AgroMétéo Burundi s'est appuyée sur un environnement technique "
        "moderne, hautement performant et rigoureusement configuré. L'équipe a tiré parti des avancées les plus récentes "
        "des écosystèmes Python et JavaScript pour garantir une rapidité de développement optimale et une maintenabilité pérenne :"
    )
    
    headers_env = ["Composant Logiciel", "Version Retenue", "Rôle Technique & Responsabilité", "Justification d'Ingénierie"]
    data_env = [
        ["Python", ">= 3.14.0", "Langage d'exécution du backend FastAPI", "Nouvelles optimisations de l'interpréteur et gestion améliorée du typage statique."],
        ["uv", "0.11.17", "Gestionnaire d'environnement et de dépendances Python", "Résolution de lockfile et installation des packages 10 à 50 fois plus rapide que pip/poetry."],
        ["FastAPI", ">= 0.159.1", "Framework web asynchrone (ASGI)", "Typage fort Pydantic v2, documentation OpenAPI interactive et performance uvloop."],
        ["Node.js", "v22.x LTS", "Runtime JavaScript d'exécution serveur", "Support natif des ES Modules, haute performance du moteur V8 et compatibilité SvelteKit 3."],
        ["SvelteKit / Svelte", "Kit 3.0.0 / Svelte 5.57.1", "Framework full-stack web réactif (mode Runes)", "Compilation directe sans Virtual DOM, réactivité chirurgicale et architecture BFF native."],
        ["Vite", "8.3.0", "Compilateur et bundler de production", "Compilation ultra-rapide HMR (Hot Module Replacement) et optimisation du tree-shaking."],
        ["Tailwind CSS", "4.3.0 (@tailwindcss/vite)", "Moteur de style CSS utilitaire", "Architecture zéro-configuration intégrée à Vite, chargement dynamique des styles sans fichier de config."],
        ["Leaflet & Sveaflet", "1.9.4 / 0.1.5", "Moteur cartographique interactif libre", "Affichage fluide de la carte tuilée OpenStreetMap avec intégration de composants Svelte."],
        ["svelteplot", "0.14.2", "Moteur de visualisation vectorielle SVG", "Graphiques interactifs accessibles avec tooltips temporels basés sur la grammaire des graphiques."]
    ]
    add_table(doc, headers_env, data_env, col_widths=[2.8, 2.5, 5.0, 5.2], caption="Tableau 4.1 — Matrice de l'environnement technologique et outillage de développement")
    
    # --- 2. Implémentation du backend weather-backend ---
    add_h2(doc, "2. Implémentation du Backend `weather-backend`")
    
    add_p(doc,
        "Le répertoire `weather-backend` matérialise l'API REST asynchrone et le moteur décisionnel pur. "
        "L'arborescence du projet adopte une séparation stricte des responsabilités :"
    )
    
    figure_4_1 = """
                     ARBORESCENCE DÉTAILLÉE DE WEATHER-BACKEND
  weather-backend/
  ├── .cache.sqlite          # Base SQLite locale pour la mise en cache HTTP 1h
  ├── .env                   # Configuration secrète (DB_CONNECTION_STRING, SECRET_KEY)
  ├── pyproject.toml         # Déclaration des dépendances et configuration pytest
  ├── uv.lock                # Verrouillage reproductible des paquets Python
  ├── app/
  │   ├── main.py            # Point d'entrée FastAPI et branchement des routeurs
  │   ├── config.py          # Seuils IGEBU, classification des zones et coordonnées
  │   ├── core/
  │   │   ├── db.py          # Client singleton MongoDB Atlas (PyMongo)
  │   │   └── security.py    # Argon2id, JWT HS256, DUMMY_HASH anti-timing, get_current_user
  │   ├── routes/
  │   │   ├── token.py       # Endpoint POST /token (authentification OAuth2 Bearer)
  │   │   ├── user.py        # Endpoint POST /user (inscription d'un nouvel utilisateur)
  │   │   └── weather.py     # Endpoint sécurisé GET /{location} (collecte, agrégation, avis)
  │   ├── schemas/
  │   │   ├── security.py    # Schémas Pydantic Token et TokenData
  │   │   ├── user.py        # Schémas User, NewUser, UserInDB
  │   │   └── weather.py     # Enum Location (gitega, karusi, bujumbura, rutana, buja_rural_...)
  │   └── services/
  │       ├── advice.py      # MOTEUR PUR : évaluation des règles métier et conseils ISABU
  │       ├── measures.py    # MOTEUR PUR : extraction mathématique des séries temporelles
  │       └── weather.py     # Client réseau Open-Meteo & GloFAS avec cache SQLite
  └── tests/
      ├── test_advice.py     # 21 tests unitaires exhaustifs du moteur de décision
      └── test_measures.py   # 10 tests unitaires du moteur d'extraction temporelle
    """
    add_figure(doc, figure_4_1, caption="Figure 4.1 — Structure modulaire de la base de code du backend FastAPI")
    
    add_h3(doc, "2.1 Implémentation des Contrôleurs et Routes FastAPI")
    add_p(doc,
        "Le point d'entrée `app/main.py` instancie l'application ASGI FastAPI et inclut les trois routeurs sans préfixe superflu :"
    )
    add_bullet(doc,
        "Reçoit les requêtes au format standard application/x-www-form-urlencoded via OAuth2PasswordRequestForm. "
        "Appelle security.authenticate_user(). En cas de succès, génère un jeton JWT valide 30 minutes contenant l'identifiant "
        "('sub': username) et renvoie le schéma JSON { 'access_token': ..., 'token_type': 'bearer' }. En cas d'échec, renvoie une "
        "exception HTTP 401 Unauthorized après avoir exécuté le hachage fictif de compensation anti-timing.",
        bold_prefix="Route POST /token (app/routes/token.py) : "
    )
    add_bullet(doc,
        "Reçoit le schéma NewUser (nom, email, mot de passe). Hache le mot de passe en Argon2id et insère le document BSON "
        "dans la collection 'users' de MongoDB Atlas. Renvoie le schéma public User sans exposer le mot de passe haché.",
        bold_prefix="Route POST /user (app/routes/user.py) : "
    )
    add_bullet(doc,
        "Exige obligatoirement la dépendance de sécurité token: Annotated[User, Depends(security.get_current_user)]. "
        "Valide l'identifiant territorial via l'enum Location. Récupère les coordonnées géographiques associées, lance les "
        "requêtes asynchrones Open-Meteo et GloFAS, extrait les cumuls temporels via measures.py, évalue les conseils agricoles "
        "via advice.py et renvoie un payload JSON consolidé contenant les prévisions horaires, les relevés de crues et le tableau des conseils.",
        bold_prefix="Route GET /{location} (app/routes/weather.py) : "
    )
    
    add_h3(doc, "2.2 Client Réseau Résilient et Mise en Cache SQLite (app/services/weather.py)")
    add_p(doc,
        "La communication avec les serveurs d'Open-Meteo est blindée contre les aléas de connectivité grâce à la combinaison "
        "de `requests-cache` et `retry-requests` :"
    )
    
    code_client_weather = """
class OpenMeteoWeatherService:
    def __init__(self):
        # Configuration d'un cache local persistant SQLite avec expiration à 1 heure
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        # Politique de relance : 5 tentatives automatiques avec facteur de recul exponentiel
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        # Client FlatBuffers binaire ultra-rapide
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
    """
    add_code_block(doc, code_client_weather, title="app/services/weather.py — Client HTTP résilient avec cache local SQLite")
    
    add_h3(doc, "2.3 Moteur d'Agrégation Temporelle Pure (app/services/measures.py)")
    add_p(doc,
        "Le module `measures.py` résout la complexité de l'alignement temporel des séries horaires météorologiques. "
        "Il respecte la convention physique d'Open-Meteo où la valeur enregistrée à l'heure T correspond au cumul tombé "
        "sur l'intervalle écoulé (T - 1h, T]. Le calcul des cumuls glissants s'effectue sur des fenêtres semi-ouvertes :"
    )
    add_bullet(doc, "pluie_24h : somme des 24 pas de temps horaires sur l'intervalle (t0, t0 + 24h].", bold_prefix="• ")
    add_bullet(doc, "pluie_72h : somme des 72 pas de temps horaires sur l'intervalle (t0, t0 + 72h].", bold_prefix="• ")
    add_bullet(doc, "pluie_7j_passes : somme des 168 pas de temps passés sur (t0 - 168h, t0].", bold_prefix="• ")
    add_bullet(doc, "jours_secs : décompte des blocs successifs de 24h dont le cumul pluviométrique est strictement inférieur à 2,0 mm.", bold_prefix="• ")
    add_bullet(doc, "rafales_kmh : valeur maximale des rafales de vent anticipées sur les 24 prochaines heures.", bold_prefix="• ")
    add_bullet(doc, "Garde-fou d'intégrité : si la fenêtre temporelle est incomplète ou contient une valeur manquante (NaN / None), la fonction refuse d'interpoler et renvoie None, neutralisant tout risque de faux avis.", bold_prefix="• ")
    
    add_h3(doc, "2.4 Moteur Décisionnel Pur et Éthique des Messages (app/services/advice.py)")
    add_p(doc,
        "Le fichier `advice.py` implémente les règles de décision agricole sans aucun effet de bord. "
        "Voici un extrait significatif illustrant l'application des règles pour la culture du riz et les garanties déontologiques :"
    )
    
    code_advice = """
if culture == "riz":
    # Surveillance des débits anormaux en bas-fond rizicole
    if debit_prevu is not None and debit_ref is not None:
        if debit_prevu > debit_ref:
            regles.append("debit_inhabituel")
            actions.append(
                "Le débit prévu est inhabituel pour ce point à cette période. "
                "Vérifiez les diguettes, les canaux et les accès du bas-fond. "
                "Une pluie normale n'est pas un problème pour le riz, mais un débit "
                "inhabituel justifie une vérification locale."
            )
    # Surveillance de l'engorgement sans crue majeure
    if "debit_inhabituel" not in regles and pluie_72h is not None and pluie_72h >= seuil_72h:
        regles.append("pluie_72h_riz")
        actions.append(
            "Surveillez l'accumulation d'eau dans les points bas du bas-fond "
            "et vérifiez que les évacuations ne sont pas obstruées."
        )
    """
    add_code_block(doc, code_advice, title="app/services/advice.py — Logique métier pour la riziculture en bas-fond")
    
    # --- 3. Implémentation du frontend weather-app ---
    add_h2(doc, "3. Implémentation du Frontend SvelteKit `weather-app`")
    
    add_p(doc,
        "L'application client `weather-app` exploite la dernière génération du framework web Svelte (Svelte 5) "
        "en activant systématiquement les Runes. L'interface se caractérise par une réactivité instantanée et une ergonomie raffinée :"
    )
    
    figure_4_2 = """
                     ARBORESCENCE DÉTAILLÉE DE WEATHER-APP
  weather-app/
  ├── package.json           # Dépendances Svelte 5, SvelteKit 3, Tailwind v4, Sveaflet
  ├── vite.config.js         # Configuration Vite, compilateur Svelte (runes: true)
  ├── src/
  │   ├── app.html           # Gabarit HTML racine
  │   ├── env.js             # Validation de BASE_URL (http://localhost:8000)
  │   ├── lib/
  │   │   └── components/
  │   │       └── Leaflet.svelte # Carte interactive du Burundi (Sveaflet 0.1.5)
  │   └── routes/
  │       ├── +layout.server.js  # Garde serveur d'authentification (redirection /login)
  │       ├── +layout.svelte     # Thème sombre Slate-950, barre de navigation, déconnexion
  │       ├── +page.server.js    # ssr = false et action logout
  │       ├── +page.svelte       # Hub d'accueil : sélection des 5 provinces et carte
  │       ├── +error.svelte      # Écran d'erreur et redirection 3s sur 401/403
  │       ├── login/             # Formulaire de connexion OAuth2 et stockage cookie HttpOnly
  │       ├── signup/            # Formulaire d'inscription utilisateur
  │       └── region/[slug]/     # Dashboard complet : graphiques svelteplot et avis ISABU
    """
    add_figure(doc, figure_4_2, caption="Figure 4.2 — Structure modulaire du frontend SvelteKit")
    
    add_h3(doc, "3.1 Composant Cartographique Interactif (src/lib/components/Leaflet.svelte)")
    add_p(doc,
        "La carte interactive s'appuie sur le wrapper `sveaflet` enveloppant la bibliothèque Leaflet 1.9.4. "
        "Elle positionne six marqueurs géographiques précis matérialisant les cinq provinces et les deux sous-zones de Bujumbura Rural :"
    )
    add_bullet(doc, "Gitega (lat: -3.42708, long: 29.92463) : Hautes terres centrales, capitale politique.", bold_prefix="1. ")
    add_bullet(doc, "Karusi (lat: -3.10139, long: 30.16278) : Centre-Est, bassin fluvial de la Ruvubu.", bold_prefix="2. ")
    add_bullet(doc, "Bujumbura Mairie (lat: -3.38193, long: 29.36142) : Plaine de l'Imbo et littoral du Tanganyika.", bold_prefix="3. ")
    add_bullet(doc, "Rutana (lat: -3.92790, long: 29.99200) : Sud-Est et dépression agricole du Kumoso.", bold_prefix="4. ")
    add_bullet(doc, "Bujumbura Rural - Imbo (lat: -3.45000, long: 29.32000) : Plaine côtière basse altitude (< 1 000 m).", bold_prefix="5. ")
    add_bullet(doc, "Bujumbura Rural - Mumirwa (lat: -3.51220, long: 29.37150) : Contreforts escarpés (> 1 350 m).", bold_prefix="6. ")
    add_p(doc,
        "Chaque marqueur ouvre une infobulle (popup) au clic affichant l'appellation de la station, son sous-titre agro-écologique "
        "et un bouton d'action fluide 'Voir météo & conseils →' naviguant vers la route dynamique `/region/[slug]`."
    )
    
    add_h3(doc, "3.2 Visualisation Vectorielle Temporelle (svelteplot) et Filtrage des Avis")
    add_p(doc,
        "Sur la page de détail `/region/[slug]`, le composant exploite `svelteplot` pour restituer les séries temporelles "
        "de prévisions horaires sur 7 jours. L'utilisateur bascule entre 4 grandeurs physiques :"
    )
    add_bullet(doc, "Température (°C) : courbe ambrée (#f59e0b) avec zone ombrée semi-transparente.", bold_prefix="• ")
    add_bullet(doc, "Précipitations (mm) : courbe bleu ciel (#38bdf8) illustrant l'intensité des averses.", bold_prefix="• ")
    add_bullet(doc, "Probabilité de pluie (%) : courbe indigo (#818cf8) exprimant le niveau de certitude.", bold_prefix="• ")
    add_bullet(doc, "Vitesse du vent (km/h) : courbe verte émeraude (#34d399) avec surbrillance des rafales.", bold_prefix="• ")
    add_p(doc,
        "Le survol du graphique déclenche un composant `<Pointer>` qui projette une mire en croix (`RuleX`, `RuleY`), "
        "un point de capture (`Dot`) et une infobulle textuelle indiquant la date et l'heure UTC exacte ainsi que la valeur mesurée. "
        "Sous les graphiques, les cartes d'avis agricoles sont filtrées en temps réel par culture et par niveau de sévérité "
        "sans aucun rechargement de page, illustrant la puissance de la Rune réactive `$derived`."
    )
    
    add_h3(doc, "3.3 Modale d'Inspection des Mesures et Limitations")
    add_p(doc,
        "Chaque carte de conseil comporte un bouton 'Mesures & limitations' ouvrant une boîte de dialogue modale accessible. "
        "Cette fenêtre affiche des jauges de progression colorimétriques comparant la prévision aux seuils critiques (bleu < 75%, "
        "ambre entre 75% et 100%, rose vif ≥ 100%), garantissant une transparence scientifique absolue vis-à-vis des utilisateurs."
    )
    
    # --- 4. Gestion de version et dépendances ---
    add_h2(doc, "4. Gestion de Version Git, Dépendances et Documentation")
    
    add_p(doc,
        "La gestion des dépendances est verrouillée de manière reproductible au bit près via `uv.lock` côté Python et `package-lock.json` "
        "côté Node.js. L'API backend est documentée interactivement via les interfaces auto-générées Swagger UI (`/docs`) et ReDoc (`/redoc`). "
        "Le dépôt Git de `weather-backend` a été initialisé sur la branche principale master avec un fichier .gitignore standard "
        "excluant les caches locaux, les fichiers d'environnement (.env) et les artefacts compilés."
    )
    
    # --- 5. Synthèse de la réalisation ---
    add_h2(doc, "5. Synthèse de la Réalisation")
    add_p(doc,
        "L'implémentation logicielle d'AgroMétéo Burundi démontre une maîtrise remarquable des standards de développement actuels. "
        "En mariant la réactivité sans DOM virtuel de Svelte 5 aux performances asynchrones et à la rigueur mathématique de FastAPI, "
        "la plateforme offre un niveau d'achèvement exceptionnel, entièrement opérationnel et prêt pour l'évaluation expérimentale "
        "développée au Chapitre V."
    )
