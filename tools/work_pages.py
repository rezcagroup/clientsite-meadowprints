"""Work apparel pages for trades and blue-collar companies. Called from build_seo.py.

Writes:
  work-apparel.html                 hub: company uniforms and work shirts
  work-apparel/<industry>.html      one page per trade
  bulk-t-shirts.html                bulk / large-run t-shirt orders
"""
import shutil

# slug, name (page label), crew noun, intro, what they order, tips, featured styles, one trade-specific FAQ
INDUSTRIES = [
    ("landscaping", "Landscaping & Lawn Care", "landscaping crews",
     "Landscaping crews work in the sun, the rain and the mud from spring cleanups to snow season, and a matching shirt is how customers know your truck from the next one on the street. We print and embroider crew shirts, hi-vis tops, hoodies and hats for landscapers and lawn care companies all over Monmouth County.",
     ["Pocket tees and sun-protective long sleeves with your logo on the chest and a big back print",
      "Hi-vis and ANSI safety shirts and sweatshirts for road-side work",
      "Hoodies, quarter-zips and insulated vests for fall cleanups and plowing",
      "Mesh-back trucker caps and beanies for the whole crew"],
     ["Pick a light, breathable tee for summer and a heavier hoodie for spring and fall - most crews order both.",
      "A large back print with your company name and phone number turns every shirt into a moving ad.",
      "Order a few extra in the most common sizes so new hires are covered mid-season."],
     ["CTK87", "ST420", "PC61P", "CT106868", "CT104987", "CTK121", "C112", "CT104597"],
     ("Do you have sun-protective shirts for summer crews?",
      "Yes. We carry UV-protective and moisture-wicking tees and long sleeves from Carhartt and Sport-Tek that take a printed or embroidered logo.")),
    ("construction", "Construction & General Contractors", "construction crews",
     "On a job site, a branded crew looks organized, is easy to spot and reflects well on the contractor. We outfit general contractors, builders and site crews with durable work tees, hi-vis safety apparel, hoodies, jackets and caps - printed or embroidered, in the quantities a crew actually needs.",
     ["Heavyweight pocket tees and long sleeves for everyday site work",
      "ANSI Class 2 and Class 3 hi-vis vests, hoodies and jackets",
      "Duck jackets, vests and bib overalls with an embroidered logo",
      "Hard-hat-friendly beanies and caps for every season"],
     ["Embroider outerwear and print tees: embroidery holds up best on heavy fabrics, printing is the best value on large tee runs.",
      "Keep your logo off reflective striping on safety apparel - we place it on the chest or a solid panel.",
      "Tall sizes are available on many work tees and jackets for taller crew members."],
     ["CTK87", "CTTK87", "5300", "CT104988", "CT106171", "CT106694", "CT103828", "CT104597"],
     ("Can you put our logo on ANSI hi-vis safety apparel?",
      "Yes. We decorate ANSI Class 2 and Class 3 vests, hoodies and jackets and keep the logo off the reflective striping. If your site has specific rules, tell us on your quote and we will plan around them.")),
    ("hvac", "HVAC", "HVAC technicians",
     "HVAC techs spend the day inside customers' homes, so a clean, professional uniform builds trust before anyone says a word. We make embroidered polos, work shirts, quarter-zips and jackets for heating and air conditioning companies, plus printed tees for install crews.",
     ["Embroidered polos and twill work shirts for service techs",
      "Moisture-wicking tees for attic and summer install work",
      "Quarter-zips, soft shells and vests for winter service calls",
      "Caps and beanies with the company logo"],
     ["Service techs going into homes look best in embroidered polos or button-up work shirts; install crews can wear printed tees.",
      "Add the tech's first name above the pocket - customers remember a name.",
      "Choose stain-resistant, easy-care fabrics for techs working around equipment."],
     ["S663", "W400", "CT106880", "ST272", "CT105294", "CT106438", "CT106433", "CT106687"],
     ("Can you add each technician's name to their shirt?",
      "Yes. We can embroider individual names on polos, work shirts and jackets. Just send us the name list with sizes when you approve your proof.")),
    ("plumbing", "Plumbing", "plumbers",
     "Plumbers are judged the moment they knock on the door. We help plumbing companies show up looking professional with embroidered polos and work shirts, durable tees, hoodies and jackets that hold up to the work and the wash.",
     ["Embroidered polos and short sleeve work shirts for service calls",
      "Heavyweight pocket tees for new construction and rough-in crews",
      "Rain-resistant soft shells and hoodies for cold-weather jobs",
      "Caps and beanies to match"],
     ["Dark colors like navy, charcoal and black hide the wear of the job between washes.",
      "Put your phone number on the back of tees and jackets - it's free advertising at every job.",
      "Embroidered names on service shirts help customers feel comfortable letting your techs in."],
     ["S664", "CT106880", "CTK87", "PC54P", "CT100615", "CT106438", "CT105298", "CTA205"],
     ("What colors work best for plumbing uniforms?",
      "Navy, charcoal, black and dark gray are the most popular because they stay looking clean. We will show your logo on your color choices on the proof.")),
    ("electrical", "Electricians", "electricians",
     "Electrical contractors need uniforms that look sharp in a homeowner's kitchen and hold up on a commercial job site. We print and embroider work shirts, tees, hi-vis apparel and outerwear for electricians and electrical contractors across Monmouth County.",
     ["Embroidered polos and twill shirts for residential service",
      "Pocket tees and long sleeves for commercial and new-construction crews",
      "Hi-vis safety tops for road and utility work",
      "Jackets, vests and caps for year-round crews"],
     ["Ask us about fabric content - some electricians prefer cotton-rich garments over synthetics; we can source what your safety program calls for.",
      "Match service-tech polos and crew tees in the same color so the whole company looks unified.",
      "Long sleeve options are popular for crews that want arm coverage."],
     ["S663", "CT106880", "CTK126", "PC61LSP", "CT106171", "SRJ754", "CT106433", "C836"],
     ("Do you carry flame-resistant (FR) clothing?",
      "FR garments are specialty items. Tell us what your safety program requires and we will tell you what we can source and decorate before you order.")),
    ("roofing", "Roofing & Siding", "roofing crews",
     "Roofing and siding crews are up high and in full view of the neighborhood, so matching shirts double as advertising on every job. We make bright, durable crew tees, long sleeves, hoodies and hats for roofers and exterior contractors.",
     ["Bright, high-contrast crew tees that stand out from the street",
      "Sun-protective long sleeves for hot roof days",
      "Hi-vis shirts and hoodies for street-side work",
      "Hoodies, beanies and jackets for cold-season jobs"],
     ["Use a big, simple back print - it's readable from the street and the yard sign does the rest.",
      "Bright colors like safety green, orange or gold make crews easy to spot on a roof.",
      "Order a summer tee and a long sleeve so the crew is covered all year."],
     ["5000", "ST420", "CT106972", "CT104987", "PC78H", "CT104597", "C112", "CT106652"],
     ("Can you print our company name big on the back?",
      "Yes. Full-back prints are one of the most popular options for roofing crews. We will size it on your proof so it is readable from a distance.")),
    ("painting", "Painting Contractors", "painting crews",
     "Painters go through shirts fast, so they need a good-looking uniform that's affordable to reorder. We print and embroider painter's whites, crew tees, hoodies and caps for interior and exterior painting contractors.",
     ["White and light-colored crew tees, the classic painter's look",
      "Long sleeves and hoodies for exterior work in cooler months",
      "Embroidered polos for estimators and owners meeting customers",
      "Caps and beanies to finish the crew look"],
     ["Value tees like Gildan and Port & Company keep reorders affordable when shirts get worn hard.",
      "Give estimators an embroidered polo and the crew printed tees in the same color family.",
      "Keep your logo file on record with us so reorders are quick."],
     ["5000", "PC54", "8300", "5400", "PC61LSP", "K469", "18500", "C813"],
     ("Can you do all-white painter shirts?",
      "Yes. White tees and long sleeves are some of our most common painter orders, and we print your logo in any color that reads well on white.")),
    ("pool-service", "Pool Service & Installation", "pool crews",
     "Pool service and installation companies spend the season in backyards around the Shore, so crew shirts need to handle sun, water and chemicals and still look professional. We make sun-protective tees, polos, hats and outerwear for pool builders and service routes.",
     ["UV-protective, quick-drying tees and long sleeves",
      "Embroidered polos for service techs and sales staff",
      "Lightweight jackets and hoodies for opening and closing season",
      "Bucket hats, caps and visors for full-sun days"],
     ["Moisture-wicking fabrics dry quickly after a splash and stay comfortable in the heat.",
      "Light colors stay cooler in direct sun; we will check your logo reads well on them.",
      "Give route techs an embroidered polo for customer-facing visits."],
     ["ST420", "ST272", "CT106868", "CT106899", "K469", "CT106438", "C112", "CT106687"],
     ("Which shirts hold up best for pool crews?",
      "Performance and UV-protective polyester tees from Sport-Tek and Carhartt Force dry fast and handle sun better than plain cotton. We print or embroider your logo on either.")),
    ("auto-repair", "Auto Repair & Body Shops", "shop crews",
     "Auto repair shops, body shops and dealership service departments need uniforms that hold up to grease, look professional at the counter and are easy to reorder. We embroider mechanic shirts, polos and jackets and print shop tees and hoodies.",
     ["Embroidered twill work shirts with name patches or names stitched on",
      "Dark shop tees and hoodies that hide grease",
      "Service-writer polos and quarter-zips for the front counter",
      "Mechanic soft shell jackets and caps"],
     ["Dark gray, navy and black hide shop wear; save lighter colors for front-counter staff.",
      "Stitch each tech's name on the chest for a classic shop look.",
      "Snag-resistant and stain-release fabrics last longer in the shop."],
     ["S663", "S500T", "J417", "CT106880", "PC54", "18500", "K469", "CT105298"],
     ("Can you do classic mechanic-style shirts with names?",
      "Yes. We embroider names and your shop logo on twill work shirts and jackets for the classic garage look.")),
    ("trucking", "Trucking, Moving & Delivery", "drivers and movers",
     "Drivers, movers and delivery crews are the face of the company at every stop. We outfit trucking, moving and logistics companies with matching tees, polos, hi-vis tops, hoodies and jackets so customers know exactly who is at the door.",
     ["Matching crew tees for movers and helpers",
      "Embroidered polos for drivers making customer deliveries",
      "Hi-vis shirts and vests for yards, docks and roadside work",
      "Jackets, hoodies and beanies for winter routes"],
     ["Movers go through shirts fast - order plenty of the common sizes and keep a reorder on file.",
      "A back print with your company name is visible while crews are carrying and loading.",
      "Give drivers a polo or work shirt for a sharper look at customer stops."],
     ["PC54", "5000", "CTK87", "K469", "CT106171", "CT104987", "CT106438", "CT104597"],
     ("We hire seasonal help - how do reorders work?",
      "We keep your artwork and the details of your last order on file, so you can reorder a handful of shirts in new sizes any time without starting over.")),
    ("tree-service", "Tree Service & Arborists", "tree crews",
     "Tree crews work in tough conditions and need gear that's visible, durable and comfortable to climb in. We print and embroider hi-vis tees, long sleeves, hoodies, jackets and beanies for tree service and arborist companies.",
     ["Hi-vis and bright crew tees so ground crews are easy to see",
      "Long sleeves and hoodies for brush and cold-weather work",
      "Insulated jackets and vests for winter storm cleanup",
      "Beanies and caps that fit under helmets"],
     ["Bright colors and hi-vis options help keep ground crews visible around equipment and traffic.",
      "Stretchy, durable fabrics like Carhartt Force move with climbers.",
      "Embroider jackets and hats; print tees for value on larger crews."],
     ["CT104987", "CT106171", "CT106656", "CT106652", "CT100615", "CT106543", "CT104597", "C836"],
     ("Do you have hi-vis tees for ground crews?",
      "Yes. We carry hi-vis and ANSI-rated tops and outerwear from Carhartt and Port Authority, plus bright safety colors on standard tees.")),
    ("cleaning", "Cleaning & Power Washing", "cleaning crews",
     "Cleaning and power washing companies work in customers' homes and businesses, so a clean, branded uniform is part of the service. We make matching tees, polos, hoodies and hats for residential cleaners, commercial janitorial crews and power washing companies.",
     ["Matching tees and polos for residential and commercial cleaners",
      "Quick-drying performance shirts for power washing crews",
      "Hoodies and quarter-zips for early-morning and winter work",
      "Caps and visors with the company logo"],
     ["Polos give cleaners in customers' homes a professional, trustworthy look.",
      "Quick-dry performance fabrics are a good fit for power washing crews.",
      "Put your website or phone number on the back for easy referrals."],
     ["K469", "ST272", "PC54", "5000", "CT106880", "18500", "CT105294", "C112"],
     ("Do you make uniforms for small cleaning teams?",
      "Yes. Many of our products have no minimum, so a team of three can get matching polos or tees, and you can add more later.")),
    ("marine", "Marine, Boatyards & Marinas", "marine crews",
     "From the marinas on the Shrewsbury and Navesink to the boatyards in Brielle and the bayshore, marine businesses need apparel that handles sun, salt and wind. We embroider and print crew shirts, polos, jackets and hats for marinas, boatyards, charter boats and dock crews.",
     ["Sun-protective long sleeves and performance tees for dock crews",
      "Embroidered polos and quarter-zips for marina and sales staff",
      "Rain and soft shell jackets for spring and fall launches",
      "Caps and visors for full-sun days on the water"],
     ["UV-protective long sleeves are a favorite for crews working on the docks all day.",
      "Embroidery holds up well to salt air and repeated washing on polos and jackets.",
      "Retail-style tees and hats with your marina logo also sell well in the ship store."],
     ["CT106972", "ST420", "CT106899", "K469", "CT105294", "CT106438", "C112", "CT106687"],
     ("Can you make shirts we can sell in our ship store?",
      "Yes. We print and embroider retail-quality tees, hoodies and hats with your logo that you can sell as well as wear.")),
]


