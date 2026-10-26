"""Hornsey Unit 6. Units: source px (half-res crop of the Unit 6 PDF), ~73.6 px = 1 m (from occupancy sq ft)."""
PX_PER_M = 73.6
TEXT_SCALE = 1.6
FLAT_AREA_W = 800
FURN_SCALE = 2.0
WALL_W = (8, 15)

def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

OUTER = (18, 18, 1312, 1200)
WALLS = [
    (452, 18, 452, 250, []),
    (18, 250, 892, 250, [(382, 437)]),
    (892, 18, 892, 567, [(176, 234), (262, 318)]),
    (892, 155, 1022, 155, []),
    (1022, 155, 1022, 245, [(172, 228)]),
    (1022, 245, 1312, 245, []),
    (1022, 455, 1312, 455, []),
    (1022, 623, 1312, 623, []),
    (877, 815, 1312, 815, [(952, 1004)]),
    (877, 1040, 877, 1200, [(1060, 1170)]),
    (877, 1040, 1312, 1040, []),
    (682, 250, 682, 567, []),
    (682, 412, 892, 412, []),
    (452, 567, 892, 567, [(610, 665), (702, 757)]),
    (452, 250, 452, 567, []),
    (345, 250, 345, 428, [(258, 318)]),
    (345, 328, 452, 328, [(382, 438)]),
    (345, 428, 452, 428, []),
    (128, 400, 128, 692, [(474, 522), (600, 650)]),
    (18, 400, 128, 400, []), (18, 468, 128, 468, [(72, 118)]), (18, 528, 128, 528, [(72, 118)]), (18, 595, 128, 595, []),
    (18, 692, 697, 692, [(150, 212), (410, 465), (497, 552)]),
    (232, 692, 232, 1200, []),
    (480, 692, 480, 1200, []),
    (480, 870, 697, 870, []),
    (480, 1045, 697, 1045, []),
    (697, 692, 697, 1200, [(892, 947), (1128, 1183)]),
]
GLASS_WALLS = [(877, 815, 877, 1040, []),   # glazed screen between Office 1 and reception
               (1022, 245, 1022, 815, [(260, 315), (562, 617), (757, 812)])]   # Offices 2-4 corridor screen

def THIN(w):
    return (w[0] == 18 and w[2] == 128) or (w[1] == 1045 and w[0] == 232)

DOORS = [
    (382, 250, 55, 'h', 1, -1),
    (892, 234, 58, 'v', -1, -1), (892, 262, 56, 'v', -1, 1),
    (1022, 228, 56, 'v', 1, -1), (1022, 260, 55, 'v', 1, 1),
    (1022, 617, 55, 'v', 1, -1),
    (1022, 812, 55, 'v', 1, -1),
    (1004, 815, 52, 'h', -1, 1),
    (877, 1060, 55, 'v', 1, 1), (877, 1170, 55, 'v', 1, -1),
    (610, 567, 55, 'h', 1, -1), (702, 567, 55, 'h', 1, -1),
    (345, 258, 60, 'v', -1, 1), (382, 328, 56, 'h', 1, 1),
    (212, 692, 62, 'h', -1, 1), (410, 692, 55, 'h', 1, 1), (552, 692, 55, 'h', -1, 1),
    (697, 892, 55, 'v', -1, 1), (697, 1128, 55, 'v', -1, 1),
    (128, 474, 46, 'v', 1, 1), (118, 468, 44, 'h', -1, -1), (118, 528, 44, 'h', -1, 1), (128, 600, 48, 'v', -1, 1),
]

WINDOWS = [('R', a, b) for a, b in [(92, 158), (262, 428), (470, 540), (735, 800), (830, 1030)]] + \
          [('B', a, b) for a, b in [(100, 220), (255, 405), (487, 557)]]

