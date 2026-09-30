#!/usr/bin/env python3
"""Builds the local-SEO layer of the Meadow Prints site.

Run from the repo root:  python3 tools/build_seo.py

It (re)writes:
  - the <head> SEO block (title, description, canonical, Open Graph, JSON-LD) of every page
  - one landing page per town in TOWNS, plus service-areas.html
  - screen-printing.html and custom-t-shirts.html
  - sitemap.xml and robots.txt

Business facts live in BUSINESS below - update them here (phone, address, domain)
and re-run, rather than editing the generated pages by hand.
"""
import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.meadowprintsandembroidery.com"
ASSET_V = "22"
TODAY = datetime.date.today().isoformat()

BUSINESS = {
    "name": "Meadow Prints & Embroidery",
    "legal": "Meadow Prints & Embroidery LLC",
    "founder": "Roger Padalec",
    "founder_title": "Founder & Head of Operations",
    "founded": "2024",
    "county": "Monmouth County",
    "region": "NJ",
    # Fill these in once confirmed with the client, then re-run. Empty values are left out.
    "phone": "+1-732-763-6078",
    "email": "meadowprintsembroidery@gmail.com",
    "street": "",
    "city": "",
    "zip": "",
}

# ---------------------------------------------------------------- towns
# slug, name, intro (unique copy), what that town orders most, nearby slugs
TOWNS = [
    ("freehold", "Freehold",
     "Freehold is the Monmouth County seat, and between the restaurants and shops along Main Street, the offices around the courthouse, and the stores near Freehold Raceway Mall there is always a crew that needs to look the part. We print and embroider for Freehold Borough and Freehold Township businesses, school groups, and rec teams.",
     ["Embroidered polos and quarter-zips for downtown offices and professional firms",
      "Staff tees and aprons for Main Street restaurants, bars and cafes",
      "Spirit wear and booster-club merch for Freehold school teams",
      "Hi-vis hoodies and work shirts for local contractors and trades"],
     ["manalapan", "howell", "colts-neck", "marlboro"]),
    ("red-bank", "Red Bank",
     "Red Bank packs a lot into a small downtown: the boutiques and restaurants on Broad Street, the theaters and galleries, and a riverfront that fills up for events all year. We make custom apparel for Red Bank shops, restaurants, nonprofits and event organizers who want merch people actually keep wearing.",
     ["Branded tees and hats for Broad Street boutiques, salons and restaurants",
      "Event shirts for festivals, 5Ks and fundraisers along the Navesink",
      "Embroidered jackets and polos for real estate and professional offices",
      "Short-run merch for bands, artists and theater groups"],
     ["shrewsbury-little-silver", "middletown", "rumson-fair-haven", "tinton-falls"]),
    ("middletown", "Middletown",
     "Middletown is the largest township in Monmouth County, stretching from Lincroft to Belford, Leonardo and Port Monmouth on the bayshore. That means a lot of youth leagues, school clubs, swim teams and family businesses - and we outfit all of them with custom printed and embroidered gear.",
     ["Team jerseys, warmups and fan gear for Middletown youth sports leagues",
      "Class shirts, club tees and PTA merch for township schools",
      "Embroidered workwear for landscapers, plumbers, electricians and builders",
      "Family reunion and block-party shirts in any size mix"],
     ["red-bank", "holmdel", "hazlet", "atlantic-highlands"]),
    ("howell", "Howell",
     "Howell is one of the biggest townships in the county, with busy Route 9 storefronts, a huge base of contractors and landscapers, and rec leagues that run in every season. We print and stitch durable, good-looking gear for Howell crews, teams and small businesses.",
     ["Hi-vis shirts, hoodies and embroidered hats for landscaping and construction crews",
      "Rec league and travel team uniforms with names and numbers",
      "Logo tees and hoodies for Route 9 gyms, garages and shops",
      "Fundraiser shirts for school and community groups"],
     ["freehold", "wall", "manalapan", "colts-neck"]),
    ("marlboro", "Marlboro",
     "Marlboro families are always on a field, in a gym or at a school event, and local businesses along Routes 9 and 79 serve them year-round. We make the spirit wear, team apparel and branded staff gear that keeps Marlboro looking sharp.",
     ["Spirit wear and team apparel for Marlboro school and rec programs",
      "Dance, cheer and gymnastics studio jackets and bags",
      "Embroidered polos for medical, dental and professional offices",
      "Bar and bat mitzvah, birthday and family event shirts"],
     ["manalapan", "freehold", "holmdel", "matawan-aberdeen"]),
    ("manalapan", "Manalapan",
     "From the Route 9 corridor to the fields at the rec complex, Manalapan and neighboring Englishtown keep busy with youth sports, school activities and family-run businesses. We supply custom t-shirts, hoodies and embroidered gear for all of it.",
     ["Uniforms and sideline gear for Manalapan rec and travel teams",
      "School club, band and graduating-class shirts",
      "Branded apparel for Route 9 retailers, restaurants and fitness studios",
      "Embroidered caps and jackets for local trades"],
     ["marlboro", "freehold", "millstone-upper-freehold", "howell"]),
    ("holmdel", "Holmdel",
     "Holmdel mixes quiet neighborhoods and farms with the companies and shops at Bell Works. We make polished embroidered apparel for Holmdel offices and startups, plus team and school gear for local families.",
     ["Embroidered polos, vests and quarter-zips for offices and tech teams",
      "Company swag and onboarding kits for growing businesses",
      "Spirit wear for Holmdel school teams and clubs",
      "Golf outing and charity event apparel"],
     ["middletown", "hazlet", "marlboro", "colts-neck"]),
    ("asbury-park", "Asbury Park",
     "Asbury Park runs on its boardwalk, its music venues and the restaurants and shops along Cookman Avenue. We print merch that fits the city's style - band tees, bar and restaurant shirts, surf-shop hoodies and event apparel in small or large runs.",
     ["Band, venue and festival merch in short runs or bulk",
      "Staff shirts and hats for boardwalk and downtown bars and restaurants",
      "Retail-quality tees and hoodies for surf shops and boutiques",
      "Event shirts for races, parades and community organizations"],
     ["neptune", "ocean-township", "belmar", "long-branch"]),
    ("long-branch", "Long Branch",
     "Long Branch is a year-round oceanfront city, from the shops and restaurants at Pier Village to the neighborhoods along Broadway. We produce custom apparel for Long Branch hospitality businesses, beach clubs, schools and summer events.",
     ["Uniform tees and polos for restaurants, hotels and beach clubs",
      "Lifeguard, camp and summer-staff shirts",
      "Team apparel for Long Branch school and rec sports",
      "Branded merch for shops and seasonal pop-ups"],
     ["west-long-branch", "oceanport", "ocean-township", "asbury-park"]),
    ("wall", "Wall Township",
     "Wall Township sits where the Shore meets the highway corridors of Routes 34, 35 and 138, with Allaire State Park in its backyard. It is home to a lot of trades, service companies and competitive sports programs, and we outfit them with custom printed and embroidered gear.",
     ["Embroidered workwear and hats for HVAC, plumbing and electrical companies",
      "Team uniforms, warmups and spirit wear for Wall sports programs",
      "Logo apparel for car dealerships, marinas and service shops",
      "Event tees for charity runs and community days"],
     ["manasquan", "belmar", "howell", "spring-lake"]),
    ("neptune", "Neptune",
     "Neptune Township covers a lot of ground, from the Victorian streets of Ocean Grove to the medical campus and the businesses along Routes 33 and 35. We make custom apparel for Neptune healthcare teams, churches, schools and local companies.",
     ["Embroidered scrubs jackets, fleeces and polos for healthcare and office teams",
      "Church, youth group and community organization shirts",
      "Team and spirit apparel for Neptune schools",
      "Shop merch for Ocean Grove stores and cafes"],
     ["asbury-park", "ocean-township", "tinton-falls", "wall"]),
    ("tinton-falls", "Tinton Falls",
     "Tinton Falls is a hub for corporate parks, medical offices and retail around the Garden State Parkway. We handle branded apparel programs for Tinton Falls employers along with team and event shirts for residents.",
     ["Company polos, jackets and caps with embroidered logos",
      "Trade-show and conference giveaways",
      "Retail and restaurant staff uniforms",
      "Rec team and school club apparel"],
     ["eatontown", "red-bank", "neptune", "shrewsbury-little-silver"]),
    ("ocean-township", "Ocean Township",
     "Ocean Township includes Oakhurst, Wanamassa and Wayside, with a long stretch of Route 35 businesses and a very active sports community. We print and embroider for Ocean Township teams, schools, temples, churches and shops.",
     ["Team uniforms and fan apparel for township sports",
      "School, camp and swim-club shirts",
      "Embroidered apparel for Route 35 retailers and offices",
      "Shirts for charity events and family celebrations"],
     ["asbury-park", "long-branch", "eatontown", "neptune"]),
    ("eatontown", "Eatontown",
     "Eatontown sits at the crossroads of Routes 35 and 36, with retail, restaurants and new businesses moving into the former Fort Monmouth. We supply those employers with uniforms and branded merch, and local teams with custom gear.",
     ["Uniform shirts for retail, auto and restaurant staff",
      "Embroidered polos and outerwear for offices and contractors",
      "Grand-opening and promotional giveaway tees",
      "Youth sports and school apparel"],
     ["tinton-falls", "oceanport", "ocean-township", "shrewsbury-little-silver"]),
    ("colts-neck", "Colts Neck",
     "Colts Neck is horse country - farms, orchards, equestrian barns and farm markets along Route 34 and Route 537. We embroider the barn jackets, vests, caps and polos that suit it, and print tees for farm stands, teams and events.",
     ["Embroidered vests, quarter-zips and caps for farms and equestrian barns",
      "Farm market and orchard staff shirts and retail merch",
      "Team and spirit wear for Colts Neck schools",
      "Golf, charity and hunt-club event apparel"],
     ["freehold", "holmdel", "howell", "tinton-falls"]),
    ("hazlet", "Hazlet",
     "Hazlet is a tight-knit bayshore township with busy storefronts on Routes 35 and 36 and strong youth sports. We make affordable, good-looking custom apparel for Hazlet teams, schools, first responders and small businesses.",
     ["Youth league uniforms, hoodies and parent fan gear",
      "Shirts for fire companies, first aid squads and benefit events",
      "Logo tees and hats for local shops and restaurants",
      "School club and graduation shirts"],
     ["holmdel", "middletown", "keyport", "matawan-aberdeen"]),
    ("matawan-aberdeen", "Matawan & Aberdeen",
     "Matawan and Aberdeen share a train station, a school district and a Main Street full of independent businesses. We print and embroider for both towns - commuter-town startups, restaurants, school groups and rec teams alike.",
     ["Spirit wear for Matawan-Aberdeen school teams and clubs",
      "Branded tees and hats for Main Street shops and restaurants",
      "Embroidered workwear for local trades and service companies",
      "Community event, fundraiser and memorial shirts"],
     ["hazlet", "keyport", "marlboro", "holmdel"]),
    ("belmar", "Belmar",
     "Belmar is a classic Shore town: the beach and boardwalk, the marina, the Main Street bars and restaurants, and events that draw crowds all year. We make the staff shirts, event tees and beach-town merch Belmar businesses sell and wear.",
     ["Staff tees, tanks and hats for bars, restaurants and beach concessions",
      "Shirts for races, parades and summer events",
      "Fishing charter and marina apparel",
      "Rental-house and family beach-week shirts"],
     ["wall", "spring-lake", "asbury-park", "manasquan"]),
    ("manasquan", "Manasquan",
     "Manasquan has a walkable Main Street, a beachfront and inlet that define its summers, and sports teams the whole town follows. We print and embroider for Manasquan shops, surf and fishing businesses, teams and beach clubs.",
     ["Retail tees and hoodies for Main Street and beachfront shops",
      "Team apparel and booster-club gear",
      "Embroidered hats and outerwear for marine and fishing businesses",
      "Summer camp, lifeguard and beach-club shirts"],
     ["wall", "spring-lake", "belmar", "howell"]),
    ("rumson-fair-haven", "Rumson & Fair Haven",
     "Rumson and Fair Haven sit side by side between the Navesink and Shrewsbury rivers, with active school communities, clubs and small downtowns. We produce clean, well-made embroidered and printed apparel for both towns.",
     ["Embroidered quarter-zips, vests and caps for clubs and teams",
      "School, sailing and swim-team apparel",
      "Staff apparel for River Road shops and restaurants",
      "Charity event, gala and golf outing gear"],
     ["red-bank", "shrewsbury-little-silver", "middletown", "oceanport"]),
    ("shrewsbury-little-silver", "Shrewsbury & Little Silver",
     "Shrewsbury and Little Silver are home to the shops along Broad Street and Route 35, medical and professional offices, and busy school and rec programs. We make custom apparel for the businesses and families in both towns.",
     ["Embroidered polos and fleeces for medical and professional offices",
      "Boutique and restaurant staff apparel",
      "Spirit wear for school teams and clubs",
      "Rec league shirts and coach gear"],
     ["red-bank", "tinton-falls", "eatontown", "rumson-fair-haven"]),
    ("keyport", "Keyport",
     "Keyport is a bayshore town with a waterfront promenade, an old-fashioned downtown on Front Street, and a calendar full of festivals. We print and embroider for Keyport restaurants, antique and specialty shops, marinas and community groups.",
     ["Staff shirts and hats for waterfront restaurants and bars",
      "Festival and event tees",
      "Shop merch for downtown retailers",
      "Apparel for fire companies, civic groups and school teams"],
     ["hazlet", "matawan-aberdeen", "middletown", "holmdel"]),
    ("spring-lake", "Spring Lake",
     "Spring Lake is known for its boardwalk, its inns and the shops on Third Avenue. We make refined embroidered apparel and retail-quality printed pieces for Spring Lake businesses, clubs and events, including neighboring Spring Lake Heights and Sea Girt.",
     ["Embroidered polos, quarter-zips and caps for inns, clubs and shops",
      "Retail sweatshirts and tees for Third Avenue stores",
      "Race and charity event apparel",
      "Beach-club and lifeguard gear"],
     ["belmar", "wall", "manasquan", "asbury-park"]),
    ("oceanport", "Oceanport",
     "Oceanport is home to Monmouth Park and a growing mix of businesses on the former Fort Monmouth property. We supply custom apparel for Oceanport stables and racing teams, new businesses, schools and community events.",
     ["Embroidered jackets, vests and caps for stables and racing outfits",
      "Branded apparel for new and relocating businesses",
      "School and rec team gear",
      "Shirts for community days and charity events"],
     ["long-branch", "eatontown", "west-long-branch", "rumson-fair-haven"]),
    ("west-long-branch", "West Long Branch",
     "West Long Branch is a college town, home to Monmouth University alongside family neighborhoods and the shops on Route 36 and Route 71. We print for student organizations, clubs, local businesses and teams.",
     ["Club, Greek life and student organization shirts and hoodies",
      "Intramural and rec team apparel",
      "Staff uniforms for local restaurants and retailers",
      "Event, fundraiser and alumni gear"],
     ["long-branch", "oceanport", "eatontown", "ocean-township"]),
    ("millstone-upper-freehold", "Millstone & Upper Freehold",
     "Western Monmouth County - Millstone, Upper Freehold and Allentown - is farm and horse country with wineries, nurseries and open space. We embroider and print for farms, equestrian businesses, 4-H and school groups, and the trades that work out here.",
     ["Embroidered caps, vests and jackets for farms, nurseries and barns",
      "4-H, scouting and school club shirts",
      "Workwear for excavation, tree-service and landscaping companies",
      "Winery, farm-market and agritourism merch"],
     ["manalapan", "freehold", "howell", "marlboro"]),
    ("atlantic-highlands", "Atlantic Highlands & Highlands",
     "Atlantic Highlands and Highlands sit at the gateway to Sandy Hook, with a busy marina, a ferry to the city, and waterfront restaurants and seafood spots. We make custom apparel for marine businesses, restaurants, charter boats and community groups on the bayshore.",
     ["Staff shirts for waterfront restaurants and seafood markets",
      "Charter boat, marina and yacht-club apparel",
      "Shirts for clam fests, regattas and local events",
      "School and rec team gear"],
     ["middletown", "rumson-fair-haven", "hazlet", "red-bank"]),
]
TOWN_BY_SLUG = {t[0]: t for t in TOWNS}


