# Handoff Report — spec_miner_cadrage_1

**Auteur :** spec_miner_cadrage_1 (Teamwork Specification Miner)  
**Parent :** orchestrator_1 (conversation ID: e47c32ca-a804-4068-8d51-a33db036fb24)  
**Date :** 2026-10-29  
**Type de handoff :** Hard (Mission accomplie avec succès)  
**Livrable principal généré :** `c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\spec_miner_cadrage_1\analysis.md`

---

## 1. Observation (Faits Directement Observés et Extraits)

### 1.1 Documents Sources Extraits
- **Document 1 (Cadrage MVP) :** Localisé et extrait depuis le payload protobuf de la session utilisateur initiale (Step 0 de `fa7a1370-4a70-4d36-8811-edd24d0c19f5.db`). Fichier texte complet extrait à `c:\Users\PC\Desktop\Projects\weather-app\DOCUMENT_1_CADRAGE_MVP.txt` (14 573 octets). Titre : *"Système de veille météo et climatique au Burundi — Document de cadrage du projet à développer en deux semaines — Version révisée du 11 octobre 2026"*.
- **Document 2 (Canevas UPG) :** Extrait du même payload à `c:\Users\PC\Desktop\Projects\weather-app\DOCUMENT_2_CANEVAS_UPG.txt` (4 856 octets). Titre : *"CANEVAS RAPPORT PROJET II (UNIVERSITÉ POLYTECHNIQUE DE GITEGA - UPG, FACULTÉ DES TIC, GÉNIE LOGICIEL)"*.
- **Consignes de mise en forme UPG :** Police Times New Roman 12 pt, interligne 1,5, marges Gauche 3 cm / Autres 2,5 cm, texte justifié, numérotation figures/tableaux par chapitre, style bibliographique IEEE, exclusion stricte des pages liminaires demandée par l'utilisateur.

### 1.2 Observations du Code Source Réel (`weather-backend`)
- **Base de données et Client MongoDB :** `app/core/db.py` lignes 1–18 :
  ```python
  from pymongo import MongoClient
  ...
  self.__client = MongoClient(str(os.getenv("DB_CONNECTION_STRING")))
  self.__db = self.__client[str(os.getenv("DB"))]
  ```
  Le backend n'utilise **aucun modèle PostgreSQL, SQLAlchemy ou Alembic**. Il se connecte à MongoDB Atlas (`cluster0.3iilu.mongodb.net`, base `weather-app`).
