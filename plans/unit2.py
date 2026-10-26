"""Hornsey Unit 2 geometry. Units: source-plan px, 54 px = 1 m (calibrated from occupancy sq ft)."""
PX_PER_M = 54.0

OUTER = (20, 20, 655, 1203)

# walls: (x0,y0,x1,y1, [gaps as (a,b) along the wall])
WALLS = [
    (97, 80, 370, 80, []),
    (370, 20, 370, 80, []),
    (97, 80, 97, 245, []),
    (270, 80, 270, 245, [(135, 175)]),
    (97, 245, 655, 245, [(102, 140), (350, 390)]),
    (432, 245, 432, 958, [(375, 415), (585, 625), (763, 800), (810, 850)]),
    (432, 432, 655, 432, []),
    (432, 630, 655, 630, []),
    (432, 805, 655, 805, []),
    (432, 958, 655, 958, []),
    (532, 958, 532, 1203, [(965, 1000)]),
    (345, 378, 345, 963, [(485, 520), (585, 620), (785, 820)]),
    (20, 378, 345, 378, [(20, 90), (168, 205), (290, 325)]),
    (90, 378, 90, 570, []),
    (213, 378, 213, 570, []),
    (213, 473, 345, 473, []),
    (20, 570, 345, 570, []),
    (20, 778, 345, 778, []),
    (220, 963, 345, 963, []),
    (220, 963, 220, 1203, [(1020, 1058)]),
    (20, 1002, 220, 1002, []),
    (20, 1100, 220, 1100, [(28, 62), (76, 108), (124, 158)]),
    (70, 1100, 70, 1203, []),
    (117, 1100, 117, 1203, []),
    (165, 1100, 165, 1203, []),
    (475, 1088, 475, 1203, []),
    (475, 1088, 532, 1088, [(485, 525)]),
]

# doors: hinge point, leaf length, wall orientation, swing quadrant (dx,dy signs)
DOORS = [
    # (hx, hy, length, 'h' or 'v' wall, sx, sy)
    (102, 245, 38, 'h', 1, -1),   # Office 1
    (270, 135, 40, 'v', 1, 1),    # O1 <-> O2
    (350, 245, 40, 'h', 1, -1),   # Office 2
    (432, 415, 40, 'v', 1, -1),   # Office 3
    (432, 625, 40, 'v', 1, -1),   # Office 4
    (432, 800, 37, 'v', 1, -1),   # Office 5
    (432, 810, 40, 'v', 1, 1),    # Office 6
    (532, 965, 35, 'v', 1, 1),    # Office 7
    (205, 378, 37, 'h', -1, 1),   # Office 10
    (325, 378, 35, 'h', -1, 1),   # Office 11
    (345, 485, 35, 'v', -1, 1),   # Office 12
    (345, 585, 35, 'v', -1, 1),   # Office 9
    (345, 785, 35, 'v', -1, 1),   # Office 8
    (220, 1058, 38, 'v', 1, -1),  # WCs
]

WINDOWS_L = [(88, 168), (240, 360), (585, 730), (790, 930), (1012, 1095)]
WINDOWS_R = [(48, 170), (258, 420), (442, 560), (640, 760), (820, 945), (1000, 1150)]

def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

# Offices: id, polygon, sq ft, label anchor
OFFICES = [
    ("1", rect(97, 80, 270, 245), 102, (140, 205)),
    ("2", [(370, 20), (655, 20), (655, 245), (270, 245), (270, 80), (370, 80)], 317, (440, 95)),
    ("3", rect(432, 245, 655, 432), 154, (560, 332)),
    ("4", rect(432, 432, 655, 630), 159, (560, 532)),
    ("5", rect(432, 630, 655, 805), 130, (500, 706)),
    ("6", rect(432, 805, 655, 958), 125, (503, 840)),
    ("7", rect(532, 958, 655, 1203), 96, (593, 1125)),
    ("8", [(20, 778), (345, 778), (345, 963), (220, 963), (220, 1002), (20, 1002)], 246, (183, 880)),
    ("9", rect(20, 570, 345, 778), 244, (183, 672)),
    ("10", rect(90, 378, 213, 570), 86, (151, 420)),
    ("11", rect(213, 378, 345, 473), 45, (279, 408)),
    ("12", rect(213, 473, 345, 570), 44, (279, 503)),
]

COMMON_POLY = [(20, 20), (370, 20), (370, 80), (97, 80), (97, 245), (432, 245), (432, 958),
               (532, 958), (532, 1203), (220, 1203), (220, 963), (345, 963), (345, 378), (20, 378)]
WC_POLY = rect(20, 1002, 220, 1203)
STAIR2_POLY = rect(20, 378, 90, 570)
STORE_POLY = rect(475, 1088, 532, 1203)

STAIRS = [  # x0,y0,x1,y1, tread direction
    (172, 26, 365, 78, 'v'),
    (26, 382, 88, 568, 'h'),
]

