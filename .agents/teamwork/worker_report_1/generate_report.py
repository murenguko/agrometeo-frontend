"""
generate_report.py - Script principal de génération du rapport académique complet
Génère le document Word 'Rapport_Projet_Veille_Meteo_Burundi.docx'
à la racine de c:\\Users\\PC\\Desktop\\Projects\\weather-app\\
conforme aux normes académiques UPG (Université Polytechnique de Gitega).
"""

import os
import sys
import time
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Import des constructeurs et des modules de contenu
from builder import create_upg_document
from content_intro import build_intro
from content_chap1 import build_chap1
from content_chap2 import build_chap2
from content_chap3 import build_chap3
from content_chap4 import build_chap4
from content_chap5 import build_chap5
from content_conclusion import build_conclusion
from content_annexes import build_annexes

def add_footer_page_number(doc):
    """Ajoute la numérotation des pages en chiffres arabes centrée en pied de page."""
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Ajout du champ dynamique Word PAGE
        p_pr = p._p
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        p_pr.append(fldSimple)

def main():
    start_time = time.time()
    print("=" * 80)
    print("DÉMARRAGE DE LA GÉNÉRATION DU RAPPORT ACADÉMIQUE UPG")
    print("Projet : Système de veille météo et climatique au Burundi (AgroMétéo Burundi)")
    print("Normes : Université Polytechnique de Gitega (UPG) - Faculté des TIC")
    print("=" * 80)
    
    # 1. Initialisation du document Word conforme aux normes UPG
    print("[1/9] Initialisation du document Word avec marges et styles UPG...")
    doc = create_upg_document()
    
    # 2. Rédaction de l'Introduction Générale (commence directement sans pages liminaires)
    print("[2/9] Génération de l'INTRODUCTION GÉNÉRALE...")
    build_intro(doc)
    
    # 3. Chapitre I — État des lieux et diagnostic
    print("[3/9] Génération du CHAPITRE I — ÉTAT DES LIEUX ET DIAGNOSTIC...")
    build_chap1(doc)
    
    # 4. Chapitre II — Étude théorique et état de l'art
    print("[4/9] Génération du CHAPITRE II — ÉTUDE THÉORIQUE ET ÉTAT DE L'ART...")
    build_chap2(doc)
    
    # 5. Chapitre III — Conception de la solution cible
    print("[5/9] Génération du CHAPITRE III — CONCEPTION DE LA SOLUTION CIBLE...")
    build_chap3(doc)
    
    # 6. Chapitre IV — Implémentation et réalisation
    print("[6/9] Génération du CHAPITRE IV — IMPLÉMENTATION ET RÉALISATION...")
    build_chap4(doc)
    
    # 7. Chapitre V — Tests, validation et évaluation (avec comparaison Cadrage MVP vs Code Réel)
    print("[7/9] Génération du CHAPITRE V — TESTS, VALIDATION ET ÉVALUATION...")
    build_chap5(doc)
    
    # 8. Conclusion Générale et Perspectives (Section 9 du cadrage)
    print("[8/9] Génération de la CONCLUSION GÉNÉRALE ET PERSPECTIVES...")
    build_conclusion(doc)
    
    # 9. Annexes (A, B, D, F) et Bibliographie IEEE
    print("[9/9] Génération des ANNEXES (A, B, D, F) et de la BIBLIOGRAPHIE IEEE...")
    build_annexes(doc)
    
    # 10. Ajout de la numérotation des pages
    print("Ajout de la numérotation dynamique des pages en pied de page...")
    add_footer_page_number(doc)
    
    # 11. Sauvegarde du fichier cible
    target_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
    print(f"Sauvegarde du document à l'emplacement exact : {target_path} ...")
    doc.save(target_path)
    
    duration = time.time() - start_time
    file_size_bytes = os.path.getsize(target_path)
    file_size_kb = file_size_bytes / 1024
    
    # Métriques
    num_paragraphs = len(doc.paragraphs)
    num_tables = len(doc.tables)
    total_words = sum(len(p.text.split()) for p in doc.paragraphs)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                total_words += len(cell.text.split())
                
    print("=" * 80)
    print("GÉNÉRATION DU RAPPORT TERMINÉE AVEC SUCCÈS !")
    print(f"Fichier généré : {target_path}")
    print(f"Taille du fichier : {file_size_kb:.2f} Ko ({file_size_bytes} octets)")
    print(f"Nombre de paragraphes : {num_paragraphs}")
    print(f"Nombre de tableaux et encadrés : {num_tables}")
    print(f"Nombre total de mots estimés : {total_words}")
    print(f"Durée totale d'exécution : {duration:.2f} secondes")
    print("=" * 80)

if __name__ == "__main__":
    main()
