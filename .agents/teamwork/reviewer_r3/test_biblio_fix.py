import docx
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import shutil
import win32com.client
import os

src_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')
test_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r3\test_biblio_fix.docx')

shutil.copyfile(src_path, test_path)
doc = docx.Document(test_path)

biblio_idx = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().upper() == "RÉFÉRENCES BIBLIOGRAPHIQUES":
        biblio_idx = i
        break

print(f"Biblio heading at p{biblio_idx}")

for p in doc.paragraphs[biblio_idx + 1:]:
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

doc.save(test_path)
print("Saved test document with 12pt / 1.5 spacing for bibliography")

# Query Word COM to verify layout impact
word = win32com.client.Dispatch('Word.Application')
word.Visible = False
try:
    wdoc = word.Documents.Open(test_path)
    total_pages = wdoc.ComputeStatistics(2)
    print(f"Total pages in test doc: {total_pages}")
    
    sec2 = wdoc.Sections(2)
    paras = [(p.Range.Text.strip(), p.Range.Information(1)) for p in sec2.Range.Paragraphs if p.Range.Text.strip()]
    
    for t, pg in paras:
        if 'RÉFÉRENCES BIBLIOGRAPHIQUES' in t or 'ANNEXE D' in t or 'CONCLUSION' in t:
            print(f"{t[:40]} at page {pg}")
            
    wdoc.Close(False)
finally:
    word.Quit()