def featured(B, by_style, styles):
    import catalog_pages as C
    items = [by_style[s] for s in styles if s in by_style]
    return "".join("\n      " + C.card(B, p) for p in items)


def with_base(html):
    return html.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                        '<meta name="viewport" content="width=device-width, initial-scale=1">\n<base href="/">', 1)


def industry_chips(B, exclude=None):
    return "".join(f'\n      <a class="chip" href="work-apparel/{slug}">{B.esc(name)}</a>'
                   for slug, name, *_ in INDUSTRIES if slug != exclude)


HOW_IT_WORKS = """
<section>
  <div class="container">
    <div class="center" style="max-width:640px;margin:0 auto 44px">
      <span class="eyebrow">Company orders</span>
      <h2>How crew and company orders work</h2>
    </div>
    <div class="grid g4">
      <div class="step reveal"><div class="step-num">1</div><h3>Send your logo &amp; headcount</h3><p>Tell us the garments, colors and roughly how many people. Email your logo to <a href="mailto:meadowprintsembroidery@gmail.com">meadowprintsembroidery@gmail.com</a> - any file works.</p></div>
      <div class="step reveal"><div class="step-num">2</div><h3>Get a quote &amp; proof</h3><p>You get a quote and a digital proof within 24 hours. Volume pricing kicks in automatically on larger orders.</p></div>
      <div class="step reveal"><div class="step-num">3</div><h3>Send your size run</h3><p>Send sizes (and names, if you want them stitched) as a simple list. Mixed sizes and tall sizes are fine.</p></div>
      <div class="step reveal"><div class="step-num">4</div><h3>Reorder any time</h3><p>We keep your logo and order details on file, so restocking for new hires is one call or email.</p></div>
    </div>
  </div>
</section>
"""


