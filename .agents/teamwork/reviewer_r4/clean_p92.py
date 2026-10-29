import docx

doc_path = r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx'
doc = docx.Document(doc_path)

p = doc.paragraphs[92]
print(f"Before: {len(p.runs)} runs")
for r in p.runs:
    print(f"  run: {repr(r.text)}, font: {r.font.name}")

# If the first run is empty, remove it
if len(p.runs) > 1 and p.runs[0].text == '':
    p._p.remove(p.runs[0]._r)
    print("Removed empty run.")

print(f"After: {len(p.runs)} runs")
for r in p.runs:
    print(f"  run: {repr(r.text)}, font: {r.font.name}")

doc.save(doc_path)
print("Saved clean document.")
