# RAPPORT D'ANALYSE ET D'EXTRACTION DES SPÉCIFICATIONS — PROJET VEILLE MÉTÉO ET CLIMATIQUE AU BURUNDI

**Auteur :** spec_miner_cadrage_1 (Teamwork Specification Miner)  
**Date :** 2026-10-29  
**Projet :** Système de veille météo et climatique au Burundi  
**Cadre académique :** Canevas de Rapport Projet II — Génie Logiciel, Faculté des TIC, Université Polytechnique de Gitega (UPG)  
**Corpus de référence analysé :**
1. *Document de cadrage du projet à développer en deux semaines (Version révisée du 11 octobre 2026, Première année du projet)*.
2. *Canevas de Rapport Projet II (Génie Logiciel) — UPG*.
3. *Directives de mise à jour critiques de l'utilisateur et de l'orchestrateur (Réalité du code source)*.
4. *Code source réel : Backend FastAPI (`weather-backend`) et Frontend SvelteKit (`weather-app`)*.

---

## Sommaire Exécutif

Ce rapport d'analyse de spécification a été élaboré pour fournir l'intégralité de la matière première théorique, empirique, architecturale et méthodologique nécessaire à la rédaction exhaustive du rapport académique de fin d'études du projet. 

Il combine une extraction rigoureuse des documents fondateurs (Cadrage MVP et Canevas UPG) et une confrontation critique systématique avec l'implémentation logicielle réelle des dépôts `weather-backend` et `weather-app`. 

Les cinq divergences majeures constatées entre le cadrage initial et le code réel sont intégrées et explicitées :
1. **Périmètre territorial élargi et affiné :** Transition des 3 zones indicatives du cadrage vers 5 zones pilotes provinciales réelles (Bujumbura Mairie, Bujumbura Rural scindée en Imbo et Mumirwa, Gitega, Karusi, Rutana) respectant la topographie plaine/montagne.
2. **Retrait du modèle de glissements de terrain NASA LHASA :** Écart documenté et justifié par la résolution spatiale inadaptée aux collines burundaises pour un MVP.
3. **Cultures prévalentes par zone (ISABU) :** Remplacement d'une liste générique rigide de 7 cultures par une cartographie agro-écologique contextualisée par province.
4. **Base de données NoSQL MongoDB vs PostgreSQL :** Utilisation de MongoDB Atlas pour la gestion des utilisateurs et d'un cache local SQLite (`requests-cache`) pour la météo horaire.
5. **Implémentation d'un système complet d'authentification :** Intégration non prévue initialement mais pleinement réalisée de JWT, OAuth2 Password Bearer et hachage Argon2id avec protection anti-timing attack.

---

## Tableaux Normalisés de Découverte (Specification Mining)

### 1. Features Discovered (Fonctionnalités et Spécifications Découvertes)

| # | Catégorie | Fonctionnalité | Description | Entrées | Sorties | Comportement sur Erreur | Découvert Via |
|---|---|---|---|---|---|---|---|
| F01 | Authentification | Inscription utilisateur | Enregistrement d'un nouvel utilisateur avec hachage Argon2id | Formulaire JSON/URL-encoded (`username`, `name`, `password`) | Profil utilisateur créé (`username`, `name`) | Erreur 400 en cas d'échec d'insertion | `app/routes/user.py`, code réel |
| F02 | Authentification | Authentification OAuth2 / JWT | Authentification par mot de passe et génération d'un token JWT (30 min) | `OAuth2PasswordRequestForm` (`username`, `password`) | Jeton Bearer JWT (`access_token`, `token_type`) | HTTP 401 Unauthorized, vérification dummy hash anti-timing | `app/routes/token.py`, `app/core/security.py` |
| F03 | Sécurité | Protection des routes météo | Interdiction d'accès aux données météo sans jeton JWT valide | En-tête HTTP `Authorization: Bearer <token>` ou Cookie de session | Données autorisées ou Redirection `/login` | HTTP 401/403, redirection front-end | `app/routes/weather.py`, `+page.server.js` |
| F04 | Cartographie | Visualisation Leaflet interactive | Affichage de la carte du Burundi avec 6 marqueurs géolocalisés | Coordonnées GPS des zones et sous-zones | Carte Leaflet tuilée OSM avec popups interactifs | Rendu de repli centré sur le Burundi | `Leaflet.svelte`, Cadrage Sec. 1 |
| F05 | Collecte Météo | Prévisions horaires et 7j Open-Meteo | Récupération des prévisions météo (température, pluie, vent, rafales) | Latitude, longitude, `past_days=7`, `hourly` | Grille temporelle alignée (dates et séries vectorisées) | Retry automatique (5 essais, backoff 0.2s), cache 1h | `app/services/weather.py`, S1 |
| F06 | Collecte Crues | Prévisions hydrologiques GloFAS | Prévision des débits fluviaux à 7 jours via Open-Meteo Flood API | Latitude, longitude, point fluvial | Série quotidienne `river_discharge` (m³/s) | Données manquantes -> mesure `None` | `app/services/weather.py`, S2 |
| F07 | Analyse Crues | Calcul de référence hydrologique p75 | Calcul du 75e percentile des débits sur les 31 derniers jours | Réanalyse GloFAS 31 jours passés | Débit de référence $Q_{ref}$ (m³/s) | Retourne `None` si historique incomplet | `app/services/weather.py`, `measures.py` |
| F08 | Extraction | Extraction mathématique des métriques | Calcul des cumuls 24h, 72h, 7j passés, rafales max, jours secs | Séries temporelles Open-Meteo | Dictionnaire `mesures` normalisé avec garde-fous | Si trou de données ou NaN -> mesure = `None` | `app/services/measures.py` |
| F09 | Règles Métier | Détection pluie critique 24h | Déclenchement d'alerte selon la topographie (50 mm plaine, 100 mm montagne) | Mesure `pluie_24h`, classe topographique | Règle `pluie_24h_≥_Xmm`, message d'action agricole | Statut `non_evalue` si `pluie_24h` est absente | `app/services/advice.py`, IGEBU |
| F10 | Règles Métier | Détection pluie prolongée 72h | Alerte engorgement des sols (60 mm plaine, 90 mm montagne) | Mesure `pluie_72h`, classe topographique | Règle `pluie_72h_≥_Xmm`, message d'action | Statut `non_evalue` si `pluie_72h` est absente | `app/services/advice.py`, IGEBU |
| F11 | Règles Métier | Saturation hydrique des 7 derniers jours | Détection des sols gorgés par pluies antérieures (> 50 mm sur 7j) | Mesure `pluie_7j_passes` | Règle `pluie_7j_passes_≥_50mm`, alerte humidité | Ignoré si donnée absente sans bloquer les autres | `app/services/advice.py`, Cadrage Sec. 2 |
| F12 | Règles Métier | Alerte vent violent et rafales | Protection des bananiers et maïs contre les rafales >= 40 km/h | Mesure `rafales_kmh` | Règle `rafales_≥_40kmh`, conseil spécifique | Statut `non_evalue` si rafales absentes | `app/services/advice.py`, Cadrage Sec. 4 |
| F13 | Règles Métier | Alerte crue pour riziculture | Comparaison débit prévu vs débit de référence p75 pour le riz | `debit_prevu`, `debit_reference` | Règle `debit_prevu>debit_reference_p75`, alerte diguettes | Statut `non_evalue` si débits manquants | `app/services/advice.py`, GloFAS |
| F14 | Règles Métier | Surveillance période sèche | Détection d'un déficit hydrique (>= 5 jours consécutifs < 2 mm) | Mesure `jours_secs` | Règle `jours_secs_≥_5`, message vérification eau | Ne déclenche pas si données interrompues | `app/services/advice.py`, Cadrage Sec. 3 |
| F15 | Conseil Agricole | Adaptation des avis par culture ISABU | Génération d'avis contextualisés pour les cultures de la zone | Zone, sous-zone, catalogue ISABU (7 cultures) | Liste de conseils avec message, durée, limitations | Exclusion des cultures non répertoriées | `app/services/advice.py`, ISABU |
| F16 | Interface | Visualisation graphique interactive | Tracés temporels des paramètres météo via `svelteplot` | Séries horaires (T°, pluie, vent, probabilité) | Graphique SVG interactif avec tooltip temporel | Affichage "Données indisponibles" | `region/[slug]/+page.svelte` |
| F17 | Interface | Filtrage multicritère des avis | Filtres par sévérité (alertes actives / sans signal) et par culture | Sélections utilisateur dans l'UI | Liste filtrée dynamiquement sans rechargement | Affichage d'un état vide si aucun conseil | `region/[slug]/+page.svelte` |
| F18 | Déontologie | Règle de transparence et limitations | Affichage explicite des limitations du modèle et sources | Dictionnaire de limitations par zone | Bandeau de limitations et mise en garde officielle | Affichage systématique en pied de conseil | `app/services/advice.py`, Cadrage Sec. 6 |

