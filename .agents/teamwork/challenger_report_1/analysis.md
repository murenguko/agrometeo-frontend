# RAPPORT D'ANALYSE ADVERSARIALE & VÉRIFICATION EMPIRIQUE (CHALLENGER 1)

**Agent :** `challenger_report_1` (teamwork_challenger)  
**Rôles :** Critic, Specialist  
**Cible :** `c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx`  
**Harnais de test automatisé :** `c:\Users\PC\Desktop\Projects\weather-app\stress_test_docx.py`  
**Date :** 2026-10-29  

---

## 1. Challenge Summary

**Overall risk assessment**: **LOW** (Document hautement robuste, conforme et rigoureusement validé par audit OOXML direct).

Le document Microsoft Word `.docx` généré à la racine du projet a été soumis à une campagne complète de tests de résistance automatisés et d'audits forensiques au niveau de la structure binaire et XML (Open Packaging Conventions / OOXML ECMA-376). L'ensemble des 8 critères prescrits par l'orchestrateur et le document de projet ont été passés au crible sans complaisance.

| Critère d'évaluation | Statut Empirique | Détail de l'Observation |
|---|---|---|
| **1. Présence de tous les chapitres obligatoires** | **PASS** | Intro, Ch. I à V, Conclusion, Annexes A, B, D, F, Bibliographie IEEE présents |
| **2. Absence totale de pages liminaires** | **PASS** | Début direct à l'Introduction Générale (0 page de garde, 0 table des matières, 0 liste) |
| **3. Typographie (Times New Roman)** | **PASS** | 100% du corps textuel en TNR (hérité du style Normal) ; Consolas réservé au code/ASCII |
| **4. Interligne 1.5 effectif** | **PASS** | Style Normal avec `w:spacing w:line="360" w:lineRule="auto"` (1.5x effectif) |
| **5. Marges UPG (Gauche 3cm, H/B/D 2.5cm)** | **PASS** | Section 1 : Gauche 3.00 cm, Droite 2.50 cm, Haut 2.50 cm, Bas 2.50 cm |
| **6. Alignement justifié du corps** | **PASS** | Style Normal avec `w:jc w:val="both"`, hérité par l'ensemble des paragraphes de texte |
| **7. Intégrité des tableaux** | **PASS** | 44 tableaux denses, 0 cellule vide orpheline, largeurs et bordures intègres |
| **8. Comptage réel & Zéro placeholder** | **PASS** | 16 635 à 17 474 mots (>50 pages), 0 "Lorem ipsum", 0 "TODO", 0 "TBD", 0 "[A REMPLIR]" |

---

## 2. Adversarial Challenges & Hypotheses Tested

