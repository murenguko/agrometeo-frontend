import docx
from docx.shared import Pt
import win32com.client
import os

test_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r3\test_biblio_fix.docx')
doc = docx.Document(test_path)

# Find where LISTE DES SIGLES is
in_sigles = False
p_intro = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == 'LISTE DES SIGLES, ABRÉVIATIONS ET ACRONYMES':
        in_sigles = True
        continue
    if p.text.strip() == 'INTRODUCTION GÉNÉRALE':
        p_intro = i
        break
    if in_sigles and p.text.strip():
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)

doc.save(test_path)
print("Updated sigles to 12pt")

word = win32com.client.Dispatch('Word.Application')
word.Visible = False
try:
    wdoc = word.Documents.Open(test_path)
    print("Section 1 pages:", wdoc.Sections(1).Range.ComputeStatistics(2))
    print("Section 2 pages:", wdoc.Sections(2).Range.ComputeStatistics(2))
    print("Total doc pages:", wdoc.ComputeStatistics(2))
    
    sec1 = wdoc.Sections(1)
    paras = [(p.Range.Text.strip(), p.Range.Information(1)) for p in sec1.Range.Paragraphs if p.Range.Text.strip()]
    for t, pg in paras:
        if any(h in t for h in ['LISTE DES SIGLES', 'API :', 'XSS :']):
            print(f"{t[:25]} at sec1 pg {pg}")
            
    sec2 = wdoc.Sections(2)
    paras2 = [(p.Range.Text.strip(), p.Range.Information(1)) for p in sec2.Range.Paragraphs if p.Range.Text.strip()]
    for t, pg in paras2:
        if 'INTRODUCTION GÉNÉRALE' in t:
            print(f"{t[:25]} at sec2 pg {pg}")
            
    wdoc.Close(False)
finally:
    word.Quit()
