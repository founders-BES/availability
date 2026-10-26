#!/usr/bin/env python3
"""
Builds availability.bespokespaces.co from the public availability CSV.

- Reads ONLY the published CSV (the "Website" tab of "Bespoke Availability - Public & Agents").
- Uses only allow-listed columns. Grade is never shown.
- Offices only (dedicated desks are left out on purpose).
- Status wording matches the live list on bespokespaces.co (statusOf in the footer script).
- If the CSV can't be fetched or looks wrong, it exits with an error and the
  existing page is left untouched (never publishes an empty page).

Usage:  python3 build.py [--csv local.csv] [--out docs]
Standard library only.
"""
import argparse, csv, datetime as dt, html, io, json, os, sys, urllib.request
from zoneinfo import ZoneInfo

CSV_URL = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-nso5y4VC4vsKARwjzw38rJjGFmAOLOaHXi7"
           "ZQ3bhlkyhaEJeIjNapexXuRrjyb9lfjCmm-tO_0pG/pub?gid=1&single=true&output=csv")
PAGE_URL = "https://availability.bespokespaces.co/"
MAIN = "https://www.bespokespaces.co"
TZ = ZoneInfo("Europe/London")

ALLOWED = ["site", "label", "product", "desks", "sqft", "price", "vat", "status", "available_from"]

# Master Facts guard: lowest advertised office price per site. A room below this fails the build.
MIN_PRICE = {"archway": 595, "hornsey": 450}

# Google Analytics 4 + Google Ads tag (added 25 Oct 2026).
# Consent mode defaults to "denied": no cookies are set, Google gets anonymous pings only.
# Clicks on WhatsApp, phone and Book-a-viewing links are sent as events.
GA_SNIPPET = """<script>
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});
gtag('js',new Date());gtag('config','G-F75EW0QBMW');gtag('config','AW-944783854');
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'';
if(h.indexOf('wa.me')>-1){gtag('event','whatsapp_click',{link_url:h});}
else if(h.indexOf('tel:')===0){gtag('event','tel_click',{link_url:h});}
else if(h.indexOf('/contact')>-1){gtag('event','book_viewing_click',{link_url:h});}});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-F75EW0QBMW"></script>"""

SITES = {
    "archway": {
        "name": "Archway", "full": "Bespoke Spaces Archway",
        "street": "14 Windermere Road", "postcode": "N19 5SG",
        "id": MAIN + "/locations/archway#location", "loc": MAIN + "/locations/archway",
        "offices": MAIN + "/office-spaces-archway",
        "phone": "+447878925736", "phone_h": "07878 925736", "wa": "447878925736",
        "email": "hello@bespokespaces.co",
        "blurb": "A 2-minute walk from Archway station (Northern Line). Rooftop sauna and cold plunge "
                 "for members. Private offices from £595 + VAT/month, for teams of 1 to 15.",
    },
    "hornsey": {
        "name": "Hornsey Road", "full": "Bespoke Spaces Hornsey Road",
        "street": "465C Hornsey Road", "postcode": "N19 4DR",
        "id": MAIN + "/locations/hornsey#location", "loc": MAIN + "/locations/hornsey",
        "offices": MAIN + "/office-spaces-hornsey",
        "phone": "+447412891613", "phone_h": "07412 891613", "wa": "447412891613",
        "email": "info@bespokespaces.co",
        "blurb": "A converted warehouse with high ceilings and on-site parking (extra monthly cost). "
                 "Private offices from £450/month. Rooms in Units 1, 2 and 4 have no VAT to add; "
                 "rooms in Unit 6 are + VAT.",
    },
}
ORDER = ["archway", "hornsey"]


class BuildError(Exception):
    pass


# ---------- data ----------
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "bespoke-availability-build/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status != 200:
            raise BuildError(f"CSV fetch returned HTTP {r.status}")
        return r.read().decode("utf-8-sig")


