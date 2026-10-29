import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import shutil

# Make a test copy
test_docx = r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\implementer_r1_retry\test_doc.docx"
shutil.copyfile(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx.bak", test_docx)

doc = docx.Document(test_docx)
print("Initial sections:", len(doc.sections))
p0 = doc.paragraphs[0]
print("p0 text:", p0.text)

# Insert a preliminary paragraph before p0
p_pre = p0.insert_paragraph_before("Ceci est une page de test liminaire.")

# Add sectPr to p_pre.paragraph_format or oxml
pPr = p_pre._element.get_or_add_pPr()
sectPr = OxmlElement('w:sectPr')

# Margins: left=3cm (1701 twips), others=2.5cm (1417 twips)
pgMar = OxmlElement('w:pgMar')
pgMar.set(qn('w:top'), '1417')
pgMar.set(qn('w:right'), '1417')
pgMar.set(qn('w:bottom'), '1417')
pgMar.set(qn('w:left'), '1701')
pgMar.set(qn('w:header'), '720')
pgMar.set(qn('w:footer'), '720')
sectPr.append(pgMar)

# pgSz
pgSz = OxmlElement('w:pgSz')
pgSz.set(qn('w:w'), '12240')
pgSz.set(qn('w:h'), '15840')
sectPr.append(pgSz)

# pgNumType lowerRoman start=1
pgNumType = OxmlElement('w:pgNumType')
pgNumType.set(qn('w:fmt'), 'lowerRoman')
pgNumType.set(qn('w:start'), '1')
sectPr.append(pgNumType)

pPr.append(sectPr)

# Now check how many sections doc has!
# We might need to save and reload or inspect doc.sections
doc.save(test_docx)

doc2 = docx.Document(test_docx)
print("Reloaded sections count:", len(doc2.sections))
for i, s in enumerate(doc2.sections):
    print(f"Section {i}: left={s.left_margin.cm:.2f}cm, top={s.top_margin.cm:.2f}cm")

print("Section 0 footer:", len(doc2.sections[0].footer.paragraphs))
print("Section 1 footer:", len(doc2.sections[1].footer.paragraphs))