def company_faqs(name):
    who = name.lower()
    return [
        (f"Do you give bulk pricing for {who} companies?",
         "Yes. Pricing drops as quantity goes up, and every quote includes free art setup. Screen printing gives the best value on runs of 12 shirts or more."),
        ("How fast can you turn around a crew order?",
         "About two weeks after you approve your proof. Rush production is available in as few as 3 business days, and if you give us a hard deadline we will make sure it arrives on time."),
        ("Can we mix sizes, styles and decoration in one order?",
         "Yes. Mix sizes freely, including tall and bigger sizes where available, and combine printed tees with embroidered polos, jackets and hats in one order."),
    ]


def build(B):
    import catalog_pages as C
    root = B.ROOT
    products = C.load_products(root)
    by_style = {p.get("style"): p for p in products if p.get("style")}
    paths = []
    shutil.rmtree(root / "work-apparel", ignore_errors=True)
    (root / "work-apparel").mkdir()
    towns = "".join(f'\n      <a class="chip" href="{B.town_href(t[0])}">{B.esc(t[1])}</a>' for t in B.TOWNS[:16])

    # ---- one page per trade
    for slug, name, crew, intro, orders, tips, styles, faq in INDUSTRIES:
        path = f"work-apparel/{slug}.html"
        title = f"Custom {name} Shirts & Uniforms | Monmouth County, NJ"
        desc = (f"Custom work shirts, uniforms, hi-vis apparel and hats for {crew} in Monmouth County, NJ. "
                f"Bulk pricing, logo kept on file for reorders, free proof in 24 hours.")
        faqs = company_faqs(name) + [faq]
        schemas = [
            B.service_ld(f"Custom {name.lower()} uniforms and work shirts", path,
                         {"@type": "AdministrativeArea", "name": "Monmouth County, New Jersey"}, desc),
            B.breadcrumb_ld([("Home", "index.html"), ("Work Apparel", "work-apparel.html"), (name, path)]),
            B.faq_ld([(q, B.strip_tags(a)) for q, a in faqs]),
        ]
        order_items = "".join(f"\n        <li>{B.esc(o)}</li>" for o in orders)
        tip_items = "".join(f"\n        <li>{B.esc(t)}</li>" for t in tips)
        body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / <a href="work-apparel">Work Apparel</a> / {B.esc(name)}</div>
    <span class="eyebrow">Work apparel for {B.esc(crew)}</span>
    <h1 style="font-size:clamp(1.9rem,4.4vw,3.2rem)">{B.esc(name)} shirts &amp; uniforms</h1>
    <p class="lead" style="max-width:68ch">{B.esc(intro)}</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="quote">Get a Crew Quote</a>
      <a class="btn btn-outline btn-lg" href="tel:+17327636078">Call (732) 763-6078</a>
    </div>
  </div>