def town_file(slug):
    return f"custom-apparel-{slug}-nj.html"


def town_href(slug):
    return href(town_file(slug))


# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=True)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def href(path):
    """Site-relative link for a page file: clean URLs, no .html (see vercel.json)."""
    name, _, frag = path.partition("#")
    name = "/" if name == "index.html" else name[:-5] if name.endswith(".html") else name
    return name + ("#" + frag if frag else "")


def url(path):
    return BASE + "/" + ("" if path == "index.html" else href(path))


def business_ld():
    b = BUSINESS
    address = {"@type": "PostalAddress", "addressRegion": b["region"], "addressCountry": "US"}
    if b["street"]:
        address["streetAddress"] = b["street"]
    if b["city"]:
        address["addressLocality"] = b["city"]
    if b["zip"]:
        address["postalCode"] = b["zip"]
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": BASE + "/#business",
        "name": b["name"],
        "legalName": b["legal"],
        "url": BASE + "/",
        "logo": BASE + "/images/logo/newlogo.png",
        "image": BASE + "/images/hero/hero.jpg",
        "description": "Custom apparel shop in Monmouth County, New Jersey offering screen printing, embroidery, and custom t-shirts, hoodies, hats and workwear for businesses, teams, schools and events.",
        "foundingDate": b["founded"],
        "founder": {"@type": "Person", "name": b["founder"], "jobTitle": b["founder_title"]},
        "address": address,
        "areaServed": [{"@type": "AdministrativeArea", "name": "Monmouth County, New Jersey"}]
                      + [{"@type": "City", "name": f"{n.replace(' & ', ' and ')}, NJ"} for _, n, *_ in TOWNS],
        "knowsAbout": ["Screen printing", "Custom embroidery", "Custom t-shirts", "Direct-to-garment printing",
                       "Team uniforms", "Corporate apparel", "Custom hats", "Workwear"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Custom apparel services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": url(u)}}
                for n, u in [("Screen printing", "screen-printing"), ("Custom embroidery", "embroidery"),
                             ("Custom t-shirts", "custom-t-shirts"), ("Custom apparel catalog", "products.html")]
            ],
        },
    }
    data["openingHoursSpecification"] = [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "08:00", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "16:00"},
    ]
    if b["phone"]:
        data["telephone"] = b["phone"]
    if b["email"]:
        data["email"] = b["email"]
    return data


