"""
verify_docx.py - Script de vérification et d'audit indépendant du rapport académique généré
Vérifie la conformité absolue aux exigences UPG et aux directives de l'utilisateur.
"""

import os
import sys
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def verify_report(docx_path):
    print("=" * 80)
    print(f"AUDIT INDÉPENDANT DU DOCUMENT : {docx_path}")
    print("=" * 80)
    
    if not os.path.exists(docx_path):
        print(f"ERREUR CRITIQUE : Le fichier {docx_path} n'existe pas !")
        return False
        
    doc = docx.Document(docx_path)
    
    # 1. Vérification des sections et des marges UPG
    print("\n--- 1. VÉRIFICATION DES MARGES DE PAGE (UPG) ---")
    section = doc.sections[0]
    top_cm = round(section.top_margin.cm, 2)
    bottom_cm = round(section.bottom_margin.cm, 2)
    left_cm = round(section.left_margin.cm, 2)
    right_cm = round(section.right_margin.cm, 2)
    
    print(f"Marge Gauche (reliure) : {left_cm} cm (Attendu : 3.0 cm)")
    print(f"Marge Droite           : {right_cm} cm (Attendu : 2.5 cm)")
    print(f"Marge Haute            : {top_cm} cm (Attendu : 2.5 cm)")
    print(f"Marge Basse            : {bottom_cm} cm (Attendu : 2.5 cm)")
    
    assert abs(left_cm - 3.0) < 0.1, "La marge gauche doit être de 3.0 cm"
    assert abs(right_cm - 2.5) < 0.1, "La marge droite doit être de 2.5 cm"
    assert abs(top_cm - 2.5) < 0.1, "La marge haute doit être de 2.5 cm"
    assert abs(bottom_cm - 2.5) < 0.1, "La marge basse doit être de 2.5 cm"
    print("-> MARGES VALIDÉES : 100% Conformes aux normes UPG.")
    
    # 2. Vérification des pages liminaires supprimées
    print("\n--- 2. VÉRIFICATION DE LA SUPPRESSION DES PAGES LIMINAIRES ---")
    first_p = ""
    for p in doc.paragraphs:
        if p.text.strip():
            first_p = p.text.strip()
            break
            
    print(f"Premier paragraphe du document : '{first_p}'")
    assert "INTRODUCTION GÉNÉRALE" in first_p or "INTRODUCTION GENERALE" in first_p, (
        f"Le document doit commencer immédiatement par l'INTRODUCTION GÉNÉRALE, trouvé : {first_p}"
    )
    print("-> PAGES LIMINAIRES : Totalement absentes, début direct sur INTRODUCTION GÉNÉRALE validé.")
    
    # 3. Vérification des chapitres et sections obligatoires
    print("\n--- 3. VÉRIFICATION DES TITRES ET DE LA STRUCTURE ---")
    required_chapters = [
        "INTRODUCTION GÉNÉRALE",
        "CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC",
        "CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART",
        "CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE",
        "CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION",
        "CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION",
        "CONCLUSION GÉNÉRALE ET PERSPECTIVES",
        "ANNEXE A — DIAGRAMMES UML STRUCTURÉS ET DÉTAILLÉS",
        "ANNEXE B — SCHÉMA D'ARCHITECTURE DE LA BASE DE DONNÉES",
        "ANNEXE D — MANUEL D'INSTALLATION, DE CONFIGURATION ET D'UTILISATION",
        "ANNEXE F — DÉPÔT GIT, STRUCTURE DU CODE SOURCE ET MÉTRIQUES",
        "RÉFÉRENCES BIBLIOGRAPHIQUES"
    ]
    
    full_text = "\n".join(p.text for p in doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text += "\n" + cell.text
    for chap in required_chapters:
        assert chap in full_text, f"Titre manquant dans le document : {chap}"
        print(f" [OK] {chap}")
        
    print("-> STRUCTURE DES CHAPITRES : 100% Présente et conforme.")
    
    # 4. Vérification du contenu technique critique
    print("\n--- 4. VÉRIFICATION DES CONCEPTS TECHNIQUES CRITIQUES DU CODE ---")
    critical_terms = [
        ("Bujumbura Rural (Imbo)", "Zonage avec scission Imbo / Mumirwa"),
        ("Mumirwa", "Sous-zone de montagne Mumirwa"),
        ("50.0 mm", "Seuil IGEBU plaine"),
        ("100.0 mm", "Seuil IGEBU montagne"),
        ("Argon2id", "Algorithme de hachage Argon2id"),
        ("DUMMY_HASH", "Protection anti-timing attack side-channel"),
        ("MongoDB", "Base de données NoSQL Atlas"),
        (".cache.sqlite", "Cache persistant SQLite local"),
        ("Svelte 5", "Framework réactif Svelte 5"),
        ("FastAPI", "Framework ASGI Python"),
        ("GloFAS", "Système mondial des crues GloFAS"),
        ("river_discharge_p75", "75e percentile des 31 derniers jours"),
        ("CULTURES_PAR_ZONE", "Matrice ISABU par zone provinciale"),
        ("non_evalue", "Statut déontologique en cas de donnée manquante"),
        ("31 tests", "Validation des 31 tests pytest backend"),
        ("[1] Open-Meteo", "Source S1 référencée en IEEE"),
        ("[2] Copernicus", "Source S2 référencée en IEEE")
    ]
    
    for term, desc in critical_terms:
        assert term in full_text, f"Terme critique manquant : {term} ({desc})"
        print(f" [OK] {desc} ('{term}') trouvé.")
        
    print("-> INTÉGRITÉ TECHNIQUE : Tous les concepts du code réel et du cadrage sont validés.")
    
    # 5. Métriques globales
    total_words = sum(len(p.text.split()) for p in doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                total_words += len(cell.text.split())
                
    print("\n--- 5. MÉTRIQUES GLOBALES ---")
    print(f"Nombre total de paragraphes : {len(doc.paragraphs)}")
    print(f"Nombre de tableaux / encadrés : {len(doc.tables)}")
    print(f"Volume total estimé de mots   : {total_words} mots")
    
    assert total_words > 12000, f"Le volume de mots ({total_words}) est insuffisant pour un rapport complet."
    assert len(doc.tables) >= 20, f"Le nombre de tableaux ({len(doc.tables)}) est insuffisant."
    
    print("\n" + "=" * 80)
    print("RÉSULTAT DE L'AUDIT : TOUTES LES VÉRIFICATIONS ONT RÉUSSI AVEC SUCCÈS (100% CONFORME) !")
    print("=" * 80)
    return True

if __name__ == "__main__":
    report_file = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
    success = verify_report(report_file)
    sys.exit(0 if success else 1)
