"""Hornsey Unit 1. Units: source px (half-res crop of the Unit 1 PDF), ~57 px = 1 m (from occupancy sq ft)."""
PX_PER_M = 57.0

def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

OUTER = (50, 18, 668, 1172)
FOOTPRINT = [(50, 18), (668, 18), (668, 1172), (458, 1160), (258, 1143), (50, 1143)]
OUTER_WALLS = [
    (50, 18, 668, 18, []),
    (668, 18, 668, 1172, []),
    (50, 18, 50, 1143, [(640, 720)]),      # side exit double doors
    (50, 1143, 258, 1143, []),
]
SLANTS = [  # (p0, p1, kind, gaps as fractions along the segment)
    ((258, 1143), (458, 1160), 'glass', [(0.27, 0.78)]),
    ((458, 1160), (668, 1172), 'wall', []),
]

WALLS = [
    (458, 18, 458, 1160, [(150, 205), (330, 380), (578, 622), (722, 772), (922, 972), (1062, 1110)]),
    (458, 220, 668, 220, []),
    (458, 432, 668, 432, []),
    (458, 630, 668, 630, []),
    (458, 807, 668, 807, []),
    (458, 995, 668, 995, []),
    (375, 148, 458, 148, [(395, 440)]),
    (375, 148, 375, 622, [(270, 315), (560, 620)]),
    (50, 208, 375, 208, []),
    (138, 378, 375, 378, [(150, 192)]),
    (50, 350, 138, 350, []),
    (138, 350, 138, 622, []),
    (138, 505, 375, 505, []),
    (50, 622, 375, 622, [(50, 138)]),
    (170, 622, 170, 743, [(645, 688)]),
    (50, 743, 400, 743, []),
    (255, 743, 255, 945, [(890, 945)]),
    (258, 945, 258, 1143, [(955, 1000), (1052, 1102)]),
    (400, 743, 400, 890, []),
    (255, 890, 400, 890, [(265, 312)]),
    (50, 945, 258, 945, []),
    (50, 1045, 258, 1045, []),
    (50, 995, 165, 995, []),
]
def THIN(w):
    return w[1] == 995 and w[3] == 995

DOORS = [
    (458, 205, 45, 'v', 1, -1), (458, 380, 48, 'v', 1, -1), (458, 622, 44, 'v', 1, -1),
    (458, 772, 48, 'v', 1, -1), (458, 972, 48, 'v', 1, -1), (458, 1110, 46, 'v', 1, -1),
    (395, 148, 45, 'h', 1, -1),
    (375, 315, 45, 'v', -1, -1),
    (150, 378, 42, 'h', 1, 1),
    (375, 620, 55, 'v', -1, -1),
    (170, 645, 43, 'v', 1, 1),
    (255, 890, 55, 'v', -1, 1),
    (265, 890, 47, 'h', 1, -1),
    (258, 955, 45, 'v', -1, 1),
    (258, 1052, 50, 'v', -1, 1),
    (50, 640, 40, 'v', -1, 1), (50, 720, 40, 'v', -1, -1),
]

WINDOWS = [('L', a, b) for a, b in [(48, 168), (232, 345), (762, 825), (870, 925), (1005, 1040)]] + \
          [('R', a, b) for a, b in [(30, 158), (232, 355), (475, 595), (612, 772), (835, 950), (1015, 1140)]]

OFFICES = [
    ("1", [(458, 995), (668, 995), (668, 1170), (458, 1160)], 148, (563, 1062)),
    ("2", rect(458, 807, 668, 995), 150, (563, 930)),
    ("3", rect(458, 630, 668, 807), 129, (502, 725)),
    ("4", rect(458, 432, 668, 630), 129, (525, 535)),
    ("5", rect(458, 220, 668, 432), 139, (575, 325)),
    ("6", rect(458, 18, 668, 220), 133, (562, 118)),
    ("7", [(50, 18), (458, 18), (458, 148), (375, 148), (375, 208), (50, 208)], 158, (245, 125)),
    ("8", [(50, 208), (375, 208), (375, 378), (138, 378), (138, 350), (50, 350)], 263, (215, 305)),
    ("8A", rect(138, 378, 375, 505), 112, (180, 425)),
    ("9", rect(138, 505, 375, 622), 105, (260, 590)),
    ("10", rect(255, 743, 400, 890), 70, (328, 845)),
    ("11", rect(50, 743, 255, 945), 203, (150, 865)),
]
DESKS_PER = {"1": 4, "2": 2, "3": 4, "4": 3, "5": 3, "6": 4, "7": 9, "8": 6, "8A": 2, "9": 2, "10": 2, "11": 3}

