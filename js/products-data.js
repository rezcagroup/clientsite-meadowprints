/* Shared product catalog + portfolio for Meadow Prints & Embroidery
   Blank product images: official SanMar dealer photos in images/blanks/<STYLE>.jpg
   Real decorated work photos: images/products/<file>.jpg */
const IMGDIR = "images/products/";
const BLANKDIR = "images/blanks/";

/* style = SanMar style number (blank image + brand);  work = our decorated photo */
window.MEADOW_PRODUCTS = [
  { id:"meadow-soft-tee", name:"Heavy Cotton Tee", brand:"Gildan 5000", style:"5000", cat:"tshirts", price:"9.98", rating:5, reviews:2140, tag:"Best Seller", best:true, color:"#26400f", work:"IMG_9997", blurb:"The workhorse tee - 100% heavy cotton that takes bold screen prints beautifully." },
  { id:"heritage-ring-tee", name:"Cotton Crew Tee", brand:"Next Level 3600", style:"NL3600", cat:"tshirts", price:"11.40", rating:5, reviews:980, best:true, color:"#243b63", work:"IMG_0835", blurb:"Fitted ringspun tee with a smooth, retail-soft hand and a clean print surface." },
  { id:"tri-blend-tee", name:"Tri-Blend Tee", brand:"Bella+Canvas 3413", style:"BC3413", cat:"tshirts", price:"13.20", rating:4, reviews:640, tag:"Softest", color:"#1c1c1c", work:"IMG_9996", blurb:"Heathered, ultra-soft tri-blend - a premium tee that shows off big prints." },
  { id:"performance-tee", name:"Performance Tee", brand:"Sport-Tek ST272", style:"ST272", cat:"activewear", price:"13.40", rating:5, reviews:520, best:true, color:"#7fc6ea", work:"IMG_0773", blurb:"Moisture-wicking performance tee for teams on the move - great for prints." },
  { id:"pullover-hoodie", name:"Pullover Hoodie", brand:"Gildan 18500", style:"18500", cat:"hoodies", price:"22.50", rating:5, reviews:1510, tag:"Best Seller", best:true, color:"#164a2b", work:"IMG_9629", blurb:"Heavyweight fleece pullover with a roomy hood and front pouch pocket." },
  { id:"zip-hoodie", name:"Soft Shell Jacket", brand:"Port Authority J317", style:"J317", cat:"hoodies", price:"46.90", rating:5, reviews:430, best:true, color:"#1c1c1c", work:"IMG_9895", blurb:"Wind- and water-resistant full-zip softshell that embroiders like a dream." },
  { id:"crew-sweatshirt", name:"Crewneck Sweatshirt", brand:"Gildan 18000", style:"18000", cat:"hoodies", price:"19.80", rating:4, reviews:360, color:"#e7ddc6", work:"IMG_0138", blurb:"Classic brushed-fleece crewneck - comfortable and clean for printed branding." },
  { id:"structured-cap", name:"Trucker Snapback Cap", brand:"Richardson 112", style:"C112", cat:"hats", price:"16.75", rating:5, reviews:610, best:true, color:"#1c1c1c", work:"IMG_0280", blurb:"The industry-favorite 112 - structured front, mesh back, perfect for embroidery or patches." },
  { id:"trucker-cap", name:"Mesh-Back Trucker", brand:"Sport-Tek STC26", style:"STC26", cat:"hats", price:"15.90", rating:5, reviews:280, best:true, color:"#4a5850", work:"IMG_0768", blurb:"Retro mesh-back trucker with a comfortable snapback closure." },
  { id:"beanie", name:"Fine-Knit Beanie", brand:"Port & Co. CP90", style:"CP90", cat:"hats", price:"14.20", rating:5, reviews:190, color:"#243b63", work:"IMG_0126", blurb:"Cozy cuffed knit beanie with a crisp surface for embroidered logos and patches." },
  { id:"cotton-tote", name:"Access Backpack", brand:"Port Authority BG615", style:"BG615", cat:"bags", price:"38.20", rating:5, reviews:140, tag:"Premium", best:true, color:"#4a5850", work:"IMG_0961", blurb:"Durable everyday backpack with a padded laptop sleeve and clean embroidery panel." },
  { id:"drawstring-bag", name:"Drawstring Cinch Pack", brand:"Port & Co. BG85", style:"BG85", cat:"bags", price:"6.50", rating:4, reviews:210, color:"#2f9bd6", work:null, blurb:"Lightweight cinch pack - an easy, affordable giveaway for events." },
  { id:"duffel", name:"Improved Duffel", brand:"Port Authority BG99", style:"BG99", cat:"bags", price:"28.00", rating:5, reviews:120, color:"#164a2b", work:null, blurb:"Roomy, rugged duffel - embroider a team name or monogram on the end panel." },
  { id:"embroidered-polo", name:"Silk Touch Polo", brand:"Sport-Tek K500", style:"K500", cat:"activewear", price:"18.60", rating:5, reviews:820, tag:"Pro Look", best:true, color:"#1e6a3d", work:"IMG_0036", blurb:"The go-to embroidered polo - soft, wrinkle-resistant, and endlessly professional." },
  { id:"quarter-zip", name:"1/4-Zip Pullover", brand:"Sport-Tek ST253", style:"ST253", cat:"activewear", price:"28.40", rating:5, reviews:300, color:"#4a5850", work:"IMG_9969", blurb:"Polished 1/4-zip mid-layer with a smooth left-chest embroidery area." },
  { id:"apron", name:"Full-Length Apron", brand:"Port Authority A700", style:"A700", cat:"promo", price:"16.00", rating:5, reviews:260, color:"#ef6b53", work:"IMG_0374", blurb:"Café, shop, and event-ready apron - print or stitch your brand front and center." },
  { id:"rally-towel", name:"Rally Towel", brand:"Port & Co. PT38", style:"PT38", cat:"promo", price:"5.40", rating:5, reviews:410, tag:"Popular", color:"#f5a623", work:null, blurb:"Spirit-day rally towel - print your logo or team name for games, events, and giveaways." },
  { id:"stadium-blanket", name:"Sweatshirt Blanket", brand:"Port Authority BP35", style:"BP35", cat:"promo", price:"22.80", rating:5, reviews:190, color:"#6b4e9e", work:null, blurb:"Cozy fleece-back sweatshirt blanket - a premium embroidered gift for clients and staff." },
  { id:"golf-towel", name:"Microfiber Golf Towel", brand:"Port Authority TW540", style:"TW540", cat:"promo", price:"9.20", rating:5, reviews:150, color:"#2f9bd6", work:null, blurb:"Grommeted microfiber golf towel - a clean canvas for embroidered logos at outings and events." },
  { id:"youth-tee", name:"Youth Heavy Cotton Tee", brand:"Gildan 5000B", style:"5000B", cat:"tshirts", price:"8.90", rating:5, reviews:340, color:"#ef6b53", work:"IMG_0096", blurb:"The kid-sized version of our best-selling heavy cotton tee." },
  { id:"long-sleeve", name:"Long-Sleeve Cotton Tee", brand:"Gildan 2400", style:"2400", cat:"tshirts", price:"13.60", rating:4, reviews:230, color:"#ef6b53", work:"IMG_0093", blurb:"Cooler-weather staple with room for a full-size back graphic." },
  { id:"tank-top", name:"Jersey Tank", brand:"Bella+Canvas 3480", style:"BC3480", cat:"activewear", price:"11.90", rating:4, reviews:150, color:"#ffffff", work:"IMG_9985", blurb:"Soft, relaxed jersey tank - a warm-weather and event-day essential." },
  { id:"work-jacket", name:"Challenger Jacket", brand:"Port Authority J754", style:"J754", cat:"hoodies", price:"39.00", rating:5, reviews:90, tag:"Premium", color:"#1c1c1c", work:"IMG_0251", blurb:"Rugged, warm shell jacket built for embroidered company branding." },
  { id:"visor", name:"Camo Mesh Trucker", brand:"Sport-Tek STC26 Camo", style:"C874", cat:"hats", price:"15.40", rating:5, reviews:70, color:"#4a5850", work:"IMG_0536", blurb:"Camo-front mesh trucker that makes embroidered logos pop." },
];

