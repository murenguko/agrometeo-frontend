import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

# Find the comparison matrix table
for t_idx, t in enumerate(doc.tables):
    t_text = "\n".join(" | ".join(c.text.strip() for c in r.cells) for r in t.rows)
    if "Spécification Initiale Cadrage MVP" in t_text or "Matrice comparative exhaustive" in t_text or "Qualification de l'Écart" in t_text:
        print(f"=== TABLE {t_idx} : COMPARISON MATRIX ===")
        for r_idx, r in enumerate(t.rows):
            cells = [c.text.strip().replace("\n", " ") for c in r.cells]
            print(f"\n--- Row {r_idx} ---")
            for c_idx, c in enumerate(cells):
                print(f"  Col {c_idx}: {c}")