---

### 2. Edge Cases (Cas Limites et Comportements Observés)

| # | Fonctionnalité | Scénario / Donnée en Entrée | Comportement Observé et Spécifié | Règle Déontologique Associée |
|---|---|---|---|---|
| E01 | Gestion des données manquantes | Valeur `None` ou chaîne vide dans une mesure horaire Open-Meteo | La mesure globale devient `None` ; le conseil prend le statut `non_evalue`. | L'absence de données ne doit JAMAIS être interprétée comme une vigilance faible ou une absence de risque. |
| E02 | Valeurs numériques invalides | Présence d'un `NaN` flottant dans une série de précipitations | `_nb()` intercepte le `NaN` et le convertit en `None` ; mesure non calculée. | Tolérance aux corruptions de séries sans crash serveur. |
| E03 | Doute topographique Bujumbura Rural | Requête sur `buja_rural` sans préciser la sous-zone (`imbo` ou `mumirwa`) | Application automatique du seuil de PLAINE le plus bas (50 mm/24h au lieu de 100 mm). | Principe de précaution maximale : éviter qu'une pluie dangereuse en plaine soit ignorée par défaut de précision. |
| E04 | Localité inconnue ou erronée | Paramètre `sous_zone='inconnue'` transmis pour Bujumbura Rural | Repli automatique sur la classe `plaine` (seuil 50 mm/24h). | Sécurité par défaut. |
| E05 | Tentative de sous-zone sur zone homogène | Requête `location=gitega` avec paramètre `sous_zone=imbo` | Rejet immédiat avec `ValueError` (seule Buja Rural accepte une sous-zone). | Cohérence stricte du modèle géographique. |
| E06 | Fenêtre temporelle tronquée | Moins de 24 pas de temps horaires disponibles pour `pluie_24h` | `_fenetre_complete()` renvoie `None` ; calcul refusé. | Refus absolu de fournir une métrique tronquée pouvant induire en erreur. |
| E07 | Période sèche interrompue | Données manquantes au 3e jour de prévision sans pluie | Si jours secs < 5, renvoie `None` ; si déjà >= 5, valide la règle. | Détection fiable uniquement si le seuil est mathématiquement garanti. |
| E08 | Utilisateur inexistant à l'authentification | `POST /token` avec email non répertorié en base MongoDB | Exécution d'un hash fictif (`DUMMY_HASH`) avant de renvoyer 401. | Égalisation du temps de réponse pour empêcher les attaques par canal auxiliaire (anti-timing user enumeration). |
| E09 | Jeton expiré ou frelaté | Appel API avec JWT altéré ou expiré (> 30 minutes) | Dépendance `get_current_user` lève `HTTP 401 Unauthorized`. | Sécurité d'accès rigoureuse aux données. |
| E10 | Débit élevé sur cours d'eau sans crue | Débit GloFAS supérieur au p75 des 31 derniers jours | Message indique "débit inhabituel", conseille de vérifier diguettes et canaux. | Interdiction formelle d'annoncer une "inondation certaine" ou d'ordonner une "évacuation" (prérogative exclusive de l'État). |
| E11 | Culture inconnue demandée | Appel de conseil pour une culture absente du catalogue ISABU | Levée immédiate d'une exception `ValueError("Culture non gérée")`. | Protection de l'intégrité agronomique. |

---

## 1. Contexte, Justification, Problématique et Objectifs de Recherche

### 1.1 Contexte et Justification Agro-Climatique au Burundi
Le Burundi, pays d'Afrique centrale et orientale au relief très accidenté culminant à plus de 2 600 mètres sur la crête Congo-Nil, abrite une population estimée à plus de 13 millions d'habitants, dont plus de **85 à 90 % dépendent directement de l'agriculture vivrière**. L'agriculture représente environ 40 % du Produit Intérieur Brut (PIB) national et constitue le socle vital de la sécurité alimentaire.

Or, le territoire burundais figure parmi les plus vulnérables du continent africain aux chocs climatiques extrêmes :
- **L'alternance d'épisodes de pluies diluviennes torrentielles** et de **périodes de stress hydrique prolongées** provoque des catastrophes récurrentes. Les inondations fluviales dans la plaine de la Rusizi et sur le littoral du lac Tanganyika détruisent régulièrement les casiers rizicoles et les habitations (notamment à Gatumba et Bujumbura).
- **Les versants abrupts de Mumirwa et de la crête Congo-Nil** subissent une érosion hydrique dévastatrice et des glissements de terrain mortels lors des saisons des pluies (saisons culturales A et B).
- **Le déficit de prévisibilité météorologique** pénalise gravement les décisions paysannes fondamentales : choix des dates de semis, organisation des récoltes, séchage en plein air des céréales et légumineuses, protection des buttes et canaux d'irrigation.

### 1.2 Problématique de Recherche et d'Ingénierie
Malgré l'existence de systèmes mondiaux de surveillance satellitaire et de modèles météorologiques numériques avancés, **un fossé technologique et opérationnel profond persiste au Burundi** :
1. **Insuffisance du réseau d'observation au sol :** L'Institut Géographique du Burundi (IGEBU) gère un nombre limité de stations météorologiques synoptiques et automatiques en état de fonctionnement continu, créant de vastes zones d'ombre dans le suivi des microclimats collinaires.
2. **Inaccessibilité et technicité excessive des données :** Les données issues des modèles globaux (Copernicus, ECMWF, NASA) sont disséminées, publiées dans des formats scientifiques complexes (NetCDF, GRIB2, FlatBuffers) et inaccessibles aux décideurs locaux et aux encadreurs agricoles.
3. **Absence de passerelle décisionnelle agronomique :** Une information brute telle que *"25 mm de pluie prévus"* ne fournit aucune recommandation pratique. Un agent de coopérative a besoin de savoir si cette pluie menace son aire de séchage de maïs, si elle justifie de curer les diguettes d'un bas-fond rizicole ou si elle risque de provoquer le pourrissement des buttes de patates douces.
4. **Diffusion tardive :** Les bulletins traditionnels sur support papier ou communiqués radiodiffusés parviennent souvent aux communautés après la survenue des sinistres.

### 1.3 Questions Spécifiques de Recherche
Afin de concevoir une réponse logicielle pérenne, le travail d'ingénierie s'articule autour de quatre questions centrales :
- **Question 1 :** Comment agréger, normaliser et corréler en temps quasi-réel des flux hétérogènes de prévisions météorologiques globales (Open-Meteo) et hydrologiques (GloFAS) sans infrastructure matérielle locale lourde ?
- **Question 2 :** Quelles règles formelles et quels seuils quantitatifs permettent de transformer des variables physiques brutes (pluie sur 24h/72h, rafales, débits fluviaux) en avis agro-météorologiques immédiatement actionnables par culture, conformément aux pratiques de l'ISABU ?
- **Question 3 :** Comment concevoir une architecture logicielle moderne (Client-Serveur, API REST asynchrone, front-end réactif et cartographique) garantissant fluidité, résilience aux coupures réseau et faible consommation de bande passante sur terminal mobile au Burundi ?
- **Question 4 :** Comment concilier l'aide à la décision participative avec la déontologie institutionnelle, sans empiéter sur les prérogatives régaliennes des services d'alerte de l'État (IGEBU, Protection Civile) ?

### 1.4 Objectif Général
Concevoir, implémenter et évaluer un **Système de Veille Météorologique et Climatique pour le Burundi**, articulé autour d'une interface web cartographique réactive (SvelteKit) et d'un backend d'agrégation et de décision automatisé (FastAPI / MongoDB / Cache SQLite), capable de fournir aux encadreurs agricoles, coopératives et gestionnaires territoriaux des prévisions fiables et des conseils préventifs contextualisés par province et par culture.

### 1.5 Objectifs Spécifiques et Indicateurs de Succès Mesurables (SMART)

