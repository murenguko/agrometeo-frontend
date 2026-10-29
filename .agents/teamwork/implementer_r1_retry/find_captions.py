import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

fig_regex = re.compile(r'^(Figure\s+\d+(\.\d+)*\s*[:—–-]\s*.+)', re.IGNORECASE)
tab_regex = re.compile(r'^(Tableau\s+\d+(\.\d+)*\s*[:—–-]\s*.+)', re.IGNORECASE)

figures = []
tables = []

for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    m_fig = fig_regex.match(text)
    if m_fig:
        figures.append((idx, text))
    m_tab = tab_regex.match(text)
    if m_tab:
        tables.append((idx, text))
    # also check if "Figure " or "Tableau " is in the line
    if ("Figure " in text or "Tableau " in text) and not m_fig and not m_tab:
        if any(text.startswith(prefix) for prefix in ["Figure", "Tableau"]):
            print(f"Potential uncaptured caption at P[{idx}]: {text}")

print(f"Found {len(figures)} figures:")
for idx, f in figures:
    print(f"  P[{idx}]: {f}")

print(f"\nFound {len(tables)} tables captions:")
for idx, t in tables:
    print(f"  P[{idx}]: {t}")

print(f"\nDoc has {len(doc.tables)} actual table objects.")
