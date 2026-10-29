import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re
import json
import win32com.client
import os

DOC_PATH = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

print("1. Opening target document...")
doc = docx.Document(DOC_PATH)

# Find RÉFÉRENCES BIBLIOGRAPHIQUES in TOC and in Body
toc_biblio_p = None
p_intro_idx = None
body_biblio_p = None

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if t == 'INTRODUCTION GÉNÉRALE':
        p_intro_idx = i
    if p_intro_idx is None and 'RÉFÉRENCES BIBLIOGRAPHIQUES' in t:
        toc_biblio_p = p
    elif p_intro_idx is not None and t == 'RÉFÉRENCES BIBLIOGRAPHIQUES':
        body_biblio_idx = i
        body_biblio_p = p

print(f"TOC Biblio paragraph: {repr(toc_biblio_p.text)}")
print(f"Body Biblio paragraph at index {body_biblio_idx}: {repr(body_biblio_p.text)}")

# 1. Update Body Bibliography entries to Times New Roman 12pt, line_spacing 1.5 (R4 compliance)
biblio_entries = doc.paragraphs[body_biblio_idx + 1:]
print(f"Updating {len(biblio_entries)} bibliography entries to 12pt, 1.5 line spacing...")

for p in biblio_entries:
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

# 2. Update TOC Biblio line to page 59 and add space_before=8 to separate clearly from Table des Annexes
toc_biblio_p.text = ""
toc_biblio_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
toc_biblio_p.paragraph_format.line_spacing = 1.15
toc_biblio_p.paragraph_format.space_before = Pt(8)
toc_biblio_p.paragraph_format.space_after = Pt(2)

pPr = toc_biblio_p._element.get_or_add_pPr()
tabs = OxmlElement('w:tabs')
tab = OxmlElement('w:tab')
tab.set(qn('w:val'), 'right')
tab.set(qn('w:leader'), 'dot')
tab.set(qn('w:pos'), '9070')
tabs.append(tab)
pPr.append(tabs)

r1 = toc_biblio_p.add_run("RÉFÉRENCES BIBLIOGRAPHIQUES")
r1.font.name = "Times New Roman"
r1.font.size = Pt(12)
r1.bold = True

r2 = toc_biblio_p.add_run("\t59")
r2.font.name = "Times New Roman"
r2.font.size = Pt(12)
r2.bold = True

from docx.enum.text import WD_BREAK
r2.add_break(WD_BREAK.PAGE)

# Save document
doc.save(DOC_PATH)
print("Saved Rapport_Projet_Veille_Meteo_Burundi.docx with updated typography and TOC page.")

# 3. Update headings_pages.json
json_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r2\headings_pages.json')
with open(json_path, 'r', encoding='utf-8') as f:
    hdata = json.load(f)

hdata["RÉFÉRENCES BIBLIOGRAPHIQUES"] = 59
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(hdata, f, ensure_ascii=False, indent=2)

print("Updated headings_pages.json with page 59 for RÉFÉRENCES BIBLIOGRAPHIQUES.")

# 4. Verify in Word COM
print("Verifying in Microsoft Word via COM...")
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
try:
    wdoc = word.Documents.Open(DOC_PATH)
    total_pages = wdoc.ComputeStatistics(2)
    print(f"Total pages computed in Word: {total_pages}")
    
    sec2 = wdoc.Sections(2)
    paras = [(p.Range.Text.strip(), p.Range.Information(1)) for p in sec2.Range.Paragraphs if p.Range.Text.strip()]
    
    found_ref = None
    for t, pg in paras:
        if t == "RÉFÉRENCES BIBLIOGRAPHIQUES":
            found_ref = pg
            print(f"Word rendered 'RÉFÉRENCES BIBLIOGRAPHIQUES' at Section 2 page {pg}")
            break
            
    assert found_ref == 59, f"Expected 59 but got {found_ref}"
    print("SUCCESS: Word layout confirmed RÉFÉRENCES BIBLIOGRAPHIQUES is exactly on page 59!")
    wdoc.Close(False)
finally:
    word.Quit()
