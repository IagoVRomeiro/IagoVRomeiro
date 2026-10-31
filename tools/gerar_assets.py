import os, random, sys, textwrap
from xml.sax.saxutils import escape
out = sys.argv[1]
os.makedirs(f"{out}/assets/cards", exist_ok=True)

# ---------- Cavaleiro em pixel art (desenho próprio) ----------
KNIGHT = """
..W..........W..
..W..........W..
.WW..........WW.
.WW..........WW.
.WWW........WWW.
..WWW......WWW..
...WWWWWWWWWW...
..WWWWWWWWWWWW..
..WWWWWWWWWWWW..
..WWBBBWWBBBWW..
..WWBBBWWBBBWW..
..WWBBBWWBBBWW..
..WWWBWWWWBWWW..
...WWWWWWWWWW...
....WWWWWWWW....
....CCCCCCCC....
...CCCCCCCCCC...
..CCCCECCCCCCC..
..CCCCECCCCCCC..
.CCCCCECCCCCCCC.
.CCCCCCECCCCCCC.
CCCCCCCECCCCCCCC
CC.CCCCCCCCCC.CC
...DD......DD...
...DD......DD...
""".strip().splitlines()
COL = {"W": "#f2f0ea", "B": "#0b0d14", "C": "#2c3150", "D": "#1b1f33", "E": "#454d7d", "O": "#05060a"}

def knight_rects(px, ox=0, oy=0):
    h, w = len(KNIGHT), len(KNIGHT[0])
    grid = [list(r) for r in KNIGHT]
    filled = lambda x, y: 0 <= y < h and 0 <= x < w and grid[y][x] != "."
    rects = []
    # contorno escuro: aparece no tema claro e no escuro
    for y in range(-1, h + 1):
        for x in range(-1, w + 1):
            if not filled(x, y) and any(filled(x + dx, y + dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
                rects.append((x, y, "O"))
    for y in range(h):
        for x in range(w):
            if grid[y][x] != ".":
                rects.append((x, y, grid[y][x]))
    return "".join(f'<rect x="{ox+(x)*px}" y="{oy+(y)*px}" width="{px}" height="{px}" fill="{COL[c]}"/>' for x, y, c in rects)

px = 10
kw, kh = (16 + 2) * px, (len(KNIGHT) + 2) * px
souls = "".join(
    f'<circle cx="{random.Random(i).randint(10, kw+50)}" cy="{kh+60}" r="{random.Random(i*7).choice([2,3,3,4])}" fill="#dfe8ff">'
    f'<animate attributeName="cy" values="{kh+60};20" dur="{4+i%3}s" begin="{i*0.7}s" repeatCount="indefinite"/>'
    f'<animate attributeName="opacity" values="0;.9;0" dur="{4+i%3}s" begin="{i*0.7}s" repeatCount="indefinite"/></circle>'
    for i in range(8))
open(f"{out}/assets/knight.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{kw+60}" height="{kh+70}" viewBox="0 0 {kw+60} {kh+70}" shape-rendering="crispEdges">
<style>.k{{animation:bob 1.6s steps(2) infinite}}@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-{px}px)}}}}
.sh{{animation:sh 1.6s steps(2) infinite;transform-origin:center}}@keyframes sh{{0%,100%{{opacity:.35}}50%{{opacity:.2}}}}</style>
<ellipse class="sh" cx="{30+kw/2}" cy="{kh+35}" rx="{kw/2.6}" ry="7" fill="#000"/>
{souls}
<g transform="translate(30,30)"><g class="k">{knight_rects(px, px, px)}</g></g>
</svg>''')

# ---------- Banner ----------
W, H = 1280, 400
rnd = random.Random(42)
parts = "".join(
    (lambda x, d, b, r: f'<circle cx="{x}" cy="{H+10}" r="{r}" fill="#e8eeff"><animate attributeName="cy" values="{H+10};-10" dur="{d}s" begin="-{b}s" repeatCount="indefinite"/>'
     f'<animate attributeName="opacity" values="0;.8;.8;0" dur="{d}s" begin="-{b}s" repeatCount="indefinite"/></circle>')
    (rnd.randint(0, W), rnd.uniform(7, 14), rnd.uniform(0, 14), rnd.choice([1.5, 2, 2.5, 3]))
    for _ in range(40))
def hills(y0, amp, seed, color, op):
    r = random.Random(seed); pts = []
    for x in range(0, W + 81, 80):
        pts.append(f"{x},{y0 - r.randint(0, amp)}")
    return f'<polygon points="0,{H} {" ".join(pts)} {W},{H}" fill="{color}" opacity="{op}"/>'
def spires(seed, base, color, op, n):
    r = random.Random(seed); s = ""
    for _ in range(n):
        x = r.randint(0, W); w = r.randint(14, 34); h = r.randint(90, 230)
        s += f'<polygon points="{x},{base} {x},{base-h} {x+w/2},{base-h-w*1.4} {x+w},{base-h} {x+w},{base}" fill="{color}" opacity="{op}"/>'
    return s
mist = lambda y, d, op: (f'<ellipse cx="{W/2}" cy="{y}" rx="{W*0.7}" ry="40" fill="url(#mist)" opacity="{op}">'
    f'<animate attributeName="cx" values="{W*0.35};{W*0.65};{W*0.35}" dur="{d}s" repeatCount="indefinite"/></ellipse>')
knight_small = knight_rects(5)
open(f"{out}/assets/banner.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0e1c"/><stop offset=".6" stop-color="#1a2440"/><stop offset="1" stop-color="#2a3658"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".42" r=".45"><stop offset="0" stop-color="#9fb4ff" stop-opacity=".35"/><stop offset="1" stop-color="#9fb4ff" stop-opacity="0"/></radialGradient>
<radialGradient id="mist"><stop offset="0" stop-color="#c9d4f5" stop-opacity=".35"/><stop offset="1" stop-color="#c9d4f5" stop-opacity="0"/></radialGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
{spires(3, H, "#3a4670", .35, 14)}
{hills(330, 60, 1, "#1d2642", .9)}
{mist(300, 26, .9)}
{spires(9, H, "#121829", .9, 8)}
{hills(370, 30, 2, "#0b0f1c", 1)}
{mist(360, 34, .7)}
{parts}
<g transform="translate({W-210},{H-150})" shape-rendering="crispEdges">{knight_small}</g>
<g font-family="'Trajan Pro','Cinzel','Times New Roman',Georgia,serif" text-anchor="middle" fill="#f4f1ea" stroke="#05060a" stroke-linejoin="round" paint-order="stroke">
<text x="{W/2}" y="150" font-size="38" stroke-width="6" letter-spacing="10">OLÁ, EU SOU O</text>
<text x="{W/2}" y="265" font-size="128" font-weight="700" stroke-width="12" letter-spacing="18">IAGO</text>
<text x="{W/2}" y="315" font-size="24" stroke-width="5" letter-spacing="5" fill="#c8d2ee">ENGENHARIA DE COMPUTAÇÃO · PUC MINAS</text>
</g>
<path d="M{W/2-170} 178 h120 l12 -6 l12 6 h96 l12 -6 l12 6 h120" stroke="#f4f1ea" stroke-width="2" fill="none" opacity=".7"/>
</g>
</svg>''')

