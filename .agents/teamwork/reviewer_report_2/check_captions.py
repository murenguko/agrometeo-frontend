import docx

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

print("=== CHECKING TABLE AND FIGURE CAPTION POSITIONS ===")
# In python-docx, document element order: doc.element.body contains both <w:p> and <w:tbl> elements in document order!
body_elements = doc.element.body

elements = []
for child in body_elements:
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        p = docx.text.paragraph.Paragraph(child, doc)
        txt = p.text.strip()
        if txt.startswith("Tableau ") or "Tableau " in txt[:15]:
            elements.append(('TABLE_CAPTION', txt[:60]))
        elif txt.startswith("Figure ") or "Figure " in txt[:15]:
            elements.append(('FIGURE_CAPTION', txt[:60]))
    elif tag == 'tbl':
        elements.append(('TABLE_OBJECT', 'tbl'))

print(f"Total relevant elements: {len(elements)}")
for i, el in enumerate(elements[:25]):
    print(f"{i:2d}: {el[0]} -> {el[1]}")