def breadcrumb_ld(trail):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url(path)}
            for i, (name, path) in enumerate(trail)
        ],
    }


def service_ld(name, path, area, description):
    return {
        "@context": "https://schema.org", "@type": "Service",
        "name": name, "serviceType": name, "url": url(path), "description": description,
        "provider": {"@id": BASE + "/#business"},
        "areaServed": area,
    }


def faq_ld(pairs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs
        ],
    }


def seo_block(path, title, desc, schemas, image="images/hero/hero.jpg"):
    lines = [
        "<!-- seo:start (generated by tools/build_seo.py) -->",
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(desc)}">',
        f'<link rel="canonical" href="{url(path)}">',
        '<meta name="robots" content="index,follow,max-image-preview:large">',
        '<meta name="geo.region" content="US-NJ">',
        '<meta name="geo.placename" content="Monmouth County, New Jersey">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{esc(BUSINESS["name"])}">',
        '<meta property="og:locale" content="en_US">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url(path)}">',
        f'<meta property="og:image" content="{BASE}/{image}">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<link rel="icon" href="/favicon.ico" sizes="48x48">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
    ] + [ld(s) for s in schemas] + ["<!-- seo:end -->"]
    return "\n".join(lines)


FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Archivo:wght@400;500;600;700;800'
         '&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">')