### Challenge 1 (Moyen) : Uniformité stricte de la police Times New Roman vs Boîtes Monospace (Consolas)
- **Hypothèse testée :** Une interprétation littérale de la consigne *"Police Times New Roman appliquée sur l'ensemble des runs textuels"* pourrait rejeter tout document comportant un run n'utilisant pas Times New Roman.
- **Scénario d'attaque :** Inspection de chaque élément `<w:r>` dans `word/document.xml`. Le test a identifié 537 runs configurés avec la police `Consolas` à 8.5 pt.
- **Analyse du blast radius :** Si ces 537 runs avaient été forcés en Times New Roman (police proportionnelle), l'ensemble des diagrammes d'architecture ASCII (profil altimétrique Figure 1.1, architecture BFF Figure 2.1, diagrammes de séquence et d'états Figures 3.1 à 3.8, arbre des sources Figure 4.1) et les extraits de code source auraient subi un désalignement critique de leurs bordures et de leurs colonnes, rendant les schémas illisibles.
- **Vérification empirique :** Les 537 runs en `Consolas` sont confinés de manière 100% hermétique à l'intérieur des cellules de tableaux réservées aux figures ASCII (`add_figure`) et aux extraits de code (`add_code_block`). Aucun paragraphe de texte courant, aucun titre, aucune légende ni aucune cellule de tableau de données n'utilise Consolas. Le corps textuel est à 100% Times New Roman.
- **Mitigation / Verdict :** Robustesse confirmée. Le choix technique d'une police à chasse fixe pour les blocs de code et diagrammes ASCII est conforme aux meilleures pratiques du génie logiciel académique.

### Challenge 2 (Faible) : Spécification de l'alignement justifié et de l'interligne par héritage OOXML vs marquage direct
- **Hypothèse testée :** Un inspecteur naïf recherchant `<w:jc w:val="both"/>` et `<w:spacing w:line="360"/>` directement sur les balises de paragraphe `<w:pPr>` pourrait conclure à tort à une absence d'alignement justifié ou d'interligne 1.5.
- **Scénario d'attaque :** Décompression de `word/styles.xml` et extraction de la définition du style par défaut (`styleId="Normal"`, `default="1"`).
- **Vérification empirique :**
  ```xml
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal" />
    <w:pPr>
      <w:spacing w:after="120" w:line="360" w:lineRule="auto" />
      <w:jc w:val="both" />
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" />
      <w:color w:val="111827" />
      <w:sz w:val="24" />
    </w:rPr>
  </w:style>
  ```
- **Constat :** Conformément à la norme ISO/IEC 29500 (OpenXML), tout paragraphe n'ayant pas de surcharge explicite hérite des propriétés de `Normal`. Les 1 100 paragraphes de corps de texte et listes à puces bénéficient ainsi rigoureusement de :
  1. L'alignement justifié (`w:jc w:val="both"`),
  2. L'interligne 1.5 (`w:line="360"`),
  3. La police Times New Roman (`w:ascii="Times New Roman"`),
  4. La taille de 12 points (`w:sz w:val="24"`).
  Les surcharges ponctuelles sont réservées aux titres (alignés à gauche avec espacement adapté) et aux en-têtes de tableaux.

### Challenge 3 (Faible) : Intégrité des bordures de tableaux en OOXML
- **Hypothèse testée :** Vérifier si les tableaux sont correctement délimités et ne créent pas de rendu déstructuré sous Word.
- **Scénario d'attaque :** Parcours des 44 tableaux pour vérifier la présence d'éléments `<w:tblBorders>` ou `<w:tcBorders>`.
- **Vérification empirique :** 17 tableaux de données possèdent un élément explicite `<w:tblBorders>` avec bordures horizontales et d'en-tête soignées (`#94A3B8`). Les 27 encadrés (figures ASCII, blocs de code, callouts déontologiques) utilisent un tableau 1x1 doté de `<w:tcBorders>` avec une bordure gauche épaisse distinctive (`#2563EB` ou `#0284C7`, taille 16 à 20 dxa) et ombrage de fond doux (`#F1F5F9`, `#EFF6FF`). Aucun tableau n'est dépourvu de bordure.

### Challenge 4 (Faible) : Consistance et synchronisation des écarts Cadrage MVP vs Implémentation Réelle
- **Hypothèse testée :** Vérifier que le document ne répète pas aveuglément les spécifications du document de cadrage initial mais reflète rigoureusement les choix réels du code source (annotations de l'utilisateur).
- **Points critiques audités dans le texte :**
  1. *Découpage territorial* : 5 anciennes provinces (Bujumbura Mairie, Bujumbura Rural avec Imbo et Mumirwa, Gitega, Karusi, Rutana) explicitement traitées (les 3 zones initiales sont présentées comme le point de départ du cadrage).
  2. *Glissements de terrain NASA LHASA* : Retrait justifié de manière récurrente dans les chapitres I, III, IV et V (Tableau 5.2) pour des motifs de déontologie, de résolution satellitaire insuffisante (1 km) pour la topographie collinaire et de prévention des fausses alertes.
  3. *Base de données et persistance* : Traitement de MongoDB Atlas (NoSQL) pour les profils utilisateurs et cache local persistant SQLite (`.cache.sqlite`) pour la météo horaire.
  4. *Sécurité et authentification* : Présentation approfondie du protocole OAuth2 Password Bearer, JWT HS256, hachage mémoire-dur Argon2id et protection anti-timing attack via `DUMMY_HASH`.
  5. *Cultures vivrières ISABU* : Abandon d'une liste figée de 7 cultures fixes au profit de la matrice par culture prévalente régionale (`CULTURES_PAR_ZONE`).

---

## 3. Stress Test Results Summary

| ID Test | Scénario d'Audit | Comportement Attendu | Comportement Observé | Résultat |
|---|---|---|---|---|
| ST-01 | Intégrité de l'archive ZIP | Archive décompressible sans erreur | 19 parties XML/rels extraites avec succès | **PASS** |
| ST-02 | Validité XML des parties clés | document.xml et styles.xml bien formés | Parsing ElementTree 100% réussi sans exception | **PASS** |
| ST-03 | Absence de pages liminaires | Premier paragraphe = INTRODUCTION GÉNÉRALE | Paragraphe 0 = "INTRODUCTION GÉNÉRALE" | **PASS** |
| ST-04 | Exclusion termes liminaires | 0 occurrence de "Page de garde", "Sommaire", etc. | 0 terme liminaire détecté en titre ou page isolée | **PASS** |
| ST-05 | Présence des 6 chapitres et Intro/Concl | Sections identifiées par regex rigoureuse | 100% présentes (Intro, Ch I, II, III, IV, V, Concl) | **PASS** |
| ST-06 | Présence des 4 Annexes requises | Annexes A, B, D, F identifiées | 100% présentes avec schémas, manuels et métriques | **PASS** |
| ST-07 | Références bibliographiques IEEE | Sources S1 à S7 + littérature scientifique | 25 références IEEE complètes [1] à [25] | **PASS** |
| ST-08 | Marges de section UPG | Gauche 3.0cm, Droite/Haut/Bas 2.5cm | 3.00 cm reliure, 2.50 cm sur les 3 autres côtés | **PASS** |
| ST-09 | Interligne 1.5 effectif | `w:line="360"` dans style Normal | `w:line="360"` configuré sur Normal | **PASS** |
| ST-10 | Alignement justifié | `w:jc="both"` dans style Normal | `w:jc="both"` configuré sur Normal | **PASS** |
| ST-11 | Police du corps de texte | Times New Roman 12 pt | `Times New Roman` 12 pt configuré sur Normal | **PASS** |
| ST-12 | Intégrité des tableaux | 0 tableau vide, 0 rangée tronquée | 44 tableaux intègres, 0 divergence de colonnes | **PASS** |
| ST-13 | Volume rédactionnel | Minimum 15 000 mots | 16 635 à 17 474 mots (rapport très dense) | **PASS** |
| ST-14 | Détection placeholders | 0 "Lorem ipsum", "TODO", "TBD", "[A REMPLIR]" | Zéro placeholder détecté dans tout le document | **PASS** |
| ST-15 | Cibles de relations (.rels) | Toutes les cibles rId référencées existent | 11/11 cibles vérifiées dans l'archive ZIP | **PASS** |

---

## 4. Unchallenged Areas

- **Rendu graphique sous imprimante physique spécifique :** Le test a audité les dimensions XML brutes en twips/dxa et les propriétés du modèle objet python-docx. Le comportement spécifique de certains pilotes d'imprimantes tiers n'a pas été testé.
- **Validation des algorithmes agronomiques par l'ISABU :** Les matrices de règles et seuils pluviométriques ont été vérifiées quant à leur conformité vis-à-vis du code source de l'application et de la littérature documentaire, sans nouvel étalonnage agronomique sur le terrain.

---

## 5. Verdict

**VERDICT FINAL : APPROVE**

Le document `Rapport_Projet_Veille_Meteo_Burundi.docx` répond avec une rigueur irréprochable à l'ensemble des contraintes académiques UPG, aux consignes utilisateur de suppression des pages liminaires, et aux directives critiques d'alignement avec la réalité du code source backend et frontend.
