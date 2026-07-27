from pathlib import Path
import re
import xml.etree.ElementTree as ET

source = Path("profile-3d-contrib/profile-gitblock.svg")
target = Path("assets/02-contributions-panel.svg")

if not source.exists():
    raise SystemExit(f"Missing generated file: {source}")

raw = source.read_text(encoding="utf-8")
match = re.search(r"<svg\b([^>]*)>(.*)</svg>\s*$", raw, re.S)
if not match:
    raise SystemExit("Could not parse generated Git Block SVG")

attrs, inner = match.groups()
viewbox_match = re.search(r'viewBox="([^"]+)"', attrs)
if viewbox_match:
    viewbox = viewbox_match.group(1)
else:
    width = re.search(r'width="([^"]+)"', attrs)
    height = re.search(r'height="([^"]+)"', attrs)
    viewbox = f"0 0 {width.group(1) if width else 1000} {height.group(1) if height else 500}"

panel = f"""<svg xmlns="http://www.w3.org/2000/svg"
 width="1200" height="720" viewBox="0 0 1200 720">
 <defs>
  <linearGradient id="profileBg" x1="0" y1="0" x2="1" y2="1">
   <stop offset="0" stop-color="#010604"/>
   <stop offset=".52" stop-color="#07130c"/>
   <stop offset="1" stop-color="#010604"/>
  </linearGradient>
  <radialGradient id="profileGlow" cx=".5" cy=".45" r=".72">
   <stop offset="0" stop-color="#1cff72" stop-opacity=".11"/>
   <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <pattern id="profileGrid" width="30" height="30" patternUnits="userSpaceOnUse">
   <path d="M30 0H0V30" fill="none" stroke="#2aff79" stroke-opacity=".035"/>
  </pattern>
 </defs>
 <rect width="1200" height="720" fill="url(#profileBg)"/>
 <rect width="1200" height="720" fill="url(#profileGlow)"/>
 <rect width="1200" height="720" fill="url(#profileGrid)"/>
 <path d="M1 0V720 M1199 0V720" stroke="#1f6b3c" stroke-opacity=".8"/>
 <rect x="48" y="42" width="1104" height="636" rx="22"
       fill="#020604" fill-opacity=".72"
       stroke="#2ddc72" stroke-opacity=".36"/>
 <svg x="76" y="68" width="1048" height="584"
      viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet">
  {inner}
 </svg>
</svg>"""

target.write_text(panel, encoding="utf-8")
ET.parse(target)
print(f"Built {target}")