- **Authentification complète et Sécurité :** `app/core/security.py` lignes 19–72 :
  - `OAuth2PasswordBearer(tokenUrl="token")`
  - Algorithme de hachage Argon2id via `PasswordHash.recommended()` de `pwdlib`
  - JWT HS256 (`pyjwt`), expiration à 30 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES = 30`)
  - Parade anti-timing attack dans `authenticate_user` (lignes 62–67) :
    ```python
    DUMMY_HASH = self.password_hash.hash("dummypassword")
    if not user:
        self.verify_password(password, DUMMY_HASH)
        return False
    ```
- **Découpage géographique et Coordonnées réelles :** `app/routes/weather.py` lignes 16–49 et `app/config.py` lignes 80–99 :
  5 zones pilotes administratives (anciennes provinces) :
  - `gitega` : lat: -3.42708, long: 29.9246 (classe montagne)
  - `karusi` : lat: -3.10139, long: 30.16278 (classe montagne)
  - `bujumbura` : lat: -3.38193, long: 29.36142 (classe plaine)
  - `rutana` : lat: -3.9279, long: 29.992 (classe montagne)
  - `buja_rural` : mixte, scindée en `buja_rural_imbo` (-3.4292, 29.3165, plaine) et `buja_rural_mumirwa` (-3.4389, 29.6944, montagne).
- **Règle de précaution topographique :** `app/config.py` lignes 168–174 : en cas de doute sur la sous-zone de Bujumbura Rural, le système se rabat automatiquement sur le seuil de plaine (50 mm/24h au lieu de 100 mm).
- **Retrait explicite de NASA LHASA :** `app/services/advice.py` lignes 98–101 :
  > *"Les versants escarpés sont naturellement exposés à l'érosion et aux glissements, mais ce module n'est pas inclus dans ce périmètre météo–crues : aucun conseil de glissement n'est affiché."*
- **Cultures prévalentes par zone (ISABU) :** `app/config.py` lignes 104–115 (`CULTURES_PAR_ZONE` et `CULTURES_PAR_SOUS_ZONE_BUJA_RURAL`).
- **Tests unitaires :** Exécution de `pytest` dans `weather-backend` : **31 passed in 7.59s** (100% de réussite sur les 21 tests de `test_advice.py` et 10 tests de `test_measures.py`).

### 1.3 Observations du Code Source Réel (`weather-app`)
- **Framework :** SvelteKit 2 avec Svelte 5 (syntaxe moderne Runes `$state`, `$derived`, `$props`).
- **Composant cartographique :** `src/lib/components/Leaflet.svelte` utilisant `sveaflet` et tuiles OpenStreetMap avec 6 marqueurs de zones.
- **Visualisation graphique :** `src/routes/region/[slug]/+page.svelte` intégrant `svelteplot` pour le tracé interactif des séries temporelles (température, pluie, vent, probabilités).
- **Gestion des sessions :** Cookies HTTP-Only `access_token` gérés dans `src/routes/login/+page.server.js` et protégés par `src/routes/+layout.server.js`.

---

## 2. Logic Chain (Chaîne de Déduction et Rapprochement Critique)

1. **Prémisse 1 (Cadrage initial théorique) :** Le document de cadrage du 11 octobre 2026 prévoyait un MVP exploratoire sur 3 zones avec PostgreSQL, croisement NASA LHASA et 7 cultures génériques.
2. **Prémisse 2 (Réalité empirique du code) :** L'inspection du code démontre que les développeurs ont affiné le découpage à 5 provinces (avec gestion altitudinale fine de Bujumbura Rural), remplacé PostgreSQL par MongoDB Atlas (users) + cache SQLite local (météo), éliminé NASA LHASA pour des motifs de résolution spatiale non viable sur micro-bassins, et implémenté un système d'authentification robuste avec Argon2id et JWT.
3. **Prémisse 3 (Exigences académiques du canevas UPG) :** Le canevas exige une justification théorique de l'état de l'art (Chapitre II), une conception rigoureuse (Chapitre III), une description fidèle de l'implémentation réelle (Chapitre IV) et une **discussion comparative et critique entre le cadrage initial et la réalisation effective** (Chapitre V).
4. **Déduction logique :** Le rapport académique final ne doit pas faire semblant que PostgreSQL ou NASA LHASA sont présents dans le code. Au contraire, il doit valoriser ces divergences comme des choix d'ingénierie d'une grande maturité (allègement d'infrastructure, sécurité accrue, déontologie face aux faux positifs de glissements, respect des orientations agro-écologiques de l'ISABU).

---

## 3. Caveats (Limites de l'Investigation et Hypothèses)

- **Gestion des versions Git :** Les dépôts `weather-backend` et `weather-app` possèdent un dossier `.git` initialisé mais aucun commit n'a été finalisé (`Untracked files`). Le rapport devra signaler ce point comme un chantier de consolidation des bonnes pratiques de développement (Annexe F).
- **Absence de conteneurisation Docker :** Aucun `Dockerfile` n'est actuellement présent dans les projets ; le déploiement s'effectue en environnement local Python/Node. Ce point est documenté comme perspective d'amélioration immédiate.
- **CORS Middleware :** Aucun middleware `CORSMiddleware` n'est déclaré dans `weather-backend/app/main.py`. L'intégration actuelle fonctionne parce que les requêtes sont proxifiées via le serveur SvelteKit (`+page.server.js`), mais un appel direct client-side nécessitera l'ajout de ce middleware.

---

## 4. Conclusion

L'ensemble des exigences de la mission de spécification est atteint à 100%. Le fichier `c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\spec_miner_cadrage_1\analysis.md` met à disposition de l'orchestrateur et des futurs rédacteurs :
- Toutes les formulations textuelles pour l'Introduction Générale (contexte, problématique, objectifs SMART chiffrés).
- Le tableau complet des caractéristiques des 5 zones pilotes burundaises.
- L'analyse exhaustive des 7 sources scientifiques et documentaires (S1 à S7).
- Les fiches des 3 personas et les flux d'interaction détaillés.
- L'étude de faisabilité quadridimensionnelle complète.
- L'état de l'art comparatif complet (SvelteKit vs React/Vue, FastAPI vs Django/Node/Spring, MongoDB vs Postgres, OAuth2/JWT/Argon2id).
- Les tables des Exigences Fonctionnelles (EF-01 à EF-20) et Non-Fonctionnelles (ENF-01 à ENF-10) numérotées.
- La formalisation mathématique de toutes les règles métier et des seuils IGEBU/ISABU.
- La planification W1–W2 et les perspectives d'évolution pour la deuxième année.
- La matrice comparative détaillée Cadrage MVP vs Implémentation réelle.

---

## 5. Verification Method (Méthode de Vérification Indépendante)

Pour vérifier de manière indépendante les constats et données de ce rapport :
1. **Inspection des documents sources extraits :**
   - Ouvrir et vérifier `c:\Users\PC\Desktop\Projects\weather-app\DOCUMENT_1_CADRAGE_MVP.txt`
   - Ouvrir et vérifier `c:\Users\PC\Desktop\Projects\weather-app\DOCUMENT_2_CANEVAS_UPG.txt`
2. **Vérification de l'absence de PostgreSQL et présence de MongoDB :**
   - Inspecter `c:\Users\PC\Desktop\Projects\weather-backend\app\core\db.py` (ligne 1 : `from pymongo import MongoClient`)
   - Vérifier `c:\Users\PC\Desktop\Projects\weather-backend\pyproject.toml` (dépendance `pymongo>=4.19.0`, absence de `psycopg2` ou `sqlalchemy`)
3. **Vérification de l'exclusion de NASA LHASA :**
   - Inspecter `c:\Users\PC\Desktop\Projects\weather-backend\app\services\advice.py` (lignes 98–101)
4. **Vérification de l'exécution des tests unitaires backend :**
   - Lancer dans le terminal PowerShell :
     ```powershell
     cd c:\Users\PC\Desktop\Projects\weather-backend
     .venv\Scripts\pytest -v
     ```
     Constater le résultat : **31 passed in ~7.5s**.
5. **Vérification de l'analyse détaillée :**
   - Consulter `c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\spec_miner_cadrage_1\analysis.md`.
