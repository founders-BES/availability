"""Generic Bespoke Spaces floor plan renderer.

usage: python3 plan.py <building_module> <outdir> [--avail 6,8,11 --date "26 Oct 2026"]
Without --avail it renders the base plan (no availability)."""
import math, base64, os, sys, importlib, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
FONTDIR = os.path.join(HERE, '..', 'fonts', 'node_modules', '@fontsource')

C = dict(cream='#EAE6DD', char='#2D2D2A', teal='#7BB5B2', mustard='#EDD286')
S = dict(page=C['cream'], floor='#F6F3EC', let='#DDD7C9', avail=C['teal'], wall=C['char'], ink=C['char'],
         sub='#6b6a63', win='#9cc9c6', wc='#EFEBE2', stair='#E4DFD3')

def font_css(embed):
    if not embed:
        return ("@import url('https://fonts.googleapis.com/css2?family=Bitter:wght@400;600;700&amp;"
                "family=Young+Serif&amp;display=swap');")
    out = []
    for fam, file, w in [('Young Serif', 'young-serif/files/young-serif-latin-400-normal.woff2', 400),
                         ('Bitter', 'bitter/files/bitter-latin-400-normal.woff2', 400),
                         ('Bitter', 'bitter/files/bitter-latin-600-normal.woff2', 600),
                         ('Bitter', 'bitter/files/bitter-latin-700-normal.woff2', 700)]:
        b = base64.b64encode(open(os.path.join(FONTDIR, file), 'rb').read()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');}}")
    return ''.join(out)

def pts(poly):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in poly)

def wall_pieces(w):
    x0, y0, x1, y1, gaps = w
    horiz = y0 == y1
    a, b = (x0, x1) if horiz else (y0, y1)
    cuts, cur = [], a
    for g0, g1 in sorted(gaps):
        if g0 > cur: cuts.append((cur, g0))
        cur = max(cur, g1)
    if cur < b: cuts.append((cur, b))
    return [((s, y0, e, y0) if horiz else (x0, s, x0, e)) for s, e in cuts]

def slant_pieces(p0, p1, gaps):
    cuts, cur = [], 0.0
    for g0, g1 in sorted(gaps):
        if g0 > cur: cuts.append((cur, g0))
        cur = max(cur, g1)
    if cur < 1: cuts.append((cur, 1.0))
    L = lambda t: (p0[0] + (p1[0]-p0[0])*t, p0[1] + (p1[1]-p0[1])*t)
    return [(L(a), L(b)) for a, b in cuts]

def leaf(x, y, w, h, fill, r=None):
    r = r or h / 2
    return (f'<path d="M{x+r},{y} H{x+w} V{y+h-r} A{r},{r} 0 0 1 {x+w-r},{y+h} H{x} V{y+r} A{r},{r} 0 0 1 {x+r},{y} Z" fill="{fill}"/>')

def door_svg(d, col, sw):
    hx, hy, L, ori, sx, sy = d
    if ori == 'h':
        ex, ey, ox, oy = hx + sx * L, hy, hx, hy + sy * L
    else:
        ex, ey, ox, oy = hx, hy + sy * L, hx + sx * L, hy
    sweep = 1 if (ori == 'h') == (sx * sy > 0) else 0
    return (f'<line x1="{hx}" y1="{hy}" x2="{ox}" y2="{oy}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="M{ox},{oy} A{L},{L} 0 0 {sweep} {ex},{ey}" fill="none" stroke="{col}" stroke-width="{sw*0.6}" stroke-dasharray="2 3" opacity=".7"/>')

def office_list(P):
    return [dict(id=o[0], poly=o[1], sq=o[2], lab=o[3], name=(o[4] if len(o) > 4 else f'Office {o[0]}')) for o in P.OFFICES]

def room_centre(P, x, y):
    for o in office_list(P):
        xs = [p[0] for p in o['poly']]; ys = [p[1] for p in o['poly']]
        if min(xs) <= x <= max(xs) and min(ys) <= y <= max(ys):
            return sum(xs)/len(xs), sum(ys)/len(ys)
    return x, y

def chairs_for(P, d):
    x, y, w, h, pair = d[:5]
    r = 6.5 * getattr(P, 'FURN_SCALE', 1)
    off = 8 * getattr(P, 'FURN_SCALE', 1)
    cx0, cy0 = x + w/2, y + h/2
    rx, ry = room_centre(P, cx0, cy0)
    if pair == 'v':
        return [(cx0, y-off, r), (cx0, y+h+off, r)]
    if pair == 'h':
        return [(x-off, cy0, r), (x+w+off, cy0, r)]
    if pair == 'none':
        return []
    unit = 34 * getattr(P, 'FURN_SCALE', 1)
    if pair and w > 1.5*h:
        n = max(1, round(w / unit)); xs = [x + w*(i+.5)/n for i in range(n)]
        return [(cx, cy, r) for cx in xs for cy in (y-off, y+h+off)]
    if pair and h > 1.5*w:
        n = max(1, round(h / unit)); ys = [y + h*(i+.5)/n for i in range(n)]
        return [(cx, cy, r) for cy in ys for cx in (x-off, x+w+off)]
    if pair:
        return [(x-off, cy0, r), (x+w+off, cy0, r)]
    if w >= h:
        n = max(1, round(w / unit)); xs = [x + w*(i+.5)/n for i in range(n)]
        cy = y+h+off if ry > cy0 else y-off
        return [(cx, cy, r) for cx in xs]
    n = max(1, round(h / unit)); ys = [y + h*(i+.5)/n for i in range(n)]
    cx = x+w+off if rx > cx0 else x-off
    return [(cx, cy, r) for cy in ys]

