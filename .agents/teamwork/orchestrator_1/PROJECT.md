# Project: Système de veille météo et climatique au Burundi — Rapport Académique UPG

## Architecture

Le livrable final est un document académique exhaustif au format Microsoft Word (.docx), situé à `c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx`.
Il compare rigoureusement l'implémentation réelle de l'application (frontend SvelteKit dans `weather-app` et backend FastAPI/MongoDB dans `weather-backend`) au document de cadrage MVP révisé du 11 octobre 2026, en respectant scrupuleusement le canevas de Projet II (Génie Logiciel) de l'Université Polytechnique de Gitega (UPG).

### Normes de Présentation Académique UPG
- **Police du corps de texte** : Times New Roman, 12 pt.
- **Titres de chapitre** : Times New Roman, 14–16 pt, gras, majuscules.
- **Sous-titres (Niveaux 2 et 3)** : Times New Roman, 12–13 pt, gras.
- **Interligne** : 1,5 ligne.
- **Marges** : Gauche 3,0 cm (marge de reliure) ; Haut, Bas, Droite 2,5 cm.
- **Alignement du texte** : Justifié sur l'ensemble du document.
- **Numérotation des figures et tableaux** : Préfixée par le numéro de chapitre (ex. Figure 2.1, Tableau 3.2). Légende sous les figures, au-dessus des tableaux.
- **Citations et références bibliographiques** : Style IEEE homogène `[1]`, `[2]`, etc., intégrant les sources scientifiques et techniques S1 à S7.
- **Pages liminaires** : Strictement omises selon la consigne validée avec l'utilisateur (démarrage direct à l'INTRODUCTION GÉNÉRALE).

---

## Feature Inventory

| # | Feature / Composante | Description | Milestone | Source |
|---|----------------------|-------------|-----------|--------|
| F01 | Normes UPG & Typographie | TNR 12pt, 1.5 interligne, marges 3cm/2.5cm, justifié, suppression pages liminaires | M1 | Canevas UPG (CONFORME) |
| F02 | Introduction Générale | Contexte, problématique, 4 questions, objectifs SMART chiffrés | M1 | Cadrage §1 & spec_miner (CONFORME) |
| F03 | Découpage Territorial 5 Zones | Gitega, Karusi, Buja Mairie, Rutana, Buja Rural (Imbo/Mumirwa) | M1 | Code backend config.py & Leaflet (CONFORME) |
| F04 | Sources Scientifiques S1-S7 | Open-Meteo, GloFAS, NASA LHASA (retrait), Leaflet/OSM, ISABU, IGEBU, CHIRPS | M1 | Cadrage §3 & analysis.md (CONFORME) |
| F05 | Personas & Parcours | Pierre (agriculteur), Chantal (coopérative), Dr. Alexis (expert) | M1 | Cadrage §2 & spec_miner (CONFORME) |
| F06 | Étude de Faisabilité 4D | Technique, économique, opérationnelle, juridique/déontologique | M1 | Canevas UPG Ch. I (CONFORME) |
| F07 | État de l'Art Comparatif | SvelteKit vs React/Vue, FastAPI vs Django/Node, MongoDB vs Postgres, OAuth2/JWT | M1 | Canevas UPG Ch. II (CONFORME) |
| F08 | Exigences EF & ENF | EF-01 à EF-20 et ENF-01 à ENF-10 chiffrées et vérifiables | M1 | Cadrage §4 & spec_miner (CONFORME) |
| F09 | Architecture Globale & BFF | Schéma conceptuel d'échange client-serveur et proxy SvelteKit | M1 | Code frontend/backend (CONFORME) |
| F10 | Diagrammes UML Complets | Use Case, Classes, Composants, Séquence, États-transitions, Déploiement | M1 | Canevas Ch. III & Annexe A (CONFORME) |
| F11 | Schéma Base de Données | Structure MongoDB (users) et SQLite (.cache) | M1 | Code db.py & Annexe B (CONFORME) |
| F12 | Moteur de Règles & Seuils | IGEBU 50/100mm, crues GloFAS p75, vent 40km/h, matrice cultures ISABU | M1 | Code advice.py/measures.py (CONFORME) |
| F13 | Planification W1-W2 | Décomposition Scrum/Agile sur 10 jours ouvrés | M1 | Cadrage §8 (CONFORME) |
| F14 | Implémentation Backend | FastAPI, Python 3.14, uv, collecteurs avec retries, sécurité Argon2id anti-timing | M1 | weather-backend (CONFORME) |
| F15 | Implémentation Frontend | Svelte 5 Runes, SvelteKit 3, Tailwind v4, Sveaflet Leaflet 1.9, svelteplot | M1 | weather-app (CONFORME) |
| F16 | Tests & Résultats d'Exécution | 31/31 tests pytest backend réussis, build Vite 8 exit code 0 | M1 | Code tests & execution (CONFORME) |
| F17 | Matrice Comparative Cadrage vs Réel | Analyse critique exhaustive des divergences (MongoDB, Provinces, LHASA, Auth) | M1 | Cadrage vs Code réel (CONFORME) |
| F18 | Conclusion & Roadmap An 2 | Limites actuelles, perspectives Section 9 (USSD, IoT, IA, Kirundi) | M1 | Cadrage §9 & Canevas (CONFORME) |
| F19 | Annexes D & F | Manuel d'installation pas-à-pas et métriques de code source (>3700 SLOC) | M1 | Canevas Annexes (CONFORME) |
| F20 | Bibliographie IEEE | 25 références normalisées (S1-S7 + standards techniques) | M1 | Canevas & normes IEEE (CONFORME) |

---

## Milestones

| # | Nom du Milestone | Périmètre et Description | Dépendances | Statut |
|---|-------------------|--------------------------|-------------|--------|
| M1 | Génération & Compilation du Rapport DOCX | Script Python `generate_report.py` construisant l'intégralité du document `Rapport_Projet_Veille_Meteo_Burundi.docx` selon les normes UPG | Survey complet | **DONE** |
| M2 | Revue Indépendante & Assurance Qualité | Inspection par 2 Reviewers indépendants (reviewer_report_1 & reviewer_report_2_rep) | M1 | **DONE (APPROVE)** |
| M3 | Vérification Adversariale & Challenge | Audit par 2 Challengers (challenger_report_1 & challenger_report_2_rep) | M1 | **DONE (APPROVE)** |
| M4 | Audit Forensique d'Intégrité | Audit binaire par Forensic Auditor (auditor_report_1) | M1, M2, M3 | **DONE (CLEAN)** |
| M5 | Clôture & Livraison au Parent | Notification finale et transmission au Sentinel parent | M4 CLEAN | **DONE** |

---

## Livrable Final Validé

- **Fichier** : `c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx`
- **Taille** : 158 688 octets (154,97 Ko)
- **Empreinte SHA-256** : `4a6c4271d2f1d73e557e00d9729e5a32c2716c71fd82e3718b89cc402f430147`
- **Volumétrie** : ~17 600 mots, 429 paragraphes, 45 tableaux et encadrés, 13 figures, 25 références IEEE.
