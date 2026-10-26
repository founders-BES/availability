"""Archway, 14 Windermere Road. Units: px of a half-res crop of the Archway PDF.
Scale from the drawing's own dimensions (27.03 m overall width): 37.4 px = 1 m."""
PX_PER_M = 37.4
TEXT_SCALE = 1.45
FURN_SCALE = 0.9
WALL_W = (4, 8)
FLAT_AREA_W = 800
TREAD = 9

def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

OUTER = (67, 87, 1072, 1135)
FOOTPRINT = [(67, 87), (1072, 87), (1072, 900), (992, 900), (992, 1135), (750, 1135), (750, 357), (67, 357)]
_T, _R, _B1, _R2, _B2, _L2, _B3, _L = ((67, 87, 1072, 87), (1072, 87, 1072, 900), (992, 900, 1072, 900),
                                      (992, 900, 992, 1135), (750, 1135, 992, 1135), (750, 357, 750, 1135),
                                      (67, 357, 750, 357), (67, 87, 67, 357))
OUTER_WALLS = [_T + ([],), _R + ([],), _B1 + ([],), _R2 + ([],), _B2 + ([],), _L2 + ([(865, 895)],), _B3 + ([(141, 170)],), _L + ([],)]
OUTER_WALLS = [(a, b, c, d, g) for (a, b, c, d, g) in OUTER_WALLS]
WINDOWS = [(_T, a, b) for a, b in [(180, 240), (250, 395), (405, 550), (560, 620), (630, 700), (712, 755), (765, 840), (850, 905), (915, 1060)]] + \
          [(_L2, a, b) for a, b in [(420, 480), (650, 700), (790, 860), (950, 1010), (1080, 1120)]] + \
          [(_R, a, b) for a, b in [(100, 175), (195, 245), (360, 420), (430, 492), (800, 880)]] + \
          [(_R2, a, b) for a, b in [(950, 1100)]]

WALLS = [
    (173, 87, 173, 357, [(192, 228)]),
    (173, 182, 928, 182, [(216, 242), (250, 275), (525, 553), (598, 622), (630, 655), (712, 737), (765, 790), (848, 872)]),
    (243, 87, 243, 182, []), (400, 87, 400, 182, []), (555, 87, 555, 182, []), (627, 87, 627, 182, []),
    (708, 87, 708, 182, []), (760, 87, 760, 182, []), (843, 87, 843, 182, []), (912, 87, 912, 182, []),
    (928, 182, 928, 500, [(185, 215), (360, 392)]),
    (928, 252, 1072, 252, [(977, 1007)]), (928, 352, 1072, 352, []), (928, 500, 1072, 500, []),
    (173, 232, 860, 232, [(218, 243), (367, 395), (405, 430), (630, 657), (667, 695)]),
    (250, 232, 250, 357, []), (400, 232, 400, 357, []), (487, 232, 487, 357, []), (662, 232, 662, 357, []),
    (750, 232, 750, 357, []),
    (860, 232, 860, 310, []), (750, 310, 860, 310, [(790, 818)]),
    (750, 355, 860, 355, [(753, 782)]), (785, 355, 785, 492, [(360, 388), (397, 425), (432, 458), (466, 490)]),
    (860, 355, 860, 495, []), (750, 492, 860, 492, []),
    (785, 392, 860, 392, []), (785, 428, 860, 428, []), (785, 462, 860, 462, []),
    (750, 627, 860, 627, []),
    (955, 680, 955, 900, []),
    (955, 680, 1072, 680, [(978, 1048)]),   # double doors at the top of the stairs
    (750, 900, 992, 900, [(757, 785)]),
    (875, 900, 875, 1135, [(915, 947)]),
    (787, 1048, 875, 1048, []), (787, 1048, 787, 1135, [(1052, 1080)]),
]
def THIN(w):
    return (w[0] == 785 and w[2] == 860 and w[1] in (392, 428, 462)) or (w[1] == 627 and w[3] == 627)

