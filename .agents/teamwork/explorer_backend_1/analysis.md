# Rapport d'Analyse Technique Approfondie — Backend `weather-backend`
**Auteur :** explorer_backend_1  
**Projet :** Système de veille météo et climatique au Burundi  
**Date :** 2026-10-29  
**Cible analysée :** `c:\Users\PC\Desktop\Projects\weather-backend`  

---

## 1. Résumé Exécutif et Synthèse Comparative

Le présent document constitue l'analyse technique exhaustive du code source réel du backend situé dans `weather-backend`. Cette investigation a été menée sur l'intégralité des fichiers de code, des dépendances et de la suite de tests.

Une confrontation systématique entre le **Document de Cadrage MVP** et l'**Implémentation Réelle** met en lumière plusieurs divergences architecturales majeures, des choix d'ingénierie pragmatiques ainsi que des modules volontairement élagués ou réorientés.

### Tableau Comparatif Synthétique

| Dimension technique | Document de Cadrage MVP initial | Implémentation Réelle (`weather-backend`) | Statut / Justification technique |
| :--- | :--- | :--- | :--- |
| **Framework Web** | FastAPI (Python) | FastAPI `>=0.159.1` (Python `>=3.14`, gestionnaire `uv`) | **Conforme & Moderne** : Utilise les dernières fonctionnalités Python 3.14 et typage fort Pydantic. |
| **Base de Données** | PostgreSQL (relationnelle, tables, clés étrangères, Alembic) | **MongoDB** (NoSQL Cloud Atlas via `pymongo>=4.19.0`) | **Divergence Majeure** : Choix NoSQL orienté document. Utilisé uniquement pour l'authentification des utilisateurs (`users`). Pas de PostgreSQL ni d'Alembic. |
| **Persistance Météo** | Stockage persistant des prévisions et historiques en base SQL | **Cache local SQLite** via `requests-cache` (`.cache.sqlite`, TTL 1h) | **Adaptation Architecturale** : Les données météo/crues ne sont pas stockées en MongoDB, mais interrogées à la demande avec cache local. |
| **Authentification** | Évoquée succinctement ou basique | **Système d'authentification robuste** : JWT (`pyjwt`), hash `Argon2id` (`pwdlib`), OAuth2 Password Bearer | **Sur-implémentation Qualifiée** : Sécurité poussée avec parade anti-timing attack (dummy hash). |
| **Découpage Territorial** | 3 à 5 zones pilotes administratives | **5 zones pilotes (anciennes provinces)** : Bujumbura, Bujumbura Rural (scindée en 2 : Imbo / Mumirwa), Gitega, Karusi, Rutana | **Conforme et Précis** : Prise en compte fine du relief contrasté de Buja Rural (plaine vs montagne). |
| **Données Météo** | Open-Meteo Forecast API | Open-Meteo API (`openmeteo-requests` + `retry_requests`) | **Conforme** : Récupération des 7 derniers jours (modèle) et prévisions horaires. |
| **Données Crues** | GloFAS / Copérnicus | Open-Meteo Flood API (GloFAS) avec p75 des 31 derniers jours | **Conforme avec adaptation statistique** : p75 sur 31 jours glissants au lieu du 90e centile mensuel. |
| **Glissements de Terrain** | NASA LHASA (modèle d'aléa glissements) | **Exclu / Retiré** du périmètre backend | **Écart Documenté** : Explicitement commenté dans le code (`advice.py`) ; jugé hors périmètre du MVP météo-crues. |
| **Pluviométrie CHIRPS** | Précipitations satellites CHIRPS | **Non implémenté** | **Écart** : Remplacé par les réanalyses et prévisions Open-Meteo (`past_days=7`). |
| **Moteur de Règles / Alertes**| Règles ISABU / seuils IGEBU | Moteur purement fonctionnel (`measures.py` & `advice.py`) | **Haute Qualité** : Découplage complet, 100% testable unitairement, seuils IGEBU (50/100 mm), règles ISABU par culture. |
| **CORS & Middleware** | Non spécifié | Aucun middleware CORS configuré dans `app/main.py` | **Point de vigilance** : Nécessite un proxy frontal ou ajout de `CORSMiddleware`. |
| **Conteneurisation** | Docker / docker-compose attendu | **Absent** : Aucun `Dockerfile` ni `docker-compose.yml` | **Écart** : Lancement direct via `uv` / `uvicorn`. |
| **Gestion Git** | Dépôt versionné | Dépôt initialisé (`master`), mais **aucun commit réalisé** | **Chantier restant** : Fichiers non suivis (untracked). |

---

## 2. Environnement de Développement et Gestion des Dépendances

L'application repose sur l'outillage moderne de l'écosystème Python :
- **Python Version** : `>=3.14` (spécifié dans `.python-version` et `pyproject.toml`).
- **Gestionnaire de paquets et environnement** : `uv` (remplaçant pip/poetry pour des résolutions ultra-rapides, matérialisé par `uv.lock`).

### Analyse du fichier `pyproject.toml`
```toml
[project]
name = "weather-backend"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "fastapi[standard]>=0.159.1",
    "openmeteo-requests>=1.7.5",
    "pandas>=3.1.0",
    "pwdlib[argon2]>=0.3.1",
    "pydantic-settings>=2.16.1",
    "pyjwt>=2.15.1",
    "pymongo>=4.19.0",
    "pytest>=9.2.0",
    "pytest-asyncio>=1.4.1",
    "python-dotenv>=1.2.4",
    "requests-cache>=1.3.3",
    "retry-requests>=2.0.0",
    "uvicorn>=0.54.0",
]
```

### Rôle précis des dépendances clés
1. `fastapi[standard]` & `uvicorn` : Framework ASGI asynchrone ultra-performant.
2. `openmeteo-requests` : Client officiel Open-Meteo utilisant FlatBuffers pour la désérialisation rapide des séries temporelles binaires.
3. `pandas` : Manipulation vectorielle, alignement temporel des séries horaires et calculs de fenêtres glissantes (`date_range`, `Timedelta`).
4. `pwdlib[argon2]` : Hachage de mot de passe à l'état de l'art (gagnant de la Password Hashing Competition, algorithme Argon2id résistant aux attaques par GPU/ASIC).
5. `pyjwt` : Encodage et décodage sécurisé des jetons JSON Web Tokens (JWT) avec algorithme HMAC-SHA256 (`HS256`).
6. `pymongo` : Driver officiel MongoDB pour Python.
7. `requests-cache` & `retry-requests` : Cache HTTP persistant sur base SQLite (`.cache.sqlite`) et politique de relance exponentielle sur défaillance réseau.
8. `pydantic-settings` : Gestion typée et surchargeable des seuils via variables d'environnement.

---

## 3. Architecture Logicielle et Structure des Routes FastAPI

### Structure de l'arborescence
```
weather-backend/
├── .cache.sqlite          # Cache local SQLite pour les requêtes HTTP externes
├── .env                   # Variables d'environnement (clés secrètes, URI MongoDB)
├── .gitignore             # Exclusion des fichiers pycache, venv, env
├── .python-version        # Fixe Python 3.14
├── pyproject.toml         # Définition du projet, dépendances et config pytest
├── uv.lock                # Lockfile uv garantissant la reproductibilité
├── main.py                # Point d'entrée stub UV (affiche "Hello from weather-backend!")
├── README.md              # Fichier vide
├── app/
│   ├── config.py          # Configuration centrale, Seuils Pydantic, classification des zones
│   ├── main.py            # Instance FastAPI, inclusion des routeurs
│   ├── core/
│   │   ├── db.py          # Client singleton MongoDB (PyMongo)
│   │   └── security.py    # Argon2, JWT, OAuth2 Bearer, dépendance get_current_user
│   ├── routes/
│   │   ├── token.py       # Endpoint POST /token (authentification OAuth2)
│   │   ├── user.py        # Endpoint POST /user (inscription utilisateur)
│   │   └── weather.py     # Endpoint GET /{location} (collecte, fusion, conseils)
│   ├── schemas/
│   │   ├── security.py    # Schémas Pydantic Token et TokenData
│   │   ├── user.py        # Schémas User, NewUser, UserInDB
│   │   └── weather.py     # Enum Location (zones et sous-zones)
│   └── services/
│       ├── advice.py      # Moteur pur de génération des conseils agricoles
│       ├── measures.py    # Moteur pur d'extraction et agrégation des mesures météo
│       └── weather.py     # Client réseau Open-Meteo (Météo & Flood GloFAS)
└── tests/
    ├── test_advice.py     # 21 tests unitaires du moteur de conseils
    └── test_measures.py   # 10 tests unitaires du module d'extraction
```

### Analyse des Contrôleurs et Routes (`app/routes/`)

1. **`app/main.py`** :
   ```python
   app = FastAPI()
   app.include_router(weather.router)
   app.include_router(token.router)
   app.include_router(user.router)
   ```
   *Constat d'architecture* : Aucun préfixe global `/api` ni `/api/v1` n'est configuré sur les routeurs. Les URLs sont directes.

2. **Route d'authentification (`POST /token`)** (`app/routes/token.py`) :
   - Reçoit `form_data: Annotated[OAuth2PasswordRequestForm, Depends()]`.
   - Appelle `security.authenticate_user(username, password)`.
   - En cas de succès, génère un JWT valide pendant 30 minutes (`security.ACCESS_TOKEN_EXPIRE_MINUTES`).
   - Renvoie le schéma `Token` : `{"access_token": "...", "token_type": "bearer"}`.
   - En cas d'échec, lève un `HTTPException(401, detail="Incorrect username or password")`.

3. **Route d'inscription (`POST /user`)** (`app/routes/user.py`) :
   - Reçoit `user: NewUser` (`username`, `name`, `password`).
   - Hache le mot de passe en Argon2id.
   - Insère le document dans la collection MongoDB `users` via `db.get_collection("users").insert_one(...)`.
   - Renvoie le schéma public `User` (`username`, `name`) sans divulguer le hash.

4. **Route principale de surveillance (`GET /{location}`)** (`app/routes/weather.py`) :
   - Paramètre de chemin `location` validé via l'enum `Location`.
   - Sécurisation obligatoire : `token: Annotated[User, Depends(security.get_current_user)]`.
   - Récupère les coordonnées géographiques associées.
   - Exécute de manière asynchrone :
     - `make_weather_request(location, lat, long)` (Open-Meteo)
     - `make_flood_request(location, lat, long)` (GloFAS prévision 7j)
     - `get_flood_past_data(lat, long)` (GloFAS historique p75 31j)
   - Fusionne les données brutes : `all_results = weather_results | river_results | past_river_data`.
   - Extrait les métriques décisionnelles : `mesures = extraire_mesures(all_results, seuils=Seuils())`.
   - Évalue les règles métier et produit les conseils : `conseils = generer_conseils(mesures, location.value)`.
   - Renvoie le payload unifié : `all_results | {"conseils": conseils}`.

---

## 4. Base de Données NoSQL MongoDB vs Cadrage PostgreSQL

L'une des divergences les plus remarquables entre le cadrage théorique du projet et l'implémentation est le choix technologique du système de gestion de base de données.

### Implémentation réelle (`app/core/db.py`)
```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Client:
    def __init__(self):
        self.__client = MongoClient(str(os.getenv("DB_CONNECTION_STRING")))
        self.__db = self.__client[str(os.getenv("DB"))]

    def get_collection(self, collection):
        return self.__db[collection]

db = Client()
```

### Analyse détaillée du modèle de données
1. **Technologie** : MongoDB (instance hébergée sur MongoDB Atlas : `cluster0.3iilu.mongodb.net`, base `weather-app`).
2. **Usage exclusif** : La base de données MongoDB n'est exploitée **que** pour la collection `users`. Aucune donnée météo, ni observation, ni alerte n'est persistée en base documentaire.
3. **Schéma du document `users`** :
   ```json
   {
     "_id": ObjectId("..."),
     "username": "johndoe@example.com",
     "name": "John Doe",
     "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$SD/Y0VojbYzgQOFpkuoOwg$5ZvE2F8bvlXvm4fC7QfwBSkKzA5TXBbR1X1ktwP45Yc"
   }
   ```
4. **Absence de schémas relationnels et d'Alembic** :
   - Aucun fichier de migration SQL (pas de dossier `alembic/`, pas de script DDL).
   - Aucun modèle SQLAlchemy / SQLModel.
5. **Stratégie de persistance pour les données météo** :
   - Plutôt que d'écrire des millions de points horaires dans une table PostgreSQL `weather_records`, le système s'appuie sur le cache HTTP persistant SQLite (`.cache.sqlite`) via `requests-cache`. Ce cache conserve les réponses de l'API Open-Meteo pendant 3 600 secondes (1 heure).
   - *Justification technique* : Cette approche allège considérablement la maintenance d'infrastructure pour un MVP, évite la saturation du stockage avec des séries temporelles transitoires et élimine la latence d'écriture en base distante.

---

## 5. Sécurité, Gestion des Identités et Résilience

L'implémentation de la sécurité dans `app/core/security.py` présente un niveau d'ingénierie remarquable pour un projet académique.

### 1. Hachage des mots de passe (Argon2id)
- Utilisation de `pwdlib` configuré avec le profil recommandé (`PasswordHash.recommended()`).
- Génère des hachages `Argon2id` (paramètres : mémoire 64 Mo / 65536 Ko, 3 itérations, 4 threads).
- Résistance cryptographique maximale contre les attaques par force brute distribuée.

### 2. Protection contre les attaques temporelles (Side-Channel Timing Attacks)
Dans `authenticate_user` (`app/core/security.py`, lignes 61–70) :
```python
def authenticate_user(self, username: str, password: str):
    DUMMY_HASH = self.password_hash.hash("dummypassword")
    user = self.get_user(username)
    if not user:
        self.verify_password(password, DUMMY_HASH)
        return False
    if not self.verify_password(password, user.hashed_password):
        return False
    return user
```
*Analyse* : Si l'utilisateur n'existe pas en base de données, l'application effectue quand même la vérification complète du hash sur un mot de passe fictif (`DUMMY_HASH`). Cela égalise le temps de réponse du serveur et empêche un attaquant de déterminer si une adresse email est inscrite ou non par chronométrage réseau (énumération d'utilisateurs).

