import docx
import re
import sys
import json

DOC_PATH = r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx"

doc = docx.Document(DOC_PATH)

paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
tables_data = []
for t_idx, table in enumerate(doc.tables):
    rows_data = []
    for row in table.rows:
        row_text = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
        rows_data.append(row_text)
    tables_data.append(rows_data)

total_paragraphs = len(doc.paragraphs)
total_tables = len(doc.tables)
total_words = sum(len(p.split()) for p in paragraphs)
for t in tables_data:
    for row in t:
        for cell in row:
            total_words += len(cell.split())

print(f"Total paragraphs in doc: {total_paragraphs}")
print(f"Non-empty paragraphs: {len(paragraphs)}")
print(f"Total tables: {total_tables}")
print(f"Total words: {total_words}")

# Save full text to text file for analysis
with open(r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\challenger_report_2\extracted_text.txt", "w", encoding="utf-8") as f:
    f.write("=== PARAGRAPHS ===\n")
    for i, p in enumerate(doc.paragraphs):
        f.write(f"[{i}] {p.text}\n")
    f.write("\n=== TABLES ===\n")
    for t_idx, t in enumerate(tables_data):
        f.write(f"\n--- TABLE {t_idx} ---\n")
        for row in t:
            f.write(" | ".join(row) + "\n")

print("Saved extracted_text.txt successfully.")