OFFICES = [
    ("1", rect(877, 815, 1312, 1040), 260, (1095, 925)),
    ("2", rect(1022, 623, 1312, 815), 113, (1165, 730)),
    ("3", rect(1022, 455, 1312, 623), 113, (1165, 540)),
    ("4", rect(1022, 245, 1312, 455), 130, (1165, 345)),
    ("5", [(892, 18), (1312, 18), (1312, 245), (1022, 245), (1022, 155), (892, 155)], 198, (1060, 150)),
    ("6", rect(452, 18, 892, 250), 209, (700, 150)),
    ("7", rect(682, 250, 892, 412), 80, (787, 320)),
    ("8", rect(452, 250, 682, 567), 165, (567, 315)),
    ("9", rect(682, 412, 892, 567), 0, (787, 445), 'Meeting room'),
    ("10", rect(18, 18, 452, 250), 200, (300, 145)),
    ("11", rect(18, 692, 232, 1200), 197, (125, 880)),
    ("12", rect(232, 692, 480, 1200), 223, (380, 840)),
    ("13", rect(480, 692, 697, 870), 79, (588, 765)),
    ("14", rect(480, 870, 697, 1045), 75, (600, 958)),
    ("15", rect(480, 1045, 697, 1200), 63, (600, 1150)),
]
DESKS_PER = {"1": 7, "2": 3, "3": 3, "4": 4, "5": 4, "6": 6, "7": 2, "8": 4, "10": 8, "11": 5, "12": 3, "13": 2, "14": 2, "15": 1}

SHADED = [rect(18, 400, 128, 692), rect(345, 250, 452, 428)]
GREYED = [rect(877, 1040, 1312, 1200)]
STAIR_FILL = '#D2CDC2'
STAIRS = [(1017, 1048, 1300, 1195, 'v')]
TREAD = 40
COMMON_LABELS = [
    ("Kitchen", (240, 560)),
    ("Reception", (790, 1110)),
    ("Store", (398, 300)),
    ("Boiler", (398, 395)),
]

DESKS = [
    (76, 28, 88, 88, 'h'), (262, 28, 88, 88, 'h'), (77, 160, 88, 88, 'h'), (268, 158, 85, 90, 'h'),
    (457, 28, 88, 44, False), (600, 28, 88, 44, False), (735, 28, 90, 44, False),
    (457, 205, 88, 45, False), (585, 205, 88, 45, False), (715, 205, 90, 45, False),
    (457, 255, 45, 88, False), (457, 377, 45, 90, False), (635, 255, 45, 90, False), (635, 380, 45, 88, False),
    (685, 362, 88, 44, False), (800, 362, 90, 44, False),
    (967, 28, 44, 88, False), (1137, 28, 88, 88, 'h'), (1175, 150, 44, 90, False),
    (1102, 250, 90, 44, False), (1210, 250, 90, 44, False), (1025, 410, 90, 44, False), (1212, 410, 90, 44, False),
    (1025, 460, 45, 88, False), (1132, 460, 90, 44, False), (1258, 530, 45, 88, False),
    (1025, 628, 90, 45, False), (1215, 628, 85, 45, False), (1205, 768, 90, 44, False),
    (1018, 820, 88, 44, False), (1118, 820, 88, 44, False), (1218, 820, 88, 44, False),
    (885, 993, 95, 44, False), (997, 993, 90, 44, False), (1105, 993, 90, 44, False), (1213, 993, 90, 44, False),
    (28, 920, 45, 88, False), (28, 1100, 45, 95, False), (185, 820, 45, 88, False), (185, 970, 45, 88, False), (185, 1100, 45, 92, False),
    (272, 705, 45, 88, False), (277, 887, 45, 88, False), (370, 1108, 88, 44, False),
    (483, 825, 88, 42, False), (607, 823, 88, 42, False),
    (484, 875, 88, 42, False), (592, 993, 90, 44, False),
    (485, 1050, 44, 85, False),
]
KITCHEN = [("table", (315, 475, 133, 53))]
KITCHEN_ISO = [("worktop", (25, 253, 237, 45)), ("tall", (25, 298, 40, 100)), ("cabinet", (130, 400, 42, 70))]
TABLES = [(830, 500, 32), (80, 770, 38)]
SOFAS = [(827, 830, 46, 115)]
PLANTS = [(330, 667), (60, 960), (818, 975), (120, 1020)]

SKYLIGHTS = [(75, 312, 107, 70), (200, 315, 45, 68), (180, 112, 73, 46), (470, 128, 105, 70), (545, 358, 68, 50)]

META = dict(site='HORNSEY · 465 HORNSEY ROAD, N19', floor='', title='Unit 6', slug='hornsey-unit6',
            summary='14 private offices · meeting room')