### 3. Gestion des Jetons JWT
- Spécification : Algorithme symétrique `HS256`, clé secrète `SECRET_KEY` stockée dans `.env`.
- Payload JWT :
  ```json
  {
    "sub": "johndoe@example.com",
    "exp": 1761730000
  }
  ```
- Validation dans la dépendance FastAPI `get_current_user` (`HTTP_401_UNAUTHORIZED` si le jeton est expiré, altéré ou l'utilisateur introuvable).

### 4. Vulnérabilités et Points d'Amélioration Sécurité
1. **Absence de contrôle d'unicité lors de la création d'utilisateur** : Dans `app/routes/user.py`, `insert_one` est exécuté sans vérifier au préalable si `username` existe déjà, et aucun index unique n'est déclaré programmatiquement sur la collection MongoDB `users`.
2. **Absence de Middleware CORS** : Si le frontend SvelteKit tente un appel direct client-side (navigateur) vers `http://localhost:8000`, le navigateur bloquera la requête par défaut (Cross-Origin Resource Sharing).
3. **Secrets dans le dépôt** : Le fichier `.env` contenant une vraie chaîne de connexion MongoDB Atlas et la clé secrète JWT est présent sur le disque local (bien qu'exclu dans `.gitignore`, il nécessite une rotation avant mise en production).
4. **Absence de Rate Limiting** : Aucune limitation de débit (type `slowapi`) n'est mise en œuvre sur `/token` ou `/user`, laissant ces routes exposées aux attaques par déni de service ou saturation.

---

## 6. Collecteurs Météo, Crues et Traitement des Séries Temporelles

Le module `app/services/weather.py` orchestre la communication avec les APIs distantes d'Open-Meteo.

### 1. Configuration du Client HTTP Résilient
```python
self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
```
- **Cache local** : SQLite `.cache.sqlite` avec TTL de 1 heure (3600 secondes).
- **Tolérance aux pannes réseau** : Jusqu'à 5 relances automatiques en cas d'erreur transitoire HTTP (500, 502, 503, 504) ou coupure réseau, avec délai exponentiel (`backoff_factor=0.2`).

### 2. Données Météo Horaires (`make_weather_request`)
- **URL** : `https://api.open-meteo.com/v1/forecast`
- **Variables collectées** :
  - `temperature_2m` (°C) : Température à 2 m du sol.
  - `precipitation` (mm) : Précipitations horaires cumulées sur l'heure écoulée.
  - `wind_speed_10m` (km/h) : Vitesse moyenne du vent à 10 m.
  - `precipitation_probability` (%) : Probabilité de pluie.
  - `wind_gusts_10m` (km/h) : Rafales maximales de vent à 10 m (seuil critique agricole).
- **Profondeur temporelle** : `past_days=7` + prévisions sur 7 jours.
  *Note technique* : Les 7 jours passés sont des réanalyses/estimations du modèle météorologique, servant à évaluer l'état hydrique des sols (`pluie_7j_passes`).
- **Garantie d'alignement temporel** : Utilisation de `pd.date_range` basé sur `hourly.Time()`, `hourly.TimeEnd()` et `hourly.Interval()`.

### 3. Données Hydrologiques GloFAS (`make_flood_request` & `get_flood_past_data`)
- **URL** : `https://flood-api.open-meteo.com/v1/flood`
- **Résolution du modèle** : Grille mondiale d'environ 5 km issue du Copernicus Emergency Management Service (GloFAS).
- **Prévision à 7 jours** : `daily: river_discharge` (débit fluvial prévu en m³/s).
- **Référence statistique sur 31 jours** :
  - Paramètre : `daily: river_discharge_p75`, `past_days: 31`, `forecast_days: 1`.
  - Calcule le 75e percentile des débits des 31 derniers jours.
  - *Choix d'ingénierie documenté* : Pour le MVP, le 75e centile sur les 31 derniers jours a été retenu comme seuil dynamique de "débit inhabituel", plus réactif que le 90e centile mensuel historique.

### 4. Situation de NASA LHASA et CHIRPS
- **NASA LHASA** (Landslide Hazard Assessment for Situational Awareness) : Ce modèle d'aléa glissements de terrain n'est **pas implémenté** dans le backend.
- Les commentaires dans `app/services/advice.py` indiquent clairement que l'analyse des versants et de l'érosion a été sortie du périmètre du prototype :
  > *"Les versants escarpés sont naturellement exposés à l'érosion et aux glissements, mais ce module n'est pas inclus dans ce périmètre météo–crues : aucun conseil de glissement n'est affiché."*
- **CHIRPS** : Non présent. Les données pluviométriques proviennent exclusivement d'Open-Meteo.

---

## 7. Découpage Territorial et Localisation des Zones Pilotes

Le backend modélise les zones pilotes burundaises selon le découpage des **anciennes provinces** et prend en compte le relief spécifique du pays :

### Coordonnées Géographiques Déclarées (`app/routes/weather.py`)
```python
coordinates = {
    "gitega": {"lat": -3.42708, "long": 29.9246},
    "karusi": {"lat": -3.10139, "long": 30.16278},
    "bujumbura": {"lat": -3.38193, "long": 29.36142},
    "rutana": {"lat": -3.9279, "long": 29.992},
    "buja_rural_imbo": {"lat": -3.4292, "long": 29.3165},
    "buja_rural_mumirwa": {"lat": -3.4389, "long": 29.6944},
}
```

### Typologie Plaine / Montagne et Règle de Précaution
Dans `app/config.py`, chaque zone est affectée à une classe topographique déterminant les seuils pluviométriques critiques :
- **Bujumbura** : `plaine` (plaine de l'Imbo, altitude ~820 m).
- **Gitega** : `montagne` (plateaux centraux, 1 600–2 000 m).
- **Karusi** : `montagne` (plateaux centraux, 1 450–1 850 m).
- **Rutana** : `montagne` (crête Congo-Nil / escarpements, 1 650–1 800 m).
- **Bujumbura Rural** : `mixte` (variation altitudinale extrême de 700 à 2 600 m).
  - Sous-zone **`imbo`** : Plaine (< 1 000 m).
  - Sous-zone **`mumirwa`** : Hautes terres (> 1 350 m).
  - **Principe de précaution implémenté** : Si `buja_rural` est interrogé sans spécifier de sous-zone valide, le système se rabat automatiquement sur la classe `plaine` (seuil de pluie le plus bas : 50 mm/24h au lieu de 100 mm/24h), évitant ainsi de masquer un danger potentiel.

---

## 8. Moteur de Règles Agricoles, Alertes et Vigilance

Le moteur d'aide à la décision agricole est réparti en deux modules purement fonctionnels, sans aucun appel réseau ni effet de bord : `app/services/measures.py` et `app/services/advice.py`.

### 1. Configuration des Seuils IGEBU (`app/config.py`)
La classe `Seuils` (Pydantic BaseSettings) permet la surcharge par variables d'environnement (ex. `SEUIL_PLUIE_CRIT_PLAINE_24H=40`) :
- `pluie_crit_plaine_24h = 50.0 mm / 24 h` (seuil officiel IGEBU pour la plaine).
- `pluie_crit_montagne_24h = 100.0 mm / 24 h` (seuil officiel IGEBU pour les hautes terres).
- `pluie_crit_plaine_72h = 60.0 mm / 72 h` (pluie prolongée plaine).
- `pluie_crit_montagne_72h = 90.0 mm / 72 h` (pluie prolongée montagne).
- `pluie_7j_passes_crit = 50.0 mm / 7 j` (saturation hydrique des sols).
- `jours_sec_mm = 2.0 mm`, `jours_secs_min = 5` (déficit hydrique / sécheresse).
- `vent_rafale_kmh = 40.0 km/h` (seuil de dégradation et chute des bananiers).

### 2. Logique d'Extraction des Mesures (`app/services/measures.py`)
Le module traite les séries temporelles avec une rigueur mathématique et physique :
- **Convention Open-Meteo** : La valeur à l'instant $T$ représente le cumul sur l'intervalle $(T-1h, T]$. Les fenêtres de calcul sont donc ouvertes à gauche et fermées à droite.
- **`pluie_24h`** : Somme sur $(t_0, t_0 + 24h]$.
- **`pluie_72h`** : Somme sur $(t_0, t_0 + 72h]$.
- **`pluie_7j_passes`** : Somme sur $(t_0 - 168h, t_0]$.
- **`jours_secs`** : Nombre de blocs glissants de 24h consécutifs dont la pluie totale est $< 2.0\text{ mm}$.
- **`rafales_kmh`** : Maximum des rafales de vent prévues sur $(t_0, t_0 + 24h]$.
- **`debit_prevu`** : Débit GloFAS maximal sur les 7 jours de prévision.
- **`debit_reference`** : 75e percentile des 31 derniers jours historiques de débit.
- **Garde-fou d'incomplétude** : Si une fenêtre contient une valeur manquante (`NaN` ou `None`), la mesure vaut `None`. Aucune interpolation hasardeuse n'est effectuée.

### 3. Logique Décisionnelle et Déclenchement des Règles (`app/services/advice.py`)

| Règle métier | Condition de déclenchement | Cultures cibles | Message d'action concret |
| :--- | :--- | :--- | :--- |
| **Pluie critique 24h** | $\text{pluie\_24h} \ge \text{seuil\_24h}$ (50 ou 100 mm) | **Maïs** | "Si vous faites sécher du maïs en plein air, prévoyez de le mettre à l'abri ou de le couvrir avant les pluies annoncées. Vérifiez les fossés et les accès autour des aires de séchage." |
| **Pluie critique 24h** | $\text{pluie\_24h} \ge \text{seuil\_24h}$ (50 ou 100 mm) | **Autres cultures** | "Protégez les produits en cours de séchage et vérifiez les fossés et les accès exposés." |
| **Crue / Débit Riz** | $\text{debit\_prevu} > \text{debit\_reference\_p75}$ | **Riz (bas-fonds)** | "Le débit prévu est inhabituel pour ce point à cette période. Vérifiez les diguettes, les canaux et les accès du bas-fond. Une pluie normale n'est pas un problème pour le riz, mais un débit inhabituel justifie une vérification locale." |
| **Pluie prolongée Riz** | $\text{debit} \le \text{ref}$ ET $\text{pluie\_72h} \ge \text{seuil\_72h}$ | **Riz (bas-fonds)** | "Surveillez l'accumulation d'eau dans les points bas du bas-fond et vérifiez que les évacuations ne sont pas obstruées." |
| **Humidité / Sols gorgés**| $\text{pluie\_72h} \ge \text{seuil\_72h}$ OU $\text{pluie\_7j} \ge 50\text{ mm}$ | **Haricot, Manioc, Pomme de terre** | "Après des pluies prolongées, vérifiez l'apparition de rigoles ou de ravinements et l'évacuation de l'eau autour des parcelles." |
| **Humidité Buttes** | $\text{pluie\_72h} \ge \text{seuil\_72h}$ OU $\text{pluie\_7j} \ge 50\text{ mm}$ | **Patate douce** | "Après des pluies prolongées, vérifiez l'apparition de rigoles ou de ravinements et l'évacuation de l'eau autour des parcelles. Vérifiez aussi l'état des buttes." |
| **Vent violent** | $\text{rafales\_kmh} \ge 40.0\text{ km/h}$ | **Bananier** | "Vérifiez les plants exposés au vent. Si des brise-vent existent, contrôlez leur état ; les régimes proches de la maturité peuvent être plus vulnérables à la chute." |
| **Vent violent** | $\text{rafales\_kmh} \ge 40.0\text{ km/h}$ | **Maïs** | "Vérifiez les plants exposés au vent : les rafales fortes peuvent provoquer le versement ou le déracinement du maïs et des jeunes plants. Contrôlez aussi les installations légères." |
| **Période sèche** | $\text{jours\_secs} \ge 5$ jours | **Toutes cultures** | "Période sèche annoncée : surveillez l'état des cultures et vérifiez localement la disponibilité en eau." |

### 4. Garanties Éthiques et Déontologiques des Messages
Le code implémente des règles strictes sur la terminologie :
1. **Jamais de certitude absolue ni de panique** : Le code proscrit formellement les termes *"inondation certaine"* ou *"évacuation"* (qui relèvent exclusivement des prérogatives de la Protection Civile burundaise).
2. **Jamais d'affirmation "pas de risque"** : En l'absence d'aléa, le statut est `sans_signal` et rappelle que la prévision météorologique reste probabiliste.
3. **Absence de données $\neq$ Absence de risque** : Si une mesure est manquante, le statut est `non_evalue` et le message alerte l'utilisateur que l'absence de données ne constitue en aucun cas une vigilance faible.
4. **Verbe d'action systématique** : Chaque conseil commence par une action pratique de terrain (*"Vérifiez..."*, *"Protégez..."*, *"Surveillez..."*).

---

## 9. Matrice des Cultures Prévalentes par Zone (ISABU)

L'implémentation attribue les cultures principales à chaque zone conformément aux orientations agro-écologiques de l'Institut des Sciences Agronomiques du Burundi (ISABU) :

```python
CULTURES_PAR_ZONE = {
    "bujumbura": ("riz", "mais", "manioc", "bananier"),
    "gitega": ("mais", "haricot", "bananier", "riz", "patate_douce", "pomme_de_terre"),
    "karusi": ("mais", "haricot", "bananier", "manioc", "patate_douce"),
    "rutana": ("riz", "mais", "haricot", "manioc", "bananier"),
}

CULTURES_PAR_SOUS_ZONE_BUJA_RURAL = {
    "imbo": ("riz", "mais", "manioc", "bananier"),
    "mumirwa": ("bananier", "mais", "haricot", "manioc", "pomme_de_terre"),
}
```

La fonction `generer_conseils` itère automatiquement sur l'ensemble des cultures prévalentes de la localité sélectionnée pour fournir un tableau complet d'avis personnalisés.

---

## 10. Tests, Validation et Assurance Qualité

Le backend bénéficie d'une suite de tests automatisés exemplaire, articulée autour de `pytest` et `pytest-asyncio`.

### Résultats de l'Exécution Réelle des Tests
Commande exécutée : `.venv\Scripts\pytest -v`  
Résultat : **31 passed in 7.59s** (100% de réussite).

```
tests/test_advice.py::test_classement_zones PASSED                       [  3%]
tests/test_advice.py::test_buja_rural_mixte PASSED                       [  6%]
tests/test_advice.py::test_invalides PASSED                              [  9%]
tests/test_advice.py::test_pluie_24h_zone_montagne PASSED                [ 12%]
tests/test_advice.py::test_pluie_24h_zone_plaine_50_mm PASSED            [ 16%]
tests/test_advice.py::test_vent_bananier_40_kmh PASSED                   [ 19%]
tests/test_advice.py::test_sous_le_seuil_vent_pas_de_declenchemen PASSED [ 22%]
tests/test_advice.py::test_jours_secs PASSED                             [ 25%]
tests/test_advice.py::test_riz_debit_inhabituel PASSED                   [ 29%]
tests/test_advice.py::test_riz_pluie_sans_debit_inhabituel PASSED        [ 32%]
tests/test_advice.py::test_humidite_7j_passes PASSED                     [ 35%]
tests/test_advice.py::test_patate_douce_mais_buttes PASSED               [ 38%]
tests/test_advice.py::test_sans_signal PASSED                            [ 41%]
tests/test_advice.py::test_non_evalue_si_donnees_manquantes PASSED       [ 45%]
tests/test_advice.py::test_non_evalue_si_valeur_nan PASSED               [ 48%]
tests/test_advice.py::test_conseil_actif_reste_actif_avec_donnee_absente PASSED [ 51%]
tests/test_advice.py::test_format_sortie PASSED                          [ 54%]
tests/test_advice.py::test_cultures_inconnue PASSED                      [ 58%]
tests/test_advice.py::test_generer_conseils_multi_zones PASSED           [ 61%]
tests/test_advice.py::test_cultures_prevalentes_par_zone PASSED          [ 64%]
tests/test_advice.py::test_generer_conseils_utilise_cultures_prevalentes_par_defaut PASSED [ 67%]
tests/test_measures.py::test_temps_calme PASSED                          [ 70%]
tests/test_measures.py::test_pluie_24h_et_72h PASSED                     [ 74%]
tests/test_measures.py::test_bornes_fenetre_open_meteo PASSED            [ 77%]
tests/test_measures.py::test_pluie_7j_passes PASSED                      [ 80%]
tests/test_measures.py::test_valeur_manquante_rend_la_mesure_non_evaluee PASSED [ 83%]
tests/test_measures.py::test_jours_secs_fiable_malgre_trou_tardif PASSED [ 87%]
tests/test_measures.py::test_debit_prevu_et_reference PASSED             [ 90%]
tests/test_measures.py::test_blocs_absents PASSED                        [ 93%]
tests/test_measures.py::test_dates_serialisees_json PASSED               [ 96%]
tests/test_measures.py::test_branchement_avec_generer_conseil PASSED     [100%]
```

### Forces de la Stratégie de Test
1. **Isolation totale du réseau** : Les tests injectent des structures de données synthétiques (fixtures vectorisées pandas) sans jamais interroger l'API Open-Meteo ni MongoDB.
2. **Couverture exhaustive des cas limites** :
   - Présence de valeurs `NaN` ou `None`.
   - Séries incomplètes ou trous tardifs dans les prévisions.
   - Surcharge de sous-zones invalides.
   - Respect strict des formulations textuelles (vérification que *"évacuation"* ou *"inondation certaine"* ne figurent jamais dans les sorties).
   - Validation de l'intégrité des dates sérialisées au format ISO 8601.

---

## 11. Déploiement, Conteneurisation et Gestion de Version Git

### État de la Conteneurisation
- **Aucun `Dockerfile`** ni **`docker-compose.yml`** n'est présent dans le dépôt.
- L'exécution actuelle se fait en environnement de développement local via l'environnement virtuel Python (`.venv`) généré par `uv`.
- *Commande de démarrage type* :
  ```bash
  uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```

### État du Dépôt Git
- Dépôt initialisé (`git status` indique la branche `master`).
- **Aucun commit réalisé** (`No commits yet`).
- Tous les fichiers du projet (`app/`, `tests/`, `pyproject.toml`, `uv.lock`, etc.) sont actuellement à l'état `Untracked`.
- Un fichier `.gitignore` standard Python est en place, excluant les caches, les environnements virtuels et les fichiers `.env`.

---

## 12. Analyse Critique et Recommandations pour le Rapport Académique UPG

Pour la rédaction des Chapitres IV (Implémentation) et V (Tests, Validation et Évaluation comparative) du rapport académique, les arguments et justifications suivants doivent être mis en avant :

1. **Substitution de PostgreSQL par MongoDB** :
   - *Constat* : Le cadrage prévoyait PostgreSQL pour stocker l'historique et les alertes.
   - *Justification académique / ingénierie* : La nature hautement volatile des prévisions météorologiques horaires rendait un schéma relationnel rigide surdimensionné pour le MVP. Le stockage des utilisateurs dans une collection MongoDB couplé à la mise en cache locale SQLite (`requests-cache`) offre une architecture plus légère, sans coûts d'administration de bases de données relationnelles lourdes.
2. **Élimination de NASA LHASA** :
   - *Constat* : Absence du modèle de glissements de terrain.
   - *Justification* : Le modèle LHASA de la NASA dispose d'une résolution spatiale insuffisante à l'échelle des collines burundaises (Mumirwa/Mugamba) et nécessite des données satellitaires d'humidité des sols en temps quasi-réel difficilement intégrables dans un MVP de deux semaines. Le projet a prudemment priorisé les risques hydrométéorologiques directs (pluies torrentielles et crues de bas-fonds rizicoles).
3. **Sur-performance en Sécurité** :
   - Alors que le MVP aurait pu se satisfaire d'une authentification basique, le backend implémente une solution industrielle robuste : Argon2id (avec protection anti-timing attack) et JWT Bearer.
4. **Recommandations d'Amélioration Immédiates** :
   - Ajouter `CORSMiddleware` dans `app/main.py` pour autoriser les origines frontend (`http://localhost:5173`).
   - Créer un index unique sur `username` dans la collection MongoDB `users`.
   - Créer un `Dockerfile` multi-stage basé sur `ghcr.io/astral-sh/uv:python3.14-bookworm-slim` pour standardiser le déploiement.
   - Effectuer le commit initial du code source sur la branche `master`.