# ---------- Cards dos repositórios ----------
LANG = {"Python": "#3572A5", "C++": "#f34b7d", "Dart": "#00B4AB", "Assembly": "#6E4C13", "Java": "#b07219", "TypeScript": "#3178c6"}
CARDS = [
    ("mosca-knight", "Mosca-das-frutas simulada, com cérebro do conectoma real, que aprende a jogar Hollow Knight só pela imagem da tela.", "Python"),
    ("PrevencaoIncendio_IOT", "Keep It Green: ESP32 com sensores que detectam fogo, alertam o app via MQTT e acionam irrigação. Destaque do TI da PUC Minas.", "C++"),
    ("VanGo", "App que conecta motoristas de van escolar aos alunos: rota otimizada, GPS em tempo real, chat e notificações.", "Dart"),
    ("AC3-Trabalho", "Pipeline RISC-V escalar e superescalar: hazards, forwarding, predição de desvios e Tomasulo no Ripes.", "Assembly"),
]
book = "M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"
for name, desc, lang in CARDS:
    lines = textwrap.wrap(desc, 58)[:3]
    tl = "".join(f'<tspan x="25" dy="{0 if i == 0 else 19}">{escape(l)}</tspan>' for i, l in enumerate(lines))
    open(f"{out}/assets/cards/{name}.svg", "w").write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="150" viewBox="0 0 420 150">
<style>text{{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif}}</style>
<rect x=".5" y=".5" width="419" height="149" rx="8" fill="#0d1117" stroke="#30363d"/>
<rect x=".5" y=".5" width="4" height="149" rx="2" fill="#c8d2ee" opacity=".7"/>
<g transform="translate(25,22)"><path d="{book}" fill="#8b949e" transform="scale(1.1)"/></g>
<text x="50" y="36" font-size="17" font-weight="600" fill="#e6edf3">{escape(name)}</text>
<text y="68" font-size="13.5" fill="#9da7b3">{tl}</text>
<circle cx="31" cy="128" r="6" fill="{LANG[lang]}"/>
<text x="43" y="133" font-size="13" fill="#9da7b3">{lang}</text>
</svg>''')

