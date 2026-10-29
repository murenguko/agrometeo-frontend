import docx
from docx.shared import Pt
import win32com.client
import os

test_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r3\test_toc_12pt.docx')
doc = docx.Document(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')

# Check TOC items font size
p_intro = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == 'INTRODUCTION GÉNÉRALE':
        p_intro = i
        break

# In TOC: paragraphs 17 to 92
for p in doc.paragraphs[17:93]:
    for r in p.runs:
        r.font.size = Pt(12)

doc.save(test_path)
print("Updated all TOC lines to 12pt")

word = win32com.client.Dispatch('Word.Application')
word.Visible = False
try:
    wdoc = word.Documents.Open(test_path)
    sec1 = wdoc.Sections(1)
    paras = [(p.Range.Text.strip(), p.Range.Information(1)) for p in sec1.Range.Paragraphs if p.Range.Text.strip()]
    for t, pg in paras:
        if any(h in t for h in ['TABLE DES MATIÈRES', 'TABLE DES ANNEXES', 'LISTE DES FIGURES']):
            print(f"{t[:30]} at sec1 pg {pg}")
    wdoc.Close(False)
finally:
    word.Quit()