/* Portfolio - real Meadow work, used on the homepage & gallery */
window.MEADOW_GALLERY = [
  { f:"IMG_0036", cat:"activewear", cap:"Embroidered polo" },
  { f:"IMG_0308", cat:"activewear", cap:"Embroidered polo, flag sleeves" },
  { f:"IMG_0363", cat:"activewear", cap:"Embroidered performance polo" },
  { f:"IMG_9969", cat:"activewear", cap:"Embroidered quarter-zip" },
  { f:"IMG_0773", cat:"activewear", cap:"Performance sun hoodie" },
  { f:"IMG_0771", cat:"activewear", cap:"Full-back printed sun hoodie" },
  { f:"IMG_9997", cat:"tshirts", cap:"Screen-printed tee" },
  { f:"IMG_0093", cat:"tshirts", cap:"Back-print tee" },
  { f:"IMG_0096", cat:"tshirts", cap:"Left-chest print tee" },
  { f:"IMG_0835", cat:"tshirts", cap:"Screen-printed tee run" },
  { f:"IMG_0334", cat:"tshirts", cap:"V-neck logo tee" },
  { f:"IMG_9985", cat:"tshirts", cap:"Printed tank top" },
  { f:"IMG_9996", cat:"tshirts", cap:"Back-print statement tee" },
  { f:"IMG_9817", cat:"tshirts", cap:"Two-color folded tees" },
  { f:"IMG_0138", cat:"hoodies", cap:"Printed crew sweatshirt" },
  { f:"IMG_9629", cat:"hoodies", cap:"Hi-vis embroidered hoodie" },
  { f:"IMG_9630", cat:"hoodies", cap:"Reflective safety hoodie" },
  { f:"IMG_9895", cat:"hoodies", cap:"Embroidered softshell jacket" },
  { f:"IMG_0251", cat:"hoodies", cap:"Embroidered quilted jacket" },
  { f:"IMG_9778", cat:"hoodies", cap:"Personalized softshell vest" },
  { f:"IMG_9779", cat:"hoodies", cap:"Vest back embroidery" },
  { f:"IMG_0280", cat:"hats", cap:"3D embroidered snapback" },
  { f:"IMG_0342", cat:"hats", cap:"Embroidered trucker" },
  { f:"IMG_0536", cat:"hats", cap:"Embroidered mesh trucker" },
  { f:"IMG_0617", cat:"hats", cap:"Patch camo trucker" },
  { f:"IMG_0768", cat:"hats", cap:"Embroidered cap" },
  { f:"IMG_0769", cat:"hats", cap:"Flag-sleeve trucker" },
  { f:"IMG_1011", cat:"hats", cap:"Embroidered trucker run" },
  { f:"IMG_0126", cat:"hats", cap:"Embroidered beanie" },
  { f:"IMG_9690", cat:"hats", cap:"Cap & beanie set" },
  { f:"IMG_0374", cat:"promo", cap:"Printed apron & cap set" },
  { f:"IMG_0961", cat:"bags", cap:"Embroidered backpack" },
  { f:"IMG_9689", cat:"tshirts", cap:"Full team merch set" },
  { f:"IMG_0410", cat:"hats", cap:"Embroidered camo cap" },
  { f:"IMG_0770", cat:"hats", cap:"Embroidered cap back" },
  { f:"IMG_0839", cat:"tshirts", cap:"Screen-printed tee, back" },
  { f:"IMG_9633", cat:"hats", cap:"Embroidered team set" },
  { f:"IMG_9897", cat:"hoodies", cap:"Embroidered vest detail" },
  { f:"IMG_9175", cat:"bags", cap:"Embroidered school backpacks" },
  { f:"IMG_9174", cat:"bags", cap:"Embroidered backpack" },
  { f:"IMG_8794", cat:"promo", cap:"Embroidered apron" },
  { f:"IMG_8840", cat:"hoodies", cap:"Hi-vis quarter-zip hoodie" },
  { f:"IMG_8841", cat:"hoodies", cap:"Hi-vis hooded shirt" },
  { f:"IMG_8845", cat:"hoodies", cap:"Hi-vis safety shirts" },
  { f:"IMG_8888", cat:"activewear", cap:"Embroidered Nike quarter-zips" },
  { f:"IMG_8892", cat:"hats", cap:"Embroidered team caps" },
  { f:"IMG_8936", cat:"hats", cap:"Patch knit beanie" },
  { f:"IMG_8937", cat:"hats", cap:"Embroidered beanie" },
  { f:"IMG_8938", cat:"tshirts", cap:"Printed athletics tank" },
  { f:"IMG_9045", cat:"hoodies", cap:"Embroidered crewneck" },
  { f:"IMG_9046", cat:"tshirts", cap:"Left-chest logo tee" },
  { f:"IMG_9053", cat:"hoodies", cap:"Embroidered school hoodie" },
  { f:"IMG_9054", cat:"hoodies", cap:"Printed company hoodie" },
  { f:"IMG_9102", cat:"hoodies", cap:"Printed hi-vis jacket" },
  { f:"IMG_9103", cat:"hoodies", cap:"Printed safety jacket" },
  { f:"IMG_9104", cat:"hoodies", cap:"Hi-vis work pants" },
  { f:"IMG_9105", cat:"hoodies", cap:"Hi-vis jacket with flag" },
];

