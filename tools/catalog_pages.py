"""Static, crawlable pages for the catalog. Called from build_seo.py (do not run directly).

Writes:
  product/<slug>.html   one page per product, pre-filled with its name, brand, photo and structured data
  products/<cat>.html   one landing page per category
  brands/<slug>.html    one landing page per brand, plus brands.html (the brand index)

Each file is the matching hand-written template (product.html / products.html) with the
<head> SEO block and the visible headline content swapped in, so the page is readable
before any JavaScript runs. The page scripts then take over exactly as on the template.
"""
import json
import re
import shutil
import subprocess

CATS = {
    # key: (url slug, label, headline, intro)
    "tshirts": ("t-shirts", "T-Shirts", "Custom t-shirts",
                "Heavy cotton, soft ringspun, tri-blend and performance tees, screen printed or DTG printed for teams, events, staff and fundraisers across Monmouth County."),
    "activewear": ("polos", "Polos & Activewear", "Custom polos & activewear",
                   "Embroidered polos and moisture-wicking performance wear for offices, golf outings, coaches and crews. Left-chest logos are our specialty."),
    "hoodies": ("hoodies", "Hoodies & Fleece", "Custom hoodies & fleece",
                "Pullover hoodies, crewneck sweatshirts, quarter-zips and fleece, printed or embroidered for teams, schools, job sites and merch."),
    "outerwear": ("jackets", "Jackets & Vests", "Custom jackets & vests",
                  "Soft shells, rain jackets, insulated work jackets and vests with embroidered logos for crews, staff and corporate gifts."),
    "wovens": ("woven-shirts", "Woven Shirts", "Custom woven & dress shirts",
               "Oxfords, twills, easy-care dress shirts and work shirts with crisp embroidered logos for offices, restaurants and trade shows."),
    "bottoms": ("pants-shorts", "Pants & Shorts", "Custom pants & shorts",
                "Sweatpants, joggers, athletic shorts and work pants with a printed or embroidered logo to match your hoodies and tees."),
    "hats": ("hats", "Hats & Caps", "Custom hats & caps",
             "Trucker caps, snapbacks, dad hats, visors and beanies with flat or 3D puff embroidery and patches."),
    "bags": ("bags", "Bags & Totes", "Custom bags & totes",
             "Backpacks, duffels, totes, cinch packs and coolers embroidered or printed with your logo for teams, events and giveaways."),
    "promo": ("promo", "Promo & Gifts", "Custom promo items & gifts",
              "Aprons, blankets, towels, scarves and other branded extras that round out an apparel order."),
}

BRANDS = {
    "Port Authority": "Port Authority is the go-to line for corporate apparel: polos, dress shirts, soft shell jackets, caps and bags built for embroidered logos.",
    "Sport-Tek": "Sport-Tek makes team and performance wear: moisture-wicking tees, polos, quarter-zips, fleece and caps in every team color.",
    "Port & Company": "Port & Company covers the everyday basics at a great value: cotton tees, fleece hoodies and sweatpants, caps and totes.",
    "Carhartt": "Carhartt is the workwear standard: duck jackets, vests, hoodies, beanies and rugged bags that look right with an embroidered logo.",
    "District": "District offers soft, fashion-forward tees, fleece and caps that are popular for merch, events and retail-style prints.",
    "Nike": "Nike polos, quarter-zips, fleece and bags are a favorite for golf outings, corporate gifts and coaching staffs, finished with a clean embroidered logo.",
    "Bella+Canvas": "Bella+Canvas is known for premium, retail-fit tees and fleece in a huge color range, ideal for soft-hand prints and merch.",
    "The North Face": "The North Face jackets, vests, fleece and backpacks make standout company gifts and crew outerwear when embroidered with your logo.",
    "Gildan": "Gildan is the classic, budget-friendly blank for big runs: heavy cotton tees, hoodies, crewnecks and sweatpants.",
    "Richardson": "Richardson makes the trucker caps teams and brands ask for by name, including the 112, with flat, 3D puff or patch decoration.",
    "Next Level": "Next Level Apparel makes soft, modern-fit tees, tanks and fleece that print beautifully for brands, gyms and events.",
    "Comfort Colors": "Comfort Colors garment-dyed tees and sweatshirts have the washed, lived-in look popular for beach towns, colleges and retail merch.",
}


def slugify(s):
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", s.lower().replace("&", "and").replace("+", "-")))


