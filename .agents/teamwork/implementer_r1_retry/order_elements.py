import docx
import sys
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

body_elements = doc._body._element

tbl_idx = 0
p_idx = 0

for child in body_elements:
    if isinstance(child, CT_P):
        p = docx.text.paragraph.Paragraph(child, doc)
        text = p.text.strip()
        if text.startswith("Tableau ") or text.startswith("Figure ") or text.startswith("CHAPITRE") or text.startswith("ANNEXE") or "CONCLUSION" in text or "INTRODUCTION" in text:
            print(f"P[{p_idx}]: {text[:80]}")
        p_idx += 1
    elif isinstance(child, CT_Tbl):
        table = docx.table.Table(child, doc)
        first_cell = table.cell(0, 0).text.strip().replace("\n", " ")[:60]
        print(f"  >>> TBL[{tbl_idx}] (after P[{p_idx-1}]): {first_cell}")
        tbl_idx += 1
