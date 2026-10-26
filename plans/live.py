"""Live floor plans for availability.bespokespaces.co.

Called by build.py after the CSV has been read. For every building it redraws the
floor plan with today's free and coming-up offices coloured in, and writes:

  docs/plans/<slug>.svg      flat plan (used on the pages)
  docs/plans/<slug>-3d.svg   3D cutaway
  docs/plans/office/<slug>-office-<n>.svg   one listed office picked out, for its own page

The drawings themselves live in plans/<building>.py; plans/render.py draws them.
If anything here goes wrong the availability page is still built and the
previous plans are left in place.
"""
import os, re, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# feed label -> (site, building module)
BUILDINGS = [
    # site,     module,    slug,            title,            match unit
    ("archway", "archway", "archway",       "Archway",        None),
    ("hornsey", "unit1",   "hornsey-unit1", "Hornsey Unit 1", "1"),
    ("hornsey", "unit2",   "hornsey-unit2", "Hornsey Unit 2", "2"),
    ("hornsey", "unit4",   "hornsey-unit4", "Hornsey Unit 4", "4"),
    ("hornsey", "unit6",   "hornsey-unit6", "Hornsey Unit 6", "6"),
]
LABEL = re.compile(r"^\s*office\s+([0-9]+[a-z]?)\s*,\s*(?:unit\s*([0-9]+)|archway)\s*$", re.I)


def _when(o):
    """rank/date from build.py -> the plan's 'coming up' text."""
    if o["rank"] == 1 and o["d"]:
        return f"{o['d'].day} {o['d'].strftime('%b')}"
    return "soon"


def build(data, today, out_dir, write):
    """data = build.offices() result. write = build.write_if_changed.
    Returns (changed, {site: [plan dicts]})."""
    render = importlib.import_module("render")
    date_s = f"{today.day} {today.strftime('%b %Y')}"
    os.makedirs(out_dir, exist_ok=True)
    changed, shown = False, {"archway": [], "hornsey": []}
    keep = set()
    os.makedirs(os.path.join(out_dir, "office"), exist_ok=True)
    for site, mod, slug, title, unit in BUILDINGS:
        P = importlib.import_module(mod)
        ids = {o[0] for o in P.OFFICES}
        avail, soon, listed = set(), {}, []
        for o in data.get(site, []):
            m = LABEL.match(o["label"])
            if not m:
                continue
            oid, u = m.group(1).upper(), m.group(2)
            if (unit is None and u is not None) or (unit is not None and u != unit):
                continue
            if oid not in ids:
                print(f"plans: {o['label']} is not on the {title} plan, skipped", file=sys.stderr)
                continue
            if o["rank"] == 0:
                avail.add(oid)
            elif o["rank"] in (1, 2):
                soon[oid] = _when(o)
            else:
                continue  # under offer: shown as let
            listed.append(oid)
        # single-office versions for each listed office's own page (no date, so they only change with status)
        for oid in listed:
            one_a = {oid} if oid in avail else set()
            one_s = {oid: soon[oid]} if oid in soon else {}
            name = f"{slug}-office-{oid.lower()}.svg"
            keep.add(name)
            changed |= write(os.path.join(out_dir, "office", name), render.flat(P, one_a, "", False, one_s, focus=oid))
        flat = render.flat(P, avail, date_s, False, soon)
        iso = render.isometric(P, avail, date_s, False, soon)
        changed |= write(os.path.join(out_dir, f"{slug}.svg"), flat)
        changed |= write(os.path.join(out_dir, f"{slug}-3d.svg"), iso)
        shown[site].append({"slug": slug, "title": title, "listed": listed, "svg": flat,
                            "avail": sorted(avail, key=_num), "soon": sorted(soon, key=_num)})
    # remove single-office plans for offices no longer listed (their page shows nothing then)
    for f in os.listdir(os.path.join(out_dir, "office")):
        if f.endswith(".svg") and f not in keep:
            os.remove(os.path.join(out_dir, "office", f))
            changed = True
    # which plans to show, for the loader on bespokespaces.co (buildings with a listed office)
    import json
    idx = {site: [{"slug": p["slug"], "title": p["title"], "alt": alt_text(p)} for p in v if p["listed"]]
           for site, v in shown.items()}
    changed |= write(os.path.join(out_dir, "index.json"), json.dumps(idx, ensure_ascii=False, indent=1) + "\n")
    return changed, shown


def _num(x):
    m = re.match(r"(\d+)", x)
    return (int(m.group(1)) if m else 0, x)


def alt_text(p):
    bits = []
    if p["avail"]:
        bits.append("available now: Office " + ", ".join(p["avail"]))
    if p["soon"]:
        bits.append("coming up: Office " + ", ".join(p["soon"]))
    return f"Floor plan of {p['title']}" + (" – " + "; ".join(bits) if bits else "")


def inline(p):
    """The flat plan as inline SVG for a web page (inline so it uses the page's fonts)."""
    svg = p["svg"]
    svg = svg.replace(' width="1500" height="1150"',
                      f' role="img" aria-label="{_esc(alt_text(p))}" style="display:block;width:100%;height:auto"', 1)
    return svg


def _esc(t):
    return t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