/* Category spec templates so every product page is fully populated */
const CATEGORY_SPECS = {
  tshirts:   { label:"T-Shirts & Tees", material:"Ringspun cotton or cotton-poly blend", weight:"4.3 - 6.0 oz", sizes:"Youth XS - Adult 4XL", decoration:"Screen print, DTG, or heat transfer", care:"Machine wash cold, tumble dry low",
               features:["Soft, print-ready surface","Youth and adult sizes available","Ideal for large front or back prints","Tag-free comfort on most styles"] },
  activewear:{ label:"Polos & Performance", material:"Moisture-wicking polyester or piqué knit", weight:"3.8 - 6.1 oz", sizes:"Adult XS - 4XL, ladies' cuts available", decoration:"Embroidery or screen print", care:"Machine wash cold, hang or tumble dry low",
               features:["Wrinkle- and shrink-resistant","Snag-resistant knit","Perfect for left-chest embroidery","Professional team and staff look"] },
  hoodies:   { label:"Sweatshirts & Outerwear", material:"Cotton-poly fleece or soft-shell", weight:"7.5 - 13.0 oz", sizes:"Adult S - 4XL", decoration:"Embroidery or screen print", care:"Machine wash cold, tumble dry low",
               features:["Warm, heavyweight feel","Roomy front pocket on most styles","Premium look when embroidered","Layer-ready, relaxed fit"] },
  hats:      { label:"Hats & Caps", material:"Structured twill, trucker mesh, or knit", weight:"One size", sizes:"One size / adjustable snapback", decoration:"3D embroidery, flat embroidery, or woven patch", care:"Spot clean",
               features:["Structured or relaxed crown","Snapback or flexfit sizing","Great for 3D puff embroidery","Front, side, or back logo placement"] },
  bags:      { label:"Bags & Totes", material:"Canvas, poly, or ripstop", weight:"One size", sizes:"One size", decoration:"Embroidery or screen print", care:"Spot clean",
               features:["Durable everyday construction","Roomy branded panel","Great for events and giveaways","Monogram or full-logo ready"] },
  promo:     { label:"Promo & Accessories", material:"Varies by item", weight:"One size", sizes:"One size", decoration:"Embroidery or print", care:"Follow item label",
               features:["Crowd-pleasing giveaway","Clean branding surface","Pairs well with apparel orders","Bulk pricing available"] },
};
function getSpecs(p) { return CATEGORY_SPECS[p.cat] || CATEGORY_SPECS.tshirts; }
const COMMON_COLORS = ["#1c1c1c","#ffffff","#243b63","#26400f","#7a1f2b","#4a5850","#f5a623","#2f9bd6","#e7ddc6","#6b4e9e"];

