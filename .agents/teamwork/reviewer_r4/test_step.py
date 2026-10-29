import win32com.client as win32
import time
import os

with open(r'c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\reviewer_r4\word_log.txt', 'w', encoding='utf-8') as log:
    log.write(f"Start: {time.time()}\n")
    log.flush()
    word = win32.Dispatch('Word.Application')
    log.write(f"Word dispatched: {time.time()}\n")
    log.flush()
    word.Visible = False
    doc_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')
    log.write(f"Opening doc: {time.time()}\n")
    log.flush()
    try:
        doc = word.Documents.Open(doc_path)
        log.write(f"Doc opened: {time.time()}\n")
        log.flush()
        pages = doc.ComputeStatistics(2)
        log.write(f"ComputeStatistics: {pages} at {time.time()}\n")
        log.flush()
        doc.Close(False)
        log.write(f"Doc closed at {time.time()}\n")
        log.flush()
    except Exception as e:
        log.write(f"Error: {e}\n")
        log.flush()
    finally:
        word.Quit()
        log.write(f"Word quit at {time.time()}\n")
        log.flush()
