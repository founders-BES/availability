"""Hornsey Unit 4. Traced in the source JPG's pixels (29.2 px = 1 m, from the drawing's
17.69 m overall width), then doubled so text and line weights match the other plans."""
K = 2.0
PX_PER_M = 29.2 * K

def _p(x, y): return (x * K, y * K)
def rect(x0, y0, x1, y1):
    return [_p(x0, y0), _p(x1, y0), _p(x1, y1), _p(x0, y1)]
def poly(*pp): return [_p(x, y) for x, y in pp]
def wall(x0, y0, x1, y1, gaps=()):
    return (x0 * K, y0 * K, x1 * K, y1 * K, [(a * K, b * K) for a, b in gaps])

OUTER = (215 * K, 52 * K, 728 * K, 553 * K)
FOOTPRINT = poly((215, 52), (615, 52), (615, 458), (728, 458), (728, 553), (215, 553))
OUTER_WALLS = [
    wall(215, 52, 615, 52), wall(615, 52, 615, 458), wall(615, 458, 728, 458),
    wall(728, 458, 728, 553), wall(215, 553, 728, 553), wall(215, 52, 215, 553),
]
WINDOWS = [((215*K, 52*K, 615*K, 52*K), a*K, b*K) for a, b in [(288, 383), (438, 575)]] + \
          [((615*K, 52*K, 615*K, 458*K), a*K, b*K) for a, b in [(80, 293), (320, 393)]]
SLANTS = [(_p(518, 387), _p(560, 408), 'wall', [(0.3, 0.85)])]

WALLS = [
    wall(285, 82, 285, 223),
    wall(518, 52, 518, 387, [(90, 118), (130, 155), (266, 290)]),
    wall(518, 122, 615, 122), wall(518, 210, 615, 210), wall(518, 295, 615, 295),
    wall(560, 408, 560, 418), wall(560, 418, 615, 418),
    wall(218, 223, 482, 223, [(293, 318), (368, 392)]),
    wall(327, 223, 327, 355), wall(393, 223, 393, 355),
    wall(482, 223, 482, 553, [(322, 350), (362, 390), (405, 430)]),
    wall(215, 356, 482, 356),
    wall(381, 398, 482, 398), wall(381, 398, 381, 553),
    wall(482, 437, 532, 437),
    wall(672, 458, 672, 512), wall(618, 512, 672, 512, [(630, 655)]),
    wall(652, 512, 652, 553, [(522, 548)]),
]
def THIN(w):
    return w[0] >= 615 * K and w[1] >= 458 * K

DOORS = [(x * K, y * K, L * K, o, sx, sy) for x, y, L, o, sx, sy in [
    (285, 57, 22, 'v', 1, 1),
    (518, 118, 28, 'v', 1, -1), (518, 155, 25, 'v', 1, -1), (518, 290, 24, 'v', 1, -1),
    (293, 223, 25, 'h', 1, 1), (392, 223, 24, 'h', -1, 1),
    (482, 350, 28, 'v', -1, -1), (482, 390, 28, 'v', -1, -1), (482, 430, 25, 'v', -1, -1),
]]

OFFICES = [
    ("1", poly((215, 356), (482, 356), (482, 398), (381, 398), (381, 553), (215, 553)), 500, _p(345, 482)),
    ("2", rect(393, 223, 482, 356), 125, _p(436, 330)),
    ("3", rect(215, 223, 327, 356), 150, _p(258, 302)),
    ("4", poly((518, 295), (615, 295), (615, 418), (560, 418), (560, 408), (518, 387)), 161, _p(572, 362)),
    ("5", rect(381, 398, 482, 553), 225, _p(431, 470)),
    ("6", rect(518, 210, 615, 295), 87, _p(560, 238)),
    ("7", rect(518, 122, 615, 210), 80, _p(560, 160)),
    ("8", rect(518, 52, 615, 122), 67, _p(550, 82)),
    ("9", rect(327, 223, 393, 356), 104, _p(360, 330)),
]
DESKS_PER = {"1": 6, "2": 2, "3": 3, "4": 1, "5": 6, "6": 2, "7": 2, "8": 2, "9": 2}