SHADED = [rect(50, 945, 258, 1045)]
STAIRS = [(52, 352, 136, 622, 'h')]   # stairs up to Unit 2 (above the hallway)
STAIR_FILL = '#D2CDC2'
GREYED = [rect(50, 622, 170, 743)]   # Unit 2 entrance hall, not part of Unit 1
COMMON_LABELS = [
    ("Reception", (358, 1015)),
    ("Breakout", (275, 655)),
    ("Unit 2", (110, 680)),
    ("entrance", (110, 698)),
    ("WCs", (205, 985)),
    ("Kitchen", (205, 1080)),
]

DESKS = [
    (57, 26, 63, 35, False), (120, 26, 63, 35, False), (183, 26, 63, 35, False),
    (283, 26, 128, 38, False),
    (60, 168, 128, 40, False), (247, 168, 128, 40, False),
    (57, 215, 218, 35, False),
    (125, 348, 248, 30, False),
    (300, 382, 35, 72, False), (207, 430, 35, 72, False),
    (148, 510, 72, 40, False), (300, 510, 72, 40, False),
    (528, 26, 68, 72, 'h'), (545, 145, 68, 72, 'h'),
    (525, 226, 68, 74, 'h'), (551, 357, 35, 73, False),
    (535, 438, 68, 74, 'h'), (568, 553, 35, 70, False),
    (465, 665, 72, 35, False), (592, 665, 72, 35, False), (548, 735, 70, 70, 'h'),
    (551, 815, 68, 72, 'h'),
    (465, 1005, 72, 35, False), (588, 1005, 72, 35, False), (542, 1090, 68, 66, 'h'),
    (107, 748, 66, 72, 'h'), (87, 868, 35, 72, False),
    (260, 748, 135, 32, False),
]
KITCHEN = [("sink", (58, 1052, 32, 50)), ("counter", (58, 1102, 128, 35)),
           ("bar", (178, 705, 222, 35)), ("bench", (510, 958, 150, 30)), ("shelves", (465, 815, 25, 100))]
TABLES = []
SOFAS = [(305, 662, 98, 42)]
PLANTS = [(70, 760), (165, 920), (432, 1135)]

META = dict(site='HORNSEY · 465 HORNSEY ROAD, N19', floor='', title='Unit 1', slug='hornsey-unit1', summary='11 private offices')
NORTH = (1, 0)
NOTE = 'South wall: hallway, side exit and stairs to Unit 2. Offices 5 and 6 are let together (272 sq ft).'
PINS = {'10': 'down'}
FLAT_MARGIN = (60, 10, 10, 70)

def _door_pair(S, ink, sw):
    # main entrance: double doors in the glazed front, opening outward
    return (f'<path d="M316,1148 A50,50 0 0 0 330,1198 M410,1156 A50,50 0 0 1 388,1205" fill="none" stroke="{ink}" stroke-width="{sw*0.6}" stroke-dasharray="2 3"/>'
            f'<line x1="316" y1="1148" x2="330" y2="1198" stroke="{ink}" stroke-width="{sw}"/>'
            f'<line x1="410" y1="1156" x2="388" y2="1205" stroke="{ink}" stroke-width="{sw}"/>')

def extras_flat(S):
    return [
        _door_pair(S, S['ink'], 2.2),
        f'<text x="363" y="1235" text-anchor="middle" class="bt" font-weight="700" font-size="11" letter-spacing="1.6" fill="{S["ink"]}">MAIN ENTRANCE</text>',
        f'<text x="20" y="680" text-anchor="middle" class="bt" font-size="10" letter-spacing="1.4" fill="{S["sub"]}" transform="rotate(-90 20 680)">STREET DOOR</text>',
        f'<text x="80" y="486" text-anchor="middle" class="bt" font-weight="700" font-size="11" letter-spacing="1.6" fill="{S["sub"]}" stroke="#D2CDC2" stroke-width="4" paint-order="stroke" transform="rotate(-90 80 486)">STAIRS UP TO UNIT 2</text>',
        f'<line x1="112" y1="600" x2="112" y2="378" stroke="{S["sub"]}" stroke-width="2.4"/><path d="M104,388 L112,372 L120,388 Z" fill="{S["sub"]}"/>',
    ]

def extras_iso():
    return [
        '<text x="363" y="1235" text-anchor="middle" class="bt" font-weight="700" font-size="14" letter-spacing="1.6" fill="#2D2D2A">MAIN ENTRANCE</text>',
        '<text x="94" y="486" text-anchor="middle" class="bt" font-weight="700" font-size="13" letter-spacing="1.6" fill="#6b6a63" stroke="#D2CDC2" stroke-width="5" paint-order="stroke" transform="rotate(-90 94 486)">STAIRS UP TO UNIT 2</text>',
    ]