function shirtSVG(color) {
  return `<svg viewBox="0 0 200 200" width="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <path d="M70 44l-28 16 10 24 15-6v64h66V78l15 6 10-24-28-16c-5 10-14 14-30 14s-25-4-30-14z" fill="${color}"/>
    <path d="M70 44c5 10 14 14 30 14s25-4 30-14" fill="none" stroke="rgba(0,0,0,.2)" stroke-width="2.5"/>
    <circle cx="100" cy="112" r="20" fill="rgba(255,255,255,.85)"/>
    <path d="M100 99c-6 7-2 15 0 17 2-2 6-10 0-17z" fill="${color}"/>
  </svg>`;
}

/* Category blank-garment mockups (used only when no SanMar blank is set) */
function blankSVG(shape, color) {
  const O = 'stroke="rgba(0,0,0,.28)" stroke-width="2" fill="' + color + '"';
  const wrap = inner => `<svg viewBox="0 0 200 200" width="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${inner}</svg>`;
  switch (shape) {
    case "mug": return wrap(`<rect x="66" y="72" width="60" height="72" rx="8" ${O}/><path d="M126 88c22 0 22 40 0 40" fill="none" stroke="rgba(0,0,0,.4)" stroke-width="6"/>`);
    case "bottle": return wrap(`<rect x="84" y="58" width="32" height="16" rx="3" ${O}/><path d="M82 74h36v78a8 8 0 0 1-8 8H90a8 8 0 0 1-8-8z" ${O}/>`);
    case "sticker": return wrap(`<rect x="60" y="60" width="80" height="80" rx="14" ${O} transform="rotate(-6 100 100)"/><rect x="72" y="72" width="56" height="56" rx="8" fill="rgba(255,255,255,.5)" transform="rotate(-6 100 100)"/>`);
    default: return shirtSVG(color);
  }
}
const SHAPE_BY_ID = { "ceramic-mug":"mug", "water-bottle":"bottle", "sticker-pack":"sticker" };
function productMediaSVG(p) { return blankSVG(SHAPE_BY_ID[p.id] || "tee", p.color); }