GREYED = [rect(218, 55, 285, 223)]
STAIR_FILL = '#D2CDC2'
STAIRS = [(218 * K, 83 * K, 285 * K, 188 * K, 'h')]
TREAD = 24
SHADED = [rect(615, 458, 728, 553)]
COMMON_LABELS = [
    ("Open plan · dedicated desks", _p(400, 140)),
    ("Breakout", _p(548, 490)),
    ("Kitchenette", _p(548, 507)),
]

def d(x, y, w, h, pr=False):
    return (x * K, y * K, w * K, h * K, pr)
DESKS = [
    d(330, 57, 36, 35), d(367, 57, 36, 35), d(426, 57, 36, 35), d(463, 57, 36, 35),
    d(290, 128, 32, 37), d(333, 185, 33, 33), d(392, 185, 33, 33), d(448, 185, 33, 33),
    d(520, 57, 36, 18), d(577, 103, 35, 18),
    d(541, 192, 70, 16),
    d(540, 213, 18, 35), d(574, 258, 18, 32),
    d(288, 258, 36, 38, 'v'), d(220, 323, 35, 18), d(290, 326, 30, 18), d(232, 238, 22, 30),
    d(329, 268, 32, 35, 'v'),
    d(395, 248, 18, 70), d(458, 236, 22, 70),
    d(221, 382, 70, 36, True), d(221, 455, 70, 36, True), d(311, 405, 70, 36, True),
    d(384, 440, 20, 110), d(458, 440, 22, 110),
    d(522, 300, 18, 52),
]
KITCHEN_ISO = [("counter", tuple(v * K for v in (562, 418, 51, 18))), ("run", tuple(v * K for v in (594, 436, 19, 76)))]
KITCHEN = [
           ("shelves", tuple(v * K for v in (220, 223, 66, 10))), ("storage", tuple(v * K for v in (310, 356, 64, 9)))]
TABLES = [(493 * K, 455 * K, 9 * K), (493 * K, 488 * K, 9 * K), (497 * K, 517 * K, 9 * K)]
SOFAS = [tuple(v * K for v in (588, 362, 22, 40)), tuple(v * K for v in (335, 528, 40, 20))]
PLANTS = [_p(375, 236), _p(326, 538), _p(433, 540)]

META = dict(site='HORNSEY · 465 HORNSEY ROAD, N19', floor='FIRST FLOOR', title='Unit 4', slug='hornsey-unit4',
            summary='9 private offices · open-plan desks')
NORTH = (0, -1)   # top (open-plan window) wall faces north
NOTE = 'Open plan holds 10 dedicated desks. Overall 17.7 m × 17.3 m, from the drawing.'
PINS = {'8': 'up'}
TEXT_SCALE = 1.25
FLAT_MARGIN = (20, 10, 10, 10)
FURN_SCALE = 1.0

def _toilet(x, y, col):
    X, Y = _p(x, y)
    return (f'<rect x="{X-7}" y="{Y-10}" width="14" height="6" rx="2" fill="#FBFAF6" stroke="{col}" stroke-opacity=".5"/>'
            f'<ellipse cx="{X}" cy="{Y+4}" rx="6.5" ry="9" fill="#FBFAF6" stroke="{col}" stroke-opacity=".5"/>')

def _fixtures(S):
    c = S['ink']
    tx, ty = _p(620, 462); tw = 24 * K
    out = [f'<rect x="{tx}" y="{ty}" width="{tw}" height="{tw}" rx="3" fill="#FBFAF6" stroke="{c}" stroke-opacity=".5"/>'
           f'<line x1="{tx}" y1="{ty}" x2="{tx+tw}" y2="{ty+tw}" stroke="{c}" stroke-opacity=".3"/>'
           f'<line x1="{tx+tw}" y1="{ty}" x2="{tx}" y2="{ty+tw}" stroke="{c}" stroke-opacity=".3"/>',
           _toilet(660, 470, c), _toilet(690, 470, c), _toilet(716, 470, c)]
    for txt, (x, y) in [('SHOWER + WC', _p(645, 503)), ('WCs', _p(700, 503))]:
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" class="bt" font-size="11" letter-spacing="1.2" fill="{S["sub"]}">{txt}</text>')
    return out

