import docx
import json
import re

doc_path = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"
doc = docx.Document(doc_path)

output_data = {
    "total_paragraphs": len(doc.paragraphs),
    "total_tables": len(doc.tables),
    "total_sections": len(doc.sections),
    "sections": [],
    "headings": [],
    "figures": [],
    "tables_captions": [],
    "bibliography": [],
    "acronyms_found": set(),
    "citations_found": set()
}

for i, section in enumerate(doc.sections):
    output_data["sections"].append({
        "index": i,
        "page_width_cm": round(section.page_width.cm, 2),
        "page_height_cm": round(section.page_height.cm, 2),
        "left_margin_cm": round(section.left_margin.cm, 2),
        "right_margin_cm": round(section.right_margin.cm, 2),
        "top_margin_cm": round(section.top_margin.cm, 2),
        "bottom_margin_cm": round(section.bottom_margin.cm, 2),
        "header_distance_cm": round(section.header_distance.cm, 2),
        "footer_distance_cm": round(section.footer_distance.cm, 2),
        "different_first_page_header_footer": section.different_first_page_header_footer
    })

in_biblio = False

# Common technical acronyms regex
acronym_pattern = re.compile(r'\b[A-Z]{2,10}\b')
citation_pattern = re.compile(r'\[(\d+(?:[,\s–-]+\d+)*)\]')

all_text = []

for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    all_text.append(text)

    # find citations
    for m in citation_pattern.finditer(text):
        output_data["citations_found"].add(m.group(0))

    # find acronyms
    for m in acronym_pattern.finditer(text):
        output_data["acronyms_found"].add(m.group(0))

    if "RÉFÉRENCES BIBLIOGRAPHIQUES" in text.upper():
        in_biblio = True
        output_data["headings"].append({"idx": idx, "style": p.style.name, "text": text})
        continue
        
    if in_biblio:
        output_data["bibliography"].append({"idx": idx, "style": p.style.name, "text": text})
        continue

    if text.startswith("Figure ") or text.startswith("Fig. "):
        output_data["figures"].append({"idx": idx, "style": p.style.name, "text": text})
    elif text.startswith("Tableau ") or text.startswith("Table "):
        output_data["tables_captions"].append({"idx": idx, "style": p.style.name, "text": text})
    elif (p.style.name.startswith("Heading") or 
          any(text.startswith(h) for h in ["INTRODUCTION", "CHAPITRE", "Chapitre", "CONCLUSION", "ANNEXE", "Annexe"]) or
          re.match(r"^(\d+(\.\d+)*)\s+[A-ZÀ-Ÿ]", text) or
          re.match(r"^[A-Z]\.\d+\s+[A-ZÀ-Ÿ]", text)):
        output_data["headings"].append({"idx": idx, "style": p.style.name, "text": text})

# Also inspect tables for table captions or content
table_summaries = []
for t_idx, t in enumerate(doc.tables):
    rows = len(t.rows)
    cols = len(t.columns) if rows > 0 else 0
    first_cell = t.cell(0, 0).text.strip().replace("\n", " ") if rows > 0 and cols > 0 else ""
    table_summaries.append({
        "table_index": t_idx,
        "rows": rows,
        "cols": cols,
        "first_cell": first_cell[:80]
    })
output_data["table_summaries"] = table_summaries

output_data["acronyms_found"] = sorted(list(output_data["acronyms_found"]))
output_data["citations_found"] = sorted(list(output_data["citations_found"]))

with open(r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\implementer_r1_retry\doc_analysis.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("Analysis successfully written to doc_analysis.json")