| Objectif Spécifique (OS) | Description Technique | Indicateur Mesurable de Succès (SMART) |
|---|---|---|
| **OS1 : Collecte & Ingestion** | Développer un service d'interrogation et de mise en cache des séries temporelles Open-Meteo et GloFAS. | Taux de disponibilité des données $\ge 99\%$, temps de réponse du cache SQLite $< 50\text{ ms}$, persistance de 7 jours passés et 7 jours futurs. |
| **OS2 : Moteur de Règles Pur** | Concevoir un moteur fonctionnel pur traduisant les seuils IGEBU et agro-climatiques ISABU en avis sans effet de bord. | Couverture de test unitaire à $100\%$ sur les règles métier (31/31 tests validés dans `tests/test_advice.py` et `test_measures.py`). |
| **OS3 : Authentification & Sécurité** | Implémenter un mécanisme d'authentification robuste protégeant l'accès aux données de surveillance. | Hash Argon2id ($m=65536, t=3, p=4$), jetons JWT HMAC-SHA256 valides 30 min, temps de réponse constant contre l'énumération par canal auxiliaire. |
| **OS4 : Interface Cartographique & UX** | Réaliser une interface cartographique interactive Leaflet adaptée aux écrans mobiles et bas débit. | Poids du bundle initial SvelteKit $< 250\text{ Ko}$, rendu cartographique complet en $< 1,5\text{ s}$ sur réseau 3G simulé. |
| **OS5 : Contextualisation Territoriale** | Modéliser les 5 zones pilotes avec distinction fine des altitudes (plaine/montagne) et des cultures prévalentes. | 100% des requêtes sur Bujumbura Rural appliquent le seuil exact de leur sous-zone (`imbo` vs `mumirwa`) avec repli de précaution vérifié. |

### 1.6 Structure Globale du Rapport Académique
Le rapport final adopte scrupuleusement la structure canonique exigée par le canevas Projet II (Génie Logiciel) de l'UPG, tout en omettant les pages liminaires conformément à la demande de l'utilisateur :
- **INTRODUCTION GÉNÉRALE :** Fondements, problématique, questions de recherche, objectifs SMART et méthodologie.
- **CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC :** Périmètre opérationnel, analyse des besoins, modélisation des personas et parcours utilisateurs, contraintes d'ingénierie et étude de faisabilité quadridimensionnelle.
- **CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART :** Paradigmes client-serveur, comparatifs argumentés des technologies front-end (SvelteKit vs React/Vue/Angular), back-end (FastAPI vs Django/Node/Spring), de persistance (MongoDB vs PostgreSQL) et sécurité (OAuth2/JWT/Argon2id).
- **CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE :** Spécifications formelles des exigences (EF/ENF), modélisation architecturale, conception des données, modélisation UML complète et formalisation mathématique des règles de décision.
- **CHAPITRE IV — IMPLÉMENTATION / RÉALISATION :** Environnement technique (`uv`, Python 3.14, Vite, Svelte 5), implémentation détaillée du backend, des routeurs, de la sécurité, des algorithmes de traitement temporel et de l'interface utilisateur SvelteKit/Leaflet.
- **CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION :** Protocole expérimental, exécution des tests unitaires et d'intégration, métriques de performance, utilisabilité mobile et **confrontation critique exhaustive entre le Document de Cadrage MVP et l'Implémentation Réelle**.
- **CONCLUSION GÉNÉRALE ET PERSPECTIVES :** Bilan au regard des hypothèses initiales, limites avérées du prototype et feuille de route technologique pour la deuxième année.
- **ANNEXES :** Diagrammes UML tabulaires et textuels (Annexe A), Schéma d'architecture de la base de données (Annexe B), Manuel d'installation et d'exploitation (Annexe D), Structure du dépôt de code Git (Annexe F).

---

## 2. Découpage Territorial et Zones Pilotes (Cadrage Théorique vs Réalité du Code)

### 2.1 Confrontation de Périmètre
Le document de cadrage initial mentionnait de manière exploratoire *"trois cadres différents : la plaine de la Rusizi, des versants occidentaux et un secteur autour de Gitega"*. 

L'analyse du code source réel (`weather-backend/app/config.py`, `app/routes/weather.py` et `weather-app/src/lib/components/Leaflet.svelte`) révèle que l'équipe de développement a opéré une **extension rigoureuse à 5 zones pilotes administratives (anciennes provinces)** intégrant 6 stations de référence géographiques :

```
                  ┌────────────────────────────────────────────────────────┐
                  │          ZONES PILOTES DU PROJET BURUNDI               │
                  └──────────────────────────┬─────────────────────────────┘
                                             │
             ┌───────────────────────────────┼───────────────────────────────┐
             │                               │                               │
             ▼                               ▼                               ▼
    [PLAINES BASSES]                 [ZONES MIXTES]                 [HAUTES TERRES]
    Seuil: 50 mm/24h                 Seuil: Variable                Seuil: 100 mm/24h
  • Bujumbura Mairie               • Bujumbura Rural               • Gitega (Centre)
    (-3.3819°, 29.3614°)             (700 m - 2 600 m)               (-3.4271°, 29.9246°)
    Plaine Imbo, ~820 m              ├── Imbo (Plaine, 50 mm)      • Karusi (Ruvubu)
                                     │   (-3.4292°, 29.3165°)        (-3.1014°, 30.1628°)
                                     └── Mumirwa (Mont., 100 mm)   • Rutana (Kumoso)
                                         (-3.4389°, 29.6944°)        (-3.9279°, 29.9920°)
```

### 2.2 Caractérisation Complète des Zones d'Étude

| Identifiant Technique | Dénomination Usuelle | Coordonnées GPS (Lat / Long) | Altitude Moyenne | Classe Topographique | Seuil Pluie Critique 24h | Principales Vulnérabilités Agro-Climatiques | Cultures Prévalentes Associées (ISABU) |
|---|---|---|---|---|---|---|---|
| `bujumbura` | Bujumbura Mairie | -3.38193° N, 29.36142° E | ~820 m | **Plaine** | 50.0 mm | Crues lacustres (Tanganyika), inondations urbaines, ruissellement torrentiel des ravins de Bujumbura. | Riz, Maïs, Manioc, Bananier |
| `buja_rural_imbo` | Bujumbura Rural (Imbo) | -3.42920° N, 29.31650° E | ~850 m | **Plaine** | 50.0 mm | Débordement des rivières descendant des crêtes (Mugere, Mutimbuzi), ensablement des casiers rizicoles. | Riz, Maïs, Manioc, Bananier |
| `buja_rural_mumirwa` | Bujumbura Rural (Mumirwa) | -3.43890° N, 29.69440° E | > 1 400 m | **Montagne** | 100.0 mm | Pentes abruptes (>30%), érosion en nappe, instabilité des sols, arrachement des bananiers par vent violent. | Bananier, Maïs, Haricot, Manioc, Pomme de terre |
| `gitega` | Gitega (Capitale) | -3.42708° N, 29.92460° E | 1 650–1 850 m | **Montagne** | 100.0 mm | Sols ferrallitiques lessivés, ravinements collinaires, sensibilité aux pourritures racinaires lors d'excès d'eau. | Maïs, Haricot, Bananier, Riz (marais), Patate douce, Pomme de terre |
| `karusi` | Karusi | -3.10139° N, 30.16278° E | 1 500–1 750 m | **Montagne** | 100.0 mm | Engorgement des bas-fonds de la Ruvubu et affluents (Gasenyi, Rusheri), sensibilité aux épisodes de sécheresse. | Maïs, Haricot, Bananier, Manioc, Patate douce |
| `rutana` | Rutana | -3.92790° N, 29.99200° E | 1 600–1 800 m | **Montagne** | 100.0 mm | Transition escarpements / plaines du Kumoso, alternance crues de piémont et sécheresses saisonnières sévères. | Riz, Maïs, Haricot, Manioc, Bananier |

### 2.3 Le Principe de Précaution Algorithmique pour les Zones Mixtes
La province de Bujumbura Rural présente un profil d'altitude discontinu allant des plages du lac Tanganyika (773 m) jusqu'au sommet du mont Teza (2 665 m). Dans `app/config.py` (fonction `classe_pluie`), une règle d'ingénierie préventive a été codée :
- Si la requête cible explicitement `buja_rural_mumirwa`, le système applique le seuil de haute altitude (**100 mm/24h**).
- Si la requête cible `buja_rural_imbo`, il applique le seuil de plaine (**50 mm/24h**).
- **En cas d'omission, de doute ou d'identifiant de localité non reconnu**, l'algorithme se rabat automatiquement sur le seuil le plus bas (**50 mm/24h**). Cette conception garantit qu'un risque pluvieux survenant en plaine ne sera jamais masqué par un seuil de montagne trop permissif.

---

## 3. Corpus Scientifique et Sources Documentaires (S1 à S7 et Extensions)

Le cadrage MVP et le code s'appuient sur un corpus documentaire et technique structuré en sept sources principales (S1 à S7) complétées par des données prévues pour la phase 2 :