def _kitchen(S):
    c = S['ink']
    X = lambda v: v * K
    top = '#EDE6D6'
    out = [
        # L-shaped worktop: along Office 4's wall, then down the WC wall
        f'<path d="M{X(562)},{X(418)} H{X(613)} V{X(512)} H{X(594)} V{X(436)} H{X(562)} Z" fill="{top}" stroke="{c}" stroke-opacity=".45" stroke-width="1.4"/>',
        # hob
        *[f'<circle cx="{X(cx)}" cy="{X(427)}" r="{X(3.6)}" fill="none" stroke="{c}" stroke-opacity=".55" stroke-width="1.3"/>' for cx in (570, 580)],
        # sink with tap
        f'<rect x="{X(597)}" y="{X(448)}" width="{X(13)}" height="{X(18)}" rx="5" fill="#FBFAF6" stroke="{c}" stroke-opacity=".55" stroke-width="1.3"/>',
        f'<circle cx="{X(611.5)}" cy="{X(457)}" r="2.6" fill="{c}" fill-opacity=".55"/>',
        # fridge
        f'<rect x="{X(596)}" y="{X(484)}" width="{X(15)}" height="{X(15)}" rx="2" fill="#FBFAF6" stroke="{c}" stroke-opacity=".55" stroke-width="1.3"/>',
        f'<text x="{X(603.5)}" y="{X(493.5)}" text-anchor="middle" class="bt" font-size="8" letter-spacing=".8" fill="{S["sub"]}">FRIDGE</text>',
        # stools at the counter
        *[f'<circle cx="{X(cx)}" cy="{X(445)}" r="{X(3.4)}" fill="#cbb89a" fill-opacity=".7"/>' for cx in (568, 579)],
    ]
    return out

def extras_flat(S):
    x, y = _p(240, 136)
    ax, ay0, ay1 = 268 * K, 92 * K, 182 * K
    fx = _fixtures(S) + _kitchen(S)
    return fx + [f'<text x="{x}" y="{y}" text-anchor="middle" class="bt" font-weight="700" font-size="13" letter-spacing="1.6" fill="{S["ink"]}" stroke="#D2CDC2" stroke-width="4" paint-order="stroke" transform="rotate(-90 {x} {y})">DOWN TO EXIT</text>',
            f'<line x1="{ax}" y1="{ay0}" x2="{ax}" y2="{ay1}" stroke="{S["ink"]}" stroke-width="2.6"/><path d="M{ax-9},{ay1-10} L{ax},{ay1+8} L{ax+9},{ay1-10} Z" fill="{S["ink"]}"/>']

def extras_iso():
    x, y = _p(251, 136)
    a, b = _p(645, 500); c, d = _p(700, 500)
    return [f'<text x="{x}" y="{y}" text-anchor="middle" class="bt" font-weight="700" font-size="14" letter-spacing="1.6" fill="#2D2D2A" stroke="#D2CDC2" stroke-width="5" paint-order="stroke" transform="rotate(-90 {x} {y})">DOWN TO EXIT</text>',
            f'<text x="{a}" y="{b}" text-anchor="middle" class="bt" font-size="12" letter-spacing="1.2" fill="#8a877d">SHOWER + WC</text>',
            f'<text x="{c}" y="{d}" text-anchor="middle" class="bt" font-size="12" letter-spacing="1.2" fill="#8a877d">WCs</text>']

# skylights, 1.6 m x 0.6 m, centred under each office name (Ilan, 26 Oct 2026)
def _sky(cx, top):
    w, h = 1.6 * PX_PER_M, 0.6 * PX_PER_M
    return (cx - w / 2, top, w, h)
SKYLIGHTS = [_sky(345 * K, 482 * K + 38), _sky(431 * K, 470 * K + 38)]