def parse(text):
    if not text.lower().lstrip().startswith("site"):
        raise BuildError("CSV header does not start with 'site' (got: %r)" % text[:60])
    rows = list(csv.DictReader(io.StringIO(text)))
    clean = []
    for r in rows:
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
        if not "".join(r.values()):
            continue
        clean.append({k: r.get(k, "") for k in ALLOWED})  # drop anything not allow-listed
    return clean


def money(p):
    try:
        n = float("".join(c for c in p if c.isdigit() or c == "."))
    except ValueError:
        return None
    return int(n) if n.is_integer() else n


def vat_text(v):
    v = v.lower()
    return {"no vat": "no VAT to add", "+ vat": "+ VAT", "vat included": "incl. VAT"}.get(v, "")


def parse_day(s):
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def nice(d):
    return f"{d.day} {d.strftime('%b')}"


def status_of(r, today):
    """Same rules and wording as statusOf() in the live footer script."""
    st, d = r["status"].lower(), parse_day(r["available_from"])
    if st == "under offer":
        return 3, None, "Under offer", "offer"
    if st == "available now" or (d and d <= today):
        return 0, today, "Available now", "now"
    if d:
        return 1, d, f"From {nice(d)}", "later"
    return 2, None, "Coming up – ask us", "later"


def short_label(label, site):
    # "Office 8, Archway" -> "Office 8" (the building is already the section heading)
    if site == "archway" and label.lower().endswith(", archway"):
        return label[: -len(", archway")]
    return label


def offices(rows, today):
    out = {k: [] for k in ORDER}
    for r in rows:
        site = r["site"].lower()
        if r["product"].lower() != "office":
            continue  # dedicated desks are deliberately left out
        if site not in out:
            raise BuildError(f"Unknown site {r['site']!r}")
        price = money(r["price"])
        if price is None:
            raise BuildError(f"No price for {r['label']!r}")
        if price < MIN_PRICE[site]:
            raise BuildError(f"{r['label']} at £{price} is below the Master Facts from-price "
                             f"(£{MIN_PRICE[site]}) for {site}. Check the sheet.")
        rank, d, text, cls = status_of(r, today)
        out[site].append({**r, "price_n": price, "rank": rank, "d": d, "st": text, "cls": cls,
                          "short": short_label(r["label"], site)})
    for k in out:
        out[k].sort(key=lambda o: (o["rank"], o["d"] or dt.date.max, o["price_n"]))
    if sum(len(v) for v in out.values()) == 0:
        raise BuildError("No offices in the CSV - refusing to publish an empty page")
    return out


# ---------- page ----------
E = html.escape


def fmt_price(o):
    return f"£{o["price_n"]:,}/month" + ((", " if o["vat"].lower() == "no vat" else " ") + vat_text(o["vat"]) if vat_text(o["vat"]) else "")


def people(o):
    return f"{o['desks']} people" if o["desks"] else ""


def sentence(o):
    bits = [o["short"]]
    detail = ", ".join(x for x in [people(o) and "for " + people(o),
                                   o["sqft"] and f"about {o['sqft']} sq ft"] if x)
    if detail:
        bits.append(detail)
    bits.append(fmt_price(o))
    status = o["st"].lower() if o["rank"] != 1 else o["st"].replace("From", "available from")
    if o["rank"] == 2:
        status = "coming up soon (ask us for the date)"
    return ": ".join([bits[0], ", ".join(bits[1:])]) + f" – {status}."


def summary(site, rows):
    s = SITES[site]
    now = sum(1 for o in rows if o["rank"] == 0)
    n = len(rows)
    lo = min(rows, key=lambda o: o["price_n"])
    parts = [f"{n} private office{'s' if n != 1 else ''} at {s['street']}, {s['postcode']}"]
    parts.append(f"{now} available now" if now else "none free today, more coming up")
    return (f"{s['full']} currently lists " + parts[0] + f" ({parts[1]}). "
            f"Listed rooms start at {fmt_price(lo)}.")