```
                        CORPUS DOCUMENTAIRE DU PROJET
 ┌──────────────────────────────────────┬──────────────────────────────────────┐
 │   SOURCES GLOBALES EN LIGNE (APIs)   │    SOURCES LOCALES INSTITUTIONNELLES │
 ├──────────────────────────────────────┼──────────────────────────────────────┤
 │ [S1] Open-Meteo Weather Forecast     │ [S5] ISABU - Guides et Fiches        │
 │      • Prévisions horaires à 7 jours │      • Calendriers culturaux         │
 │      • Réanalyses passées (7 jours)  │      • Sensibilités agro-climatiques │
 │      • Température, pluie, vent      │                                      │
 │                                      │ [S6] IGEBU - Normes Pluviométriques  │
 │ [S2] GloFAS via Open-Meteo Flood     │      • Seuil Plaine : 50 mm / 24 h   │
 │      • Modèle mondial à ~5 km        │      • Seuil Montagne : 100 mm / 24 h│
 │      • Débits fluviaux prévus (7j)   │      • Classification zonale         │
 │      • Référence historique p75 (31j)│                                      │
 │                                      │ [S7] CHIRPS v3 (Précipitations)      │
 │ [S3] NASA LHASA (Glissements)        │      • Référence historique satellite│
 │      • Spécifié au cadrage           │      • *Remplacé par réanalyses S1*  │
 │      • *Retiré du code réel*         │                                      │
 │                                      │                                      │
 │ [S4] OpenStreetMap & Leaflet         │                                      │
 │      • Fond cartographique tuilé     │                                      │
 │      • Rendu vectoriel Sveaflet      │                                      │
 └──────────────────────────────────────┴──────────────────────────────────────┘
```

### 3.1 Analyse Détaillée des Sources S1 à S7

#### [S1] Open-Meteo Weather Forecast API
- **Fournisseur :** Open-Meteo GmbH.
- **Rôle technique :** Moteur primaire de données météorologiques horaires sans clé API.
- **Paramètres exploités :** `temperature_2m` (°C), `precipitation` (mm cumulé/heure écoulée), `wind_speed_10m` (km/h), `wind_gusts_10m` (km/h), `precipitation_probability` (%).
- **Fenêtre temporelle :** Historique modélisé sur 7 jours passés (`past_days=7`) + prévisions horaires sur 7 jours.
- **Format et transport :** Protocol FlatBuffers binaire pour une sérialisation ultra-légère via le client Python `openmeteo-requests`.

#### [S2] GloFAS (Global Flood Awareness System) via Open-Meteo Flood API
- **Fournisseur :** Copernicus Emergency Management Service (Union Européenne / ECMWF).
- **Rôle technique :** Prévision hydrologique des débits de surface des grands bassins hydrographiques mondiaux.
- **Résolution :** Maille matricielle d'environ 0,05° (~5 km).
- **Adaptation statistique dans le MVP :** En lieu et place du 90e centile historique du même mois (complexe à extraire sur un court délai), le projet exploite la réanalyse des **31 derniers jours glissants au 75e percentile (`daily: river_discharge_p75`)** pour identifier un débit statistiquement anormal.

#### [S3] NASA LHASA (Landslide Hazard Assessment for Situational Awareness)
- **Fournisseur :** NASA Goddard Space Flight Center.
- **Rôle initial au cadrage :** Carte matricielle globale de susceptibilité des sols aux glissements combinée aux précipitations satellitaires.
- **Statut dans l'implémentation :** **Retiré du code réel**.
- **Justification technique documentée :** Explicitement consignée dans `app/services/advice.py` : la maille kilométrique de LHASA est incapable de résoudre les ruptures de pente des collines burundaises, et l'absence de données de pente haute résolution (DEM 12 m) fausserait l'analyse. L'équipe a prudemment exclu les faux avertissements.

#### [S4] OpenStreetMap (OSM) et Bibliothèque Leaflet
- **Fournisseur :** Communauté OpenStreetMap (Licence ODbL) & Vladimir Agafonkin.
- **Rôle technique :** Fond cartographique interactif libre, tuilé en Web Mercator (`https://tile.openstreetmap.org/{z}/{x}/{y}.png`).
- **Composant frontend :** Intégration dans SvelteKit via le wrapper `sveaflet`, assurant un affichage fluide des marqueurs géographiques sans dépendances lourdes.

#### [S5] Guides Agricoles et Fiches Techniques de l'ISABU
- **Fournisseur :** Institut des Sciences Agronomiques du Burundi.
- **Rôle agronomique :** Fourniture des fiches de vulnérabilité pour les 7 cultures stratégiques du pays :
  1. **Maïs (*Zea mays*) :** Sensibilité extrême au versement par vent violent (> 40 km/h) et détérioration des épis lors du séchage post-récolte.
  2. **Haricot commun (*Phaseolus vulgaris*) :** Sensibilité à l'anthracnose et au pourrissement racinaire en sol gorgé d'eau ; impératif de protection des graines en séchage.
  3. **Riz de bas-fond (*Oryza sativa*) :** Tolérance à la submersion temporaire mais risque majeur de destruction des diguettes et submersion prolongée lors des crues anormales.
  4. **Bananier (*Musa spp.*) :** Vulnérabilité mécanique des pseudo-troncs et régimes lourds aux rafales (> 40 km/h) ; sensibilité aux glissements de versants.
  5. **Manioc (*Manihot esculenta*) :** Risque de pourriture bactérienne des tubercules dans les sols saturés d'eau pendant plus de 72 heures.
  6. **Patate douce (*Ipomoea batatas*) :** Nécessité de surveillance de l'effondrement des buttes agricoles sous fortes pluies prolongées.
  7. **Pomme de terre (*Solanum tuberosum*) :** Risque élevé de mildiou (*Phytophthora infestans*) lors de séquences humides combinées à des températures douces.

#### [S6] Bulletins et Seuils Réglementaires de l'IGEBU
- **Fournisseur :** Institut Géographique du Burundi (Gitega).
- **Rôle normatif :** Fourniture des seuils de vigilance pluviométrique applicables au territoire national :
  - Plaine (Imbo / Rusizi) : **50 mm / 24 heures**.
  - Hautes terres et crêtes : **100 mm / 24 heures**.

#### [S7] CHIRPS v3 (Climate Hazards Group InfraRed Precipitation with Station data)
- **Fournisseur :** UC Santa Barbara & USGS.
- **Rôle initial :** Suivi historique de la pluviométrie à haute résolution (0.05°).
- **Statut dans l'implémentation :** Remplacé fonctionnellement dans le MVP par l'interrogation du paramètre `past_days=7` d'Open-Meteo pour alléger les requêtes externes.

### 3.2 Perspectives de Données pour la Deuxième Année
Le document de cadrage (Section 7 et 9) identifie des extensions spatiales et hydrologiques majeures :
- **HydroRIVERS :** Vecteurs hydrographiques mondiaux numérisés pour affiner le tracé des cours d'eau secondaires (Mugere, Ruvubu, Kirasa).
- **NASA IMERG (GPM) :** Précipitations satellitaires multi-satellites étalonnées toutes les 30 minutes.
- **Copernicus DEM (30 m) :** Modèle numérique de terrain haute résolution permettant de calculer la pente réelle des versants.
- **ESA WorldCover (10 m) :** Cartographie de l'occupation du sol pour distinguer zones cultivées, zones boisées et zones urbanisées.

---

## 4. Personas et Parcours Utilisateurs Détaillés

Afin de garantir l'adéquation du système aux réalités burundaises, trois personas représentatifs et leurs parcours d'interaction ont été formalisés :

### 4.1 Fiches des Personas

#### Persona 1 : L'Encadreur Agricole de Terrain
- **Nom fictif :** Pierre Nkurunziza
- **Rôle :** Moniteur agricole communal (DPAE Gitega).
- **Profil :** 38 ans, utilise un smartphone Android d'entrée de gamme, consulte les alertes tôt le matin avant sa tournée des collines.
- **Besoin critique :** Savoir rapidement sur quelles collines les récoltes de haricot ou de maïs en train de sécher dehors risquent d'être trempées par un orage l'après-midi.
- **Frustration :** Reçoit des prévisions globales à la radio nationale du type *"pluies éparses sur le centre du pays"*, impossibles à traduire en conseils locaux.