def page(path, title, desc, schemas, body, scripts=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{seo_block(path, title, desc, schemas)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
<link rel="stylesheet" href="css/styles.css?v={ASSET_V}">
</head>
<body>
<div id="site-header"></div>
{body}
<div id="site-footer"></div>
<script src="js/main.js?v={ASSET_V}"></script>
{scripts}</body>
</html>
"""


def gallery():
    src = (ROOT / "js/products-data.js").read_text()
    items = re.findall(r'\{ f:"([^"]+)", cat:"[^"]+", cap:"([^"]+)" \}', src)
    return [(f, cap) for f, cap in items if (ROOT / f"images/products/{f}.jpg").exists()]


def accordion(pairs):
    rows = "".join(
        f'\n      <div class="acc-item"><button class="acc-head">{esc(q)}<span class="chev">▾</span></button>'
        f'<div class="acc-body"><div class="acc-body-inner">{a}</div></div></div>'
        for q, a in pairs)
    return f'<div class="accordion">{rows}\n    </div>'


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def cta(heading, text):
    return f"""
<section class="band-mesh cta-band">
  <div class="container">
    <span class="eyebrow" style="background:rgba(255,255,255,.15);color:#fff">Ready when you are</span>
    <h2>{heading}</h2>
    <p class="lead" style="color:#cfe0ee;max-width:52ch;margin:0 auto 10px">{text}</p>
    <div class="mt3">
      <a class="btn btn-accent btn-lg" href="quote">Get a Free Quote</a>
      <a class="btn btn-ghost btn-lg" href="products">Browse Products</a>
    </div>
  </div>
</section>
"""


SERVICE_CARDS = [
    ("printer", "Screen Printing", "Bold, durable prints that get more affordable per shirt as the order grows.", "screen-printing"),
    ("thread", "Custom Embroidery", "Stitched logos for polos, hats, jackets and bags with a premium finish.", "embroidery"),
    ("shirt", "Custom T-Shirts", "Tees for teams, events and businesses, from one-offs to hundreds.", "custom-t-shirts"),
    ("cap", "Hats &amp; Caps", "Truckers, snapbacks and beanies, embroidered or patched.", "products/hats"),
    ("jacket", "Hoodies &amp; Outerwear", "Hoodies, crews, quarter-zips and jackets for crews and fans.", "products/hoodies"),
    ("target", "Team &amp; Spirit Wear", "Uniforms, warmups and fan gear with names and numbers.", "use-cases/sports"),
]


def service_grid():
    cards = "".join(
        f'\n      <a class="card reveal" style="padding:26px" href="{href}"><div style="font-size:2rem"><span data-icon="{icon}"></span></div>'
        f'<h3 class="mt2">{name}</h3><p class="muted mb0">{text}</p></a>'
        for icon, name, text, href in SERVICE_CARDS)
    return f'<div class="grid g3">{cards}\n    </div>'


def town_chips(slugs, light=False):
    return "".join(
        f'\n      <a class="chip" href="{town_href(s)}">{esc(TOWN_BY_SLUG[s][1])}</a>' for s in slugs)


# ---------------------------------------------------------------- town pages
def build_town(i, town, photos):
    slug, name, intro, orders, nearby = town
    path = town_file(slug)
    plural = " & " in name
    title = f"Custom T-Shirts & Embroidery in {name}, NJ | Meadow Prints"
    desc = (f"Screen printing, embroidery and custom t-shirts for {name}, NJ businesses, teams and schools. "
            f"Local Monmouth County shop. Free proof in 24 hours.")
    photo, cap = photos[(i * 5) % len(photos)]
    faqs = [
        (f"Do you serve {name}, NJ?",
         f"Yes. Meadow Prints &amp; Embroidery is based in Monmouth County and works with businesses, teams, schools and families in {name} "
         f"every week. Send us your idea through the <a href=\"quote\">quote form</a> and a real person replies within one business day."),
        (f"How fast can I get custom shirts in {name}?",
         f"Most {name} orders are finished about two weeks after you approve your proof, and rush production is available in as few as 3 days. "
         f"You get a digital proof within 24 hours, and nothing is printed until you approve it."),
        (f"Is there a minimum order for {name} customers?",
         "Many products have no minimum - you can order a single embroidered polo or a handful of tees. "
         "Screen printing is most cost-effective at 12 pieces and up, and we will always point you to the best method for your quantity."),
    ]
    schemas = [
        service_ld(f"Custom apparel, screen printing and embroidery in {name}, NJ", path,
                   {"@type": "City", "name": f"{name.replace(' & ', ' and ')}, New Jersey"}, desc),
        breadcrumb_ld([("Home", "index.html"), ("Service Areas", "service-areas.html"), (name, path)]),
        faq_ld([(q, strip_tags(a)) for q, a in faqs]),
    ]
    order_items = "".join(f"\n        <li>{esc(o)}</li>" for o in orders)
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / <a href="service-areas">Service Areas</a> / {esc(name)}</div>
    <span class="eyebrow">Serving {esc(name)}, NJ</span>
    <h1 style="font-size:clamp(1.9rem,4.4vw,3.2rem)">Custom T-Shirts, Screen Printing &amp; Embroidery in {esc(name)}, NJ</h1>
    <p class="lead" style="max-width:68ch">{esc(intro)}</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="quote">Get a Free Quote</a>
      <a class="btn btn-outline btn-lg" href="products">Browse Products</a>
    </div>
  </div>
</section>

<section class="container split">
  <div class="reveal">
    <span class="eyebrow">Popular in {esc(name)}</span>
    <h2>What {esc(name)} {"order" if plural else "orders"} most</h2>
    <p class="lead">Every order is made for you, with a free proof before anything is printed or stitched.</p>
    <ul class="checklist mt2">{order_items}
    </ul>
    <div class="hero-cta"><a class="btn btn-primary" href="quote">Start My {esc(name.split(" & ")[0])} Order</a><a class="btn btn-outline" href="gallery">See Our Work</a></div>
  </div>
  <div class="card reveal" style="padding:0;overflow:hidden"><img src="images/products/{photo}.jpg?v=8" alt="{esc(cap)} by Meadow Prints &amp; Embroidery, serving {esc(name)}, NJ" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3"></div>
</section>

<section class="band-cream">
  <div class="container">
    <div class="center" style="max-width:660px;margin:0 auto 44px">
      <span class="eyebrow">What we do</span>
      <h2>Printing &amp; embroidery services for {esc(name)}</h2>
      <p class="lead">One Monmouth County shop for printed tees, stitched logos and everything in between.</p>
    </div>
    {service_grid()}
  </div>
</section>

<section>
  <div class="container">
    <div class="center" style="max-width:620px;margin:0 auto 44px">
      <span class="eyebrow">How it works</span>
      <h2>From idea to your door in {esc(name)}</h2>
    </div>
    <div class="grid g3">
      <div class="step reveal"><div class="step-num">1</div><h3>Tell us what you need</h3><p>Pick a product, give us a quantity, and email us your logo or idea. No logo yet? We will help you design one.</p></div>
      <div class="step reveal"><div class="step-num">2</div><h3>Approve your proof</h3><p>You get a digital proof within 24 hours showing exact colors, sizing and placement.</p></div>
      <div class="step reveal"><div class="step-num">3</div><h3>We make and deliver it</h3><p>Your order is printed or embroidered in-house, then packed and sent to you in {esc(name)}.</p></div>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="container" style="max-width:820px">
    <h2 style="margin-bottom:20px">{esc(name)} custom apparel FAQ</h2>
    {accordion(faqs)}
  </div>
</section>

<section>
  <div class="container center">
    <span class="eyebrow">Nearby</span>
    <h2>Also serving towns near {esc(name)}</h2>
    <div class="chip-row mt3" style="justify-content:center">{town_chips(nearby)}
      <a class="chip" href="service-areas">All Monmouth County towns</a>
    </div>
  </div>
</section>
{cta(f"Ready to outfit your {esc(name.split(' & ')[0])} crew?", "Tell us about your project and a real Meadow specialist will reply within one business day.")}"""
    (ROOT / path).write_text(page(path, title, desc, schemas, body))
    return path


# ---------------------------------------------------------------- hub + service pages
def build_hub():
    path = "service-areas.html"
    title = "Custom Apparel Service Areas in Monmouth County, NJ | Meadow Prints"
    desc = ("Screen printing, embroidery and custom apparel across Monmouth County, NJ: "
            "Freehold, Red Bank, Middletown, Howell, Marlboro, Asbury Park and more.")
    cards = "".join(
        f'\n      <a class="card reveal" style="padding:22px" href="{town_href(slug)}"><h3 style="margin-bottom:6px">{esc(name)}</h3>'
        f'<p class="muted mb0" style="font-size:.92rem">Custom t-shirts, screen printing &amp; embroidery in {esc(name)}, NJ</p></a>'
        for slug, name, *_ in TOWNS)
    schemas = [business_ld(), breadcrumb_ld([("Home", "index.html"), ("Service Areas", path)])]
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / Service Areas</div>
    <span class="eyebrow">Monmouth County, NJ</span>
    <h1>Custom apparel for every town in Monmouth County</h1>
    <p class="lead" style="max-width:66ch">Meadow Prints &amp; Embroidery is a Monmouth County custom apparel shop. We screen print, embroider and deliver custom t-shirts, hoodies, hats and workwear for businesses, teams, schools and events from the bayshore to the beaches to the farms out west.</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="quote">Get a Free Quote</a>
      <a class="btn btn-outline btn-lg" href="products">Browse Products</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="center" style="max-width:640px;margin:0 auto 44px">
      <span class="eyebrow">Find your town</span>
      <h2>Towns we serve</h2>
      <p class="lead">Pick your town to see what local businesses, teams and schools order most.</p>
    </div>
    <div class="grid g3">{cards}
    </div>
    <p class="center muted mt4" style="max-width:60ch;margin-left:auto;margin-right:auto">Don't see your town? We work with customers in every Monmouth County municipality, and we ship orders outside the county too. <a href="quote">Ask us for a quote</a>.</p>
  </div>
</section>

<section class="band-cream">
  <div class="container">
    <div class="center" style="max-width:640px;margin:0 auto 44px">
      <span class="eyebrow">What we do</span>
      <h2>Services across Monmouth County</h2>
    </div>
    {service_grid()}
  </div>
</section>
{cta("Let's make something worth wearing", "Tell us your town, your quantity and your idea - we will take it from there.")}"""
    (ROOT / path).write_text(page(path, title, desc, schemas, body))
    return path


def build_service(path, name, title, desc, eyebrow, h1, lead, best_for, photo, photo_alt, sections, faqs):
    schemas = [
        service_ld(f"{name} in Monmouth County, NJ", path,
                   {"@type": "AdministrativeArea", "name": "Monmouth County, New Jersey"}, desc),
        breadcrumb_ld([("Home", "index.html"), (name, path)]),
        faq_ld([(q, strip_tags(a)) for q, a in faqs]),
    ]
    best = "".join(f"\n        <li>{b}</li>" for b in best_for)
    cards = "".join(
        f'\n      <div class="card reveal" style="padding:26px"><h3>{h}</h3><p class="muted mb0">{p}</p></div>' for h, p in sections)
    top = [t[0] for t in TOWNS[:12]]
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / {name}</div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead" style="max-width:66ch">{lead}</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="quote">Get a Free Quote</a>
      <a class="btn btn-outline btn-lg" href="products">Browse Products</a>
    </div>
  </div>
</section>

<section class="container split">
  <div class="reveal">
    <span class="eyebrow">Best for</span>
    <h2>When {name.lower()} is the right call</h2>
    <ul class="checklist mt2">{best}
    </ul>
    <div class="hero-cta"><a class="btn btn-primary" href="quote">Price My Order</a><a class="btn btn-outline" href="gallery">See Our Work</a></div>
  </div>
  <div class="card reveal" style="padding:0;overflow:hidden"><img src="images/products/{photo}.jpg?v=8" alt="{photo_alt}" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3"></div>
</section>

<section class="band-cream">
  <div class="container">
    <div class="center" style="max-width:640px;margin:0 auto 44px">
      <span class="eyebrow">The details</span>
      <h2>What you get with Meadow</h2>
    </div>
    <div class="grid g3">{cards}
    </div>
  </div>
</section>

<section>
  <div class="container" style="max-width:820px">
    <h2 style="margin-bottom:20px">{name} FAQ</h2>
    {accordion(faqs)}
  </div>
</section>

<section class="band-cream">
  <div class="container center">
    <span class="eyebrow">Monmouth County, NJ</span>
    <h2>{name} near you</h2>
    <div class="chip-row mt3" style="justify-content:center">{town_chips(top)}
      <a class="chip" href="service-areas">All service areas</a>
    </div>
  </div>
</section>
{cta("Have a project in mind?", "Send us your logo and quantity and we will reply within one business day with a quote and a mockup.")}"""
    (ROOT / path).write_text(page(path, title, desc, schemas, body))
    return path


def build_services():
    out = []
    out.append(build_service(
        "screen-printing.html", "Screen Printing",
        "Screen Printing in Monmouth County, NJ | Meadow Prints & Embroidery",
        "Custom screen printing in Monmouth County, NJ for t-shirts, hoodies and team gear. Bold, durable prints and a free proof in 24 hours. Get a free quote.",
        "Monmouth County, NJ",
        "Screen printing in Monmouth County, NJ",
        "Screen printing is the classic way to put a bold, long-lasting design on a shirt. We print tees, hoodies, tanks and team gear for Monmouth County businesses, schools, leagues and events, and the more you order the less each piece costs.",
        ["Orders of 12 pieces or more, where it gives the best value per shirt",
         "Bold logos and designs with a few solid colors",
         "Team shirts, event tees, staff uniforms and fundraisers",
         "Prints that need to hold up to heavy wear and washing"],
        "IMG_0835", "Run of screen-printed t-shirts by Meadow Prints &amp; Embroidery in Monmouth County, NJ",
        [("Free art review", "Send a logo, a sketch or a rough idea. We clean it up and get it print-ready at no charge."),
         ("Proof in 24 hours", "You see exact colors, size and placement on a digital proof before anything is printed."),
         ("Printed in-house", "Your order is printed by our own team, so quality and timing stay in our hands."),
         ("Front, back and sleeve prints", "Left chest, full front, full back and sleeve locations can be combined on one garment."),
         ("Mix sizes freely", "Adult and youth sizes can go in the same order, and we confirm print sizing for each."),
         ("Rush when you need it", "Standard turnaround is about two weeks after proof approval, with rush options in as few as 3 days.")],
        [("How many shirts do I need to order for screen printing?",
          "Screen printing is most cost-effective at 12 pieces and up. For smaller quantities we will usually recommend direct-to-garment printing or embroidery instead."),
         ("How much does screen printing cost?",
          "It depends on the garment, the number of ink colors and the quantity - the more you order, the lower the price per piece. <a href=\"quote\">Request a free quote</a> and we will price your exact project."),
         ("Can you screen print on hoodies and other garments?",
          "Yes. We print tees, long sleeves, tanks, hoodies, crewneck sweatshirts and many bags and performance fabrics."),
         ("Do you serve my town?",
          "We work with customers across Monmouth County, NJ, including Freehold, Red Bank, Middletown, Howell, Marlboro, Manalapan and the Shore towns. See our <a href=\"service-areas\">service areas</a>.")]))
    out.append(build_service(
        "custom-t-shirts.html", "Custom T-Shirts",
        "Custom T-Shirts in Monmouth County, NJ | Meadow Prints & Embroidery",
        "Custom t-shirts in Monmouth County, NJ for teams, businesses, schools, events and families. Screen printed, DTG or embroidered with free design help. Get a free quote.",
        "Monmouth County, NJ",
        "Custom t-shirts in Monmouth County, NJ",
        "Need shirts for a team, a staff, a fundraiser or a family reunion? We make custom t-shirts for groups all over Monmouth County - one shirt or five hundred - and help you pick the right blank and print method for your budget.",
        ["Business and staff shirts with your logo",
         "Team, club, class and spirit wear",
         "Events: 5Ks, fundraisers, reunions, bachelorette trips and birthdays",
         "Merch for shops, bands, gyms and restaurants"],
        "IMG_9817", "Folded two-color custom t-shirts by Meadow Prints &amp; Embroidery in Monmouth County, NJ",
        [("Hundreds of blanks", "Heavy cotton, soft ringspun, tri-blend and performance tees from brands like Gildan, Bella+Canvas and Next Level."),
         ("The right print method", "Screen printing for bigger runs, direct-to-garment for full-color or small orders, embroidery for a premium look."),
         ("Free design help", "No designer? Tell us the idea and we will mock it up for you."),
         ("No minimum on many items", "Order a handful or a few hundred. We will tell you where the price breaks are."),
         ("Adult and youth sizes", "Mix sizes and even shirt colors in a single order."),
         ("100% happiness guarantee", "If something is not right with your order, we reprint it or refund it.")],
        [("What is the minimum order for custom t-shirts?",
          "Many products have no minimum. Screen printing is best at 12 pieces and up; smaller orders are usually done with direct-to-garment printing."),
         ("How long do custom t-shirts take?",
          "About two weeks after you approve your proof. Rush production is available in as few as 3 days."),
         ("Can you help with my design?",
          "Yes. Every order includes a free art review, and we can create a mockup from a rough idea or an existing logo."),
         ("Where are you located?",
          "Meadow Prints &amp; Embroidery is based in Monmouth County, New Jersey, and serves the whole county. See our <a href=\"service-areas\">service areas</a>.")]))
    return out


# ---------------------------------------------------------------- existing pages
EXISTING = {
    "index.html": (
        "Custom T-Shirts, Screen Printing & Embroidery | Monmouth County, NJ",
        "Monmouth County, NJ custom apparel shop: screen printing, embroidery and custom t-shirts, hoodies and hats for teams, businesses and events. Free quote.",
        None),
    "products.html": (
        "Custom Apparel Catalog: Tees, Hoodies & Hats | Monmouth County, NJ",
        "Browse customizable t-shirts, hoodies, hats, bags, polos and promo items from Meadow Prints & Embroidery in Monmouth County, NJ. Add your logo and get a free proof.",
        "Products"),
    "product.html": (
        "Custom Apparel Product Details | Meadow Prints & Embroidery",
        "Request a quote on this custom product from Meadow Prints & Embroidery in Monmouth County, NJ. Tell us your quantity and email us your logo - mockup back within 24 hours.",
        None),
    "embroidery.html": (
        "Custom Embroidery in Monmouth County, NJ | Meadow Prints & Embroidery",
        "Custom embroidery in Monmouth County, NJ for polos, hats, jackets and bags. Premium stitched logos, free digitizing, no rush fees. Get a free embroidery quote.",
        "Custom Embroidery"),
    "use-cases.html": (
        "Custom Apparel for Businesses, Schools & Teams | Monmouth County, NJ",
        "Custom shirts and gear for Monmouth County businesses, schools, clubs, events, families and sports teams. Free design help from Meadow Prints & Embroidery.",
        "Use Cases"),
    "gallery.html": (
        "Our Work - Custom Apparel & Embroidery Portfolio | Monmouth County, NJ",
        "Real custom t-shirts, embroidered hats, polos and workwear made by Meadow Prints & Embroidery for Monmouth County, NJ businesses, teams and crews.",
        "Our Work"),
    "how-it-works.html": (
        "How Ordering Custom Apparel Works | Meadow Prints, Monmouth County",
        "How ordering custom printed and embroidered apparel works at Meadow Prints & Embroidery in Monmouth County, NJ: request, free proof, production and delivery.",
        "How It Works"),
    "about.html": (
        "About Meadow Prints & Embroidery | Monmouth County, NJ",
        "Meadow Prints & Embroidery is an independent custom apparel shop in Monmouth County, NJ, founded in 2024 by Roger Padalec. Screen printing and embroidery done with care.",
        "About"),
    "faq.html": (
        "Custom Apparel FAQ - Minimums, Turnaround & Artwork | Meadow Prints",
        "Answers about ordering custom apparel from Meadow Prints & Embroidery in Monmouth County, NJ: minimums, quotes, turnaround, artwork, embroidery and shipping.",
        "Help & FAQ"),
    "quote.html": (
        "Get a Free Custom Apparel Quote | Monmouth County, NJ | Meadow Prints",
        "Get a free, no-pressure quote for custom printed or embroidered apparel in Monmouth County, NJ. A Meadow specialist replies within one business day.",
        "Get a Quote"),
    "contact.html": (
        "Contact Meadow Prints & Embroidery | Monmouth County, NJ",
        "Contact Meadow Prints & Embroidery, a custom apparel, screen printing and embroidery shop serving all of Monmouth County, NJ. We reply within one business day.",
        "Contact"),
}


def faq_pairs_from_page(src):
    pairs = re.findall(r'<button class="acc-head">(.*?)<span class="chev">.*?<div class="acc-body-inner">(.*?)</div></div></div>', src, re.S)
    return [(strip_tags(q), strip_tags(a)) for q, a in pairs]


def patch_existing():
    for path, (title, desc, crumb) in EXISTING.items():
        f = ROOT / path
        src = f.read_text()
        schemas = []
        if path in ("index.html", "contact.html", "about.html"):
            schemas.append(business_ld())
        if path == "index.html":
            schemas.append({"@context": "https://schema.org", "@type": "WebSite", "name": BUSINESS["name"], "url": BASE + "/"})
        if crumb:
            schemas.append(breadcrumb_ld([("Home", "index.html"), (crumb, path)]))
        if path == "embroidery.html":
            schemas.append(service_ld("Custom embroidery in Monmouth County, NJ", path,
                                      {"@type": "AdministrativeArea", "name": "Monmouth County, New Jersey"}, desc))
        if path == "faq.html":
            schemas.append(faq_ld(faq_pairs_from_page(src)))
        block = seo_block(path, title, desc, schemas)
        if "<!-- seo:start" in src:
            src = re.sub(r"<!-- seo:start.*?<!-- seo:end -->", lambda m: block, src, count=1, flags=re.S)
        else:
            src, n = re.subn(r"<title>.*?</title>\s*<meta name=\"description\"[^>]*>", lambda m: block, src, count=1, flags=re.S)
            assert n == 1, path
        src = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">', FONTS, src, count=1)
        src = re.sub(r"((?:css|js)/[a-z-]+\.(?:css|js)\?v=)\d+", lambda m: m.group(1) + ASSET_V, src)
        f.write_text(src)


# ---------------------------------------------------------------- sitemap / robots
def build_sitemap(extra):
    pages = [("index.html", "1.0"), ("products.html", "0.8"), ("embroidery.html", "0.9"), ("screen-printing.html", "0.9"),
             ("custom-t-shirts.html", "0.9"), ("service-areas.html", "0.9"), ("use-cases.html", "0.7"), ("gallery.html", "0.7"),
             ("how-it-works.html", "0.6"), ("about.html", "0.6"), ("faq.html", "0.6"), ("quote.html", "0.8"), ("contact.html", "0.7")]
    pages += [(p, "0.8") for p in extra]
    pages += [(f"products/{c}", "0.7") for c in ("t-shirts", "polos", "hoodies", "jackets", "woven-shirts", "pants-shorts", "hats", "bags", "promo")]
    rows = "".join(
        f"\n  <url><loc>{url(p)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for p, pr in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{rows}\n</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")


def main():
    photos = gallery()
    towns = [build_town(i, t, photos) for i, t in enumerate(TOWNS)]
    build_hub()
    build_services()
    patch_existing()
    build_sitemap(towns)
    print(f"built {len(towns)} town pages, hub, 2 service pages; patched {len(EXISTING)} existing pages")


if __name__ == "__main__":
    main()