def offer_ld(o, site):
    s = SITES[site]
    ld = {
        "@type": "Offer",
        "name": f"Private office: {o['short']}, {s['full']}",
        "url": s["offices"],
        "price": str(o["price_n"]),
        "priceCurrency": "GBP",
        "priceSpecification": {
            "@type": "UnitPriceSpecification", "price": str(o["price_n"]), "priceCurrency": "GBP",
            "unitCode": "MON", "unitText": "month",
            "valueAddedTaxIncluded": o["vat"].lower() != "+ vat",
        },
        "availability": "https://schema.org/InStock" if o["rank"] == 0 else "https://schema.org/PreOrder",
        "offeredBy": {"@id": s["id"]},
        "itemOffered": {
            "@type": "Service", "name": f"Private serviced office ({o['short']})",
            "serviceType": "Private serviced office",
            "areaServed": "North London",
        },
    }
    if o["d"] and o["rank"] in (0, 1):
        ld["availabilityStarts"] = o["d"].isoformat()
    desc = ", ".join(x for x in [people(o), o["sqft"] and f"about {o['sqft']} sq ft"] if x)
    if desc:
        ld["description"] = desc
    return ld


def build_jsonld(data, today):
    graph = [{
        "@type": "Organization", "@id": MAIN + "/#organization",
        "name": "Bespoke Spaces London Ltd", "alternateName": "Bespoke Spaces",
        "url": MAIN, "foundingDate": "2013-05", "email": "info@bespokespaces.co",
        "telephone": "+447412891613",
    }, {
        "@type": "WebPage", "@id": PAGE_URL + "#page", "url": PAGE_URL,
        "name": "Office availability – Bespoke Spaces, North London",
        "dateModified": today.isoformat(), "inLanguage": "en-GB",
        "publisher": {"@id": MAIN + "/#organization"},
    }]
    for site in ORDER:
        s = SITES[site]
        graph.append({
            "@type": "LocalBusiness", "@id": s["id"], "name": s["full"], "url": s["loc"],
            "telephone": s["phone"], "email": s["email"],
            "address": {"@type": "PostalAddress", "streetAddress": s["street"],
                        "addressLocality": "London", "postalCode": s["postcode"],
                        "addressCountry": "GB"},
            "parentOrganization": {"@id": MAIN + "/#organization"},
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": f"Private offices available at {s['full']}",
                "itemListElement": [offer_ld(o, site) for o in data[site]],
            },
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


CSS = """
:root{--ink:#2d2d2a;--teal:#7bb5b2;--sand:#eae6dd;--card:#f6f4ef;--line:rgba(45,45,42,.14)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--sand);color:var(--ink);font:17px/1.6 Bitter,Georgia,serif}
a{color:var(--ink)}
.wrap{max-width:900px;margin:0 auto;padding:0 16px}
header.top{padding:18px 0;border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.brand{font-weight:700;text-decoration:none;font-size:1.1rem}
.top nav a{margin-left:16px;font-size:.95rem}
h1{font-size:clamp(1.7rem,4vw,2.4rem);line-height:1.2;margin:40px 0 8px}
.updated{opacity:.75;margin:0 0 20px}
.lead{font-size:1.08rem;max-width:62ch}
.btn{display:inline-block;padding:.6em 1.4em;background:var(--teal);color:var(--ink);text-decoration:none;
 font-weight:600;border-radius:45px 0;border:2px solid var(--teal)}
.btn.ghost{background:transparent}
.ctas{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 8px}
section.site{background:var(--card);border-radius:4px;padding:24px 20px;margin:36px 0}
section.site h2{margin:0 0 4px;font-size:1.5rem}
.addr{margin:0 0 10px;opacity:.85}
.summary{margin:0 0 16px}
table{width:100%;border-collapse:collapse;font-size:.97rem}
th,td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;opacity:.75}
td.room{font-weight:700}
.s{display:inline-block;padding:.05em .6em;border-radius:20px;font-size:.88em;white-space:nowrap;background:rgba(123,181,178,.35)}
.s.now{background:var(--teal)}
.s.offer{background:rgba(0,0,0,.08)}
.plans figure{margin:22px 0 6px}
.plans svg{border-radius:4px}
.plans figcaption{font-size:.85rem;opacity:.75;margin-top:6px}
.terms{margin:40px 0}
.terms li{margin:.3em 0}
footer{border-top:1px solid var(--line);padding:24px 0 40px;font-size:.92rem;opacity:.85}
@media (max-width:640px){
 thead{display:none}
 table,tbody,tr,td{display:block;width:100%}
 tr{padding:10px 0;border-bottom:1px solid var(--line)}
 td{border:0;padding:2px 0}
 td[data-l]:not(.room)::before{content:attr(data-l) ": ";opacity:.7}
 section.site{padding:20px 16px}
}
"""


def plan_figs(plans, site):
    """Live floor plans for one site (only buildings with a listed office)."""
    figs = [p for p in (plans or {}).get(site, []) if p["listed"]]
    if not figs:
        return ""
    from plans.live import inline
    return "<div class=\"plans\">" + "".join(
        f"<figure>{inline(p)}<figcaption><a href=\"plans/{p['slug']}.svg\">{E(p['title'])} floor plan</a>, "
        "teal = available now, light teal = coming up. Updated with this list.</figcaption></figure>"
        for p in figs) + "</div>"


def render(data, now, plans=None):
    today = now.date()
    date_h = f"{today.day} {today.strftime('%B %Y')}"
    total = sum(len(v) for v in data.values())
    total_now = sum(1 for v in data.values() for o in v if o["rank"] == 0)

    sections = []
    for site in ORDER:
        s, rows = SITES[site], data[site]
        if not rows:
            body = ("<p>No rooms listed right now. Offices free up regularly – "
                    f"<a href=\"{MAIN}/contact\">ask us what's coming up</a>.</p>")
        else:
            trs = "\n".join(
                f"<tr><td class=\"room\" data-l=\"Office\">{E(o['short'])}</td>"
                f"<td data-l=\"Team size\">{E(people(o)) or '–'}</td>"
                f"<td data-l=\"Size\">{E(o['sqft']) + ' sq ft' if o['sqft'] else '–'}</td>"
                f"<td data-l=\"Price\">{E(fmt_price(o))}</td>"
                f"<td data-l=\"Status\"><span class=\"s {o['cls']}\">{E(o['st'])}</span></td></tr>"
                for o in rows)
            body = (f"<p class=\"summary\">{E(summary(site, rows))}</p>"
                    "<table><thead><tr><th>Office</th><th>Team size</th><th>Size</th>"
                    f"<th>Price</th><th>Status</th></tr></thead><tbody>\n{trs}\n</tbody></table>"
                    "<h3 style=\"font-size:1rem;margin:20px 0 6px\">In plain words</h3><ul>"
                    + "".join(f"<li>{E(sentence(o))}</li>" for o in rows) + "</ul>")
        sections.append(f"""
<section class="site" id="{site}">
<h2>{E(s['full'])}</h2>
<p class="addr">{E(s['street'])}, London {E(s['postcode'])} · <a href="tel:{s['phone']}">{E(s['phone_h'])}</a> · <a href="mailto:{s['email']}">{E(s['email'])}</a></p>
<p>{E(s['blurb'])}</p>
{body}
{plan_figs(plans, site)}
<div class="ctas"><a class="btn" href="{MAIN}/contact">Book a viewing</a>
<a class="btn ghost" href="https://wa.me/{s['wa']}">WhatsApp {E(s['name'])}</a>
<a class="btn ghost" href="{s['offices']}">See the {E(s['name'])} offices</a></div>
</section>""")

    desc = (f"Live list of private offices to rent at Bespoke Spaces in Archway and on Hornsey Road, "
            f"North London N19. Updated {date_h}: {total} offices listed, {total_now} available now, "
            f"with prices, team sizes and move-in dates.")
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Office availability today | Archway &amp; Hornsey Road, N19 | Bespoke Spaces</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{PAGE_URL}">
<meta name="robots" content="index,follow,max-snippet:-1">
<meta property="og:title" content="Office availability – Bespoke Spaces, North London">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{PAGE_URL}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@400;600;700&family=Young+Serif&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">
{build_jsonld(data, today)}
</script>
{GA_SNIPPET}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{MAIN}/">Bespoke Spaces</a>
<nav><a href="{MAIN}/office-spaces-to-rent">Offices</a><a href="{MAIN}/coworking-spaces">Coworking</a><a href="{MAIN}/contact">Contact</a></nav>
</div></header>
<main class="wrap">
<h1>Office availability – Bespoke Spaces, North London</h1>
<p class="updated">Updated <time datetime="{today.isoformat()}">{date_h}</time>. This list comes straight from our booking sheet and refreshes through the day.</p>
<p class="lead">Every private office we have free now or coming up soon, in our two buildings in N19: <a href="#archway">Archway</a> and <a href="#hornsey">Hornsey Road</a>. Today that's {total} offices, {total_now} of them available now. Rooms are furnished, and you can view them in person.</p>
<div class="ctas"><a class="btn" href="{MAIN}/contact">Book a viewing</a></div>
{''.join(sections)}
<section class="terms">
<h2 style="font-size:1.3rem">How renting an office works</h2>
<ul>
<li>Contracts are 12 months. Shorter contracts are available, at a premium that depends on the length.</li>
<li>You pay the first month plus a two-month deposit, returned when you leave.</li>
<li>Rent covers business rates, electricity, heating, 24/7 access, alarm and CCTV, building maintenance and communal cleaning.</li>
<li>Internet for private offices is priced separately, based on what you need.</li>
<li>Prices shown are per month. "+ VAT" means VAT is added; "no VAT to add" means the price is what you pay.</li>
</ul>
<p>Looking for a desk rather than a room? See <a href="{MAIN}/coworking-spaces">coworking from £29 a day</a>.</p>
</section>
</main>
<footer><div class="wrap">
Bespoke Spaces London Ltd · Independent workspace in North London since May 2013 ·
<a href="{MAIN}/">bespokespaces.co</a>
</div></footer>
</body>
</html>
"""


def write_if_changed(path, content):
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="read a local CSV instead of fetching (for testing)")
    ap.add_argument("--out", default="docs")
    ap.add_argument("--now", help="override date YYYY-MM-DD (testing)")
    a = ap.parse_args()
    now = dt.datetime.now(TZ)
    if a.now:
        now = dt.datetime.combine(dt.date.fromisoformat(a.now), dt.time(9), TZ)
    try:
        text = open(a.csv, encoding="utf-8-sig").read() if a.csv else fetch(CSV_URL)
        data = offices(parse(text), now.date())
    except Exception as e:  # keep yesterday's page
        print(f"BUILD STOPPED, existing page kept: {e}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(a.out, exist_ok=True)
    plans, plans_changed = None, False
    try:  # live floor plans; a problem here never stops the page
        from plans import live
        plans_changed, plans = live.build(data, now.date(), os.path.join(a.out, "plans"), write_if_changed)
    except Exception as e:
        print(f"plans skipped, previous plans kept: {e!r}", file=sys.stderr)
    changed = write_if_changed(os.path.join(a.out, "index.html"), render(data, now, plans))
    changed = changed or plans_changed
    write_if_changed(os.path.join(a.out, "robots.txt"),
                     "User-agent: *\nAllow: /\n\n" +
                     "".join(f"User-agent: {b}\nAllow: /\n\n" for b in
                             ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
                              "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended",
                              "Bingbot", "Applebot", "Applebot-Extended"]) +
                     f"Sitemap: {PAGE_URL}sitemap.xml\n")
    write_if_changed(os.path.join(a.out, "sitemap.xml"),
                     '<?xml version="1.0" encoding="UTF-8"?>\n'
                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                     f"<url><loc>{PAGE_URL}</loc><lastmod>{now.date().isoformat()}</lastmod>"
                     "<changefreq>daily</changefreq></url>\n</urlset>\n")
    write_if_changed(os.path.join(a.out, "CNAME"), "availability.bespokespaces.co\n")
    print("changed" if changed else "unchanged")


if __name__ == "__main__":
    main()