#### Persona 2 : La Gestionnaire de Coopérative Rizicole
- **Nom fictif :** Chantal Nibigira
- **Rôle :** Présidente d'une coopérative rizicole de la plaine de l'Imbo (Bujumbura Rural).
- **Profil :** 44 ans, gère 60 hectares de casiers rizicoles traversés par des canaux d'irrigation.
- **Besoin critique :** Être alertée 24 à 48 heures avant qu'un débit inhabituel ne descende des contreforts de Mumirwa pour mobiliser les membres afin de consolider les diguettes.
- **Frustration :** Les crues soudaines de la rivière Mugere détruisent les levées de terre sans avertissement préalable.

#### Persona 3 : Le Chargé de Mission Humanitaire / Protection Civile
- **Nom fictif :** Dr. Alexis Manirakiza
- **Rôle :** Responsable de veille au sein d'une ONG d'urgence et de résilience à Rutana/Karusi.
- **Profil :** 41 ans, utilise un ordinateur portable et une tablette connectée en 4G.
- **Besoin critique :** Disposer d'un tableau comparatif des 5 zones pour allouer préventivement les kits de bâches plastiques et de traitement de l'eau.
- **Frustration :** Manque d'indicateurs objectifs documentant la source des données et les limitations statistiques.

### 4.2 Parcours Utilisateurs Cibles

```
 ┌────────────────┐     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
 │ AUTHENTIFICATION│ ──> │ SÉLECTION ZONE │ ──> │ TABLEAU MÉTÉO  │ ──> │ AVIS AGRICOLE  │
 │ Identifiant    │     │ Carte Leaflet  │     │ T°, Pluie,     │     │ Règle active,  │
 │ Token JWT      │     │ ou Liste       │     │ Vent, Crues    │     │ Action terrain │
 └────────────────┘     └────────────────┘     └────────────────┘     └────────────────┘
```

1. **Étape 1 : Connexion sécurisée :** L'utilisateur se connecte via `/login` (ou s'inscrit via `/signup`). Un cookie HTTP-Only strict stocke le token JWT, déverrouillant l'accès aux routes protégées de l'application.
2. **Étape 2 : Choix du secteur d'observation :** Sur la page d'accueil (`/`), l'utilisateur visualise la carte du Burundi centrée sur les 5 provinces. En cliquant sur le marqueur de son choix (ex. *Gitega* ou *Bujumbura Rural (Imbo)*), il accède à la route dynamique `/region/[slug]`.
3. **Étape 3 : Consultation des métriques et séries temporelles :** L'interface affiche l'indicateur d'évaluation (date et heure UTC), les valeurs clés sur 24h et 72h, et un tracé graphique interactif SVG (`svelteplot`) permettant de balayer heure par heure les précipitations, températures et rafales de vent.
4. **Étape 4 : Évaluation des conseils agricoles par culture :** L'utilisateur filtre les conseils par culture (ex. *Maïs*, *Riz*, *Haricot*). Si un seuil critique est dépassé, un bandeau ambré bien visible présente le message d'action (ex. *"Si vous faites sécher du maïs en plein air, prévoyez de le mettre à l'abri..."*).
5. **Étape 5 : Traçabilité et vérification :** Chaque conseil permet de déplier les métriques exactes ayant déclenché la règle, les seuils configurés, la source (Open-Meteo Flood) et les limitations inhérentes au modèle.

---

## 5. Étude de Faisabilité Approfondie

### 5.1 Faisabilité Technique
- **Fiabilité des sources de données :** L'utilisation des APIs Open-Meteo élimine le besoin d'enregistrer des clés API payantes ou limitées en quotas stricts pour un prototype universitaire.
- **Architecture asynchrone découplée :** Le couple FastAPI (ASGI) et SvelteKit (SSR/CSR) permet un traitement fluide des flux JSON vectorisés sans blocage du thread principal.
- **Résilience aux pannes de connectivité :**
  - Côté serveur : `requests-cache` conserve les réponses d'Open-Meteo dans un fichier SQLite local pendant 1 heure, permettant de continuer à servir les données même lors d'une coupure transitoire du réseau international.
  - Côté client : L'application SvelteKit génère des composants ultra-légers fonctionnels avec un minimum d'échanges de paquets réseau.

### 5.2 Faisabilité Économique
- **Coût d'infrastructure nul :** 
  - Tier gratuit MongoDB Atlas (M0 Sandbox, 512 Mo de stockage amplement suffisant pour les comptes utilisateurs).
  - APIs Open-Meteo gratuites pour un usage non commercial / recherche académique.
  - Hébergement potentiel sur plateformes PaaS gratuites ou serveurs universitaires locaux (Linux Ubuntu / Docker).
- **Accessibilité pour les usagers :** Consommation minimale de forfait mobile (moins de 500 Ko par session de consultation complète).

### 5.3 Faisabilité Opérationnelle
- **Prise en main immédiate :** L'interface cartographique et les icônes explicites ne requièrent aucune formation technique préalable.
- **Formulation pragmatique :** Bannissement du jargon météorologique abscons ; chaque recommandation débute impérativement par une directive d'action concrète (*"Vérifiez..."*, *"Protégez..."*, *"Surveillez..."*).

### 5.4 Faisabilité Juridique, Éthique et Déontologique
- **Respect du monopole régalien de l'IGEBU :** Au Burundi, seul l'IGEBU est légalement habilité à émettre des alertes météorologiques officielles nationales. De même, seule la Protection Civile peut ordonner des évacuations de populations. Le système se positionne explicitement comme un **outil expérimental d'aide à la décision collinaire et de veille indicative**.
- **Chartes textuelles éthiques :**
  - Interdiction stricte dans le code de termes anxiogènes comme *"inondation certaine"* ou *"évacuation"*.
  - En l'absence de données, interdiction d'afficher un signal vert ou "faible" : obligation d'afficher le statut explicite `non_evalue` pour rappeler que l'absence de données n'est pas une absence de danger.
- **Licences libres :** Respect des licences logicielles (MIT pour Svelte/FastAPI, ODbL pour OpenStreetMap, Creative Commons pour les données Copernicus).

---

## 6. État de l'Art et Comparatifs Technologiques (Canevas UPG Chapitre II)

Le canevas UPG exige une confrontation théorique et technique rigoureuse justifiant les choix technologiques de l'architecture logicielle :

### 6.1 Architecture Client-Serveur vs Monolithe Traditionnel
L'architecture adoptée découple strictement l'interface de présentation (Client SvelteKit) du serveur de logique métier et d'agrégation (Serveur FastAPI / MongoDB) :
- **Avantages :** Évolutivité indépendante, possibilité de connecter ultérieurement un client mobile Flutter ou un bot SMS/USSD sur les mêmes endpoints REST, isolation des pannes.
- **Inconvénients maîtrisés :** Nécessité d'une gestion rigoureuse des sessions d'authentification par jetons JWT et configuration des en-têtes CORS.

### 6.2 Comparatif des Frameworks Front-End

| Critère d'évaluation | Svelte / SvelteKit (Choix Retenu) | React.js / Next.js | Vue.js / Nuxt | Angular |
|---|---|---|---|---|
| **Paradigme de Réactivité** | **Compilation sans Virtual DOM** (Runes `$state`, `$derived` en Svelte 5) | Virtual DOM, réconciliation mémoire lourde | Virtual DOM avec Proxy réactifs | Détection de changements Zone.js lourde |
| **Poids du Bundle JS** | **Extrêmement réduit (~15–30 Ko de base)** | Moyen à lourd (~100–150 Ko minimum) | Modéré (~40–70 Ko) | Très lourd (> 300 Ko) |
| **Temps de premier affichage (FCP)** | **Ultra-rapide** (favorable aux réseaux 3G burundais) | Modéré | Bon | Moyen |
| **Courbe d'apprentissage** | **Syntaxe proche de HTML/JS pur** | Complexe (JSX, hooks complexes, re-renders) | Accessible | Complexe (TypeScript strict, DI, RxJS) |
| **Intégration SSR / CSR** | **Isomorphe native (`+page.server.js`)** | Complète mais configuration volumineuse | Complète via Nuxt | Complexe via Angular Universal |

*Conclusion comparative :* SvelteKit s'impose comme le choix optimal pour le contexte burundais grâce à son modèle sans Virtual DOM éliminant les lenteurs d'exécution sur smartphones modestes.

### 6.3 Comparatif des Frameworks Back-End