def stairs_svg(P, fp, col, op):
    o = []
    step = getattr(P, 'TREAD', 12)
    for sx0, sy0, sx1, sy1, d in P.STAIRS:
        o.append(f'<polygon points="{fp([(sx0,sy0),(sx1,sy0),(sx1,sy1),(sx0,sy1)])}" fill="{getattr(P, "STAIR_FILL", S["stair"])}"/>')
        if d == 'v':
            xx = sx0 + step
            while xx < sx1:
                o.append(f'<polyline points="{fp([(xx,sy0),(xx,sy1)])}" stroke="{col}" stroke-opacity="{op}" fill="none"/>'); xx += step
        else:
            yy = sy0 + step
            while yy < sy1:
                o.append(f'<polyline points="{fp([(sx0,yy),(sx1,yy)])}" stroke="{col}" stroke-opacity="{op}" fill="none"/>'); yy += step
    return o

def compass(cx, cy, nx, ny, ink='#2D2D2A'):
    L = 26
    ax, ay = cx + L*nx, cy + L*ny
    px, py = -ny, nx
    return (f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{ink}" stroke-opacity=".35"/>'
            f'<path d="M{cx-L*nx:.1f},{cy-L*ny:.1f} L{ax:.1f},{ay:.1f}" stroke="{ink}" stroke-width="2.4" fill="none"/>'
            f'<path d="M{ax-12*nx+7*px:.1f},{ay-12*ny+7*py:.1f} L{ax:.1f},{ay:.1f} L{ax-12*nx-7*px:.1f},{ay-12*ny-7*py:.1f}" stroke="{ink}" stroke-width="2.4" fill="none" stroke-linejoin="round"/>'
            f'<text x="{cx+50*nx:.1f}" y="{cy+50*ny+8:.1f}" text-anchor="middle" class="ys" font-size="24" fill="{ink}">N</text>')

def head(W, H, embed):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
            f'<style>{font_css(embed)} .ys{{font-family:"Young Serif",serif}} .bt{{font-family:"Bitter",serif}}</style>',
            f'<rect width="{W}" height="{H}" fill="{S["page"]}"/>']