def load_products(root):
    """Ask Node for the product list exactly as the browser sees it, including the URL slugs."""
    script = (
        'global.window=global;const fs=require("fs");'
        'require("vm").runInThisContext(fs.readFileSync("js/products-data.js","utf8")+"\\n"+fs.readFileSync("js/sanmar-catalog.js","utf8"));'
        'process.stdout.write(JSON.stringify(MEADOW_PRODUCTS.map(p=>Object.assign({},p,{slug:productSlugs().byId[p.id],mfr:productMfr(p)}))));'
    )
    out = subprocess.run(["node", "-e", script], cwd=root, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def card(B, p):
    tag = f'<span class="tag">{B.esc(p["tag"])}</span>' if p.get("tag") else ""
    img = (f'<img class="pc-photo pc-blank" src="images/blanks/{p["style"]}.jpg" alt="{B.esc(p["name"])} - {B.esc(p["brand"])}, '
           f'ready for custom embroidery or printing" loading="lazy" width="320" height="480">') if p.get("style") else ""
    return (f'<a class="card product-card reveal in" data-cat="{p["cat"]}" href="/product/{p["slug"]}">'
            f'<div class="pc-media{" blank" if p.get("style") else ""}">{tag}{img}</div>'
            f'<div class="pc-body"><h3>{B.esc(p["name"])}</h3><div class="pc-brand">{B.esc(p["brand"])}</div>'
            f'<div class="pc-foot"><span class="price">Get a quote</span><span class="btn btn-primary btn-sm">Request Order</span></div></div></a>')


def swap_head(B, src, path, title, desc, schemas, image):
    block = B.seo_block(path, title, desc, schemas, image=image)
    out, n = re.subn(r"<!-- seo:start.*?<!-- seo:end -->", lambda m: block, src, count=1, flags=re.S)
    assert n == 1, path
    return out.replace('<html lang="en">', '<html lang="en" data-static="1">', 1)


def sub1(src, pattern, repl, what):
    out, n = re.subn(pattern, lambda m: repl, src, count=1, flags=re.S)
    assert n == 1, what
    return out


def build_products(B, root, products):
    tpl = (root / "product.html").read_text()
    out_dir = root / "product"
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir()
    paths = []
    for p in products:
        path = f"product/{p['slug']}.html"
        cat_slug, cat_label = CATS[p["cat"]][0], CATS[p["cat"]][1]
        style = p.get("style") or ""
        mfr = p["mfr"]
        title = f"Custom {p['name']} - {mfr} {style} | Meadow Prints".replace("  ", " ")
        desc = (f"Get the {mfr} {p['name']}{' (' + style + ')' if style else ''} custom embroidered or printed by Meadow Prints & Embroidery "
                f"in Monmouth County, NJ. Free mockup within 24 hours.")
        image = f"images/blanks/{style}.jpg" if style else "images/hero/hero.jpg"
        schemas = [
            {"@context": "https://schema.org", "@type": "Product", "name": f"Custom {mfr} {p['name']}", "sku": style or p["id"],
             "brand": {"@type": "Brand", "name": mfr}, "category": cat_label, "image": f"{B.BASE}/{image}",
             "description": desc, "url": B.url(path)},
            B.breadcrumb_ld([("Home", "index.html"), ("Products", "products.html"), (cat_label, f"products/{cat_slug}.html"), (p["name"], path)]),
        ]
        html = swap_head(B, tpl, path, title, desc, schemas, image)
        html = sub1(html, r'<a href="products">Products</a> / <span id="crumb">Product</span>',
                    f'<a href="products">Products</a> / <a href="products/{cat_slug}">{B.esc(cat_label)}</a> / <span id="crumb">{B.esc(p["name"])}</span>', "crumb")
        hero = (f'<img class="pc-blank" src="{image}" alt="{B.esc(p["name"])} - {B.esc(p["brand"])}, ready for custom embroidery or printing" '
                f'width="320" height="480">') if style else ""
        html = sub1(html, r'<div class="pd-hero" id="hero-media"></div>', f'<div class="pd-hero" id="hero-media">{hero}</div>', "hero")
        html = sub1(html, r'<h1 id="p-name" style="margin-top:14px">.*?</h1>', f'<h1 id="p-name" style="margin-top:14px">{B.esc(p["name"])}</h1>', "h1")
        html = sub1(html, r'<div id="p-brand" class="pc-brand" style="font-size:.85rem;margin-bottom:10px"></div>',
                    f'<div id="p-brand" class="pc-brand" style="font-size:.85rem;margin-bottom:10px">Blank: {B.esc(p["brand"])}</div>', "brand")
        html = sub1(html, r'<p class="lead" id="p-blurb">.*?</p>', f'<p class="lead" id="p-blurb">{B.esc(p["blurb"])}</p>', "blurb")
        html = sub1(html, r'<p class="muted" id="p-long" style="margin-bottom:0">.*?</p>',
                    f'<p class="muted" id="p-long" style="margin-bottom:0">{B.esc(p["blurb"])} Available in a range of colors and sizes, ready for your custom print or embroidery.</p>', "long")
        (root / path).write_text(html)
        paths.append(path)
    return paths


def listing_page(B, tpl, path, title, desc, crumb_html, eyebrow, h1, lead, items, trail):
    schemas = [
        B.breadcrumb_ld(trail),
        {"@context": "https://schema.org", "@type": "ItemList", "name": h1, "numberOfItems": len(items),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": B.url(f"product/{p['slug']}.html"), "name": p["name"]}
                             for i, p in enumerate(items[:48])]},
    ]
    html = swap_head(B, tpl, path, title, desc, schemas, "images/hero/hero.jpg")
    html = sub1(html, r'<div class="breadcrumbs"><a href="/">Home</a> / Products</div>', f'<div class="breadcrumbs">{crumb_html}</div>', "crumbs")
    html = sub1(html, r'<span class="eyebrow">The catalog</span>', f'<span class="eyebrow">{B.esc(eyebrow)}</span>', "eyebrow")
    html = sub1(html, r"<h1>Custom products for every project</h1>", f"<h1>{B.esc(h1)}</h1>", "h1")
    html = sub1(html, r'<p class="lead" style="max-width:56ch">.*?</p>', f'<p class="lead" style="max-width:62ch">{B.esc(lead)}</p>', "lead")
    cards = "".join("\n      " + card(B, p) for p in items[:48])
    html = sub1(html, r'<div class="grid g4" id="catalog"></div>', f'<div class="grid g4" id="catalog">{cards}\n    </div>', "grid")
    return html


