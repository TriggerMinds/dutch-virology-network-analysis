"""
generate_og_image.py — STAP 1b: Generates a high-res social preview image (assets/og-preview.png).
Uses Pillow to render network visualization preview.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)
OUT = os.path.join(ASSETS, "og-preview.png")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("[og] Pillow not available — generating placeholder SVG instead")
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630">
      <rect width="1200" height="630" fill="#0B0E14"/>
      <circle cx="200" cy="200" r="6" fill="#e94560"/>
      <circle cx="400" cy="150" r="5" fill="#5dade2"/>
      <circle cx="600" cy="250" r="8" fill="#e94560"/>
      <circle cx="350" cy="300" r="4" fill="#2ecc71"/>
      <circle cx="700" cy="180" r="5" fill="#f39c12"/>
      <circle cx="500" cy="350" r="6" fill="#e94560"/>
      <line x1="200" y1="200" x2="400" y2="150" stroke="#5dade2" stroke-width="1" opacity="0.5"/>
      <line x1="400" y1="150" x2="600" y2="250" stroke="#e74c3c" stroke-width="1.5" opacity="0.5"/>
      <line x1="600" y1="250" x2="350" y2="300" stroke="#2ecc71" stroke-width="1" opacity="0.5"/>
      <line x1="200" y1="200" x2="500" y2="350" stroke="#f39c12" stroke-width="1" opacity="0.4"/>
      <text x="100" y="420" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#e94560">De Pandemische Draaischijf</text>
      <text x="100" y="460" font-family="Arial, sans-serif" font-size="16" fill="#8a8ab5">Forensisch onderzoek naar de Nederlandse virologietop · 5.401 nodes · 6.530 edges</text>
      <text x="100" y="490" font-family="Arial, sans-serif" font-size="14" fill="#4a4a75">€67,6M+ subsidies · WOO-stukken · OMT-adviezen · Feb 1 2020 call</text>
    </svg>'''
    svg_path = os.path.join(ASSETS, "og-preview.svg")
    with open(svg_path, "w") as f:
        f.write(svg)
    print(f"  -> {svg_path} (SVG placeholder)")
    sys.exit(0)

W, H = 1200, 630
img = Image.new("RGBA", (W, H), (11, 14, 20, 255))
draw = ImageDraw.Draw(img)

# Draw abstract network nodes
import random
random.seed(42)
nodes = []
node_colors = [(233,69,96), (93,173,226), (46,204,113), (243,156,18), (149,165,166)]
for i in range(60):
    x = random.randint(50, W-50)
    y = random.randint(40, H-200)
    r = random.randint(3, 9)
    c = random.choice(node_colors)
    nodes.append((x, y, r, c))
    draw.ellipse([x-r, y-r, x+r, y+r], fill=c)

# Draw edges
for i in range(min(120, len(nodes))):
    a = random.randint(0, len(nodes)-1)
    b = random.randint(0, len(nodes)-1)
    if a != b:
        x1,y1,r1,c1 = nodes[a]; x2,y2,r2,c2 = nodes[b]
        draw.line([(x1,y1),(x2,y2)], fill=(c1[0],c1[1],c1[2],80), width=1)

# Title area
try:
    font_large = ImageFont.truetype("arial.ttf", 40)
    font_med = ImageFont.truetype("arial.ttf", 18)
    font_small = ImageFont.truetype("arial.ttf", 14)
except:
    font_large = ImageFont.load_default()
    font_med = font_small = font_large

draw.text((60, H-170), "De Pandemische Draaischijf", fill=(233,69,96), font=font_large)
draw.text((60, H-125), "Forensisch onderzoek — 5.401 nodes · 6.530 edges · 3 multiplex lagen", fill=(138,138,181), font=font_med)
draw.text((60, H-95), "€67,6M+ EU/ZonMw subsidies · WOO-stukken · OMT-adviezen · Feb 1 2020 teleconferentie", fill=(74,74,117), font=font_small)

img.save(OUT, "PNG")
print(f"  -> {OUT} ({os.path.getsize(OUT)/1024:.0f} KB)")
