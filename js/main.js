/* ============================================================
   Meadow Prints & Embroidery - shared site behavior
   Injects header + footer, handles nav, cart, accordions, reveal
   ============================================================ */

const LOGO = `<img class="brand-logo" src="images/logo/newlogo-header.png?v=9" alt="Meadow Prints & Embroidery LLC" width="1420" height="1012">`;

/* Inline SVG icon set (stroke = currentColor, sized by font-size) */
const ICONS = {
  pencil: '<path d="M4 20h4L20 8l-4-4L4 16v4z"/><path d="M14 6l4 4"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
  printer:'<path d="M6 9V3h12v6"/><rect x="4" y="9" width="16" height="8" rx="1"/><path d="M8 17h8v4H8z"/>',
  truck:  '<rect x="2" y="6" width="12" height="9"/><path d="M14 9h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
  box:    '<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/>',
  thread: '<path d="M6 3v7a6 6 0 0 0 12 0V3"/><path d="M9 3h6"/><path d="M12 16v5"/><circle cx="12" cy="21" r="1.4"/>',
  palette:'<path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-1 2-2 0-1.4 1-2 2-2h1a4 4 0 0 0 4-4c0-4.4-4-8-9-8z"/><circle cx="8" cy="10" r="1"/><circle cx="12" cy="7" r="1"/><circle cx="16" cy="10" r="1"/>',
  tag:    '<path d="M3 12l9-9 9 9-9 9-9-9z"/><circle cx="9" cy="9" r="1.3"/>',
  people: '<circle cx="8" cy="9" r="3"/><circle cx="17" cy="10" r="2.4"/><path d="M3 20c0-3 2.5-5 5-5s5 2 5 5"/><path d="M15 20c0-2.4 1.4-4 3-4"/>',
  gem:    '<path d="M6 4h12l3 5-9 11L3 9z"/><path d="M3 9h18M9 4l-3 5 6 11 6-11-3-5"/>',
  leaf:   '<path d="M20 4S6 4 6 15c0 3 2 5 5 5 11 0 9-16 9-16z"/><path d="M6 20c4-8 8-10 12-11"/>',
  star:   '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
  chat:   '<path d="M4 5h16v11H9l-4 4V5z"/><path d="M8 10h8M8 13h5"/>',
  phone:  '<path d="M5 3h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
  mail:   '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 6l9 7 9-7"/>',
  pin:    '<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
  grad:   '<path d="M2 8l10-4 10 4-10 4L2 8z"/><path d="M6 10v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/>',
  heart:  '<path d="M12 20S3 14 3 8.5A4.5 4.5 0 0 1 12 6a4.5 4.5 0 0 1 9 2.5C21 14 12 20 12 20z"/>',
  target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
  building:'<rect x="5" y="3" width="14" height="18"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/>',
  paperclip:'<path d="M21 11l-8.5 8.5a5 5 0 0 1-7-7L14 4a3.5 3.5 0 0 1 5 5l-8.5 8.5a2 2 0 0 1-3-3L15 7"/>',
  file:   '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4"/>',
  bolt:   '<path d="M13 3L5 13h5l-1 8 8-11h-5z"/>',
  shirt:  '<path d="M8 4L4 6l1.5 3L8 8v12h8V8l2.5 1L20 6l-4-2c-.7 1.8-2.2 2.5-4 2.5S8.7 5.8 8 4z"/>',
  polo:   '<path d="M8 4L4 6l1.5 3L8 8v12h8V8l2.5 1L20 6l-4-2-2 2-2 2-2-2z"/><path d="M10 4l2 3 2-3"/>',
  cap:    '<path d="M4 15a8 8 0 0 1 16 0"/><path d="M12 7v8"/><path d="M20 15h2"/><path d="M4 15h16"/>',
  jacket: '<path d="M8 4L4 6v14h4V9M16 4l4 2v14h-4V9M8 4l4 3 4-3"/><path d="M12 7v13"/>',
  bag:    '<path d="M6 8h12l1 12H5L6 8z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
  gift:   '<rect x="4" y="9" width="16" height="11"/><path d="M4 9h16M12 9v11"/><path d="M12 9S9 3 7 5s5 4 5 4zM12 9s3-6 5-4-5 4-5 4z"/>',
  run:    '<circle cx="14" cy="5" r="1.6"/><path d="M12 8l-3 3 2 3-1 5M12 8l4 2 3-1M11 14l-4 1"/>',
};
function iconify(root) {
  (root || document).querySelectorAll("[data-icon]").forEach(el => {
    const p = ICONS[el.getAttribute("data-icon")];
    if (p) el.innerHTML = `<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="display:block">${p}</svg>`;
  });
}

