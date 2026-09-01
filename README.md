# Meadow Prints & Embroidery LLC — Website

A complete multi-page custom-apparel website (structure modeled on customink.com, with 100% original branding, copy, and design for Meadow Prints & Embroidery LLC).

## Run it
No build step. Just open `index.html` in a browser, or serve the folder:

```bash
cd "Meadow Embrodiery and Prints" && python3 -m http.server 8080
```

Then visit http://localhost:8080

## Pages
| File | Purpose |
|------|---------|
| `index.html` | Home |
| `products.html` | Catalog (filterable) |
| `product.html` | Product detail + "Interested in this order?" inquiry form with file drop (`?id=` param) |
| `how-it-works.html` | Ordering process + pricing |
| `embroidery.html` | Embroidery service |
| `use-cases.html` | Business / schools / events / family / sports |
| `fundraising.html` | T-shirt fundraisers |
| `quote.html` | Free-quote form |
| `about.html` | Company story + team |
| `reviews.html` | Filterable testimonials |
| `contact.html` | Contact info + form |
| `faq.html` | Help center accordion |

## Structure
- `css/styles.css` — full design system (one file)
- `js/main.js` — shared header/footer injection, nav, cart, accordions, scroll reveal
- `js/products-data.js` — product catalog data + card renderer
The header and footer are defined once in `js/main.js` and injected into every page, so navigation/branding edits happen in a single place.

## Order flow
There's no self-serve design tool. Customers browse products, open one, and fill the
**"Interested in this order?"** form — contact info, quantity, decoration, plus a
drag-and-drop file zone for their designs/logos. On submit they see a confirmation that
Meadow will send a mockup within 24 hours. The site uses an **industrial** look
(graphite + concrete, condensed uppercase type, squared edges, hi-vis orange accents)
over the meadow-green brand color.

## Customize
- **Brand name / links:** `NAV_LINKS`, `buildHeader()`, `buildFooter()` in `js/main.js`
- **Colors / fonts:** CSS variables at the top of `css/styles.css`
- **Products / prices:** `window.MEADOW_PRODUCTS` in `js/products-data.js`
- **Contact details, phone, address:** search the HTML for `1-800-MEADOW-1` / `hello@meadowprints.com`

## Notes
Forms are front-end mockups (they show a success state but don't send data yet).
To go live, wire them to a backend or a form service (e.g. Formspree) and add real
product photos in place of the SVG placeholders.
