import win32com.client as win32
import json
import os
import sys

doc_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

word = win32.Dispatch('Word.Application')
word.Visible = False
try:
    doc = word.Documents.Open(doc_path)
    total_pages = doc.ComputeStatistics(2)
    print(f"Total document pages in Word: {total_pages}")
    
    sec1 = doc.Sections(1)
    sec2 = doc.Sections(2)
    
    # Check Section 1 Footer
    sec1_style = sec1.Headers(1).PageNumbers.NumberStyle
    print(f"Sec 1 page number style: {sec1_style} (2 = wdPageNumberStyleLowercaseRoman)")
    
    # Check Section 2 Footer
    sec2_style = sec2.Headers(1).PageNumbers.NumberStyle
    sec2_start = sec2.Headers(1).PageNumbers.StartingNumber
    sec2_restart = sec2.Headers(1).PageNumbers.RestartNumberingAtSection
    print(f"Sec 2 page number style: {sec2_style} (0 = wdPageNumberStyleArabic), restart={sec2_restart}, start={sec2_start}")
    
    # Check all headings
    with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\headings_pages.json', 'r', encoding='utf-8') as f:
        headings_dict = json.load(f)
        
    sec2_paras = [(p.Range.Text.strip(), p.Range.Information(1)) for p in sec2.Range.Paragraphs if p.Range.Text.strip()]
    
    heading_errors = 0
    for title, exp_pg in headings_dict.items():
        act_pg = None
        for t, pg in sec2_paras:
            if t == title or t.startswith(title):
                act_pg = pg
                break
        if act_pg != exp_pg:
            print(f"HEADING ERROR: {title} -> exp {exp_pg}, got {act_pg}")
            heading_errors += 1
            
    if heading_errors == 0:
        print(f"SUCCESS: All {len(headings_dict)} headings match adjusted page numbers in Word exactly!")
        
    # Check figures and tables
    with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\figures_tables_pages.json', 'r', encoding='utf-8') as f:
        fig_tab_dict = json.load(f)
        
    fig_errors = 0
    for title, exp_pg in fig_tab_dict['figures'].items():
        prefix = title.split('—')[0].strip()
        act_pg = None
        for t, pg in sec2_paras:
            if t.startswith(prefix) or prefix in t:
                act_pg = pg
                break
        if act_pg != exp_pg:
            print(f"FIGURE ERROR: {title} -> exp {exp_pg}, got {act_pg}")
            fig_errors += 1
            
    tab_errors = 0
    for title, exp_pg in fig_tab_dict['tables'].items():
        prefix = title.split('—')[0].strip()
        act_pg = None
        for t, pg in sec2_paras:
            if t.startswith(prefix) or prefix in t:
                act_pg = pg
                break
        if act_pg != exp_pg:
            print(f"TABLE ERROR: {title} -> exp {exp_pg}, got {act_pg}")
            tab_errors += 1
            
    if fig_errors == 0 and tab_errors == 0:
        print(f"SUCCESS: All {len(fig_tab_dict['figures'])} figures and {len(fig_tab_dict['tables'])} tables match adjusted page numbers in Word exactly!")
        
    doc.Close(False)
finally:
    word.Quit()
