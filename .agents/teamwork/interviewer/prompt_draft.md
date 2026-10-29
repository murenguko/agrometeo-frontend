This is a single self-contained fix; keep it small and focused. Insérer uniquement les pages liminaires spécifiées dans le canevas de l'UPG au début du document existant `Rapport_Projet_Veille_Meteo_Burundi.docx` et réviser la section des sources et références bibliographiques pour la mettre en cohérence avec le contenu actuel, sans modifier ni altérer le reste du corps du rapport édité par l'utilisateur.

Working directory: c:\Users\PC\Desktop\Projects\weather-app
Integrity mode: development

## Requirements

### R1. Insertion des pages liminaires selon le canevas UPG
Insérer au début du document Word existant `Rapport_Projet_Veille_Meteo_Burundi.docx` (avant l'INTRODUCTION GÉNÉRALE) les quatre pages liminaires requises par le canevas de l'Université Polytechnique de Gitega (UPG) — Faculté des Technologies de l'Information et de la Communication (Génie Logiciel, Projet II) :
1. Page de garde : République du Burundi, Ministère de l'Éducation Nationale et de la Recherche Scientifique, Université Polytechnique de Gitega (UPG), Faculté des Technologies de l'Information et de la Communication, Projet II - Génie Logiciel, Titre du projet : Système de veille météo et climatique au Burundi, avec espaces réservés standards (ou métadonnées existantes du document si disponibles) pour l'étudiant/auteur, l'encadreur et l'année académique.
2. Table des matières et table des annexes basées sur les titres exacts présents dans le document actuel.
3. Liste des figures et liste des tableaux basées sur les légendes réelles des figures et tableaux présentes dans le document actuel.
4. Liste des sigles, abréviations et acronymes utilisés dans le rapport (UPG, TIC, ISABU, IGEBU, GloFAS, NASA, LHASA, CHIRPS, MVP, API, REST, BFF, SSR, JWT, OAuth2, OWASP, SGBD, NoSQL, SQL, JSON, GeoJSON, HTML, CSS, UI, UX, WCAG, UML, TTL, etc.).

### R2. Révision des sources et références bibliographiques
Réviser et mettre en cohérence la section des sources et références bibliographiques avec le contenu actuel du rapport édité par l'utilisateur (harmonisation du format des références, complétude des sources mentionnées dans le texte et pertinence par rapport aux données et technologies du projet).

### R3. Préservation stricte du corps du rapport existant
Lire le fichier `c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx` tel qu'il est actuellement sur le disque. Ne modifier en aucun cas le corps rédigé du texte ni les modifications manuelles apportées par l'utilisateur dans les chapitres du document (en dehors de l'insertion des pages liminaires au début et de la mise à jour de la section des sources/références). Ne pas exécuter `generate_report.py`.

### R4. Respect des normes de mise en page du canevas UPG
Appliquer aux pages liminaires et aux sections ajustées les normes de mise en page du canevas UPG :
- Police : Times New Roman, taille 12, interligne 1,5.
- Marges : Gauche 3 cm (reliure) — Haut / Bas / Droite 2,5 cm.
- Pagination : Chiffres romains pour les pages liminaires, puis chiffres arabes pour le corps du rapport (à partir de l'INTRODUCTION GÉNÉRALE), pied de page centré.

## Acceptance Criteria

### Intégrité et préservation
- [ ] Le corps rédigé du document issu des modifications de l'utilisateur est strictement préservé sans altération, à l'exception de l'insertion des pages liminaires initiales et de la mise à jour de la section des références.
- [ ] Le script `generate_report.py` n'a pas été exécuté.

### Complétude des pages liminaires
- [ ] La page de garde comporte l'ensemble des mentions institutionnelles (République du Burundi, Ministère de l'Éducation Nationale et de la Recherche Scientifique, Université Polytechnique de Gitega - UPG, Faculté des TIC, Projet II - Génie Logiciel), le titre exact du projet, et les mentions d'étudiant, encadreur et année académique.
- [ ] La table des matières et la table des annexes recensent fidèlement les titres et sections du document.
- [ ] La liste des figures et la liste des tableaux répertorient l'ensemble des figures et tableaux présents dans le document avec leurs légendes exactes.
- [ ] La liste des sigles, abréviations et acronymes explicite l'ensemble des sigles techniques et institutionnels employés dans le rapport.

### Révision des sources et références
- [ ] La section des références bibliographiques et sources est alignée et cohérente avec les citations, technologies et institutions effectivement citées dans le document.
- [ ] Chaque entrée bibliographique respecte un format homogène et complet.

### Mise en page et pagination
- [ ] Les marges sont fixées à 3 cm à gauche et 2,5 cm en haut, bas et droite.
- [ ] La typographie respecte Times New Roman, corps 12, interligne 1,5.
- [ ] Les pages liminaires sont numérotées en chiffres romains centrés en pied de page.
- [ ] Le corps du rapport commence sa numérotation à 1 en chiffres arabes centrés en pied de page à partir de l'INTRODUCTION GÉNÉRALE.
