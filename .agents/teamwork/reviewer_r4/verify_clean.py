import win32com.client as win32
import json
import os
import sys
import time

doc_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

print(f"Target: {doc_path}", flush=True)

# Clean any lock files first
lock_file = os.path.join(os.path.dirname(doc_path), f"~${os.path.basename(doc_path)}")
if os.path.exists(lock_file):
    print(f"Removing lock file: {lock_file}", flush=True)
    os.remove(lock_file)

with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\headings_pages.json', 'r', encoding='utf-8') as f:
    headings_dict = json.load(f)

with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\figures_tables_pages.json', 'r', encoding='utf-8') as f:
    fig_tab_dict = json.load(f)

# Targets to check
targets = set(headings_dict.keys())
fig_prefixes = {t.split('—')[0].strip(): t for t in fig_tab_dict['figures']}
tab_prefixes = {t.split('—')[0].strip(): t for t in fig_tab_dict['tables']}

word = win32.Dispatch('Word.Application')
word.Visible = False
t0 = time.time()
try:
    doc = word.Documents.Open(doc_path)
    print(f"Opened document in {time.time()-t0:.2f}s", flush=True)
    total_pages = doc.ComputeStatistics(2)
    print(f"Total document pages in Word: {total_pages}", flush=True)
    
    sec1 = doc.Sections(1)
    sec2 = doc.Sections(2)
    
    sec1_style = sec1.Headers(1).PageNumbers.NumberStyle
    print(f"Sec 1 page number style: {sec1_style} (2 = wdPageNumberStyleLowercaseRoman)", flush=True)
    
    sec2_style = sec2.Headers(1).PageNumbers.NumberStyle
    sec2_start = sec2.Headers(1).PageNumbers.StartingNumber
    sec2_restart = sec2.Headers(1).PageNumbers.RestartNumberingAtSection
    print(f"Sec 2 page number style: {sec2_style} (0 = wdPageNumberStyleArabic), restart={sec2_restart}, start={sec2_start}", flush=True)
    
    heading_matches = {}
    figure_matches = {}
    table_matches = {}
    
    for p in sec2.Range.Paragraphs:
        t = p.Range.Text.strip()
        if not t:
            continue
        
        # Check if t matches a heading
        matched_h = None
        if t in headings_dict:
            matched_h = t
        else:
            for h in headings_dict:
                if h not in heading_matches and (t == h or t.startswith(h)):
                    matched_h = h
                    break
        if matched_h and matched_h not in heading_matches:
            pg = p.Range.Information(1)
            heading_matches[matched_h] = pg
            continue
            
        # Check figures
        for fp, full_f in fig_prefixes.items():
            if full_f not in figure_matches and (t.startswith(fp) or fp in t):
                pg = p.Range.Information(1)
                figure_matches[full_f] = pg
                break
                
        # Check tables
        for tp, full_t in tab_prefixes.items():
            if full_t not in table_matches and (t.startswith(tp) or tp in t):
                pg = p.Range.Information(1)
                table_matches[full_t] = pg
                break

    print(f"Found {len(heading_matches)}/{len(headings_dict)} headings, {len(figure_matches)}/{len(fig_prefixes)} figures, {len(table_matches)}/{len(tab_prefixes)} tables in {time.time()-t0:.2f}s", flush=True)

    heading_errors = 0
    for h, exp_pg in headings_dict.items():
        act_pg = heading_matches.get(h)
        if act_pg != exp_pg:
            print(f"HEADING ERROR: {h} -> exp {exp_pg}, got {act_pg}", flush=True)
            heading_errors += 1
            
    fig_errors = 0
    for f_title, exp_pg in fig_tab_dict['figures'].items():
        act_pg = figure_matches.get(f_title)
        if act_pg != exp_pg:
            print(f"FIGURE ERROR: {f_title} -> exp {exp_pg}, got {act_pg}", flush=True)
            fig_errors += 1

    tab_errors = 0
    for t_title, exp_pg in fig_tab_dict['tables'].items():
        act_pg = table_matches.get(t_title)
        if act_pg != exp_pg:
            print(f"TABLE ERROR: {t_title} -> exp {exp_pg}, got {act_pg}", flush=True)
            tab_errors += 1

    if heading_errors == 0 and fig_errors == 0 and tab_errors == 0:
        print(f"ALL AUDITS PASSED PERFECTLY! 100% concordance in {time.time()-t0:.2f}s", flush=True)
    else:
        print(f"FAILURES DETECTED: Headings: {heading_errors}, Figures: {fig_errors}, Tables: {tab_errors}", flush=True)

    doc.Close(False)
finally:
    word.Quit()
print("Verification finished.", flush=True)