COMMON_LABELS = [
    ("Reception", (232, 318)),
    ("Kitchen", (385, 1005)),
    ("WCs", (120, 1052)),
    ("Corridor", None),
]

# desks: x, y, w, h, pair (chairs both sides)
DESKS = [
    (140, 85, 65, 64, True), (193, 175, 32, 66, False),
    (382, 24, 66, 33, False), (469, 24, 66, 33, False), (556, 24, 66, 33, False),
    (446, 133, 200, 68, True),
    (502, 248, 66, 64, True), (536, 363, 68, 67, True),
    (502, 437, 70, 66, True), (536, 560, 66, 66, True),
    (536, 633, 68, 67, True), (534, 735, 68, 67, True),
    (432, 888, 66, 34, False), (575, 848, 68, 67, 'v'),
    (575, 1002, 68, 66, 'v'),
    (44, 781, 67, 30, False), (129, 781, 67, 30, False), (214, 781, 67, 30, False),
    (308, 860, 35, 68, False), (42, 968, 68, 32, False), (151, 968, 68, 32, False),
    (67, 573, 66, 66, True), (212, 573, 35, 66, False),
    (67, 708, 66, 68, True), (209, 708, 66, 68, True),
    (97, 467, 66, 66, True),
    (217, 440, 124, 32, False),
    (217, 535, 124, 32, False),
]

# soft furnishings / kitchen
KITCHEN = [
    ("counter", (225, 1062, 34, 136)),
    ("counter", (259, 1167, 100, 30)),
    ("island", (325, 1062, 34, 105)),
]
TABLES = [(462, 1052, 17), (442, 1147, 17)]
SOFA = (190, 250, 118, 44)
PLANTS = [(170, 262), (325, 262), (240, 980)]

# ---- metadata for the generic renderer
META = dict(site='HORNSEY · 465 HORNSEY ROAD, N19', floor='FIRST FLOOR', title='Unit 2', slug='hornsey-unit2')
DESKS_PER = {"1": 3, "2": 9, "3": 4, "4": 4, "5": 4, "6": 3, "7": 2, "8": 6, "9": 6, "10": 2, "11": 2, "12": 2}
NORTH = (1, 0)            # plan direction of north
WINDOWS = [('L', a, b) for a, b in WINDOWS_L] + [('R', a, b) for a, b in WINDOWS_R]
SHADED = [WC_POLY]
SOFAS = [SOFA]
NOTE = 'South wall faces the street, with the entrance below Office 9.'
PINS = {'11': 'up', '8': 'left', '6': 'right'}
def THIN(w):
    return w[1] >= 1100 and w[0] < 220

def extras_flat(S):
    return [
        f'<text x="268" y="58" text-anchor="middle" class="bt" font-size="11" letter-spacing="1.8" fill="{S["sub"]}" stroke="{S["stair"]}" stroke-width="4" paint-order="stroke">STAIRS TO LOFT</text>',
        f'<text x="44" y="478" text-anchor="middle" class="bt" font-weight="700" font-size="11" letter-spacing="1.6" fill="{S["ink"]}" stroke="{S["stair"]}" stroke-width="4" paint-order="stroke" transform="rotate(-90 44 478)">DOWN TO ENTRANCE</text>',
        f'<line x1="70" y1="398" x2="70" y2="548" stroke="{S["ink"]}" stroke-width="2.4"/><path d="M62,540 L70,556 L78,540 Z" fill="{S["ink"]}"/>',
        f'<rect x="-30" y="636" width="22" height="68" rx="2" fill="none" stroke="{S["ink"]}" stroke-width="1.6" stroke-dasharray="4 3"/>',
        f'<path d="M-26,670 h14 M-19,663 l7,7 l-7,7" fill="none" stroke="{S["ink"]}" stroke-width="1.6"/>',
        f'<text x="-46" y="670" text-anchor="middle" class="bt" font-weight="700" font-size="10.5" letter-spacing="1.4" fill="{S["ink"]}" transform="rotate(-90 -46 670)">STREET DOOR BELOW</text>',
        f'<text x="-62" y="670" text-anchor="middle" class="bt" font-size="10" letter-spacing="1.2" fill="{S["sub"]}" transform="rotate(-90 -62 670)">GROUND FLOOR</text>',
    ]

def extras_iso():
    return [
        '<text x="56" y="478" text-anchor="middle" class="bt" font-weight="700" font-size="13" letter-spacing="1.6" fill="#2D2D2A" stroke="#E4DFD3" stroke-width="5" paint-order="stroke" transform="rotate(-90 56 478)">DOWN TO ENTRANCE</text>',
        '<rect x="-40" y="636" width="22" height="68" rx="2" fill="none" stroke="#2D2D2A" stroke-width="2" stroke-dasharray="5 4"/>',
        '<text x="-58" y="670" text-anchor="middle" class="bt" font-weight="700" font-size="13" letter-spacing="1.4" fill="#2D2D2A" transform="rotate(-90 -58 670)">STREET DOOR BELOW</text>',
    ]
FLAT_MARGIN = (90, 10, 10, 10)