/* Primary catalog image = SanMar blank if we have the style, else a mockup */
function productBlankMedia(p, cls) {
  return p.style
    ? `<img class="${cls} pc-blank" src="${BLANKDIR}${p.style}.jpg" alt="${p.brand} blank" loading="lazy">`
    : productMediaSVG(p);
}

function stars(n) { return "★★★★★".slice(0, n) + "☆☆☆☆☆".slice(0, 5 - n); }

/* Real "from" pricing (lowest 50+ tier from the Meadow price sheet).
   Returns a price string, or null for items we quote (bags, promo, etc.). */
function priceFor(p) {
  const s = (p.style || "").toUpperCase();
  const n = (p.name || "").toLowerCase();
  const c = p.cat;
  const isBeanie = /beanie|skull cap/.test(n) || ["CP90","CP91L","STC35"].includes(s);
  const isPolo = /polo/.test(n) || ["K500","K540","K420","ST650","L500","K500LS","TLK500"].includes(s);
  const isQuarterZip = /1\/4-zip|quarter-zip|quarter zip/.test(n) || ["ST253","F244"].includes(s);
  if (c === "tshirts") return "10.00";              // DTF tees, tanks, long sleeve, youth
  if (c === "hats") return isBeanie ? "12.00" : "17.00";
  if (c === "hoodies") return "20.00";              // DTF hoodie / crew / jacket / vest
  if (c === "activewear") {
    if (isPolo) return "18.00";
    if (isQuarterZip) return "20.00";
    return "10.00";                                 // performance tees & tanks
  }
  return null;                                      // bags, promo -> quote
}
function priceLabel(p) { const v = priceFor(p); return v ? `from $${v}` : "Get a quote"; }

function productCardHTML(p) {
  return `<a class="card product-card reveal" data-cat="${p.cat}" href="product.html?id=${p.id}">
    <div class="pc-media${p.style ? ' blank' : ''}">${p.tag ? `<span class="tag">${p.tag}</span>` : ""}${productBlankMedia(p, "pc-photo")}</div>
    <div class="pc-body">
      <h3>${p.name}</h3>
      ${p.brand ? `<div class="pc-brand">${p.brand}</div>` : ""}
      <div class="pc-meta"><span class="stars">${stars(p.rating)}</span> <span class="muted" style="font-size:.8rem">(${p.reviews.toLocaleString()})</span></div>
      <div class="pc-foot"><span class="price">${priceLabel(p)}</span><span class="btn btn-primary btn-sm">Request Order</span></div>
    </div>
  </a>`;
}
