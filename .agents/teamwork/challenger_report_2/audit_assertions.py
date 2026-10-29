import re

with open(r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\challenger_report_2\extracted_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

out_lines = []

def search_patterns(title, pattern, flags=re.IGNORECASE):
    out_lines.append(f"\n=================== {title} ===================")
    matches = list(re.finditer(pattern, text, flags))
    out_lines.append(f"Found {len(matches)} occurrences.")
    for i, m in enumerate(matches):
        start = max(0, m.start() - 150)
        end = min(len(text), m.end() + 150)
        snippet = text[start:end].replace('\n', ' ')
        out_lines.append(f"[{i+1}] ...{snippet}...\n")

search_patterns("POSTGRESQL MENTIONS", r"postgres(ql)?")
search_patterns("MONGODB MENTIONS", r"mongodb")
search_patterns("SQLITE MENTIONS", r"sqlite")
search_patterns("PROVINCES & IMBO/MUMIRWA", r"(imbo|mumirwa|gitega|karusi|rutana|bujumbura rural)")
search_patterns("NASA LHASA MENTIONS", r"(lhasa|glissement|landslide)")
search_patterns("ARGON2ID & DUMMY HASH", r"(argon2|dummy|timing)")
search_patterns("JWT & COOKIES HTTP-ONLY", r"(jwt|bearer|httponly|http-only)")
search_patterns("FASTAPI ROUTES", r"(/user|/token|/\{location\}|weather_data)")
search_patterns("LEAFLET & SVELTE 5", r"(leaflet|sveaflet|6 marqueurs|runes|\$state|\$derived|\$props)")
search_patterns("SEUILS IGEBU & GLOFAS", r"(50\s*mm|100\s*mm|60\s*mm|90\s*mm|40\s*km/h|glofas|p75)")
search_patterns("PYTEST & 31 TESTS", r"(pytest|31\s*tests|31/31)")

with open(r"c:\Users\PC\Desktop\Projects\weather-app\.agents\teamwork\challenger_report_2\audit_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("Audit results written to audit_results.txt successfully.")