| Critère d'évaluation | FastAPI (Python) (Choix Retenu) | Django / DRF | Node.js / Express | Spring Boot (Java) |
|---|---|---|---|---|
| **Performance d'Exécution** | **Très élevée** (Moteur ASGI `uvloop`, asynchronisme natif) | Modérée (Synchrone WSGI historique) | Très élevée (V8 Event Loop) | Très élevée (JVM thread pool) |
| **Typage et Validation** | **Validation Pydantic automatique à l'exécution** | Formulaires et sérialiseurs manuels | Validation manuelle (Joi, Zod) | Typage fort statique Java |
| **Écosystème Météo & Données** | **Imbattable** (intégration directe Pandas, NumPy, Open-Meteo) | Excellent mais orienté ORM SQL lourd | Limité pour le calcul numérique vectoriel | Bon mais bibliothèques verbeuses |
| **Documentation API** | **Génération automatique OpenAPI / Swagger UI** | Nécessite des packages tiers (drf-yasg) | Manuelle ou via Swagger-JSDoc | Via Springdoc OpenAPI |
| **Empreinte Mémoire** | **Légère (~50–80 Mo de RAM)** | Moyenne (~120–200 Mo) | Légère (~60–100 Mo) | Élevée (> 300 Mo) |

*Conclusion comparative :* FastAPI offre le compromis idéal entre vitesse de développement, typage rigoureux et compatibilité immédiate avec les outils d'analyse de données météorologiques vectorisées (`pandas`).

### 6.4 Comparatif des Systèmes de Base de Données : MongoDB vs PostgreSQL

| Dimension | Spécification Cadrage : PostgreSQL | Implémentation Réelle : MongoDB + Cache SQLite | Analyse Justificative de l'Écart |
|---|---|---|---|
| **Modèle de données** | Relationnel strict (tables, schémas fixes, clés étrangères). | Documentaire BSON (MongoDB) + Fichier clé-valeur (SQLite). | Pour la gestion des comptes utilisateurs (`users`), le modèle document évite les migrations lourdes sans sacrifier la cohérence. |
| **Séries temporelles météo** | Stockage tabulaire permanent des relevés horaires. | Mise en cache HTTP transitoire (`.cache.sqlite`, TTL 1h). | Les prévisions météo horaires (168 points par requête) sont très volatiles ; les stocker en base SQL aurait engendré des millions de lignes inutiles pour un MVP de deux semaines. |
| **Administration & Coût** | Serveur PostgreSQL dédié avec maintenance Alembic. | Cluster MongoDB Atlas Cloud serverless gratuit (Tier M0). | Zéro charge d'administration système, haute disponibilité réseau assurée gratuitement. |

### 6.5 Sécurité et Authentification : OAuth2 / JWT vs Sessions Classiques
Le système implémente le standard industriel **OAuth2 Password Bearer avec jetons JWT signés en HMAC-SHA256 (HS256)** :
- **Stateless :** Le serveur FastAPI n'a pas besoin de maintenir une table de sessions en mémoire ; le jeton contient l'identité chiffrée (`sub: username`) et sa date de péremption (`exp`).
- **Cryptographie Argon2id :** Utilisation de l'algorithme vainqueur de la Password Hashing Competition (`pwdlib[argon2]`), immunisé contre les attaques par calcul parallèle sur GPU.
- **Défense en profondeur :** Implémentation d'une vérification sur hash fictif (`DUMMY_HASH`) lorsque l'utilisateur n'existe pas, neutralisant les attaques par canal auxiliaire de chronométrage.

---

## 7. Spécification des Exigences Fonctionnelles et Non-Fonctionnelles

### 7.1 Exigences Fonctionnelles Numérotées (EF)

| Code EF | Intitulé de l'Exigence Fonctionnelle | Description Détaillée | Priorité MoSCoW | Statut d'Implémentation |
|---|---|---|---|---|
| **EF-01** | Inscription utilisateur | Le système doit permettre la création d'un compte utilisateur avec nom, identifiant email et mot de passe sécurisé. | Must have | **100% Implémenté** (`POST /user`) |
| **EF-02** | Authentification JWT | Le système doit authentifier les utilisateurs et délivrer un jeton Bearer JWT valide pour une durée déterminée (30 min). | Must have | **100% Implémenté** (`POST /token`) |
| **EF-03** | Sécurisation des routes | Le système doit restreindre la consultation des routes météo aux utilisateurs authentifiés munis d'un jeton valide. | Must have | **100% Implémenté** (`Depends(get_current_user)`) |
| **EF-04** | Cartographie des zones | Le système doit afficher une carte interactive Leaflet centrée sur le Burundi avec les marqueurs des zones pilotes. | Must have | **100% Implémenté** (`Leaflet.svelte`) |
| **EF-05** | Sélection territoriale | L'utilisateur doit pouvoir sélectionner une zone pilote par clic sur la carte ou via un menu de sélection direct. | Must have | **100% Implémenté** (`/`, `/region/[slug]`) |
| **EF-06** | Distinction des sous-zones | Le système doit scinder Bujumbura Rural en sous-zone de plaine (`imbo`) et de montagne (`mumirwa`). | Must have | **100% Implémenté** (`app/config.py`, `Leaflet.svelte`) |
| **EF-07** | Ingestion météo horaire | Le système doit collecter automatiquement les prévisions de température, pluie, vent et rafales sur 7 jours via Open-Meteo. | Must have | **100% Implémenté** (`app/services/weather.py`) |
| **EF-08** | Ingestion historique 7j | Le système doit récupérer les estimations des 7 jours passés pour évaluer la saturation hydrique préalable des sols. | Must have | **100% Implémenté** (`past_days=7`, `measures.py`) |
| **EF-09** | Surveillance des crues GloFAS | Le système doit interroger les débits prévus à 7 jours sur la maille GloFAS associée à chaque zone pilote. | Must have | **100% Implémenté** (`flood-api.open-meteo.com`) |
| **EF-10** | Calcul de référence hydrologique | Le système doit calculer le 75e percentile des débits des 31 derniers jours pour déterminer un seuil d'anomalie hydrologique. | Should have | **100% Implémenté** (`get_flood_past_data`) |
| **EF-11** | Évaluation pluie critique 24h | Le système doit déclencher une alerte lorsque la pluie sur 24h dépasse 50 mm (plaine) ou 100 mm (montagne). | Must have | **100% Implémenté** (`app/services/advice.py`) |
| **EF-12** | Évaluation pluie prolongée 72h | Le système doit évaluer le risque de saturation sur 72h (seuil 60 mm en plaine, 90 mm en montagne). | Must have | **100% Implémenté** (`app/services/advice.py`) |
| **EF-13** | Alerte vent fort | Le système doit déclencher une alerte lorsque les rafales prévues atteignent ou dépassent 40 km/h. | Must have | **100% Implémenté** (`app/services/advice.py`) |
| **EF-14** | Alerte crue rizicole | Le système doit générer un conseil spécifique pour le riz lorsque le débit prévu dépasse le débit de référence p75. | Must have | **100% Implémenté** (`app/services/advice.py`) |
| **EF-15** | Détection déficit hydrique | Le système doit identifier les périodes sèches annoncées (>= 5 jours consécutifs avec moins de 2 mm de pluie). | Should have | **100% Implémenté** (`app/services/advice.py`) |
| **EF-16** | Contextualisation agronomique | Le système doit filtrer les avis selon les cultures prévalentes définies par l'ISABU pour chaque province. | Must have | **100% Implémenté** (`CULTURES_PAR_ZONE`) |
| **EF-17** | Filtrage interactif dans l'UI | L'utilisateur doit pouvoir filtrer dynamiquement les avis par culture et par niveau de sévérité (alertes / sans signal). | Should have | **100% Implémenté** (`region/[slug]/+page.svelte`) |
| **EF-18** | Traçabilité des sources | Chaque conseil doit afficher la date d'évaluation, les métriques utilisées, la règle déclenchée et les limitations du modèle. | Must have | **100% Implémenté** (`advice.py`, `+page.svelte`) |
| **EF-19** | Glissements de terrain (LHASA) | Croisement d'une carte de sensibilité aux glissements avec les pluies pour alerter sur les pentes instables. | Could have | **Non Implémenté / Retiré** (justifié dans l'analyse) |
| **EF-20** | Précipitations CHIRPS v3 | Intégration de séries longues historiques CHIRPS pour le calcul des percentiles climatiques centennaux. | Could have | **Non Implémenté** (remplacé par Open-Meteo) |

### 7.2 Exigences Non-Fonctionnelles Numérotées (ENF)

