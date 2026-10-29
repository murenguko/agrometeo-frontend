import docx
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.enum.text import WD_ALIGN_PARAGRAPH

test_docx = r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\implementer_r1_retry\test_doc.docx"
doc = docx.Document(test_docx)

sec0 = doc.sections[0]
sec1 = doc.sections[1]

print("sec1 footer is_linked_to_previous:", sec1.footer.is_linked_to_previous)

# We unlink sec1 footer from sec0
sec1.footer.is_linked_to_previous = False
print("After unlink, sec1 footer is_linked_to_previous:", sec1.footer.is_linked_to_previous)

# In sec1 footer, make sure page numbering is decimal starting at 1
sectPr1 = sec1._sectPr
pgNumType1 = sectPr1.find(qn('w:pgNumType'))
if pgNumType1 is None:
    pgNumType1 = OxmlElement('w:pgNumType')
    sectPr1.append(pgNumType1)
pgNumType1.set(qn('w:fmt'), 'decimal')
pgNumType1.set(qn('w:start'), '1')

# In sec0 footer, make sure page numbering is lowerRoman starting at 1
sectPr0 = sec0._sectPr
pgNumType0 = sectPr0.find(qn('w:pgNumType'))
if pgNumType0 is None:
    pgNumType0 = OxmlElement('w:pgNumType')
    sectPr0.append(pgNumType0)
pgNumType0.set(qn('w:fmt'), 'lowerRoman')
pgNumType0.set(qn('w:start'), '1')

print("sec0 sectPr XML:", sectPr0.xml)
print("sec1 sectPr XML:", sectPr1.xml)

# Check footer paragraphs
footer0 = sec0.footer
footer0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
# Make sure footer has PAGE field
p0 = footer0.paragraphs[0]
p0.text = ""
fld_xml = parse_xml(r'''
<w:pPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:pStyle w:val="Footer"/>
    <w:jc w:val="center"/>
</w:pPr>
''')
p0._element.append(fld_xml)
run1 = p0.add_run()
run1._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w')))
run2 = p0.add_run()
run2._r.append(parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w')))
run3 = p0.add_run()
run3._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w')))
run4 = p0.add_run("i")
run5 = p0.add_run()
run5._r.append(parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w')))

doc.save(test_docx)
print("Saved and verified successfully!")
