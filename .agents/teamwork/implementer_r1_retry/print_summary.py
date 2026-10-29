import json
import sys

# Force stdout UTF-8
sys.stdout.reconfigure(encoding='utf-8')

with open(r".agents\teamwork\implementer_r1_retry\doc_analysis.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print("=== HEADINGS ===")
for h in d["headings"]:
    print(f"[{h['idx']}] ({h['style']}): {h['text']}")

print("\n=== FIGURES ===")
for f in d["figures"]:
    print(f"[{f['idx']}]: {f['text']}")

print("\n=== TABLES CAPTIONS ===")
for t in d["tables_captions"]:
    print(f"[{t['idx']}]: {t['text']}")

print("\n=== BIBLIOGRAPHY ===")
for b in d["bibliography"]:
    print(f"[{b['idx']}]: {b['text']}")

print("\n=== ACRONYMS FOUND ===")
print(", ".join(d["acronyms_found"][:50]))
print("\n=== CITATIONS FOUND ===")
print(", ".join(d["citations_found"]))