def build_listings(B, root, products):
    tpl = (root / "products.html").read_text()
    paths = []
    for d in ("products", "brands"):
        shutil.rmtree(root / d, ignore_errors=True)
        (root / d).mkdir()
    # categories
    for key, (slug, label, h1, intro) in CATS.items():
        items = [p for p in products if p["cat"] == key]
        path = f"products/{slug}.html"
        title = f"Custom {label} in Monmouth County, NJ | Meadow Prints & Embroidery"
        desc = f"{len(items)} {label.lower()} styles ready for custom printing or embroidery by Meadow Prints & Embroidery in Monmouth County, NJ. Free mockup in 24 hours."
        html = listing_page(B, tpl, path, title, desc, f'<a href="/">Home</a> / <a href="products">Products</a> / {B.esc(label)}',
                            f"{len(items)} styles", h1, intro, items,
                            [("Home", "index.html"), ("Products", "products.html"), (label, path)])
        (root / path).write_text(html)
        paths.append(path)
    # brands
    by_brand = {}
    for p in products:
        by_brand.setdefault(p["mfr"], []).append(p)
    brand_rows = []
    for name, intro in BRANDS.items():
        items = by_brand.get(name, [])
        if not items:
            continue
        path = f"brands/{slugify(name)}.html"
        h1 = f"Custom {name} apparel"
        title = f"Custom {name} Embroidery & Printing | Monmouth County, NJ"
        desc = f"{len(items)} {name} styles custom embroidered or printed with your logo by Meadow Prints & Embroidery in Monmouth County, NJ. Free mockup in 24 hours."
        html = listing_page(B, tpl, path, title, desc, f'<a href="/">Home</a> / <a href="brands">Brands</a> / {B.esc(name)}',
                            f"{len(items)} {name} styles", h1, intro + " We decorate it in-house with embroidery or printing and send a free proof first.",
                            items, [("Home", "index.html"), ("Brands", "brands.html"), (name, path)])
        (root / path).write_text(html)
        paths.append(path)
        brand_rows.append((name, slugify(name), len(items), intro))
    # brand index
    cards = "".join(
        f'\n      <a class="card reveal" style="padding:24px" href="brands/{slug}"><h3 style="margin-bottom:6px">{B.esc(name)}</h3>'
        f'<p class="muted" style="font-size:.92rem">{B.esc(intro)}</p><span class="pill-tag">{count} styles</span></a>'
        for name, slug, count, intro in brand_rows)
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / Brands</div>
    <span class="eyebrow">Brands we decorate</span>
    <h1>Name-brand apparel, customized in Monmouth County</h1>
    <p class="lead" style="max-width:66ch">Pick the brand your team already loves and we will embroider or print your logo on it. Nike, Carhartt, The North Face, Port Authority, Sport-Tek and more, all with a free proof before anything is made.</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="quote">Get a Free Quote</a>
      <a class="btn btn-outline btn-lg" href="products">Browse All Products</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="grid g3">{cards}
    </div>
    <p class="center muted mt4">Looking for a brand that is not listed? <a href="quote">Ask us to source it</a>.</p>
  </div>
</section>
{B.cta("Have a brand in mind?", "Tell us the brand, the style and your quantity and we will reply within one business day.")}"""
    (root / "brands.html").write_text(B.page(
        "brands.html", "Apparel Brands We Embroider & Print | Monmouth County, NJ",
        "Custom embroidery and printing on Nike, Carhartt, The North Face, Port Authority, Sport-Tek, Gildan and more from Meadow Prints & Embroidery in Monmouth County, NJ.",
        [B.breadcrumb_ld([("Home", "index.html"), ("Brands", "brands.html")])], body))
    paths.append("brands.html")
    return paths, brand_rows


def build(B, root):
    products = load_products(root)
    listing_paths, brand_rows = build_listings(B, root, products)
    product_paths = build_products(B, root, products)
    return {"products": product_paths, "listings": listing_paths, "brands": brand_rows, "count": len(products)}