</section>

<section class="container split">
  <div class="reveal">
    <span class="eyebrow">What {B.esc(crew)} order</span>
    <h2>Built for the work</h2>
    <ul class="checklist mt2">{order_items}
    </ul>
  </div>
  <div class="card reveal" style="padding:28px">
    <h3>Tips for {B.esc(name.lower())} uniforms</h3>
    <ul class="checklist mt2">{tip_items}
    </ul>
  </div>
</section>

<section class="band-cream">
  <div class="container">
    <div class="center" style="max-width:660px;margin:0 auto 36px">
      <span class="eyebrow">Popular picks</span>
      <h2>Work apparel {B.esc(crew)} order most</h2>
      <p class="lead">Every item can be printed or embroidered with your logo. <a href="products">Browse 2,100+ more styles</a>.</p>
    </div>
    <div class="grid g4">{featured(B, by_style, styles)}
    </div>
  </div>
</section>
{HOW_IT_WORKS}
<section class="band-cream">
  <div class="container" style="max-width:820px">
    <h2 style="margin-bottom:20px">{B.esc(name)} uniform FAQ</h2>
    {B.accordion(faqs)}
  </div>
</section>

<section>
  <div class="container center">
    <span class="eyebrow">More trades we outfit</span>
    <h2>Uniforms for every trade</h2>
    <div class="chip-row mt3" style="justify-content:center">{industry_chips(B, slug)}
      <a class="chip active" href="work-apparel">All work apparel</a>
    </div>
    <h3 class="mt4" style="margin-bottom:14px">Serving {B.esc(crew)} across Monmouth County</h3>
    <div class="chip-row" style="justify-content:center">{towns}
      <a class="chip" href="service-areas">All towns</a>
    </div>
  </div>
