import win32com.client as win32
import os
import sys

print("Initializing Word COM...", flush=True)
word = win32.Dispatch('Word.Application')
print(f"Word version: {word.Version}", flush=True)
word.Visible = False
word.DisplayAlerts = 0

doc_path = os.path.abspath(r'c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx')
print(f"Opening {doc_path}...", flush=True)
try:
    doc = word.Documents.Open(doc_path, ReadOnly=True, ConfirmConversions=False)
    print("Document opened successfully!", flush=True)
    total_pages = doc.ComputeStatistics(2)
    print(f"Total pages: {total_pages}", flush=True)
    doc.Close(False)
    print("Document closed.", flush=True)
finally:
    word.Quit()
    print("Word quit.", flush=True)