NORTH = (0, 1)   # bottom (Office 11-15) window wall faces north
NOTE = 'Office 9 is the meeting room.'
PINS = {'11': 'down', '7': 'left', '6': 'up', '3': 'up', '2': 'down'}
FLAT_MARGIN = (20, 10, 10, 10)

def _toilet(x, y, c):
    return (f'<rect x="{x-12}" y="{y-16}" width="24" height="9" rx="3" fill="#FBFAF6" stroke="{c}" stroke-opacity=".5" stroke-width="1.6"/>'
            f'<ellipse cx="{x}" cy="{y+5}" rx="11" ry="15" fill="#FBFAF6" stroke="{c}" stroke-opacity=".5" stroke-width="1.6"/>')

def _kitchen(S):
    c = S['ink']; top = '#EDE6D6'
    return [
        f'<path d="M25,253 H262 V298 H65 V398 H25 Z" fill="{top}" stroke="{c}" stroke-opacity=".45" stroke-width="2"/>',
        *[f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="{c}" stroke-opacity=".55" stroke-width="2"/>' for x, y in [(42, 265), (62, 265), (42, 286), (62, 286)]],
        f'<rect x="105" y="259" width="34" height="32" rx="7" fill="#FBFAF6" stroke="{c}" stroke-opacity=".55" stroke-width="2"/>',
        f'<circle cx="122" cy="257" r="4" fill="{c}" fill-opacity=".55"/>',
        f'<rect x="30" y="340" width="30" height="50" rx="3" fill="#FBFAF6" stroke="{c}" stroke-opacity=".55" stroke-width="2"/>',
        f'<text x="45" y="368" text-anchor="middle" class="bt" font-size="11" fill="{S["sub"]}" transform="rotate(-90 45 368)">FRIDGE</text>',
        f'<rect x="130" y="402" width="42" height="66" rx="3" fill="{top}" stroke="{c}" stroke-opacity=".45" stroke-width="2"/>',
        *[f'<circle cx="{x}" cy="{y}" r="13" fill="#cbb89a" fill-opacity=".7"/>' for x, y in [(338, 462), (380, 462), (422, 462), (338, 543), (380, 543), (422, 543), (300, 500)]],
    ]

def _wcs(S):
    c = S['ink']
    out = [_toilet(45, 432, c), _toilet(45, 560, c), _toilet(45, 620, c),
           f'<rect x="28" y="636" width="48" height="48" rx="4" fill="#FBFAF6" stroke="{c}" stroke-opacity=".5" stroke-width="1.6"/>'
           f'<line x1="28" y1="636" x2="76" y2="684" stroke="{c}" stroke-opacity=".3"/><line x1="76" y1="636" x2="28" y2="684" stroke="{c}" stroke-opacity=".3"/>',
           f'<rect x="30" y="480" width="34" height="34" rx="6" fill="#FBFAF6" stroke="{c}" stroke-opacity=".5" stroke-width="1.6"/>']
    for t, (x, y) in [('SHOWER', (98, 660))]:
        out.append(f'<text x="{x}" y="{y}" text-anchor="middle" class="bt" font-size="15" letter-spacing="1.2" fill="{S["sub"]}" transform="rotate(-90 {x} {y})">{t}</text>')
    return out

def extras_flat(S):
    return _kitchen(S) + _wcs(S) + [
        f'<text x="1158" y="1180" text-anchor="middle" class="bt" font-weight="700" font-size="20" letter-spacing="2" fill="{S["ink"]}" stroke="#D2CDC2" stroke-width="6" paint-order="stroke">STAIRS DOWN TO EXIT</text>',
        f'<line x1="1040" y1="1120" x2="1270" y2="1120" stroke="{S["ink"]}" stroke-width="3.5"/><path d="M1258,1108 L1280,1120 L1258,1132 Z" fill="{S["ink"]}"/>',
    ]

def extras_iso():
    return ['<text x="1158" y="1180" text-anchor="middle" class="bt" font-weight="700" font-size="24" letter-spacing="2" fill="#2D2D2A" stroke="#D2CDC2" stroke-width="6" paint-order="stroke">STAIRS DOWN TO EXIT</text>']
