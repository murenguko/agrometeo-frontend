import docx
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = docx.Document(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

# Let's inspect each heading and its position in terms of word count
total_words = 0
sections_pos = []

for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    words = len(text.split())
    
    # Check if heading
    if (text in ["INTRODUCTION GÉNÉRALE", "CONCLUSION GÉNÉRALE ET PERSPECTIVES", "RÉFÉRENCES BIBLIOGRAPHIQUES"] or
        text.startswith("CHAPITRE ") or text.startswith("ANNEXE ") or
        (p.style.name != "List Bullet" and any(text.startswith(f"{i}. ") for i in range(1, 10)))):
        sections_pos.append((idx, text, total_words))
    
    total_words += words

# Add table words (roughly 30 words per row or 1/3 page per table)
# Total document pages is 59 pages in Word
print(f"Total words in paragraphs: {total_words}")
print(f"Estimated pages: ~59 pages")

for idx, title, w in sections_pos:
    est_page = 1 + int(round((w / total_words) * 58))
    print(f"P[{idx:03d}] (w={w:5d}) -> Est Page {est_page:2d}: {title[:70]}")