DOORS = [
    (173, 228, 34, 'v', -1, -1),
    (242, 182, 25, 'h', -1, -1), (250, 182, 25, 'h', 1, -1), (553, 182, 27, 'h', -1, -1), (622, 182, 24, 'h', -1, -1),
    (630, 182, 25, 'h', 1, -1), (712, 182, 25, 'h', 1, -1), (765, 182, 25, 'h', 1, -1), (848, 182, 24, 'h', 1, -1),
    (928, 215, 30, 'v', 1, -1), (1007, 252, 30, 'h', -1, 1), (928, 392, 32, 'v', 1, -1),
    (218, 232, 25, 'h', 1, 1), (395, 232, 28, 'h', -1, 1), (405, 232, 25, 'h', 1, 1),
    (657, 232, 27, 'h', -1, 1), (667, 232, 28, 'h', 1, 1),
    (785, 360, 28, 'v', 1, 1), (785, 397, 28, 'v', 1, 1), (785, 432, 26, 'v', 1, 1), (785, 466, 24, 'v', 1, 1),
    (782, 355, 29, 'h', -1, 1),   # WC lobby door, from the passage by the WC + shower
    (978, 680, 35, 'h', 1, -1), (1048, 680, 35, 'h', -1, -1),
    (790, 310, 28, 'h', 1, -1), (757, 900, 28, 'h', 1, 1), (875, 916, 31, 'v', 1, 1), (787, 1052, 28, 'v', 1, 1),
    (141, 357, 29, 'h', 1, 1),
    (750, 895, 30, 'v', -1, -1),   # coworking out to the roof terrace
]

OFFICES = [
    ("1", rect(928, 352, 1072, 500), 180, (995, 430)),
    ("2", rect(928, 252, 1072, 352), 129, (995, 300)),
    ("3", [(912, 87), (1072, 87), (1072, 252), (928, 252), (928, 182), (912, 182)], 205, (985, 165)),
    ("4", rect(843, 87, 912, 182), 55, (877, 140)),
    ("5", rect(760, 87, 843, 182), 60, (801, 130)),
    ("6", rect(708, 87, 760, 182), 45, (734, 140)),
    ("7", rect(627, 87, 708, 182), 65, (667, 140)),
    ("8", rect(555, 87, 627, 182), 61, (591, 140)),
    ("9", rect(400, 87, 555, 182), 128, (477, 128)),
    ("10", rect(243, 87, 400, 182), 128, (322, 128)),
    ("11", rect(173, 87, 243, 182), 57, (208, 140)),
    ("12", rect(173, 232, 250, 357), 82, (211, 290)),
    ("13", rect(250, 232, 400, 357), 152, (325, 295)),
    ("14", rect(400, 232, 487, 357), 92, (443, 300)),
    ("15", rect(487, 232, 662, 357), 185, (575, 295)),
    ("16", rect(662, 232, 750, 357), 89, (706, 300)),
    ("17", rect(875, 900, 992, 1135), 214, (933, 1070)),
]
DESKS_PER = {"1": 6, "2": 4, "3": 7, "4": 2, "5": 2, "6": 1, "7": 2, "8": 1, "9": 4, "10": 4, "11": 1,
             "12": 2, "13": 4, "14": 2, "15": 4, "16": 2, "17": 6}

GREYED = [rect(67, 87, 173, 357)]   # private stairs, not for clients (Ilan, 26 Oct 2026)
STAIR_FILL = '#D2CDC2'
STAIRS = [(72, 140, 128, 272, 'h'), (958, 684, 1010, 896, 'h')]
SHADED = [rect(785, 355, 860, 492), rect(750, 232, 860, 310), rect(955, 680, 1072, 900)]
OUTSIDE = [rect(67, 357, 750, 1135)]
COMMON_LABELS = [
    ("Corridor", None),
    ("Kitchenette", (830, 548), 0.75),
    ("Lounge", (850, 600)),
    ("Coworking", (850, 860)),
    ("Reception", (1000, 610)),
    ("Designated", (818, 938), 0.6),
    ("desks", (818, 955), 0.6),
    ("Meeting", (831, 1068), 0.6),
    ("room", (831, 1083), 0.6),
]