const NAV_LINKS = [
  { label: "Products", href: "products.html", mega: [
    { icon: "", title: "T-Shirts", sub: "Soft, everyday tees", href: "products.html#tshirts" },
    { icon: "", title: "Hoodies & Fleece", sub: "Cozy custom layers", href: "products.html#hoodies" },
    { icon: "", title: "Embroidery", sub: "Polos, caps, jackets", href: "embroidery.html" },
    { icon: "", title: "Hats & Caps", sub: "Stitched or printed", href: "products.html#hats" },
    { icon: "", title: "Bags & Totes", sub: "Custom carry-alls", href: "products.html#bags" },
    { icon: "", title: "Promo & Gifts", sub: "Mugs, stickers, more", href: "products.html#promo" },
  ]},
  { label: "Use Cases", href: "use-cases.html", mega: [
    { icon: "", title: "Businesses", sub: "Branded team gear", href: "use-cases.html#business" },
    { icon: "", title: "Schools & Clubs", sub: "Spirit wear & merch", href: "use-cases.html#schools" },
    { icon: "", title: "Events", sub: "Reunions, races, parties", href: "use-cases.html#events" },
    { icon: "", title: "Fundraising", sub: "Raise money with tees", href: "fundraising.html" },
    { icon: "", title: "Family & Groups", sub: "Match the whole crew", href: "use-cases.html#family" },
    { icon: "", title: "Sports Teams", sub: "Jerseys & practice gear", href: "use-cases.html#sports" },
  ]},
  { label: "Embroidery", href: "embroidery.html" },
  { label: "Our Work", href: "gallery.html" },
  { label: "How It Works", href: "how-it-works.html" },
  { label: "Reviews", href: "reviews.html" },
];

function buildHeader() {
  const megaHTML = (items) => `<div class="dropdown">${items.map(i => `
    <a href="${i.href}"><span>${i.title}<small>${i.sub}</small></span></a>`).join("")}</div>`;

  const links = NAV_LINKS.map(l => l.mega
    ? `<div class="nav-item"><button aria-haspopup="true"><a href="${l.href}" style="all:unset;cursor:pointer">${l.label}</a> ▾</button>${megaHTML(l.mega)}</div>`
    : `<a href="${l.href}">${l.label}</a>`
  ).join("");

  return `
  <div class="topbar">Free shipping on orders over $100 · Real humans, no order minimums on many items · <a href="quote.html">Get a free quote</a></div>
  <header class="site-header">
    <div class="container-wide nav">
      <a class="brand" href="index.html" aria-label="Meadow Prints & Embroidery LLC - home">${LOGO}</a>
      <nav class="nav-links" aria-label="Primary">${links}</nav>
      <div class="nav-cta">
        <a class="btn btn-outline btn-sm" href="quote.html">Get a Quote</a>
        <a class="btn btn-accent btn-sm" href="products.html">Start an Order</a>
      </div>
      <button class="hamburger" id="hamburger" aria-label="Menu"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    </div>
  </header>
  <div class="overlay" id="overlay"></div>
  <nav class="mobile-nav" id="mobileNav" aria-label="Mobile">
    <div class="mn-head"><a class="brand" href="index.html" style="border:none">${LOGO}</a>
    <button class="icon-btn" id="closeMobile" aria-label="Close"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
    <a href="products.html">Products</a>
    <a href="products.html">Start an Order</a>
    <a href="use-cases.html">Use Cases</a>
    <a href="embroidery.html">Embroidery</a>
    <a href="gallery.html">Our Work</a>
    <a href="how-it-works.html">How It Works</a>
    <a href="fundraising.html">Fundraising</a>
    <a href="reviews.html">Reviews</a>
    <a href="about.html">About</a>
    <a href="faq.html">Help &amp; FAQ</a>
    <a href="contact.html">Contact</a>
    <a class="btn btn-primary btn-block" style="margin-top:14px" href="quote.html">Get a Free Quote</a>
  </nav>`;
}