</section>
{B.cta(f"Outfit your {B.esc(crew)}", "Send us your logo and headcount and we'll reply within one business day with a quote and a proof.")}"""
        (root / path).write_text(with_base(B.page(path, title, desc, schemas, body)))
        paths.append(path)

    # ---- hub
    path = "work-apparel.html"
    title = "Custom Work Shirts & Company Uniforms | Monmouth County, NJ"
    desc = ("Custom work shirts, company uniforms and hi-vis apparel for contractors and trades in Monmouth County, NJ. "
            "Bulk pricing, Carhartt and more, logo kept on file for reorders.")
    faqs = [
        ("What's the minimum order for company shirts?",
         "Many products have no minimum. Screen-printed tees are most cost-effective at 12 pieces and up, and the price per shirt keeps dropping on larger crew orders."),
        ("Do you keep our logo on file?",
         "Yes. We keep your artwork and embroidery file after your first order, so reorders for new hires are fast and match what the crew already wears."),
        ("Can you embroider names on work shirts?",
         "Yes. We can stitch individual names on polos, work shirts and jackets. Send the name and size list when you approve your proof."),
        ("Do you carry Carhartt and hi-vis safety apparel?",
         "Yes. We decorate Carhartt workwear and ANSI Class 2 and Class 3 hi-vis vests, hoodies and jackets, along with work tees and twill shirts from Port Authority, Port & Company and Gildan."),
        ("Can you ship to our office or job site?",
         "Yes. We can ship to your shop, office or job site, and split an order between multiple addresses."),
    ]
    cards = "".join(
        f'\n      <a class="card reveal" style="padding:22px" href="work-apparel/{slug}"><h3 style="margin-bottom:6px">{B.esc(name)}</h3>'
        f'<p class="muted mb0" style="font-size:.92rem">Shirts, hi-vis, outerwear and hats for {B.esc(crew)}.</p></a>'
        for slug, name, crew, *_ in INDUSTRIES)
    hub_styles = ["CTK87", "PC61P", "5000", "CT104987", "CT106171", "S663", "CTK121", "CT104597", "C112", "CT106433", "ST420", "CT106880"]
    schemas = [
        B.service_ld("Custom work shirts and company uniforms", path, {"@type": "AdministrativeArea", "name": "Monmouth County, New Jersey"}, desc),
        B.breadcrumb_ld([("Home", "index.html"), ("Work Apparel", path)]),
        B.faq_ld([(q, B.strip_tags(a)) for q, a in faqs]),
    ]
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / Work Apparel</div>
    <span class="eyebrow">For contractors, trades &amp; crews</span>
    <h1>Work shirts &amp; uniforms for crews that work for a living</h1>
    <p class="lead" style="max-width:68ch">Meadow Prints &amp; Embroidery outfits contractors, service companies and trades across Monmouth County with custom work tees, hi-vis safety apparel, Carhartt workwear, polos, jackets and hats. Big crew orders are what we do best - bulk pricing, your logo kept on file, and reorders as easy as a phone call.</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="quote">Get a Crew Quote</a>
      <a class="btn btn-outline btn-lg" href="tel:+17327636078">Call (732) 763-6078</a>
    </div>
    <div class="hero-trust">
      <div><strong>Bulk</strong><span>volume pricing</span></div>
      <div><strong>24-hr</strong><span>proof turnaround</span></div>
      <div><strong>On file</strong><span>logo for reorders</span></div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="center" style="max-width:640px;margin:0 auto 44px">
      <span class="eyebrow">Pick your trade</span>
      <h2>Uniforms for every trade</h2>
      <p class="lead">See what crews in your line of work order most, with tips for getting it right.</p>
    </div>
    <div class="grid g3">{cards}
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">Why crews order from us</span>
      <h2>Made for big orders and busy owners</h2>
      <ul class="checklist mt2">
        <li><strong>Bulk pricing</strong> - the per-shirt price drops as your order grows</li>
        <li><strong>Logo on file</strong> - reorder for new hires without starting over</li>
        <li><strong>Hi-vis &amp; ANSI safety apparel</strong> - vests, hoodies and jackets for road and site work</li>
        <li><strong>Carhartt and workwear brands</strong> crews actually want to wear</li>
        <li><strong>Names stitched on</strong> - individual names on polos, work shirts and jackets</li>
        <li><strong>Mixed sizes, tall sizes and split shipping</strong> to the shop or job site</li>
      </ul>
      <div class="hero-cta"><a class="btn btn-primary" href="bulk-t-shirts">Bulk T-Shirt Orders</a><a class="btn btn-outline" href="brands/carhartt">Shop Carhartt</a></div>
    </div>
    <div class="card reveal" style="padding:0;overflow:hidden"><img src="images/products/IMG_8845.jpg?v=8" alt="Hi-vis safety shirts printed by Meadow Prints &amp; Embroidery for a Monmouth County crew" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3"></div>
  </div>
</section>

<section>
  <div class="container">
    <div class="center" style="max-width:660px;margin:0 auto 36px">
      <span class="eyebrow">Crew favorites</span>
      <h2>Popular work apparel</h2>
      <p class="lead">Printed or embroidered with your logo. <a href="products">See all 2,100+ styles</a>.</p>
    </div>
    <div class="grid g4">{featured(B, by_style, hub_styles)}
    </div>
  </div>
</section>
{HOW_IT_WORKS}
<section class="band-cream">
  <div class="container" style="max-width:820px">
    <h2 style="margin-bottom:20px">Company &amp; crew order FAQ</h2>
    {B.accordion(faqs)}
  </div>
</section>
{B.cta("Ready to outfit your crew?", "Send us your logo and headcount and we'll reply within one business day with a quote and a proof.")}"""
    (root / path).write_text(B.page(path, title, desc, schemas, body))
    paths.insert(0, path)

    # ---- bulk t-shirts
    path = "bulk-t-shirts.html"
    title = "Bulk Custom T-Shirts in Monmouth County, NJ | Meadow Prints"
    desc = ("Bulk custom t-shirts screen printed in Monmouth County, NJ for companies, crews, schools and events. "
            "Volume pricing on 50 to 1,000+ shirts, free proof in 24 hours.")
    faqs = [
        ("How many shirts count as a bulk order?",
         "There's no magic number - pricing improves as the quantity grows, and screen printing is the most cost-effective method from about 12 shirts up. Crew and company orders of 50, 100 or several hundred shirts get the best per-shirt price."),
        ("What's the best shirt for a large order?",
         "Value tees like Gildan Heavy Cotton and Port & Company Core Cotton keep big runs affordable. For crews, pocket tees and Carhartt workwear tees are popular upgrades."),
        ("Can a bulk order have different sizes and colors?",
         "Yes. Mix sizes freely, including youth, tall and larger sizes where available. Different shirt colors work too, as long as the ink colors read well on each - we check that on the proof."),
        ("Can you split a large order between locations?",
         "Yes. We can split-ship one order to multiple addresses, like your shop and individual job sites."),
        ("How long does a bulk order take?",
         "About two weeks after you approve your proof. Rush production is available in as few as 3 business days."),
    ]
    schemas = [
        B.service_ld("Bulk custom t-shirt printing", path, {"@type": "AdministrativeArea", "name": "Monmouth County, New Jersey"}, desc),
        B.breadcrumb_ld([("Home", "index.html"), ("Bulk T-Shirts", path)]),
        B.faq_ld([(q, B.strip_tags(a)) for q, a in faqs]),
    ]
    bulk_styles = ["5000", "PC54", "PC61", "2000", "8300", "CTK87", "PC61P", "5300"]
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumbs"><a href="/">Home</a> / Bulk T-Shirts</div>
    <span class="eyebrow">Large orders</span>
    <h1>Bulk custom t-shirts</h1>
    <p class="lead" style="max-width:66ch">Need 50, 200 or 1,000 shirts? We screen print bulk t-shirt orders for companies, contractors, schools and events across Monmouth County, with volume pricing, a free proof in 24 hours and the option to split delivery between locations.</p>
    <div class="hero-cta">
      <a class="btn btn-primary btn-lg" href="quote">Get a Bulk Quote</a>
      <a class="btn btn-outline btn-lg" href="tel:+17327636078">Call (732) 763-6078</a>
    </div>
  </div>