def d(x, y, w, h, pr=False): return (x, y, w, h, pr)
DESKS = [
    d(215, 92, 22, 40), d(250, 90, 45, 22), d(300, 90, 45, 22), d(350, 90, 45, 22), d(355, 152, 40, 22),
    d(410, 90, 40, 22), d(472, 90, 40, 22), d(410, 152, 40, 22), d(472, 152, 40, 22),
    d(585, 90, 32, 22), d(637, 122, 30, 22), d(675, 90, 28, 22), d(714, 95, 32, 30), d(770, 95, 30, 22), d(810, 140, 30, 22),
    d(853, 140, 28, 22), d(880, 90, 28, 22),
    d(945, 90, 40, 22), d(995, 90, 40, 22), d(918, 118, 20, 40),
    d(1050, 118, 20, 38), d(1050, 168, 20, 38), d(1050, 212, 20, 34),
    d(1025, 257, 40, 20), d(942, 325, 40, 22), d(990, 325, 40, 22), d(1035, 325, 34, 22),
    d(1050, 360, 20, 38), d(1050, 405, 20, 38), d(1050, 452, 20, 38), d(931, 395, 20, 40), d(931, 445, 20, 40),
    d(176, 258, 20, 38), d(176, 305, 20, 38),
    d(255, 238, 40, 22), d(300, 238, 40, 22), d(345, 238, 40, 22), d(315, 330, 60, 22, True),
    d(463, 238, 20, 40), d(405, 300, 22, 32),
    d(500, 238, 40, 22), d(560, 238, 40, 22), d(505, 330, 40, 22), d(560, 330, 40, 22),
    d(705, 262, 38, 22), d(668, 330, 36, 22),
    d(752, 700, 93, 40, True), d(860, 770, 92, 40, True), d(785, 985, 88, 38, True),
    d(877, 995, 38, 46), d(966, 902, 24, 46), d(966, 958, 24, 46), d(966, 1015, 24, 46), d(877, 1108, 40, 24), d(945, 1108, 40, 24),
]
KITCHEN = [("counter", (752, 500, 28, 62)), ("counter2", (780, 500, 50, 12)), ("recep", (950, 550, 62, 26))]
TABLES = [(840, 873, 18), (835, 1108, 15)]
SOFAS = [(775, 608, 58, 16), (775, 640, 58, 16), (955, 515, 30, 24)]
PLANTS = [(762, 773), (762, 800), (1056, 535), (965, 505)]

META = dict(site='ARCHWAY · 14 WINDERMERE ROAD, N19 5SG', floor='SECOND FLOOR', title='Archway', slug='archway',
            summary='17 private offices · coworking · roof terrace')
NORTH = (-1, 0)   # Offices 1-3 outer (right) wall faces south (Ilan, 26 Oct 2026)
ALL_BADGES = True   # one label style for every office (Ilan, 26 Oct 2026)
NOTE = 'Roof terrace on the same floor.'
PINS = {'1': 'down', '3': 'up', '17': 'right'}
FLAT_MARGIN = (20, 10, 10, 10)

def _wcs(c):
    # one toilet per cubicle, cistern on the back (x=860) wall, bowl facing the door
    out = []
    for cy in (373.5, 410, 445, 477):
        out.append(f'<rect x="846" y="{cy-9}" width="9" height="18" rx="2.5" fill="#FBFAF6" stroke="{c}" stroke-opacity=".55" stroke-width="1.3"/>'
                   f'<ellipse cx="835" cy="{cy}" rx="11" ry="7.5" fill="#FBFAF6" stroke="{c}" stroke-opacity=".55" stroke-width="1.3"/>')
    return out


def _spa(sub, big=False):
    """Roof terrace, bottom-left corner (Ilan, 26 Oct 2026): cold plunge, sauna (about 3.3 m square) about 2 m above the plunge."""
    fs = 14 if big else 12
    lab = lambda x, y, t: f'<text x="{x}" y="{y}" text-anchor="middle" class="bt" font-weight="700" font-size="{fs}" letter-spacing="1.5" fill="#6f8a63">{t}</text>'
    out = []
    # sauna
    x0, y0, w = 161, 869, 122
    out.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{w}" rx="7" fill="#D9C3A0" stroke="#8a6f4e" stroke-width="2"/>')
    for y in range(y0 + 14, y0 + w - 6, 12):
        out.append(f'<line x1="{x0+7}" y1="{y}" x2="{x0+w-7}" y2="{y}" stroke="#8a6f4e" stroke-opacity=".3" stroke-width="1.2"/>')
    out.append(f'<rect x="{x0+w/2-12}" y="{y0+w-2}" width="24" height="5" fill="#8a6f4e"/>')
    out.append(f'<text x="{x0+w/2}" y="{y0+w/2+5}" text-anchor="middle" class="bt" font-weight="700" font-size="{fs+2}" letter-spacing="2" fill="#5c4630" stroke="#D9C3A0" stroke-width="4" paint-order="stroke">SAUNA</text>')
    # cold plunge
    out.append('<circle cx="222" cy="1092" r="26" fill="#D6ECEA" stroke="#5f9b98" stroke-width="2.5"/>'
               '<circle cx="222" cy="1092" r="18" fill="none" stroke="#5f9b98" stroke-opacity=".35" stroke-width="1.2"/>')
    out.append(lab(222, 1056, 'COLD PLUNGE'))
    return out

