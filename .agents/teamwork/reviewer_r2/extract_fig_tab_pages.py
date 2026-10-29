import win32com.client as win32
import json

word = win32.gencache.EnsureDispatch('Word.Application')
word.Visible = False
try:
    doc = word.Documents.Open(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx', ReadOnly=True)
    sec2 = doc.Sections(2)
    
    figures_list = [
        ("Figure 1.2 — Diagramme de flux du parcours utilisateur complet", "Figure 1.2"),
        ("Figure 2.1 — Diagramme architectural du patron Backend-For-Frontend (BFF)", "Figure 2.1"),
        ("Figure 3.1 — Architecture logicielle globale en couches et interconnexions de données", "Figure 3.1"),
        ("Figure 3.2 — Diagramme de cas d'utilisation du système AgroMétéo Burundi", "Figure 3.2"),
        ("Figure 3.3 — Diagramme de classes métier du backend AgroMétéo Burundi", "Figure 3.3"),
        ("Figure 3.4 — Diagramme de composants logiciels du système", "Figure 3.4"),
        ("Figure 3.5 — Diagramme de séquence de l'authentification OAuth2 / JWT", "Figure 3.5"),
        ("Figure 3.6 — Diagramme de séquence de la consultation d'un bulletin agro-météorologique", "Figure 3.6"),
        ("Figure 4.1 — Structure modulaire de la base de code du backend FastAPI", "Figure 4.1"),
        ("Figure 4.2 — Structure modulaire du frontend SvelteKit", "Figure 4.2")
    ]

    tables_list = [
        ("Tableau 0.1 — Objectifs Spécifiques et Indicateurs Mesurables de Succès (SMART)", "Tableau 0.1"),
        ("Tableau 1.1 — Caractérisation géographique et agro-climatique des zones pilotes d'étude", "Tableau 1.1"),
        ("Tableau 1.2 — Matrice des besoins exprimés par typologie d'utilisateurs", "Tableau 1.2"),
        ("Tableau 3.1 — Spécification formelle des exigences fonctionnelles (EF-01 à EF-20)", "Tableau 3.1"),
        ("Tableau 3.2 — Spécification formelle des exigences non fonctionnelles (ENF-01 à ENF-10)", "Tableau 3.2"),
        ("Tableau 3.3 — Description des classes et modules logiciels métier", "Tableau 3.3"),
        ("Tableau 3.4 — Planification Scrum et exécution des sprints sur 10 jours ouvrés", "Tableau 3.4"),
        ("Tableau 4.1 — Matrice de l'environnement technologique et outillage de développement", "Tableau 4.1"),
        ("Tableau 5.1 — Registre exhaustif des 31 tests unitaires validés sous pytest (100% succès)", "Tableau 5.1"),
        ("Tableau A.1 — Spécification tabulaire détaillée des cas d'utilisation", "Tableau A.1"),
        ("Tableau A.2 — Dictionnaire formel des transitions de la machine à états de vigilance", "Tableau A.2"),
        ("Tableau B.1 — Dictionnaire des données de la collection MongoDB 'users'", "Tableau B.1"),
        ("Tableau B.2 — Schéma physique des tables du cache local SQLite", "Tableau B.2")
    ]
    
    sec2_paras = []
    for p in sec2.Range.Paragraphs:
        t = p.Range.Text.strip()
        if t:
            page_in_sec = p.Range.Information(1) # wdActiveEndAdjustedPageNumber
            sec2_paras.append((t, page_in_sec))
            
    fig_res = {}
    for full_title, prefix in figures_list:
        page = None
        for t, p in sec2_paras:
            if t.startswith(prefix) or prefix in t:
                page = p
                break
        fig_res[full_title] = page
        print(f"Fig [{page:2d}] {full_title}")
        
    tab_res = {}
    for full_title, prefix in tables_list:
        page = None
        for t, p in sec2_paras:
            if t.startswith(prefix) or prefix in t:
                page = p
                break
        tab_res[full_title] = page
        print(f"Tab [{page:2d}] {full_title}")
        
    with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\figures_tables_pages.json', 'w', encoding='utf-8') as f:
        json.dump({'figures': fig_res, 'tables': tab_res}, f, ensure_ascii=False, indent=2)
        
    doc.Close(False)
finally:
    word.Quit()
