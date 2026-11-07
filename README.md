# ZERO CARBON ASSISTANT — export website

Static site for high-pressure multi-plunger pumps and slurry pumps, built for Google SEO
and overseas B2B enquiries.

## Build

```bash
python3 build.py
```

Everything is generated from `build.py` (layout, SEO metadata, JSON-LD, sitemap, robots).
Edit copy in `build.py`, then rebuild.

## Structure

- `index.html` — home
- `plunger-pumps.html` — TL series multi-plunger pumps (40–800 m³/h, 4–50 MPa)
- `slurry-pumps.html` — V5 vertical five-plunger slurry pump (100–400 m³/h, 83%+)
- `applications.html` + 4 application pages
- `calculator.html` — client-side sizing & energy calculator
- `about.html`, `contact.html`, `404.html`
- `assets/css/style.css`, `assets/js/calc.js`

## Before going live

1. Replace placeholders in `CONFIG` in `build.py`: brand, domain, email, phone, address.
2. Replace the contact form endpoint (`formsubmit.co`) with the real one, or switch to Formspree.
3. Add real photography (product, factory, site reference) — currently no images.
4. Point the domain at the host and update `CNAME` / DNS.
5. Submit `sitemap.xml` in Google Search Console.

## Deploy

Recommended: Cloudflare Pages (free, commercial use allowed) connected to this repo,
build command `python3 build.py`, output directory `/` — or GitHub Pages for preview only
(GitHub's ToS restricts Pages for sites primarily aimed at commercial transactions).