def extras_flat(S):
    return _wcs(S['ink']) + _spa(S['sub']) + [
        f'<text x="100" y="206" text-anchor="middle" class="bt" font-weight="700" font-size="13" letter-spacing="1.5" fill="{S["sub"]}" stroke="#D2CDC2" stroke-width="4" paint-order="stroke" transform="rotate(-90 100 206)">PRIVATE STAIRS</text>',
        f'<text x="985" y="790" text-anchor="middle" class="bt" font-weight="700" font-size="12" letter-spacing="1.5" fill="{S["sub"]}" stroke="#EFEBE2" stroke-width="4" paint-order="stroke" transform="rotate(-90 985 790)">STAIRS DOWN</text>',
        f'<text x="380" y="640" text-anchor="middle" class="ys" font-size="34" fill="#6f8a63">Roof terrace</text>',
        f'<text x="380" y="672" text-anchor="middle" class="bt" font-size="15" letter-spacing="2" fill="#6f8a63">SHARED · OUTDOOR</text>',
        f'<text x="805" y="268" text-anchor="middle" class="bt" font-size="12" letter-spacing="1.2" fill="{S["sub"]}">WC + SHOWER</text>',
    ]

def extras_iso():
    return _wcs('#2D2D2A') + [
        '<text x="380" y="660" text-anchor="middle" class="ys" font-size="40" fill="#6f8a63">Roof terrace</text>',
    ]


def solids_iso(iso, box_faces, k):
    """Sauna and cold plunge as raised objects in the 3D view."""
    import math
    out = []
    # cold plunge: short round tub
    cx, cy, r, h = 222, 1092, 26, 22 * k
    ring = lambda z: ' '.join(f'{iso(cx + r*math.cos(t), cy + r*math.sin(t), z)[0]:.1f},{iso(cx + r*math.cos(t), cy + r*math.sin(t), z)[1]:.1f}'
                              for t in [i * math.pi / 24 for i in range(48)])
    # side: draw base ring filled, then top
    out.append(f'<polygon points="{ring(0)}" fill="#5f9b98"/>')
    for i in range(48):
        t0, t1 = i * math.pi / 24, (i + 1) * math.pi / 24
        p = [(cx + r*math.cos(t0), cy + r*math.sin(t0), 0), (cx + r*math.cos(t1), cy + r*math.sin(t1), 0),
             (cx + r*math.cos(t1), cy + r*math.sin(t1), h), (cx + r*math.cos(t0), cy + r*math.sin(t0), h)]
        out.append('<polygon points="' + ' '.join(f'{iso(*q)[0]:.1f},{iso(*q)[1]:.1f}' for q in p) + '" fill="#7fb3b0"/>')
    out.append(f'<polygon points="{ring(h)}" fill="#D6ECEA" stroke="#5f9b98" stroke-width="{2*k:.1f}"/>')
    # sauna: timber cabin, taller than the walls
    x0, y0, w = 161, 869, 122
    H = 70 * k
    out.append(box_faces(x0, y0, x0 + w, y0 + w, 0, H, '#E2CCA8', '#C9AB80', '#B8986C'))
    # door on the plunge-facing (south) side
    dx = x0 + w / 2
    p = [(dx - 12, y0 + w, 0), (dx + 12, y0 + w, 0), (dx + 12, y0 + w, H * .75), (dx - 12, y0 + w, H * .75)]
    out.append('<polygon points="' + ' '.join(f'{iso(*q)[0]:.1f},{iso(*q)[1]:.1f}' for q in p) + '" fill="#8a6f4e"/>')
    for (lx, ly, lz, t) in [(x0 + w / 2, y0 + w / 2, H + 8 * k, 'SAUNA'), (cx, cy, h + 30 * k, 'COLD PLUNGE')]:
        X, Y = iso(lx, ly, lz)
        out.append(f'<text x="{X:.1f}" y="{Y:.1f}" text-anchor="middle" class="bt" font-weight="700" font-size="{16*k:.1f}" letter-spacing="1.5" fill="#5c4630" stroke="#F6F3EC" stroke-width="{4*k:.1f}" paint-order="stroke">{t}</text>')
    return out