function buildFooter() {
  const col = (title, links) => `<div><h4>${title}</h4>${links.map(([t,h]) => `<a href="${h}">${t}</a>`).join("")}</div>`;
  return `
  <footer class="site-footer">
    <div class="container-wide">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand brand-footer" href="index.html">${LOGO}</a>
          <p>Custom apparel, screen printing &amp; embroidery - designed with you, made to order, and shipped with care. <strong>Quality. Precision. Every stitch.</strong> Proudly independent since 2024.</p>
          <div class="socials">
            <a href="#" aria-label="Instagram"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
            <a href="#" aria-label="Facebook"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M14 9h3V6h-3c-2 0-3 1-3 3v2H9v3h2v6h3v-6h3l1-3h-4V9c0-.6.4-1 1-1z"/></svg></a>
            <a href="#" aria-label="TikTok"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M16 3c.3 2 1.6 3.6 3.6 4v3c-1.4 0-2.7-.4-3.6-1v6.5A5.5 5.5 0 1 1 10.5 10v3a2.5 2.5 0 1 0 2.5 2.5V3H16z"/></svg></a>
            <a href="#" aria-label="Pinterest"><svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-4 19.2c-.1-.8-.2-2 .1-2.9l1.2-5s-.3-.6-.3-1.5c0-1.5.8-2.6 1.9-2.6.9 0 1.3.7 1.3 1.5 0 .9-.6 2.2-.9 3.5-.2 1 .5 1.9 1.6 1.9 2 0 3.3-2.5 3.3-5.5 0-2.3-1.5-4-4.4-4a5 5 0 0 0-5.2 5c0 1 .3 1.6.7 2.2.2.2.2.3.1.6l-.2.9c-.1.3-.3.4-.6.3-1.5-.6-2.2-2.3-2.2-4.2 0-3.1 2.6-6.8 7.8-6.8 4.2 0 6.9 3 6.9 6.3 0 4.3-2.4 7.5-5.9 7.5-1.2 0-2.3-.6-2.7-1.4l-.7 2.9c-.3 1-.9 2-1.4 2.8A10 10 0 1 0 12 2z"/></svg></a>
          </div>
        </div>
        ${col("Shop", [["All Products","products.html"],["T-Shirts","products.html#tshirts"],["Hoodies","products.html#hoodies"],["Embroidery","embroidery.html"],["Hats & Caps","products.html#hats"],["Promo Gifts","products.html#promo"]])}
        ${col("Solutions", [["Businesses","use-cases.html#business"],["Schools & Clubs","use-cases.html#schools"],["Events","use-cases.html#events"],["Fundraising","fundraising.html"],["Sports Teams","use-cases.html#sports"]])}
        ${col("Learn", [["How It Works","how-it-works.html"],["Browse Products","products.html"],["Get a Quote","quote.html"],["Reviews","reviews.html"],["Help & FAQ","faq.html"]])}
        ${col("Company", [["About Us","about.html"],["Contact","contact.html"],["Our Guarantee","how-it-works.html#guarantee"],["Careers","about.html#careers"],["Blog","index.html"]])}
      </div>
      <div class="footer-bottom">
        <div>© ${new Date().getFullYear()} Meadow Prints &amp; Embroidery LLC. All rights reserved.</div>
        <div><a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="#">Accessibility</a> · <a href="contact.html">1-800-MEADOW-1</a></div>
      </div>
    </div>
  </footer>`;
}

/* ---- Cart (localStorage) ---- */
const Cart = {
  key: "meadow_cart",
  get() { try { return JSON.parse(localStorage.getItem(this.key)) || []; } catch { return []; } },
  save(items) { localStorage.setItem(this.key, JSON.stringify(items)); this.render(); },
  add(item) { const items = this.get(); items.push(item); this.save(items); toast(`Added “${item.name}” to your project bag`); },
  count() { return this.get().reduce((n, i) => n + (i.qty || 1), 0); },
  render() { const el = document.getElementById("cartCount"); if (el) el.textContent = this.count(); }
};

function toast(msg) {
  let t = document.getElementById("toast");
  if (!t) { t = document.createElement("div"); t.id = "toast";
    t.style.cssText = "position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(20px);background:#164a2b;color:#fff;padding:14px 22px;border-radius:999px;font-weight:700;font-family:var(--font-head);box-shadow:0 10px 30px rgba(0,0,0,.25);z-index:500;opacity:0;transition:all .3s;font-size:.95rem;";
    document.body.appendChild(t); }
  t.textContent = msg;
  requestAnimationFrame(() => { t.style.opacity = "1"; t.style.transform = "translateX(-50%) translateY(0)"; });
  clearTimeout(t._h); t._h = setTimeout(() => { t.style.opacity = "0"; t.style.transform = "translateX(-50%) translateY(20px)"; }, 2600);
}

