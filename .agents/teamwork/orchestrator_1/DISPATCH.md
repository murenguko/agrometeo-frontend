## 2026-10-29T08:54:23Z

Élaborer le rapport académique complet du projet "Système de veille météo et climatique au Burundi" au format Word (`c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx`), en comparant rigoureusement l'implémentation réelle de l'application (`c:\Users\PC\Desktop\Projects\weather-app` pour le front-end SvelteKit et `c:\Users\PC\Desktop\Projects\weather-backend` pour le back-end FastAPI/PostgreSQL) au document de cadrage MVP fourni, et en suivant fidèlement le canevas de rapport Projet II (Génie Logiciel) de l'Université Polytechnique de Gitega (UPG).

Consignes validées avec l'utilisateur :
1. Pages liminaires : Ignorer totalement les pages liminaires (Page de garde, Table des matières / table des annexes, Liste des figures & liste des tableaux, Liste des sigles, abréviations et acronymes). Commencer directement par l'INTRODUCTION GÉNÉRALE.
2. Volume et niveau de détail : Produire un rapport complet, substantiel et très détaillé couvrant fidèlement chaque chapitre, section et sous-section du canevas UPG, appuyé sur l'inspection réelle du code source (`weather-app` et `weather-backend`), sans imposer artificiellement 50-80 pages mais en étant exhaustif et rigoureux sur toute la matière technique du projet.
3. Diagrammes et architectures (Chapitres & Annexes A/B) : Présenter les diagrammes UML (classes, composants, déploiement, cas d'utilisation, états-transitions, séquence), le schéma d'architecture de la base de données et les architectures sous forme textuelle structurée, schémas ASCII/Mermaid propres et tableaux détaillés.
4. Fichier de sortie : Générer le fichier DOCX à l'emplacement exact `c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx`.
5. Normes de présentation UPG :
   - Police du texte courant : Times New Roman, taille 12
   - Titres de chapitre : Times New Roman, 14–16 pt, gras, majuscules
   - Interligne : 1,5 ligne
   - Marges : Gauche 3 cm (reliure) — Haut / Bas / Droite 2,5 cm
   - Alignement du texte : Justifié
   - Numérotation figures/tableaux : Par chapitre (ex. Figure 2.1, Tableau 3.2 — légende sous la figure, au-dessus du tableau)
   - Citations & bibliographie : Style IEEE homogène (avec les sources S1 à S7 du cadrage et références techniques)
6. Contenu obligatoire à couvrir :
   - INTRODUCTION GENERALE (Contexte et justification, Problématique, Questions spécifiques, Objectif général, Objectifs spécifiques avec indicateurs mesurables, Structure du rapport)
   - CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC (Présentation de la structure et du périmètre sur les 3 zones pilotes du Burundi, Expression et analyse du besoin, Personas et parcours utilisateurs, Contraintes, Étude de faisabilité, Synthèse)
   - CHAPITRE II — ÉTUDE THEORIQUE ET ETAT DE L'ART (Architecture client-serveur, Frameworks front-end avec focus SvelteKit vs React/Vue/Angular, Frameworks back-end avec focus FastAPI vs Django/Node/Spring, BD SQL PostgreSQL, API REST, Responsive design & accessibilité, Synthèse)
   - CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE (Exigences fonctionnelles et non fonctionnelles, Architecture applicative front/back/API, Modélisation des données, Conception UI/UX et parcours, Règles métier de vigilance et seuils, Sécurité et résilience, Planification sur 2 semaines, Synthèse)
   - CHAPITRE IV — IMPLEMENTATION / REALISATION (Environnement de développement, Implémentation back-end `weather-backend` : modèles, collecteurs Open-Meteo / GloFAS / NASA LHASA / CHIRPS, moteur de règles, API, gestion du cache/historique ; Implémentation front-end `weather-app` : routes SvelteKit, carte Leaflet, composants météo/crues/glissements/cultures ISABU, comparaison des zones ; Gestion de version, dépendances, packaging et documentation)
   - CHAPITRE V — TESTS, VALIDATION ET EVALUATION (Méthodologie, Tests fonctionnels et d'interface, Compatibilité/Responsive, Utilisabilité, Performance, et **Comparaison détaillée et critique entre le Document de Cadrage MVP et l'Implémentation réelle** : ce qui est conforme, les adaptations, les écarts éventuels et leur justification)
   - CONCLUSION GENERALE ET PERSPECTIVES (Synthèse au regard de la problématique, Limites actuelles du prototype, Perspectives de 2e année selon la section 9 du cadrage)
   - ANNEXES (Annexe A : Diagrammes UML structurés/tabulaires, Annexe B : Schéma de la base de données, Annexe D : Manuel d'installation et d'utilisation, Annexe F : Dépôt Git et structure du code source)
7. Restrictions : Aucune restriction sur les outils ou bibliothèques Python (`python-docx`, etc.) pour générer et vérifier le document `.docx`.


## 2026-10-29T08:59:24Z

[CRITICAL USER UPDATE - CODE REALITY & MVP COMPARISON]
1. Zones géographiques : Ce ne sont PAS les 3 zones pilotes (Rusizi, versants occidentaux, Gitega) qui ont été retenues dans l'implémentation, mais les anciennes provinces du Burundi (consulter les fichiers de configuration et les schémas dans `weather-backend`).
2. Glissements de terrain (NASA LHASA) : La sensibilité aux glissements de terrain a été retirée de l'implémentation (expliquer cet écart et cette décision par rapport au cadrage initial).
3. Cultures agricoles : Au lieu des 7 cultures fixes génériques, l'implémentation utilise les cultures les plus prévalentes par région/province (définies dans les fichiers de configuration de `weather-backend`).
4. Base de données et Authentification : La base de données implémentée est MongoDB (NoSQL), et NON PostgreSQL (contrairement à ce qui était prévu dans le cadrage). De plus, un système d'authentification complet a été implémenté et doit être étudié dans le Chapitre II (État de l'art), le Chapitre III (Conception), le Chapitre IV (Implémentation) et le Chapitre V (Comparaison avec le cadrage).