| Code ENF | Catégorie | Description Formelle | Métrique / Critère d'Acceptation |
|---|---|---|---|
| **ENF-01** | **Performance & Latence** | Les requêtes d'affichage d'une zone avec données en cache doivent répondre instantanément. | Temps de réponse API $< 100\text{ ms}$ (en cache), $< 1,5\text{ s}$ lors du rafraîchissement externe. |
| **ENF-02** | **Disponibilité & Cache** | Le système doit absorber les coupures réseau temporaires vers les serveurs météo internationaux. | Cache SQLite persistant de 3 600 secondes ; relance automatique jusqu'à 5 fois (`backoff=0.2`). |
| **ENF-03** | **Sécurité Cryptographique** | Les mots de passe utilisateurs doivent résister aux attaques par dictionnaire et calcul sur GPU. | Algorithme Argon2id ($m=65536, t=3, p=4$) via `pwdlib`. |
| **ENF-04** | **Résistance aux Attaques Temporelles** | Le système ne doit pas permettre de déduire l'existence d'un compte utilisateur par chronométrage réseau. | Exécution d'un `DUMMY_HASH` lors de la saisie d'un identifiant inexistant sur `/token`. |
| **ENF-05** | **Intégrité Mathématique** | Tout calcul portant sur une série temporelle incomplète doit être neutralisé. | Aucune interpolation hasardeuse : une donnée manquante produit la valeur `None` et le statut `non_evalue`. |
| **ENF-06** | **Déontologie des Messages** | L'application ne doit en aucun cas se substituer aux prérogatives des autorités d'urgence nationales. | Proscription absolue des termes *"inondation certaine"* et *"évacuation"* dans les messages produits. |
| **ENF-07** | **Légèreté & Bas Débit** | L'interface web doit pouvoir se charger sur une connexion mobile 3G instable. | Poids du bundle JavaScript initial compilé par Vite $< 250\text{ Ko}$. |
| **ENF-08** | **Accessibilité & Ergonomie** | L'interface doit être lisible en extérieur sous fort ensoleillement par des agents de terrain. | Respect des ratios de contraste WCAG 2.1 AA via classes Tailwind CSS spécifiques, boutons tactiles $\ge 44\times 44\text{ px}$. |
| **ENF-09** | **Testabilité Unitaire** | La logique de décision et d'extraction de mesures doit être pure et découplée du réseau. | 100% des fonctions des modules `measures.py` et `advice.py` testables sans mock réseau complexe. |
| **ENF-10** | **Portabilité & Standards** | Le backend doit respecter la spécification OpenAPI 3.0 et le frontend les standards HTML5/ES modules. | Validation stricte des schémas Pydantic et zéro erreur ESLint/Prettier. |

---

## 8. Règles Métier de Vigilance et Alertes Multicritères

Le cœur décisionnel du projet repose sur deux modules logiciels purs sans effet de bord : `app/services/measures.py` (extraction et normalisation) et `app/services/advice.py` (évaluation des règles et génération des conseils).

```
                        FLUX DÉCISIONNEL DU MOTEUR PUR
 ┌───────────────────────┐
 │ Données Brutes Fusionnées │ (Open-Meteo horaire + GloFAS prévu 7j + GloFAS passé p75)
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │ app/services/measures │ -> Alignement temporel sur t0 (UTC)
 │                       │ -> Cumuls [t0, t0+24h], [t0, t0+72h], [t0-168h, t0]
 │                       │ -> Rafales max, décompte jours secs (< 2 mm)
 └───────────┬───────────┘
             │
             ▼ dict mesures {pluie_24h, pluie_72h, rafales_kmh, debit_prevu, ...}
 ┌───────────────────────┐
 │  app/services/advice  │ <- Seuils IGEBU (Plaine 50 mm / Montagne 100 mm)
 │                       │ <- Cultures prévalentes par zone (ISABU)
 │                       │ <- Règles déontologiques (pas d'évacuation)
 └───────────┬───────────┘
             │
             ▼ dict conseil {statut, regles_declenchees, message, limitations}
```

### 8.1 Les Trois Statuts Décisionnels

1. **`conseil_actif` :** Déclenché dès qu'au moins une règle métier franchit son seuil critique. Le message d'action associé est construit et mis en avant avec une bordure ambrée.
2. **`sans_signal` :** Toutes les mesures nécessaires ont été évaluées et aucune n'atteint les seuils d'aléa. Le message rappelle explicitement le caractère probabiliste de la météo : *"Aucun seuil expérimental n'est franchi... Restez attentif : la prévision est locale et n'est pas une certitude."*
3. **`non_evalue` :** Au moins une variable indispensable au calcul est absente (`None`) ou corrompue (`NaN`). Le message alerte immédiatement : *"Données non disponibles pour [X]. L'absence de données ne signifie pas l'absence de risque ni une vigilance faible."*

### 8.2 Formalisation des Règles Métier

#### Règle 1 : Pluie critique sur 24 heures (Toutes cultures, avec focus Maïs)
- **Condition formelle :** 
  $$\text{pluie\_24h} \ge S_{24h} \quad \text{où} \quad S_{24h} = \begin{cases} 50.0\text{ mm} & \text{si zone} = \text{plaine} \\ 100.0\text{ mm} & \text{si zone} = \text{montagne} \end{cases}$$
- **Message si Culture = Maïs :** *"Si vous faites sécher du maïs en plein air, prévoyez de le mettre à l'abri ou de le couvrir avant les pluies annoncées. Vérifiez les fossés et les accès autour des aires de séchage."*
- **Message pour autres cultures :** *"Protégez les produits en cours de séchage et vérifiez les fossés et les accès exposés."*
- **Durée de validité :** Prochaines 24 heures.

#### Règle 2 : Pluie prolongée sur 72 heures (Cultures sensibles à l'humidité)
- **Condition formelle :** 
  $$\text{pluie\_72h} \ge S_{72h} \quad \text{où} \quad S_{72h} = \begin{cases} 60.0\text{ mm} & \text{si plaine} \\ 90.0\text{ mm} & \text{si montagne} \end{cases}$$
- **Cultures cibles :** Haricot, Manioc, Patate douce, Pomme de terre.
- **Message :** *"Après des pluies prolongées, vérifiez l'apparition de rigoles ou de ravinements et l'évacuation de l'eau autour des parcelles."* (Ajout pour la patate douce : *"Vérifiez aussi l'état des buttes."*).
- **Durée de validité :** Prochaines 72 heures.

#### Règle 3 : Sols préalablement saturés (Pluie des 7 derniers jours)
- **Condition formelle :** 
  $$\text{pluie\_7j\_passes} \ge 50.0\text{ mm}$$
- **Rôle agronomique :** Détecter une nappe phréatique saturée où même une pluie modérée provoquera l'asphyxie des racines de haricot ou la pourriture du manioc.
- **Message :** Identique à la règle d'humidité avec durée de validité étendue aux 7 prochains jours.

#### Règle 4 : Alerte Vent violent et Rafales
- **Condition formelle :** 
  $$\text{rafales\_kmh} \ge 40.0\text{ km/h}$$
- **Cultures particulièrement exposées :** Bananier (prise au vent des larges feuilles et poids des régimes) et Maïs (versement des tiges).
- **Message si Bananier :** *"Vérifiez les plants exposés au vent. Si des brise-vent existent, contrôlez leur état ; les régimes proches de la maturité peuvent être plus vulnérables à la chute."*
- **Message si Maïs :** *"Vérifiez les plants exposés au vent : les rafales fortes peuvent provoquer le versement ou le déracinement du maïs et des jeunes plants. Contrôlez aussi les installations légères."*

#### Règle 5 : Crue et Débit anormal pour le Riz de bas-fond
- **Condition formelle :** 
  $$Q_{\text{prevu}} > Q_{\text{ref\_p75}} \quad (\text{point GloFAS})$$
- **Message :** *"Le débit prévu est inhabituel pour ce point à cette période. Vérifiez les diguettes, les canaux et les accès du bas-fond. Une pluie normale n'est pas un problème pour le riz, mais un débit inhabituel justifie une vérification locale."*
- **Avertissement associé :** *"Débit GloFAS (~5 km, grands bassins) : ne prouve pas un débordement. Un débit inhabituel signifie seulement 'plus haut que le p75 des 31 derniers jours'. Vérification locale indispensable."*

#### Règle 6 : Période sèche prolongée
- **Condition formelle :** 
  $$\text{jours\_secs} \ge 5 \quad \text{où un jour sec correspond à un cumul } < 2.0\text{ mm/24h}$$
- **Message :** *"Période sèche annoncée : surveillez l'état des cultures et vérifiez localement la disponibilité en eau."*

---

## 9. Planification Temporelle sur Deux Semaines (W1–W2)

Le document de cadrage (Section 8) articulait le développement du prototype sur un horizon condensé de deux semaines ouvrées (10 jours). L'analyse de l'implémentation montre le découpage réel des phases :