/* ---- Init ---- */
document.addEventListener("DOMContentLoaded", () => {
  const h = document.getElementById("site-header");
  const f = document.getElementById("site-footer");
  if (h) h.innerHTML = buildHeader();
  if (f) f.innerHTML = buildFooter();
  iconify();

  // mobile nav
  const mob = document.getElementById("mobileNav");
  const ov = document.getElementById("overlay");
  const open = () => { mob.classList.add("open"); ov.classList.add("show"); };
  const close = () => { mob.classList.remove("open"); ov.classList.remove("show"); };
  document.getElementById("hamburger")?.addEventListener("click", open);
  document.getElementById("closeMobile")?.addEventListener("click", close);
  ov?.addEventListener("click", close);

  // cart
  Cart.render();
  document.getElementById("cartBtn")?.addEventListener("click", (e) => {
    e.preventDefault();
    const n = Cart.count();
    toast(n ? `You have ${n} item(s) in your project bag - checkout coming soon!` : "Your project bag is empty. Start a design!");
  });
  document.querySelectorAll("[data-add-cart]").forEach(btn => {
    btn.addEventListener("click", () => Cart.add({ name: btn.dataset.name || "Custom item", price: btn.dataset.price || "-", qty: 1 }));
  });

  // accordions
  document.querySelectorAll(".acc-head").forEach(head => {
    head.addEventListener("click", () => {
      const item = head.closest(".acc-item");
      const body = item.querySelector(".acc-body");
      const isOpen = item.classList.toggle("open");
      body.style.maxHeight = isOpen ? body.scrollHeight + "px" : "0";
    });
  });

  // portfolio lightbox (works on any .gallery)
  (function initLightbox(){
    const items = [...document.querySelectorAll(".gallery .gitem")];
    if (!items.length) return;
    const box = document.createElement("div");
    box.className = "lightbox";
    box.innerHTML = `<button class="lb-close" aria-label="Close">✕</button>
      <button class="lb-nav prev" aria-label="Previous">‹</button>
      <button class="lb-nav next" aria-label="Next">›</button>
      <img alt=""><div class="lb-cap"></div>`;
    document.body.appendChild(box);
    const img = box.querySelector("img"), cap = box.querySelector(".lb-cap");
    let idx = 0;
    const data = items.map(it => ({ src: it.querySelector("img").src, cap: it.querySelector("figcaption")?.textContent || "" }));
    const show = i => { idx = (i + data.length) % data.length; img.src = data[idx].src; cap.textContent = data[idx].cap; };
    items.forEach((it, i) => it.addEventListener("click", () => { show(i); box.classList.add("open"); }));
    box.querySelector(".lb-close").addEventListener("click", () => box.classList.remove("open"));
    box.querySelector(".next").addEventListener("click", e => { e.stopPropagation(); show(idx + 1); });
    box.querySelector(".prev").addEventListener("click", e => { e.stopPropagation(); show(idx - 1); });
    box.addEventListener("click", e => { if (e.target === box) box.classList.remove("open"); });
    document.addEventListener("keydown", e => {
      if (!box.classList.contains("open")) return;
      if (e.key === "Escape") box.classList.remove("open");
      if (e.key === "ArrowRight") show(idx + 1);
      if (e.key === "ArrowLeft") show(idx - 1);
    });
  })();

  // reveal on scroll
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: .12 });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));

  // product filter chips
  const chips = document.querySelectorAll("[data-filter]");
  chips.forEach(chip => chip.addEventListener("click", () => {
    chips.forEach(c => c.classList.remove("active"));
    chip.classList.add("active");
    const f = chip.dataset.filter;
    document.querySelectorAll("[data-cat]").forEach(card => {
      card.style.display = (f === "all" || card.dataset.cat === f) ? "" : "none";
    });
  }));

  // simple form handler
  document.querySelectorAll("form[data-mock]").forEach(form => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const ok = form.querySelector(".form-success");
      form.querySelectorAll("input,textarea,select,button").forEach(el => el.setAttribute("disabled","true"));
      if (ok) ok.style.display = "block";
      toast("Thanks! We’ll be in touch within one business day.");
      ok?.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });
});