# ------------------------------------------------------------------ flat
def flat(P, avail, date, embed=True, soon=None):
    base = avail is None
    avail = avail or set()
    soon = soon or {}
    offices = office_list(P)
    x0, y0, x1, y1 = P.OUTER
    pw, ph = x1 - x0, y1 - y0
    margin = getattr(P, 'FLAT_MARGIN', (40, 10, 10, 10))  # left, top, right, bottom in plan units for extras
    W, H = 1500, 1150
    area_w, area_h = getattr(P, 'FLAT_AREA_W', 610), 1070
    sc = min(area_w / (pw + margin[0] + margin[2]), area_h / (ph + margin[1] + margin[3]))
    tx = 60 + (margin[0] - x0) * sc
    ty = 40 + (margin[1] - y0) * sc + (area_h - (ph + margin[1] + margin[3]) * sc) / 2
    o = head(W, H, embed)
    o.append(f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc:.4f})">')
    fs_k = getattr(P, 'TEXT_SCALE', 1.0)
    o.append(f'<polygon points="{pts(getattr(P, "FOOTPRINT", [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]))}" fill="{S["floor"]}"/>')
    for poly in getattr(P, 'SHADED', []):
        o.append(f'<polygon points="{pts(poly)}" fill="{S["wc"]}"/>')
    for poly in getattr(P, 'GREYED', []):
        o.append(f'<polygon points="{pts(poly)}" fill="{getattr(P, "STAIR_FILL", "#D2CDC2")}"/>')
    for poly in getattr(P, 'OUTSIDE', []):
        o.append(f'<polygon points="{pts(poly)}" fill="#E3E8E0" />')
    o += stairs_svg(P, pts, S['wall'], .35)
    for of in offices:
        fill = S['avail'] if of['id'] in avail else ('#C3DEDB' if of['id'] in soon else S['let'])
        o.append(f'<polygon points="{pts(of["poly"])}" fill="{fill}"/>')
    # furniture
    fk = getattr(P, 'FURN_SCALE', 1)
    for d in P.DESKS:
        for cx, cy, r in chairs_for(P, d):
            o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{C["char"]}" opacity=".16"/>')
        x, y, w, h, pr = d[:5]
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{3*fk}" fill="#FBFAF6" stroke="{C["char"]}" stroke-opacity=".28" stroke-width="{fk}"/>')
        if pr == 'v' or (pr is True and w > 1.5*h):
            o.append(f'<line x1="{x+3}" y1="{y+h/2}" x2="{x+w-3}" y2="{y+h/2}" stroke="{C["char"]}" stroke-opacity=".18" stroke-width="{fk}"/>')
        elif pr in (True, 'h'):
            o.append(f'<line x1="{x+w/2}" y1="{y+3}" x2="{x+w/2}" y2="{y+h-3}" stroke="{C["char"]}" stroke-opacity=".18" stroke-width="{fk}"/>')
    for _, (x, y, w, h) in getattr(P, 'KITCHEN', []):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#FBFAF6" stroke="{C["char"]}" stroke-opacity=".28" stroke-width="{fk}"/>')
    for cx, cy, r in getattr(P, 'TABLES', []):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FBFAF6" stroke="{C["char"]}" stroke-opacity=".28" stroke-width="{fk}"/>')
    for x, y, w, h in getattr(P, 'SOFAS', []):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{10*fk}" fill="#cbb89a" opacity=".55"/>')
    for px, py in getattr(P, 'PLANTS', []):
        o.append(f'<circle cx="{px}" cy="{py}" r="{11*fk}" fill="#7f9c6a" opacity=".55"/><circle cx="{px-3*fk}" cy="{py-3*fk}" r="{5*fk}" fill="#9bb886" opacity=".7"/>')
    for x, y, w, h in getattr(P, 'SKYLIGHTS', []):
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#D6ECEA" stroke="{C["teal"]}" stroke-width="1.6" stroke-dasharray="5 3"/>')
        if w >= 9.5 * fs_k * 6.5:
            o.append(f'<text x="{x+w/2:.1f}" y="{y+h/2+4*fs_k:.1f}" text-anchor="middle" class="bt" font-size="{9.5*fs_k:.1f}" letter-spacing="1.2" fill="#4f8582">SKYLIGHT</text>')
    # walls
    iw, ow = getattr(P, 'WALL_W', (5, 10))
    thin = getattr(P, 'THIN', lambda w: False)
    for w in P.WALLS:
        for a, b, c, d in wall_pieces(w):
            o.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{S["wall"]}" stroke-width="{iw*0.4 if thin(w) else iw}" stroke-linecap="square"/>')
    # outer walls with glazing
    for w in getattr(P, 'OUTER_WALLS', None) or [(x0,y0,x1,y0,[]),(x1,y0,x1,y1,[]),(x0,y1,x1,y1,[]),(x0,y0,x0,y1,[])]:
        wx0, wy0, wx1, wy1, _ = w
        side = None
        wins = [(a, b) for s, a, b in P.WINDOWS if
                ((wx0 == wx1) and s in ('L', 'R') and ((s == 'L' and wx0 == x0) or (s == 'R' and wx0 == x1)) and wy0 <= a < wy1) or
                ((wy0 == wy1) and s in ('T', 'B') and ((s == 'T' and wy0 == y0) or (s == 'B' and wy0 == y1)) and wx0 <= a < wx1) or
                (isinstance(s, tuple) and s == (wx0, wy0, wx1, wy1))]
        for a, b in wins:
            if wx0 == wx1:
                o.append(f'<line x1="{wx0}" y1="{a}" x2="{wx0}" y2="{b}" stroke="{S["win"]}" stroke-width="{ow*0.5}"/>')
            else:
                o.append(f'<line x1="{a}" y1="{wy0}" x2="{b}" y2="{wy0}" stroke="{S["win"]}" stroke-width="{ow*0.5}"/>')
        for a, b, c, d in wall_pieces((wx0, wy0, wx1, wy1, list(w[4]) + wins)):
            o.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{S["wall"]}" stroke-width="{ow}" stroke-linecap="square"/>')
    for p0, p1, kind, gaps in getattr(P, 'SLANTS', []):
        if kind == 'glass':
            for a, b in slant_pieces(p0, p1, gaps):
                o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{S["win"]}" stroke-width="{ow*0.5}"/>')
            for t in (0.0, 1.0):
                pass
        else:
            for a, b in slant_pieces(p0, p1, gaps):
                o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{S["wall"]}" stroke-width="{ow}" stroke-linecap="square"/>')
    for w in getattr(P, 'GLASS_WALLS', []):
        for a, b, c, d in wall_pieces(w):
            o.append(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{S["win"]}" stroke-width="{iw}" stroke-linecap="butt"/>'
                     f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{S["wall"]}" stroke-width="{max(1.2, iw*0.18):.1f}" stroke-opacity=".6"/>')
    for d in P.DOORS:
        o.append(door_svg(d, S['wall'], 2.2 * fk))
    # labels
    for of in offices:
        av = of['id'] in avail or of['id'] in soon
        lx, ly = of['lab']
        small = of['sq'] < 80 or of.get('small')
        fs = (17 if small else 23) * fs_k
        halo = S['avail'] if of['id'] in avail else ('#C3DEDB' if of['id'] in soon else S['let'])
        H_ = f' stroke="{halo}" stroke-width="{5*fs_k}" paint-order="stroke" stroke-linejoin="round"'
        rw0 = max(p[0] for p in of['poly']) - min(p[0] for p in of['poly'])
        sq_txt = f'{of["sq"]} sq ft' if of['sq'] else ''
        if (getattr(P, 'ALL_BADGES', False) or rw0 < len(of['name']) * fs * 0.5) and len(of['id']) <= 3:
            # compact: number badge for rooms too narrow for "Office N"
            r = 15 * fs_k
            st = of['id'] in soon
            bf = C['char'] if (of['id'] in avail or st) else '#FBFAF6'
            tf = C['cream'] if (of['id'] in avail or st) else C['char']
            o.append(f'<circle cx="{lx}" cy="{ly-r*0.35:.1f}" r="{r:.1f}" fill="{bf}" stroke="{C["char"]}" stroke-width="{1.4*fs_k:.1f}"/>'
                     f'<text x="{lx}" y="{ly+r*0.05:.1f}" text-anchor="middle" class="ys" font-size="{r*1.05:.1f}" fill="{tf}">{of["id"]}</text>')
            if sq_txt:
                o.append(f'<text x="{lx}" y="{ly+r*1.45:.1f}" text-anchor="middle" class="bt" font-size="{10*fs_k:.1f}" fill="{C["char"]}" fill-opacity=".7"{H_}>{of["sq"]} ft²</text>')
            continue
        o.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" class="ys" font-size="{fs:.1f}" fill="{C["char"]}"{H_}>{of["name"]}</text>')
        if av:
            rw = max(p[0] for p in of['poly']) - min(p[0] for p in of['poly'])
            if not small and rw < 168 * fs_k + 30:
                small = True
            if of['id'] in soon:
                when = 'COMING SOON' if soon[of['id']] == 'soon' else f'FROM {soon[of["id"]].upper()}'
                txt = when if small else f'{when} · {sq_txt.upper()}'
            else:
                txt = 'AVAILABLE' if small else f'AVAILABLE · {sq_txt.upper()}'
            bw = ((112 if of['id'] in soon else 84) if small else 168) * fs_k; bh = (20 if small else 24) * fs_k
            o.append(f'<g transform="translate({lx-bw/2:.1f},{ly+8*fs_k:.1f})">' + leaf(0, 0, bw, bh, C['char'], r=bh/2) +
                     f'<text x="{bw/2:.1f}" y="{bh*0.69:.1f}" text-anchor="middle" class="bt" font-weight="700" font-size="{11*fs_k:.1f}" letter-spacing=".6" fill="{C["cream"]}">{txt}</text></g>')
        elif sq_txt:
            pre = '' if base else 'Let · '
            o.append(f'<text x="{lx}" y="{ly+(17 if small else 21)*fs_k:.1f}" text-anchor="middle" class="bt" font-size="{(11 if small else 12.5)*fs_k:.1f}" fill="{C["char"]}" fill-opacity=".65"{H_}>{pre}{sq_txt}</text>')
    for lab in P.COMMON_LABELS:
        name, pos = lab[0], lab[1]
        kk = lab[2] if len(lab) > 2 else 1.0
        if pos:
            o.append(f'<text x="{pos[0]}" y="{pos[1]}" text-anchor="middle" class="bt" font-size="{14*fs_k*kk:.1f}" letter-spacing="{2.2*kk:.1f}" fill="{S["sub"]}">{name.upper()}</text>')
    o += P.extras_flat(S)
    o.append('</g>')
    # side panel
    px = 60 + area_w + 50
    LW = min(620, W - px - 50)
    ink, sub = S['ink'], S['sub']
    nlist = (0 if base else len(avail) + len(soon))
    step = 58 if nlist <= 2 else 44
    M = P.META
    _hdr = f'{M["site"]}{" · " + M["floor"] if M.get("floor") else ""}'
    _ls = 3 if len(_hdr) <= 44 else 1.6
    o.append(f'<text x="{px}" y="120" class="bt" font-size="15" letter-spacing="{_ls}" fill="{sub}">{_hdr}</text>')
    o.append(f'<text x="{px}" y="200" class="ys" font-size="72" fill="{ink}" letter-spacing="-1.4">{M["title"]}</text>')
    n_off = len([of for of in offices if of['sq']])
    tot = sum(of['sq'] for of in offices)
    o.append(f'<text x="{px}" y="245" class="bt" font-size="19" fill="{sub}">{M.get("summary", f"{n_off} private offices")}</text>')
    o.append(f'<line x1="{px}" y1="290" x2="{px+LW}" y2="290" stroke="{ink}" stroke-opacity=".2"/>')
    yy = 345
    if not base:
        o.append(f'<text x="{px}" y="{yy}" class="ys" font-size="30" fill="{ink}">Available now</text>')
        o.append(f'<text x="{px+LW}" y="{yy}" text-anchor="end" class="bt" font-size="15" fill="{sub}">As of {date}</text>')
        yy += 50
        if not avail:
            o.append(f'<text x="{px}" y="{yy}" class="bt" font-size="19" fill="{sub}">{"Nothing free today." if soon else "Fully let. Ask us about upcoming space."}</text>'); yy += 58
        for oid in sorted(avail, key=lambda s: (len(s), s)):
            of = next(x for x in offices if x['id'] == oid)
            o.append(leaf(px, yy - 26, 36, 36, S['avail'], r=18))
            o.append(f'<text x="{px+54}" y="{yy}" class="ys" font-size="26" fill="{ink}">{of["name"]}</text>')
            dk = P.DESKS_PER.get(oid)
            o.append(f'<text x="{px+230}" y="{yy}" class="bt" font-size="19" fill="{sub}">{of["sq"]} sq ft{f" · {dk} desks" if dk else ""}</text>')
            yy += step
        if soon:
            yy += 20
            o.append(f'<text x="{px}" y="{yy}" class="ys" font-size="24" fill="{ink}">Coming up</text>'); yy += 46
            for oid, when in sorted(soon.items(), key=lambda kv: (len(kv[0]), kv[0])):
                of = next(x for x in offices if x['id'] == oid)
                o.append(leaf(px, yy - 26, 36, 36, '#C3DEDB', r=18))
                o.append(f'<text x="{px+54}" y="{yy}" class="ys" font-size="24" fill="{ink}">{of["name"]}</text>')
                o.append(f'<text x="{px+230}" y="{yy}" class="bt" font-size="19" fill="{sub}">{of["sq"]} sq ft · {"date to be confirmed" if when == "soon" else "from " + when}</text>')
                yy += step
        yy += 30
        o.append(f'<line x1="{px}" y1="{yy}" x2="{px+LW}" y2="{yy}" stroke="{ink}" stroke-opacity=".2"/>')
        yy += 55
        legend = [('Available', S['avail'])] + ([('Coming up', '#C3DEDB')] if soon else []) + [('Let', S['let']), ('Shared spaces', S['floor'])]
    else:
        legend = [('Private offices', S['let']), ('Shared spaces', S['floor'])]
    lstep = 40 if nlist <= 2 else 32
    for lab, fill in legend:
        o.append(f'<rect x="{px}" y="{yy-18}" width="24" height="24" rx="3" fill="{fill}" stroke="{ink}" stroke-opacity=".25"/>')
        o.append(f'<text x="{px+38}" y="{yy}" class="bt" font-size="18" fill="{ink}">{lab}</text>')
        yy += lstep
    yy += 40 if nlist <= 2 else 24
    if P.NORTH:
        nx, ny = P.NORTH
        o.append(compass(px + LW - 150, yy + 2, nx, ny, ink))
    m = P.PX_PER_M * sc
    for i in range(5):
        o.append(f'<rect x="{px+i*m:.1f}" y="{yy}" width="{m:.1f}" height="8" fill="{ink if i%2==0 else "none"}" stroke="{ink}" stroke-width="1"/>')
    o.append(f'<text x="{px}" y="{yy+30}" class="bt" font-size="14" fill="{sub}">0 m</text>')
    o.append(f'<text x="{px+5*m:.1f}" y="{yy+30}" text-anchor="end" class="bt" font-size="14" fill="{sub}">5 m</text>')
    o.append(f'<text x="{px}" y="{yy+80}" class="bt" font-size="13.5" fill="{sub}">Drawn to scale. Sizes are approximate and for guidance only.</text>')
    if getattr(P, 'NOTE', None):
        o.append(f'<text x="{px}" y="{yy+104}" class="bt" font-size="13.5" fill="{sub}">{P.NOTE}</text>')
    o.append(f'<text x="{px}" y="{H-70}" class="ys" font-size="30" fill="{ink}">Bespoke Spaces</text>')
    o.append(f'<text x="{px}" y="{H-42}" class="bt" font-size="15" fill="{sub}">bespokespaces.co · Book a viewing</text>')
    o.append('</svg>')
    return '\n'.join(o)

# ------------------------------------------------------------------ isometric
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
def iso(x, y, z=0):
    return ((x - y) * C30, (x + y) * S30 - z)

def box_faces(x0, y0, x1, y1, z0, z1, top, east, south):
    f = lambda P_: ' '.join(f'{iso(*p)[0]:.1f},{iso(*p)[1]:.1f}' for p in P_)
    return (f'<polygon points="{f([(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)])}" fill="{south}"/>'
            f'<polygon points="{f([(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)])}" fill="{east}"/>'
            f'<polygon points="{f([(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])}" fill="{top}"/>')

def isometric(P, avail, date, embed=True, soon=None):
    base = avail is None
    avail = avail or set()
    soon = soon or {}
    offices = office_list(P)
    x0, y0, x1, y1 = P.OUTER
    k = P.PX_PER_M / 54.0          # keep 3D proportions consistent across buildings
    W, H = 1500, 1150
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    xs = [iso(x, y)[0] for x, y in corners]; ys = [iso(x, y)[1] for x, y in corners]
    sc = min(1150 / (max(xs) - min(xs)), 760 / (max(ys) - min(ys)))
    tx = (W - (max(xs) - min(xs)) * sc) / 2 - min(xs) * sc + 90
    ty = (H - (max(ys) - min(ys)) * sc) / 2 - min(ys) * sc + 40
    o = head(W, H, embed)
    o.append(f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc:.4f})">')
    fp = lambda poly: ' '.join(f'{iso(x,y)[0]:.1f},{iso(x,y)[1]:.1f}' for x, y in poly)
    foot = getattr(P, 'FOOTPRINT', corners)
    o.append(f'<polygon points="{fp([(x+30*k, y+30*k) for x, y in foot])}" fill="#000" opacity=".06"/>')
    if hasattr(P, 'FOOTPRINT'):
        o.append(f'<polygon points="{fp(foot)}" fill="#F6F3EC" stroke="#c7c0b0" stroke-width="{6*k}"/>')
    else:
        o.append(box_faces(x0 - 6*k, y0 - 6*k, x1 + 6*k, y1 + 6*k, -16*k, 0, '#F6F3EC', '#d6d0c2', '#c7c0b0'))
    for poly in getattr(P, 'OUTSIDE', []):
        o.append(f'<polygon points="{fp(poly)}" fill="#E3E8E0"/>')
    for poly in getattr(P, 'SHADED', []):
        o.append(f'<polygon points="{fp(poly)}" fill="#EFEBE2"/>')
    for poly in getattr(P, 'GREYED', []):
        o.append(f'<polygon points="{fp(poly)}" fill="{getattr(P, "STAIR_FILL", "#D2CDC2")}"/>')
    for of in offices:
        o.append(f'<polygon points="{fp(of["poly"])}" fill="{C["teal"] if of["id"] in avail else ("#C3DEDB" if of["id"] in soon else "#E2DCCF")}"/>')
    o += stairs_svg(P, fp, '#2D2D2A', .3)
    Mx = f'matrix({C30:.4f},{S30:.4f},{-C30:.4f},{S30:.4f},0,0)'
    o.append(f'<g transform="{Mx}">')
    for lab in P.COMMON_LABELS:
        name, pos = lab[0], lab[1]
        if pos:
            o.append(f'<text x="{pos[0]}" y="{pos[1]+30*k}" text-anchor="middle" class="bt" font-size="{15*k:.1f}" letter-spacing="2.5" fill="#8a877d">{name.upper()}</text>')
    o += P.extras_iso()
    for x, y, w, h in getattr(P, 'SKYLIGHTS', []):
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#D6ECEA" stroke="{C["teal"]}" stroke-width="2" stroke-dasharray="6 4"/>')
    o.append('</g>')
    if hasattr(P, 'solids_iso'):
        o += P.solids_iso(iso, box_faces, k)
    solids = []
    WH, T = 24 * k, 3 * k
    seg = 24 * k
    WALLC = ('#2D2D2A', '#d9d3c6', '#c3bcac')
    def add_wall(a, b, c, d, t, cols=WALLC):
        if a == c:
            yy = b
            while yy < d:
                e = min(d, yy + seg)
                solids.append(((yy + e) / 2 + 2 * a, (a - t, yy, a + t, e, 0, WH) + cols)); yy = e
        else:
            xx = a
            while xx < c:
                e = min(c, xx + seg)
                solids.append(((xx + e) / 2 + 2 * b, (xx, b - t, e, b + t, 0, WH) + cols)); xx = e
    thin = getattr(P, 'THIN', lambda w: False)
    for w in P.WALLS:
        for a, b, c, d in wall_pieces(w):
            add_wall(a, b, c, d, T * (0.5 if thin(w) else 1))
    for w in getattr(P, 'GLASS_WALLS', []):
        for a, b, c, d in wall_pieces(w):
            add_wall(a, b, c, d, T, ('#9cc9c6', '#c5e0de', '#a9d0cd'))
    for w in getattr(P, 'OUTER_WALLS', None) or [(x0,y0,x1,y0,[]),(x1,y0,x1,y1,[]),(x0,y1,x1,y1,[]),(x0,y0,x0,y1,[])]:
        wx0, wy0, wx1, wy1, _ = w
        wins = [(a, b) for s, a, b in P.WINDOWS if
                ((wx0 == wx1) and s in ('L', 'R') and ((s == 'L' and wx0 == x0) or (s == 'R' and wx0 == x1)) and wy0 <= a < wy1) or
                ((wy0 == wy1) and s in ('T', 'B') and ((s == 'T' and wy0 == y0) or (s == 'B' and wy0 == y1)) and wx0 <= a < wx1) or
                (isinstance(s, tuple) and s == (wx0, wy0, wx1, wy1))]
        for a, b, c, d in wall_pieces((wx0, wy0, wx1, wy1, list(w[4]) + wins)):
            add_wall(a, b, c, d, 5 * k)
        for a, b in wins:
            if wx0 == wx1:
                add_wall(wx0, a, wx0, b, 3 * k, ('#9cc9c6', '#c5e0de', '#a9d0cd'))
            else:
                add_wall(a, wy0, b, wy0, 3 * k, ('#9cc9c6', '#c5e0de', '#a9d0cd'))
    for p0, p1, kind, gaps in getattr(P, 'SLANTS', []):
        cols = ('#9cc9c6', '#c5e0de', '#a9d0cd') if kind == 'glass' else WALLC
        for a, b in slant_pieces(p0, p1, gaps):
            n = max(1, int(math.hypot(b[0]-a[0], b[1]-a[1]) / seg))
            for i in range(n):
                pa = (a[0] + (b[0]-a[0])*i/n, a[1] + (b[1]-a[1])*i/n)
                pb = (a[0] + (b[0]-a[0])*(i+1)/n, a[1] + (b[1]-a[1])*(i+1)/n)
                q = [iso(pa[0], pa[1], 0), iso(pb[0], pb[1], 0), iso(pb[0], pb[1], WH), iso(pa[0], pa[1], WH)]
                face = ' '.join(f'{u:.1f},{v:.1f}' for u, v in q)
                t1, t2 = iso(pa[0], pa[1], WH), iso(pb[0], pb[1], WH)
                svg = (f'<polygon points="{face}" fill="{cols[2]}"/>'
                       f'<line x1="{t1[0]:.1f}" y1="{t1[1]:.1f}" x2="{t2[0]:.1f}" y2="{t2[1]:.1f}" stroke="{cols[0]}" stroke-width="{(10 if kind != "glass" else 6)*k:.1f}" stroke-linecap="square"/>')
                solids.append(((pa[0] + pb[0] + pa[1] + pb[1]) / 2 + 20, ('raw', svg)))
    for d in P.DESKS:
        x, y, w, h = d[:4]
        solids.append((x + w / 2 + y + h / 2, (x, y, x + w, y + h, 0, 13 * k, '#FBFAF6', '#ddd8cc', '#cfc9bb')))
    for _, (x, y, w, h) in list(getattr(P, 'KITCHEN', [])) + list(getattr(P, 'KITCHEN_ISO', [])):
        solids.append((x + w / 2 + y + h / 2, (x, y, x + w, y + h, 0, 15 * k, '#FBFAF6', '#ddd8cc', '#cfc9bb')))
    for sx, sy, sw_, sh in getattr(P, 'SOFAS', []):
        solids.append((sx + sw_ / 2 + sy + sh / 2, (sx, sy, sx + sw_, sy + sh, 0, 11 * k, '#d8c6a6', '#c3b08f', '#b39f7e')))
    solids.sort(key=lambda s: s[0])
    for _, b in solids:
        o.append(b[1] if b[0] == 'raw' else box_faces(*b))
    for cx, cy, r in getattr(P, 'TABLES', []):
        X, Y = iso(cx, cy, 13 * k)
        o.append(f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{r*1.22:.1f}" ry="{r*0.7:.1f}" fill="#FBFAF6" stroke="#2D2D2A" stroke-opacity=".25"/>')
    for px_, py_ in getattr(P, 'PLANTS', []):
        X, Y = iso(px_, py_, 18 * k)
        o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{13*k:.1f}" fill="#7f9c6a"/><circle cx="{X-4*k:.1f}" cy="{Y-4*k:.1f}" r="{6*k:.1f}" fill="#a3bf8c"/>')
    # badges (inverse-scaled so they read the same size in every building)
    bs = 0.9 / sc
    for of in offices:
        if of['id'] in avail or of['id'] in soon:
            continue
        lx, ly = of['lab']
        X, Y = iso(lx, ly - 10 * k, 40 * k)
        num = of['id'] if len(of['name']) <= 10 else of['name']
        o.append(f'<g transform="translate({X:.1f},{Y:.1f}) scale({bs:.3f})">'
                 + (f'<circle r="19" fill="#FBFAF6" stroke="#2D2D2A" stroke-width="1.6"/><text y="7" text-anchor="middle" class="ys" font-size="19" fill="#2D2D2A">{num}</text>'
                    if len(of['name']) <= 10 else f'<text y="7" text-anchor="middle" class="ys" font-size="17" fill="#2D2D2A" stroke="#F6F3EC" stroke-width="5" paint-order="stroke">{num}</text>')
                 + (f'<text y="38" text-anchor="middle" class="bt" font-weight="600" font-size="15" fill="#2D2D2A" stroke="#F6F3EC" stroke-width="5" paint-order="stroke" stroke-linejoin="round">{of["sq"]} sq ft</text>' if of['sq'] else '')
                 + '</g>')
    pins = getattr(P, 'PINS', {})
    for of in offices:
        if of['id'] not in avail and of['id'] not in soon:
            continue
        lx, ly = of['lab']
        X, Y = iso(lx, ly - 10 * k, 0)
        bw, bh = 230, 70
        dirn = pins.get(of['id'], 'right')
        L = 1 / bs
        if dirn == 'up':
            ex, ey = X, Y - 300 * bs * 1.0
            bx, by = ex - bw * bs / 2, ey - bh * bs
        elif dirn == 'left':
            ex, ey = X - 330 * bs, Y - 170 * bs
            bx, by = ex - bw * bs, ey - bh * bs / 2
        elif dirn == 'down':
            ex, ey = X - 200 * bs, Y + 200 * bs
            bx, by = ex - bw * bs, ey - bh * bs / 2
        else:
            ex, ey = X + 260 * bs, Y + 150 * bs
            bx, by = ex, ey - bh * bs / 2
        o.append(f'<polyline points="{X:.1f},{Y:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="#2D2D2A" stroke-width="{2.2*bs:.2f}"/>')
        o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{5*bs:.2f}" fill="#2D2D2A"/>')
        o.append(f'<g transform="translate({bx:.1f},{by:.1f}) scale({bs:.3f})">' + leaf(0, 0, bw, bh, '#2D2D2A', r=30) +
                 f'<text x="{bw/2}" y="31" text-anchor="middle" class="ys" font-size="25" fill="{C["cream"]}">{of["name"]}</text>'
                 f'<text x="{bw/2}" y="55" text-anchor="middle" class="bt" font-weight="600" font-size="15" letter-spacing="1" fill="{C["teal"]}">{(("COMING SOON" if soon[of["id"]] == "soon" else "FROM " + soon[of["id"]].upper())) if of["id"] in soon else "AVAILABLE"} · {of["sq"]} SQ FT</text></g>')
    o.append('</g>')
    M = P.META
    o.append(f'<text x="70" y="105" class="bt" font-size="15" letter-spacing="3" fill="#6b6a63">{M["site"]}{" · " + M["floor"] if M.get("floor") else ""}</text>')
    o.append(f'<text x="70" y="180" class="ys" font-size="68" fill="#2D2D2A" letter-spacing="-1.3">{M["title"]}</text>')
    n_off = len([of for of in offices if of['sq']])
    first = M['summary'].split(' · ')[0] if M.get('summary') else f'{n_off} private offices'
    sub = first + ('' if base else f' · {len(avail)} available' + (f', {len(soon)} coming up' if soon else '') + f' as of {date}')
    o.append(f'<text x="70" y="222" class="bt" font-size="19" fill="#6b6a63">{sub}</text>')
    lx_, ly_ = 72, 290
    legend = [('Private offices', '#E2DCCF'), ('Shared spaces', '#F6F3EC')] if base else \
             [('Available', C['teal'])] + ([('Coming up', '#C3DEDB')] if soon else []) + [('Let', '#E2DCCF'), ('Shared spaces', '#F6F3EC')]
    for lab, fill in legend:
        o.append(f'<rect x="{lx_}" y="{ly_-18}" width="24" height="24" rx="3" fill="{fill}" stroke="#2D2D2A" stroke-opacity=".25"/>')
        o.append(f'<text x="{lx_+38}" y="{ly_}" class="bt" font-size="18" fill="#2D2D2A">{lab}</text>')
        ly_ += 38
    if P.NORTH:
        nx, ny = P.NORTH
        sx_, sy_ = (nx - ny) * C30, (nx + ny) * S30
        nn = math.hypot(sx_, sy_)
        o.append(compass(120, ly_ + 50, sx_ / nn, sy_ / nn))
    o.append(f'<text x="72" y="{H-70}" class="ys" font-size="30" fill="#2D2D2A">Bespoke Spaces</text>')
    o.append(f'<text x="72" y="{H-42}" class="bt" font-size="15" fill="#6b6a63">bespokespaces.co · Illustrative, sizes approximate</text>')
    o.append('</svg>')
    return '\n'.join(o)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('module'); ap.add_argument('outdir')
    ap.add_argument('--avail'); ap.add_argument('--date', default='')
    ap.add_argument('--tag', default='')
    ap.add_argument('--soon', default='')
    a = ap.parse_args()
    P = importlib.import_module(a.module)
    avail = None if a.avail is None else set(x for x in a.avail.split(',') if x)
    os.makedirs(a.outdir, exist_ok=True)
    slug = P.META['slug']
    tag = a.tag or ('base' if avail is None else 'availability')
    for kind, fn in (('flat', flat), ('3d', isometric)):
        for embed, suffix in ((True, ''), (False, '_web')):
            soon = dict(kv.split('=') for kv in a.soon.split(';') if kv)
            open(os.path.join(a.outdir, f'{slug}-{kind}-{tag}{suffix}.svg'), 'w').write(fn(P, avail, a.date, embed, soon))
    print('ok', slug, tag)