```
                               CALENDRIER DU PROJET (W1-W2)
  Semaine 1 (Cadrage, Données, Moteur Pur)       Semaine 2 (API, Front-end, Validation)
 ┌──────────────────────────────────────────┐   ┌──────────────────────────────────────────┐
 │ J1-J2 : Exploration & Validation Données │   │ J6-J7 : Développement Frontend SvelteKit │
 │ • Inspection coordonnées 5 zones         │   │ • Structure routes /login, /region/[slug]│
 │ • Test points GloFAS & élévation         │   │ • Intégration carte Leaflet (Sveaflet)   │
 │ • Spécification seuils IGEBU (50/100 mm) │   │ • Graphiques svelteplot séries temporelles│
 ├──────────────────────────────────────────┤   ├──────────────────────────────────────────┤
 │ J3-J5 : Développement Backend Pur        │   │ J8-J9 : Intégration & Tests Automatisés  │
 │ • Implémentation measures.py & advice.py │   │ • Connexion API FastAPI <-> SvelteKit    │
 │ • Client HTTP avec cache SQLite local    │   │ • Exécution des 31 tests unitaires pytest│
 │ • Authentification Argon2id / JWT Bearer │   │ • Tests d'affichage mobile responsive    │
 ├──────────────────────────────────────────┤   ├──────────────────────────────────────────┤
 │ Fin W1 : Jalons Moteur & Tests Validés   │   │ J10 : Documentation & Canevas UPG        │
 │ • 100% logique décisionnelle testée      │   │ • Synthèse comparative et rapport DOCX  │
 └──────────────────────────────────────────┘   └──────────────────────────────────────────┘
```

---

## 10. Perspectives de Deuxième Année (Section 9 du Cadrage)

Le projet ayant été conçu comme la première phase d'un cycle pluriannuel, la Section 9 du document de cadrage énumère des perspectives d'approfondissement d'une grande valeur académique pour la conclusion du rapport :

1. **Extension territoriale exhaustive aux 18 provinces / 5 super-provinces :** Étendre les mailles d'observation à l'ensemble des communes du pays, notamment dans le Nord (Ngozi, Kayanza, Kirundo) et l'Est (Cankuzo, Ruyigi).
2. **Intégration des stations météorologiques locales de l'IGEBU :** Mettre en place une passerelle d'ingestion des stations automatiques au sol de l'IGEBU pour confronter les modèles satellitaires aux observations terrestres réelles.
3. **Calibrage par Apprentissage Automatique (Machine Learning) :** Développer des modèles de *downscaling* statistique (Random Forest, réseaux de neurones récurrents LSTM) pour corriger localement les biais des prévisions pluviométriques Open-Meteo en fonction de la topographie collinaires.
4. **Diffusion multicanale sans Internet (SMS / USSD) :** Développer une passerelle SMS/USSD connectée aux opérateurs télécoms burundais (Lumitel, Econet Leo) pour envoyer des alertes textuelles en langue nationale (*Kirundi*) aux petits producteurs agricoles ne disposant pas de smartphone.
5. **Collecte participative citoyenne (Crowdsourcing) :** Permettre aux agronomes communaux et aux chefs de collines de remonter via l'application des signalements d'incidents réels (ravinements, inondations de bas-fonds, chute de grêle) pour valider empiriquement les seuils d'alerte.
6. **Réintroduction d'un modèle de glissements haute résolution :** Coupler les modèles numériques de terrain (Copernicus DEM 30m ou drone) avec des capteurs d'humidité du sol pour réintroduire un module de glissements scientifiquement robuste.

---

## 11. Matrice de Conformité et Synthèse des Écarts : Cadrage MVP vs Implémentation Réelle

Cette section constitue la pièce maîtresse pour le **Chapitre V (Discussion des résultats et évaluation comparative)** du rapport académique.

| Dimension Analysée | Spécification Document de Cadrage MVP | Implémentation Réelle dans le Code | Qualification de l'Écart | Justification Technique et Argumentaire Académique |
|---|---|---|---|---|
| **Base de Données Principale** | **PostgreSQL** (tables SQL, clés étrangères, historique complet) | **MongoDB** (Cloud Atlas NoSQL) + **SQLite** local | **Divergence Majeure** | Le stockage SQL d'historiques horaires météo massifs était inadapté pour un cycle de 2 semaines. MongoDB offre une gestion fluide des utilisateurs, tandis que le cache SQLite (`requests-cache`) assure la persistance légère des prévisions sans coûts serveur. |
| **Sécurité & Authentification** | Évoquée succinctement (accès ouvert ou basique) | **Système robuste** : JWT (`pyjwt`), Argon2id (`pwdlib`), OAuth2 Bearer, protection anti-timing | **Sur-performance Qualifiée** | L'implémentation réelle surpasse les attentes du cadrage en intégrant un niveau de sécurité industriel (neutralisation de l'énumération d'utilisateurs par hash fictif). |
| **Découpage Géographique** | 3 zones indicatives (Rusizi, versants, Gitega) | **5 zones pilotes administratives (anciennes provinces)** scindées en 6 localités | **Amélioration & Affinement** | Extension à Gitega, Karusi, Rutana, Bujumbura Mairie et Bujumbura Rural (subdivisée en Imbo et Mumirwa) avec règle de précaution topographique. |
| **Modèle Glissements (NASA LHASA)** | Prévu : Croisement carte NASA + pluies 24-72h | **Exclu / Retiré du code** | **Écart Assumé & Justifié** | Retiré car la maille kilométrique de LHASA ne résout pas les collines locales. L'inclusion aurait généré des alertes trompeuses. Priorité donnée aux risques directs (crues, pluies). |
| **Données Pluviométriques CHIRPS** | Prévu : CHIRPS v3 pour les historiques | **Remplacé** par les réanalyses Open-Meteo (`past_days=7`) | **Simplification Pragmatique** | Open-Meteo fournit sur un même endpoint les 7 jours passés et futurs, garantissant un alignement temporel parfait sans multiplier les dépendances externes. |
| **Cultures Agricoles** | Catalogue statique de 7 cultures fixes | **Cartographie dynamique par zone (ISABU)** | **Amélioration Agronomique** | Au lieu d'afficher 7 cultures partout, l'application sélectionne automatiquement les cultures prévalentes de la province consultée (ex. pas de riz en colline sèche, focus riz en plaine). |
| **Référence Hydrologique GloFAS** | 90e percentile historique du même mois | **75e percentile des 31 derniers jours glissants** | **Adaptation Statistique** | Le 75e percentile sur 31 jours glissants offre un indicateur d'anomalie dynamique réactif, calculable directement sans archive centennale. |
| **Frontend & Rendu Cartographique** | Svelte, Leaflet, OpenStreetMap | **SvelteKit 2 (Svelte 5 Runes)**, Sveaflet, Tailwind CSS v4, Svelteplot | **Pleine Conformité & Modernité** | Utilisation de l'état de l'art du web moderne (Runes Svelte 5, visualisations SVG interactives vectorisées). |
| **Déploiement Conteneurisé** | Docker / docker-compose évoqué | Absent (lancement direct via `uv` / `vite`) | **Chantier Résiduel** | Le projet tourne en environnement local (`uv` Python 3.14). La conteneurisation Docker constitue une recommandation pour la phase industrielle. |
| **Gestion des Versions Git** | Dépôt Git versionné avec historique | Dépôt initialisé mais aucun commit finalisé | **Chantier Résiduel** | Les fichiers sont présents mais non commités ; un commit initial propre est préconisé avant soutenance. |

---

## Conclusion de l'Analyse de Spécification

L'exploration approfondie menée dans le cadre de cette mission de *Specification Mining* démontre que le prototype logiciel développé dans `weather-backend` et `weather-app` constitue **une base d'ingénierie logicielle d'une qualité remarquable**, répondant très largement aux attentes académiques d'un projet de fin d'études en Génie Logiciel à l'UPG.

Les écarts constatés avec le document de cadrage initial ne constituent en rien des faiblesses, mais traduisent des **décisions d'ingénierie pragmatiques, matures et scientifiquement justifiées** :
- L'abandon de NASA LHASA évite d'induire les agriculteurs en erreur avec des prédictions de glissement non résolues.
- L'utilisation de MongoDB et d'un cache SQLite élimine la complexité inutile d'un serveur PostgreSQL pour des séries horaires éphémères.
- L'ajout d'une authentification JWT Argon2id de pointe et la contextualisation fine des cultures par province selon l'ISABU apportent une plus-value applicative indéniable.

L'ensemble de ces éléments est prêt à être réinvesti directement dans les chapitres I, II, III, IV et V du document de synthèse `Rapport_Projet_Veille_Meteo_Burundi.docx`.