</section>

<section class="container split">
  <div class="reveal">
    <span class="eyebrow">Why order in bulk</span>
    <h2>The more you order, the less each shirt costs</h2>
    <ul class="checklist mt2">
      <li>Screen printing setup is spread across the whole run, so the per-shirt price drops as quantity grows</li>
      <li>Free art review and setup on every order</li>
      <li>Mixed sizes and colors in one order</li>
      <li>Your artwork kept on file for fast reorders</li>
      <li>Split shipping to multiple addresses</li>
    </ul>
    <div class="hero-cta"><a class="btn btn-primary" href="quote">Price My Order</a><a class="btn btn-outline" href="screen-printing">About Screen Printing</a></div>
  </div>
  <div class="card reveal" style="padding:0;overflow:hidden"><img src="images/products/IMG_0835.jpg?v=8" alt="Bulk run of screen-printed t-shirts by Meadow Prints &amp; Embroidery in Monmouth County, NJ" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block;aspect-ratio:4/3"></div>
</section>

<section class="band-cream">
  <div class="container">
    <div class="center" style="max-width:660px;margin:0 auto 36px">
      <span class="eyebrow">Best for big runs</span>
      <h2>Popular bulk t-shirts</h2>
    </div>
    <div class="grid g4">{featured(B, by_style, bulk_styles)}
    </div>
  </div>
</section>

<section>
  <div class="container" style="max-width:820px">
    <h2 style="margin-bottom:20px">Bulk t-shirt FAQ</h2>
    {B.accordion(faqs)}
  </div>
</section>

<section class="band-cream">
  <div class="container center">
    <span class="eyebrow">For companies</span>
    <h2>Bulk shirts for your trade</h2>
    <div class="chip-row mt3" style="justify-content:center">{industry_chips(B)}
      <a class="chip active" href="work-apparel">All work apparel</a>
    </div>
  </div>
</section>
{B.cta("Get a bulk quote", "Tell us the shirt, the quantity and your logo and we'll reply within one business day.")}"""
    (root / path).write_text(B.page(path, title, desc, schemas, body))
    paths.insert(1, path)
    return paths
