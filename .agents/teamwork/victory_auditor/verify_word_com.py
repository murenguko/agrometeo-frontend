import win32com.client as win32
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DOCX_PATH = os.path.abspath(r"c:\Users\PC\Desktop\Projects\weather-app\Rapport_Projet_Veille_Meteo_Burundi.docx")

print(f"Testing MS Word COM automation on: {DOCX_PATH}")

word = win32.Dispatch('Word.Application')
word.Visible = False
word.DisplayAlerts = 0

try:
    doc = word.Documents.Open(DOCX_PATH, ReadOnly=True, ConfirmConversions=False)
    total_pages = doc.ComputeStatistics(2)
    print(f"Total document pages reported by Word engine: {total_pages}")
    
    sec1 = doc.Sections(1)
    sec2 = doc.Sections(2)
    
    sec1_style = sec1.Headers(1).PageNumbers.NumberStyle
    sec2_style = sec2.Headers(1).PageNumbers.NumberStyle
    sec2_start = sec2.Headers(1).PageNumbers.StartingNumber
    sec2_restart = sec2.Headers(1).PageNumbers.RestartNumberingAtSection
    
    print(f"Section 1 PageNumberStyle: {sec1_style} (2 = wdPageNumberStyleLowercaseRoman)")
    print(f"Section 2 PageNumberStyle: {sec2_style} (0 = wdPageNumberStyleArabic)")
    print(f"Section 2 RestartNumbering: {sec2_restart}, StartingNumber: {sec2_start}")
    
    assert sec1_style == 2, f"Expected Section 1 to be lowercase roman (2), got {sec1_style}"
    assert sec2_style == 0, f"Expected Section 2 to be arabic (0), got {sec2_style}"
    assert sec2_restart == True or sec2_restart == -1, f"Expected Section 2 to restart numbering"
    assert sec2_start == 1, f"Expected Section 2 starting number to be 1, got {sec2_start}"

    # Verify paragraph count
    para_count = doc.Paragraphs.Count
    print(f"Total Word paragraphs: {para_count}")
    
    # Check margins reported by Word
    print(f"Section 1 Margins: Left={sec1.PageSetup.LeftMargin * 2.54 / 72:.2f} cm, Right={sec1.PageSetup.RightMargin * 2.54 / 72:.2f} cm, Top={sec1.PageSetup.TopMargin * 2.54 / 72:.2f} cm, Bottom={sec1.PageSetup.BottomMargin * 2.54 / 72:.2f} cm")
    print(f"Section 2 Margins: Left={sec2.PageSetup.LeftMargin * 2.54 / 72:.2f} cm, Right={sec2.PageSetup.RightMargin * 2.54 / 72:.2f} cm, Top={sec2.PageSetup.TopMargin * 2.54 / 72:.2f} cm, Bottom={sec2.PageSetup.BottomMargin * 2.54 / 72:.2f} cm")
    
    assert abs((sec1.PageSetup.LeftMargin * 2.54 / 72) - 3.0) < 0.1, "Sec1 left margin not 3 cm"
    assert abs((sec2.PageSetup.LeftMargin * 2.54 / 72) - 3.0) < 0.1, "Sec2 left margin not 3 cm"

    doc.Close(False)
    print("ALL MS WORD COM CHECKS PASSED PERFECTLY!")
finally:
    word.Quit()
