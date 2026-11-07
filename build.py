#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for the Dalian Hongshi Technology export website.
Edit CONFIG + page copy here, then run: python3 build.py
Output: ./ (index.html, *.html, sitemap.xml, robots.txt)
"""
import os, json, html
from datetime import date

CONFIG = {
    "brand": "DALIAN HONGSHI TECHNOLOGY",
    "brand_short": "HONGSHI",        # header/footer logo
    "brand_cn": "大连宏实科技有限公司",
    "brand_full": "Dalian Hongshi Technology Co., Ltd.",
    "tagline": "High-pressure reciprocating pump systems",
    "domain": "https://jeeftang.github.io/tonglan-fluid-site",   # GitHub Pages (temp home until domain)
    "email": "18041136555@189.cn",
    "phone": "+86 180 4113 6555",
    "teams": "18041136555@189.cn",
    "wechat_qr": "assets/img/wechat-qr.png",
    "address": "Dalian, Liaoning, China",
    "year": date.today().year,
}

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- layout
NAV = [
    ("plunger-pumps.html", "Plunger Pumps"),
    ("slurry-pumps.html", "Slurry Pumps"),
    ("applications.html", "Applications"),
    ("calculator.html", "Calculator"),
    ("about.html", "About"),
]

LOGO = """<svg width="34" height="34" viewBox="0 0 34 34" fill="none" aria-hidden="true">
<rect width="34" height="34" rx="9" fill="#0c1a26"/>
<path d="M17 6.5c3.6 2.4 6 6.2 6 10.2 0 3.3-2.7 6-6 6s-6-2.7-6-6c0-4 2.4-7.8 6-10.2Z" fill="#e2570f"/>
<path d="M17 22.7v4.8M11 14.5h12" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".85"/>
</svg>"""


def head(title, desc, slug, extra_head="", jsonld=None):
    canonical = f"{CONFIG['domain']}/{slug}" if slug else f"{CONFIG['domain']}/"
    ld = ""
    if jsonld:
        ld = '<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{CONFIG['brand']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0c1a26">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 34'><rect width='34' height='34' rx='9' fill='%230c1a26'/><path d='M17 6.5c3.6 2.4 6 6.2 6 10.2 0 3.3-2.7 6-6 6s-6-2.7-6-6c0-4 2.4-7.8 6-10.2Z' fill='%23e2570f'/></svg>">
{ld}
{extra_head}
</head>
<body>"""


def header(active=""):
    items = ""
    for href, label in NAV:
        cls = ' class="on"' if href == active else ""
        items += f'<li><a href="{href}"{cls}>{label}</a></li>'
    return f"""<header class="site">
  <div class="wrap nav">
    <a class="brand" href="index.html">{LOGO}<span>{CONFIG['brand_short']}<small>Industrial Pumps</small></span></a>
    <ul>{items}</ul>
    <a class="btn cta" href="contact.html">Request a Quote</a>
  </div>
</header>"""


def footer():
    return f"""<footer class="site">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <a class="brand" href="index.html" style="color:#fff">{LOGO}<span style="color:#fff">{CONFIG['brand_short']}<small style="color:#8fa6b2">Industrial Pumps</small></span></a>
        <p style="margin-top:16px;max-width:320px">{CONFIG['brand_cn']}<br>High-pressure reciprocating pumps and slurry pumps for mining, power, oil &amp; gas and process industries.</p>
      </div>
      <div>
        <h4>Products</h4>
        <ul>
          <li><a href="plunger-pumps.html">Multi-plunger pumps</a></li>
          <li><a href="slurry-pumps.html">Slurry pumps</a></li>
          <li><a href="calculator.html">Sizing calculator</a></li>
        </ul>
      </div>
      <div>
        <h4>Applications</h4>
        <ul>
          <li><a href="mine-dewatering.html">Mine dewatering</a></li>
          <li><a href="filter-press-feed.html">Filter press feed</a></li>
          <li><a href="tailings-transport.html">Tailings transport</a></li>
          <li><a href="water-injection.html">Water injection</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a></li>
          <li><a href="tel:{CONFIG['phone'].replace(' ', '')}">{CONFIG['phone']}</a></li>
          <li>Microsoft Teams: <a href="mailto:{CONFIG['teams']}">{CONFIG['teams']}</a></li>
          <li>{CONFIG['address']}</li>
        </ul>
      </div>
    </div>
    <div class="copy">
      <span>© {CONFIG['year']} {CONFIG['brand_cn']}. All rights reserved.</span>
      <span>Engineered in Shanghai · Serviced worldwide</span>
    </div>
  </div>
</footer>"""


def page(slug, title, desc, body, active="", jsonld=None, extra_head=""):
    doc = head(title, desc, slug, extra_head, jsonld) + header(active) + body + footer() + """
<script src="assets/js/calc.js" defer></script>
</body>
</html>"""
    with open(os.path.join(OUT, slug), "w", encoding="utf-8") as f:
        f.write(doc)
    print("wrote", slug, len(doc))


def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": CONFIG["brand_cn"],
        "alternateName": CONFIG["brand"],
        "url": CONFIG["domain"] + "/",
        "description": "Manufacturer of multi-plunger reciprocating pumps and slurry pumps for mining, power, oil and gas, and process industries.",
        "address": {"@type": "PostalAddress", "addressLocality": "Shanghai", "addressCountry": "CN"},
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": CONFIG["phone"],
            "email": CONFIG["email"],
            "contactType": "sales",
            "availableLanguage": ["English", "Chinese"],
        },
    }


def product_ld(name, desc, slug, extra=None):
    d = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": desc,
        "brand": {"@type": "Brand", "name": CONFIG["brand"]},
        "manufacturer": {"@type": "Organization", "name": CONFIG["brand_cn"]},
        "url": f"{CONFIG['domain']}/{slug}",
        "category": "Industrial pump",
    }
    if extra:
        d.update(extra)
    return d


def crumbs(items):
    lis = "".join(
        f'<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">'
        f'<a itemprop="item" href="{u}"><span itemprop="name">{n}</span></a>'
        f'<meta itemprop="position" content="{i+1}"></li>'
        for i, (u, n) in enumerate(items)
    )
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol style="list-style:none;display:flex;gap:8px;padding:0;margin:0" itemscope itemtype="https://schema.org/BreadcrumbList">{lis}</ol></div></nav>'


def faq_ld(pairs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in pairs
        ],
    }


# ---------------------------------------------------------------- HOME
home_body = f"""
<section class="hero">
  <div class="wrap">
    <div class="badge"><i></i> Reciprocating pump technology · 12–600 m³/h · up to 3,150 m head</div>
    <h1>High-pressure pumps that cut your energy bill — not your uptime.</h1>
    <p class="lead">Multi-plunger reciprocating pumps and slurry pumps built for continuous duty in mines, power plants, oilfields and processing plants. 90%+ efficiency, direct mechanical drive, and drop-in replacement for multistage centrifugal pumps.</p>
    <div class="hero-actions">
      <a class="btn" href="contact.html">Send your duty point</a>
      <a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.35)" href="calculator.html">Size a pump in 30 seconds</a>
    </div>
    <div class="stats">
      <div class="stat"><b>90%+</b><span>Pump efficiency, stable in service</span></div>
      <div class="stat"><b>12–600</b><span>m³/h flow range</span></div>
      <div class="stat"><b>4–50</b><span>MPa discharge pressure</span></div>
      <div class="stat"><b>30,000 h</b><span>Overhaul interval</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">What we build</p>
      <h2>Two product families, one engineering approach</h2>
      <p class="lead">Mechanical direct drive instead of a hydraulic power pack. Fewer failure points, higher efficiency, and a footprint that drops straight into your existing pump house.</p>
    </div>
    <div class="grid-2">
      <article class="card prod-card">
        <div>
          <p class="tag">UDZ series · 3 / 5 / 7 plungers</p>
          <h3>Multi-plunger high-pressure pumps</h3>
          <p>12–600 m³/h and 200–3,150 m of head (2.0–31.5 MPa), plus an injection series to 70 MPa, all with efficiency above 90%. Used for boiler feed, oilfield water injection, high-pressure descaling and mine dewatering. Same suction and discharge orientation as the multistage centrifugal pump it replaces — a 500 m³/h centrifugal pump is replaced by one UDZ 600 unit, not a parallel pair.</p>
          <ul class="checks">
            <li>No hydraulic station — mechanical crank drive</li>
            <li>Wear parts 5,000 h+, overhaul 30,000 h+</li>
            <li>On-site maintenance, no factory return</li>
          </ul>
        </div>
        <a class="more" href="plunger-pumps.html">Explore the UDZ series →</a>
      </article>
      <article class="card prod-card">
        <div>
          <p class="tag">V5 · vertical five-plunger</p>
          <h3>Slurry pumps for abrasive duty</h3>
          <p>100–400 m³/h up to 150 m head, handling solids above 30% by weight. Ceramic plungers and alloy valve seats take the wear that destroys centrifugal slurry pumps, at more than 83% efficiency.</p>
          <ul class="checks">
            <li>Efficiency 83%+ vs 25–50% for centrifugal slurry pumps</li>
            <li>Ceramic plunger + alloy valve seat</li>
            <li>Wear parts 4,000 h+, overhaul 30,000 h+</li>
          </ul>
        </div>
        <a class="more" href="slurry-pumps.html">Explore the V5 slurry pump →</a>
      </article>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">Where they run</p>
      <h2>Built for the duties that eat pumps</h2>
    </div>
    <div class="grid-4">
      <article class="card">
        <div class="icon">⛏</div>
        <h3>Mine dewatering</h3>
        <p>Multi-stage lift from underground sumps to surface, at pressures centrifugal pumps cannot hold.</p>
        <a class="more" href="mine-dewatering.html">Read more →</a>
      </article>
      <article class="card">
        <div class="icon">▤</div>
        <h3>Filter press feed</h3>
        <p>Stable high pressure through the whole fill cycle, so cakes form faster and drier.</p>
        <a class="more" href="filter-press-feed.html">Read more →</a>
      </article>
      <article class="card">
        <div class="icon">≋</div>
        <h3>Tailings &amp; coal slime</h3>
        <p>High-density slurry transport without the wear-and-replace cycle of centrifugal slurry pumps.</p>
        <a class="more" href="tailings-transport.html">Read more →</a>
      </article>
      <article class="card">
        <div class="icon">◎</div>
        <h3>Oilfield water injection</h3>
        <p>120–500 m³/h at 16–25 MPa, with specific power down to 0.3 kWh/m³·MPa.</p>
        <a class="more" href="water-injection.html">Read more →</a>
      </article>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid-2" style="align-items:center;gap:56px">
      <div>
        <p class="eyebrow">Why operators switch</p>
        <h2>Efficiency you can measure, maintenance you can plan</h2>
        <p>A multistage centrifugal pump in abrasive or high-pressure service typically runs at 45–65% efficiency once wear rings open up. A positive-displacement plunger pump holds 90%+ because its volumetric efficiency does not depend on fine clearances.</p>
        <ul class="checks">
          <li><strong>Direct mechanical drive.</strong> No hydraulic power pack, no high-speed friction pairs, no oil overheating in summer.</li>
          <li><strong>Drop-in retrofit.</strong> Matches the piping orientation of the centrifugal pump, so the change is a swap — not a rebuild.</li>
          <li><strong>Predictable wear.</strong> Plungers, valve seats and seals are consumables with published intervals; the crank, crosshead and frame are not.</li>
          <li><strong>Smart control.</strong> VFD, condition monitoring, fault diagnosis and remote data as an option on every unit.</li>
        </ul>
      </div>
      <div class="card" style="background:#0c1a26;border-color:#0c1a26;color:#fff">
        <p class="tag" style="color:#ffb08a">Field reference</p>
        <h3 style="color:#fff">Shengli Oilfield — Wanggang injection station</h3>
        <p style="color:#c6d6df">Seven-plunger reciprocating injection pump commissioned in August 2023 and running continuously since. Specific power measured at 0.3 kWh/m³·MPa against 0.5–0.8 for the multistage centrifugal units it replaced.</p>
        <div class="kv" style="border-color:rgba(255,255,255,.14)"><span>Configuration</span><b>7-plunger, VFD</b></div>
        <div class="kv" style="border-color:rgba(255,255,255,.14)"><span>Duty</span><b>120–500 m³/h · 16–25 MPa</b></div>
        <div class="kv" style="border:0"><span>Status</span><b style="color:#7ee2c4">In continuous service</b></div>
      </div>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="band">
      <div>
        <h2>Send us a duty point, get a selection.</h2>
        <p>Flow, head or pressure, fluid and temperature — that is enough to start. We answer with a model, a curve and a budgetary price.</p>
      </div>
      <a class="btn light" href="contact.html">Request a quotation</a>
    </div>
  </div>
</section>
"""

page(
    "index.html",
    "High-Pressure Plunger Pumps & Slurry Pumps | DALIAN HONGSHI TECHNOLOGY",
    "Multi-plunger reciprocating pumps 12–600 m³/h, heads to 3,150 m, injection series to 70 MPa; slurry pumps 100–400 m³/h at 83%+ efficiency. Drop-in replacement for multistage centrifugal pumps.",
    home_body,
    active="",
    jsonld=org_ld(),
)

# ---------------------------------------------------------------- PLUNGER PUMPS
plunger_body = f"""
{crumbs([("index.html", "Home"), ("plunger-pumps.html", "Plunger Pumps")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">UDZ series · multi-plunger reciprocating</p>
    <h1>Multi-plunger pumps, 12–600 m³/h and up to 3,150 m of head</h1>
    <p class="lead">Three, five and seven-plunger machines with mechanical crank drive. Stable efficiency above 90%, wear parts from 5,000 hours, and a footprint that replaces a multistage centrifugal pump without re-piping the station.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="gap:56px;align-items:start">
    <div class="prose">
      <h2>Why reciprocating instead of centrifugal</h2>
      <p>Above roughly 10 MPa, a multistage centrifugal pump is fighting its own physics: every stage adds clearance losses, and efficiency falls away as wear rings open. A plunger pump displaces a fixed volume per stroke, so its volumetric efficiency stays high for the life of the plunger — typically above 90% in continuous service.</p>
      <p>The practical consequence is energy. On a 400 m³/h duty at 20 MPa, the difference between 62% and 90% efficiency is roughly 1,100 kW of shaft power — around 8.8 million kWh a year at 8,000 hours.</p>
      <div class="callout"><p><strong>Retrofit without civil works.</strong> Our pump heads are arranged with the same suction and discharge orientation as the multistage centrifugal unit, so the replacement is a piping tie-in rather than a pump-house rebuild.</p></div>
      <h2>Mechanical drive, not hydraulic</h2>
      <p>Most Chinese plunger pumps in industrial service are hydraulically driven: an oil power pack pressurises a cylinder that pushes the plunger. That architecture adds a hydraulic station, heat management, oil filtration and a second family of failure modes. Our machines use a crankshaft, connecting rod and crosshead — the architecture used in oilfield pumps, where availability is the whole point.</p>
      <ul>
        <li>No hydraulic power pack, no oil cooler, no servo valve</li>
        <li>Lower parasitic load, so more of the motor output reaches the fluid</li>
        <li>Faults are mechanical and visible — not hidden in a hydraulic circuit</li>
      </ul>
    </div>
    <div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Series</th><th>Flow (m³/h)</th><th>Head (m)</th><th>Pressure (MPa)</th><th>Typical duty</th></tr></thead>
          <tbody>
                        <tr><td><strong>UDQ 12</strong></td><td class="num">12</td><td class="num">200–630</td><td class="num">2.0–6.3</td><td>Small boiler feed, high-mountain supply</td></tr>
            <tr><td><strong>UDQ 20</strong></td><td class="num">20</td><td class="num">300–1,250</td><td class="num">3.0–12.5</td><td>Boiler feed, descaling</td></tr>
            <tr><td><strong>UDQ 30</strong></td><td class="num">30</td><td class="num">300–1,250</td><td class="num">3.0–12.5</td><td>Boiler feed, process</td></tr>
            <tr><td><strong>UDQ 46</strong></td><td class="num">46</td><td class="num">300–800</td><td class="num">3.0–8.0</td><td>Boiler feed, water supply</td></tr>
            <tr><td><strong>UDQ 60</strong></td><td class="num">60</td><td class="num">300–3,150</td><td class="num">3.0–31.5</td><td>Highest head in the range</td></tr>
            <tr><td><strong>UDQ 85</strong></td><td class="num">85</td><td class="num">300–2,000</td><td class="num">3.0–20.0</td><td>Boiler feed, mine dewatering</td></tr>
            <tr><td><strong>UDQ 120</strong></td><td class="num">120</td><td class="num">300–1,600</td><td class="num">3.0–16.0</td><td>Boiler feed, mine dewatering</td></tr>
            <tr><td><strong>UDQ 155</strong></td><td class="num">155</td><td class="num">300–1,600</td><td class="num">3.0–16.0</td><td>Mine dewatering, water supply</td></tr>
            <tr><td><strong>UDQ 200</strong></td><td class="num">200</td><td class="num">300–1,000</td><td class="num">3.0–10.0</td><td>Mine dewatering</td></tr>
            <tr><td><strong>UDZ 280</strong></td><td class="num">280</td><td class="num">300–800</td><td class="num">3.0–8.0</td><td>Mine dewatering, ash transfer</td></tr>
            <tr><td><strong>UDZ 450</strong></td><td class="num">450</td><td class="num">300–1,000</td><td class="num">3.0–10.0</td><td>Large mine dewatering</td></tr>
            <tr><td><strong>UDZ 600</strong></td><td class="num">600</td><td class="num">300–630</td><td class="num">3.0–6.3</td><td>Largest single unit — replaces 500 m³/h centrifugal</td></tr>
            <tr><td><strong>UDQ 600</strong></td><td class="num">600</td><td class="num">700–1,000</td><td class="num">7.0–10.0</td><td>600 m³/h at high head, up to 2,240 kW</td></tr>
          </tbody>
        </table>
      </div>
      <p class="small" style="margin-top:12px">Speeds 180–310 rpm, volumetric efficiency ≥97%, overall efficiency ≥90%. Head in metres ÷ 100 gives the equivalent pressure in MPa. Injection series UDZ 30/50/100/160/320 …/16 covers 7–320 m³/h at 16–70 MPa — ask for that datasheet.</p>
      <div class="card" style="margin-top:24px">
        <h3>Mechanical data</h3>
        <ul class="checks">
          <li>Wear parts (plunger, seat, seal): 5,000 h+</li>
          <li>Overhaul interval: 30,000 h+</li>
          <li>Maintenance on site — no return to factory</li>
          <li>VFD, condition monitoring and remote I/O optional</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head"><h2>Where the UDZ series is used</h2></div>
    <div class="grid-3">
      <article class="card"><h3>Boiler feed</h3><p>Replacing multistage centrifugal feed pumps on industrial and utility boilers, with stable pressure across the load range.</p><a class="more" href="contact.html">Discuss a duty →</a></article>
      <article class="card"><h3>Oilfield water injection</h3><p>120–500 m³/h at 16–25 MPa; specific power down to 0.3 kWh/m³·MPa without a separate lubrication skid.</p><a class="more" href="water-injection.html">Water injection →</a></article>
      <article class="card"><h3>Mine dewatering</h3><p>Multi-stage lift from underground sumps, at pressures that shorten centrifugal pump life to months.</p><a class="more" href="mine-dewatering.html">Dewatering →</a></article>
      <article class="card"><h3>High-pressure descaling</h3><p>Steel and aluminium mill descaling at 20–40 MPa, with pressure held through the pass.</p><a class="more" href="contact.html">Descaling →</a></article>
      <article class="card"><h3>Pipeline boost</h3><p>Long-distance slurry and water transfer where pressure, not flow, is the constraint.</p><a class="more" href="tailings-transport.html">Tailings →</a></article>
      <article class="card"><h3>Process high pressure</h3><p>Chemical, petrochemical and power process duties requiring heavy-duty reciprocating pump design.</p><a class="more" href="contact.html">Process duties →</a></article>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>Frequently asked</h2>
    <h3>Can it replace our existing multistage centrifugal pump directly?</h3>
    <p>In most cases yes. The pump head is laid out with the same suction and discharge orientation, so the baseplate and piping tie in with minor modification. We ask for a piping sketch and the existing duty point before confirming.</p>
    <h3>What maintenance does it need?</h3>
    <p>Plungers, valve seats and seals are consumables with intervals from 5,000 hours. The crank, crosshead and frame are designed for 30,000 hours between overhauls. All wear-part replacement is done on site.</p>
    <h3>Do you supply the motor and VFD?</h3>
    <p>Yes — the unit can be supplied as a bare pump, a pump-and-motor set, or a complete skid with VFD, instrumentation and controls.</p>
    <h3>Which standards apply?</h3>
    <p>The UDZ range is built to Chinese national standards for reciprocating positive-displacement pumps. Material certificates, test reports and any third-party inspection required for your project are agreed at order stage — we state clearly what is and is not certified for each market.</p>
  </div>
</section>
"""

page(
    "plunger-pumps.html",
    "Multi-Plunger Reciprocating Pumps 12–600 m³/h, up to 3,150 m Head | DALIAN HONGSHI TECHNOLOGY",
    "Three, five and seven-plunger reciprocating pumps: 12–600 m³/h, heads 200–3,150 m, injection series to 70 MPa, 90%+ efficiency. Drop-in replacement for multistage centrifugal pumps.",
    plunger_body,
    active="plunger-pumps.html",
    jsonld=product_ld(
        "TL Series Multi-Plunger Reciprocating Pump",
        "Multi-plunger reciprocating pump, 12–600 m³/h, heads 200–3,150 m, efficiency above 90%, mechanical crank drive.",
        "plunger-pumps.html",
        {"additionalProperty": [
            {"@type": "PropertyValue", "name": "Flow rate", "value": "12–600 m³/h"},
            {"@type": "PropertyValue", "name": "Discharge pressure", "value": "2.0–31.5 MPa (clear water) / 16–70 MPa (injection)"},
            {"@type": "PropertyValue", "name": "Efficiency", "value": ">90%"},
        ]},
    ),
)

# ---------------------------------------------------------------- SLURRY PUMPS
slurry_body = f"""
{crumbs([("index.html", "Home"), ("slurry-pumps.html", "Slurry Pumps")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">V5 series · vertical five-plunger</p>
    <h1>Slurry pumps that hold 83% efficiency on abrasive duty</h1>
    <p class="lead">100–400 m³/h, up to 150 m head, solids above 30% by weight. A mechanical five-plunger pump with ceramic plungers and alloy valve seats — built to replace centrifugal slurry pumps that wear out in weeks and hydraulic ceramic plunger pumps that waste a third of their energy.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">The problem</p>
      <h2>Slurry is where pump economics go wrong</h2>
      <p class="lead">In mineral processing, slurry transport is the acknowledged weak point: centrifugal slurry pumps erode, and the energy bill follows the efficiency curve down.</p>
    </div>
    <div class="grid-3">
      <div class="card"><p class="tag">Wear</p><h3>15 days to 6 months</h3><p>Impeller and casing life on abrasive slurry, depending on solids size and velocity. Every rebuild is a production interruption.</p></div>
      <div class="card"><p class="tag">Efficiency</p><h3>25–50%</h3><p>Actual operating efficiency of a centrifugal slurry pump once wear has opened the clearances. The rest becomes heat and noise.</p></div>
      <div class="card"><p class="tag">Energy</p><h3>$40–50k a year</h3><p>Annual electricity for a single medium-sized slurry pump at industrial tariffs — most of it lost to inefficiency.</p></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">The V5 answer</p>
      <h2>Positive displacement, engineered for abrasion</h2>
    </div>
    <div class="grid-2" style="gap:56px;align-items:start">
      <div class="prose">
        <p>Instead of accelerating abrasive solids against a spinning impeller, the V5 displaces them slowly with five vertical plungers. Velocity stays low, so erosion is a function of the materials in contact — not of the whole hydraulic path.</p>
        <ul>
          <li><strong>Ceramic plungers</strong> resist abrasion far beyond coated steel.</li>
          <li><strong>Alloy valve seats</strong> keep volumetric efficiency high as the slurry passes.</li>
          <li><strong>Mechanical drive</strong> — no hydraulic station, no high-speed friction pairs.</li>
          <li><strong>Vertical layout</strong> keeps the footprint small and the suction flooded.</li>
        </ul>
        <div class="callout"><p><strong>Result:</strong> efficiency above 83% — more than 33 percentage points above a centrifugal slurry pump — and roughly half the electricity for the same duty.</p></div>
      </div>
      <div>
        <div class="table-wrap">
          <table>
            <thead><tr><th>Parameter</th><th>V5 five-plunger</th></tr></thead>
            <tbody>
              <tr><td>Flow</td><td class="num">100–400 m³/h</td></tr>
              <tr><td>Head</td><td class="num">up to 150 m</td></tr>
              <tr><td>Discharge pressure</td><td class="num">up to 1.5 MPa</td></tr>
              <tr><td>Solids concentration</td><td class="num">≥30% by weight</td></tr>
              <tr><td>Efficiency</td><td class="num">&gt;83%</td></tr>
              <tr><td>Wear parts life</td><td class="num">4,000 h+</td></tr>
              <tr><td>Overhaul interval</td><td class="num">30,000 h+</td></tr>
              <tr><td>Drive</td><td>Mechanical crank, no hydraulic station</td></tr>
            </tbody>
          </table>
        </div>
        <p class="small" style="margin-top:12px">Duty ranges are indicative; final selection depends on solids size distribution, density and pH.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Comparison</p><h2>Three technologies, one duty</h2></div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>&nbsp;</th><th>Centrifugal slurry pump</th><th>Hydraulic ceramic plunger</th><th>V5 mechanical plunger</th></tr></thead>
        <tbody>
          <tr><td><strong>Efficiency</strong></td><td class="num">25–50%</td><td class="num">65–70%</td><td class="num"><strong>&gt;83%</strong></td></tr>
          <tr><td><strong>Wear life</strong></td><td>15 days – 6 months</td><td>Moderate</td><td>4,000 h+ on wear parts</td></tr>
          <tr><td><strong>Hydraulic station</strong></td><td>No</td><td>Yes — oil, cooling, filtration</td><td>No</td></tr>
          <tr><td><strong>Maintenance</strong></td><td>Frequent rebuilds</td><td>Complex circuit</td><td>On-site wear parts</td></tr>
          <tr><td><strong>High solids (&gt;30%)</strong></td><td>Poor</td><td>Good</td><td>Good</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head"><h2>Typical installations</h2></div>
    <div class="grid-3">
      <article class="card"><h3>Filter press feed</h3><p>Stable pressure through the fill and hold phases, faster cycles and drier cake.</p><a class="more" href="filter-press-feed.html">Filter press feed →</a></article>
      <article class="card"><h3>Tailings &amp; coal slime</h3><p>High-density transport with low velocity and predictable wear.</p><a class="more" href="tailings-transport.html">Tailings transport →</a></article>
      <article class="card"><h3>Dense-medium &amp; concentrate</h3><p>Concentrate and dense-medium transfer where centrifugal impellers fail early.</p><a class="more" href="contact.html">Discuss a duty →</a></article>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <h2>Frequently asked</h2>
    <h3>What solids size can it handle?</h3>
    <p>The V5 is designed for the particle sizes typical of mill discharge, filter press feed and tailings. Send the size distribution with your enquiry — valve and seat selection depends on it.</p>
    <h3>Is 1.5 MPa enough for our line?</h3>
    <p>For 100–400 m³/h slurry duties up to 150 m of head, yes. If you need more pressure, the TL multi-plunger range goes to 70 MPa.</p>
    <h3>How long does a rebuild take?</h3>
    <p>Wear-part replacement is done in place and is measured in hours, not days. Overhauls at 30,000 hours are planned, not emergency work.</p>
  </div>
</section>
"""

page(
    "slurry-pumps.html",
    "Slurry Pumps 100–400 m³/h, 83%+ Efficiency | DALIAN HONGSHI TECHNOLOGY",
    "V5 vertical five-plunger slurry pumps for abrasive duty: 100–400 m³/h, 150 m head, 30%+ solids, 83%+ efficiency with ceramic plungers and alloy valve seats.",
    slurry_body,
    active="slurry-pumps.html",
    jsonld=product_ld(
        "V5 Vertical Five-Plunger Slurry Pump",
        "Slurry pump, 100–400 m³/h, up to 150 m head, above 30% solids by weight, 83%+ efficiency.",
        "slurry-pumps.html",
        {"additionalProperty": [
            {"@type": "PropertyValue", "name": "Flow rate", "value": "100–400 m³/h"},
            {"@type": "PropertyValue", "name": "Head", "value": "up to 150 m"},
            {"@type": "PropertyValue", "name": "Efficiency", "value": ">83%"},
        ]},
    ),
)

# ---------------------------------------------------------------- APPLICATIONS HUB
apps_body = f"""
{crumbs([("index.html", "Home"), ("applications.html", "Applications")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Applications</p>
    <h1>Four duties where pump choice decides the operating cost</h1>
    <p class="lead">Dewatering, filter press feed, tailings transport and water injection share one trait: the duty punishes centrifugal pumps. Here is what we specify, and why.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2">
    <article class="card prod-card">
      <div><p class="tag">UDZ 100/16 · UDZ 160/16</p><h3>Mine dewatering</h3>
      <p>Multi-stage lift from underground sumps to surface. High head, abrasive water, and no tolerance for a pump that stops.</p></div>
      <a class="more" href="mine-dewatering.html">Mine dewatering →</a>
    </article>
    <article class="card prod-card">
      <div><p class="tag">V5</p><h3>Filter press feed</h3>
      <p>Pressure must hold through the fill cycle, then rise for the squeeze. A centrifugal pump cannot do both well.</p></div>
      <a class="more" href="filter-press-feed.html">Filter press feed →</a>
    </article>
    <article class="card prod-card">
      <div><p class="tag">V5</p><h3>Tailings &amp; coal slime</h3>
      <p>High-density slurry at low velocity. Wear life is the whole economic argument.</p></div>
      <a class="more" href="tailings-transport.html">Tailings transport →</a>
    </article>
    <article class="card prod-card">
      <div><p class="tag">UDZ 320/16</p><h3>Oilfield water injection</h3>
      <p>120–500 m³/h at 16–25 MPa. Specific power is the number that matters, and multistage centrifugal units lose it.</p></div>
      <a class="more" href="water-injection.html">Water injection →</a>
    </article>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="sec-head"><h2>Typical duty envelopes</h2><p class="lead">Use these as a starting point, then confirm with the calculator or send us the duty point.</p></div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Application</th><th>Flow (m³/h)</th><th>Head / pressure</th><th>Solids</th><th>Recommended</th></tr></thead>
        <tbody>
          <tr><td>Mine dewatering</td><td class="num">12–600</td><td class="num">200–3,150 m</td><td>abrasive water</td><td>UDQ 60–UDZ 600</td></tr>
          <tr><td>Filter press feed</td><td class="num">100–400</td><td class="num">≤150 m</td><td>30%+</td><td>V5</td></tr>
          <tr><td>Tailings transport</td><td class="num">100–400</td><td class="num">≤150 m</td><td>30–60%</td><td>V5</td></tr>
          <tr><td>Water injection</td><td class="num">7–320</td><td class="num">16–70 MPa</td><td>clean water</td><td>UDZ …/16 family</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="tight"><div class="wrap"><div class="band"><div><h2>Not sure which family fits?</h2><p>Send flow, head and fluid description. We will tell you which range applies — and if neither does, we say so.</p></div><a class="btn light" href="contact.html">Ask an engineer</a></div></div></section>
"""

page(
    "applications.html",
    "Pump Applications: Dewatering, Filter Press, Tailings, Water Injection | DALIAN HONGSHI TECHNOLOGY",
    "Application guide for high-pressure plunger and slurry pumps in mine dewatering, filter press feed, tailings transport and oilfield water injection.",
    apps_body,
    active="applications.html",
)

# ---------------------------------------------------------------- MINE DEWATERING
mine_body = f"""
{crumbs([("index.html", "Home"), ("applications.html", "Applications"), ("mine-dewatering.html", "Mine Dewatering")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Application · mining</p>
    <h1>Mine dewatering pumps for high head and abrasive water</h1>
    <p class="lead">Underground sumps to surface, often in stages. The water carries fines, the head is high, and a stopped pump stops the mine.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="gap:56px;align-items:start">
    <div class="prose">
      <h2>What goes wrong with centrifugal dewatering pumps</h2>
      <p>A multistage centrifugal pump is efficient on clean water at its design point. Underground, neither condition holds: the water carries fines that open wear rings, and the head varies with sump level, so the pump runs off its best efficiency point for much of the day.</p>
      <p>The result is a pump that starts at 65% and settles near 45–50%, with impeller and wear-ring replacement every few months. In a three-pump-house arrangement, the maintenance burden multiplies.</p>
      <h2>How we specify it</h2>
      <ul>
        <li><strong>Positive displacement multi-plunger pumps</strong> hold efficiency as the head changes — output is set by speed, not by the system curve.</li>
        <li><strong>Ceramic or hardened plungers</strong> handle fines that would erode a centrifugal impeller.</li>
        <li><strong>Parallel or series staging</strong> across pump houses, with each unit sized to its own lift.</li>
        <li><strong>Level-based speed control</strong> so the pump matches inflow instead of cycling.</li>
      </ul>
      <div class="callout"><p><strong>Reference:</strong> three pump houses at −50, −250 and −500 m on a Chinese coal mine, replacing 24 multistage centrifugal units with six multi-plunger machines. Measured energy saving 22–37% across the three stations.</p></div>
      <h2>Selection range</h2>
      <p>Typical dewatering duties fall between UDQ 60 and UDZ 600: 60–600 m³/h at 300–3,150 m of head. Where the lift is lower but the flow higher, the V5 slurry pump handles dirty water with solids.</p>
    </div>
    <div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Duty</th><th>Typical value</th></tr></thead>
          <tbody>
            <tr><td>Flow per pump</td><td class="num">100–400 m³/h</td></tr>
            <tr><td>Discharge pressure</td><td class="num">4–25 MPa</td></tr>
            <tr><td>Lift per stage</td><td class="num">150–500 m</td></tr>
            <tr><td>Solids</td><td>fine coal / rock fines</td></tr>
            <tr><td>Efficiency</td><td class="num">&gt;90%</td></tr>
            <tr><td>Wear parts</td><td class="num">5,000 h+</td></tr>
          </tbody>
        </table>
      </div>
      <div class="card" style="margin-top:24px">
        <h3>What we need to quote</h3>
        <ul class="checks">
          <li>Flow per pump house and total inflow</li>
          <li>Vertical lift and pipe length / diameter</li>
          <li>Solids content and particle size</li>
          <li>Power supply voltage and frequency</li>
          <li>Existing pump model and measured power, if replacing</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="tight"><div class="wrap"><div class="band"><div><h2>Replacing an existing dewatering station?</h2><p>Send the existing pump model and a measured power reading — that is enough to size the replacement and estimate the saving.</p></div><a class="btn light" href="contact.html">Send details</a></div></div></section>
"""

page(
    "mine-dewatering.html",
    "Mine Dewatering Pumps — High Head, Abrasive Water | DALIAN HONGSHI TECHNOLOGY",
    "Multi-plunger dewatering pumps for underground mines: 100–400 m³/h at 4–25 MPa, 90%+ efficiency, on-site wear parts, parallel or series staging across pump houses.",
    mine_body,
    active="applications.html",
)

# ---------------------------------------------------------------- FILTER PRESS FEED
fp_body = f"""
{crumbs([("index.html", "Home"), ("applications.html", "Applications"), ("filter-press-feed.html", "Filter Press Feed")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Application · mineral processing</p>
    <h1>Filter press feed pumps that hold pressure through the whole cycle</h1>
    <p class="lead">A filter press asks for low flow at first, then constant pressure as the cake builds. A centrifugal pump delivers the opposite. A positive-displacement slurry pump delivers what the press actually needs.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="gap:56px;align-items:start">
    <div class="prose">
      <h2>The cycle, and why it matters</h2>
      <p>Filling: the chambers are empty, so resistance is low and flow is high. Squeeze: the cake is formed, resistance rises, and the pump must hold pressure at very low flow without dead-heading itself to destruction.</p>
      <p>A centrifugal pump lives on its curve — as resistance rises, flow collapses and so does pressure. Operators compensate by throttling or by accepting a longer cycle. A plunger pump displaces a fixed volume per stroke, so pressure is set by the relief valve and the cycle stays short.</p>
      <h2>Practical benefits</h2>
      <ul>
        <li><strong>Shorter cycles</strong> because pressure is held to the end of the fill.</li>
        <li><strong>Drier cake</strong> from consistent terminal pressure, which cuts transport and drying cost.</li>
        <li><strong>No cavitation at the suction</strong> — the vertical five-plunger layout keeps the inlet flooded.</li>
        <li><strong>Predictable wear</strong> — ceramic plungers and alloy seats, 4,000 h+.</li>
      </ul>
      <div class="callout"><p><strong>Sizing note:</strong> feed pumps are usually sized on the fill rate, not on the average flow. Tell us chamber volume, cycle time target and slurry density.</p></div>
    </div>
    <div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Parameter</th><th>Typical</th></tr></thead>
          <tbody>
            <tr><td>Flow</td><td class="num">100–400 m³/h</td></tr>
            <tr><td>Pressure</td><td class="num">0.8–1.5 MPa</td></tr>
            <tr><td>Solids</td><td class="num">30–60% by weight</td></tr>
            <tr><td>Efficiency</td><td class="num">&gt;83%</td></tr>
            <tr><td>Model</td><td>V5 vertical five-plunger</td></tr>
          </tbody>
        </table>
      </div>
      <div class="card" style="margin-top:24px">
        <h3>Compared with a centrifugal feed pump</h3>
        <ul class="checks">
          <li>Pressure held to end of fill, not just at start</li>
          <li>Roughly half the installed power for the same duty</li>
          <li>No impeller erosion from the abrasive cake</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="tight"><div class="wrap"><div class="band"><div><h2>Tell us your press size</h2><p>Chamber volume, target cycle time and slurry density — we will size the feed pump and give you the expected cycle.</p></div><a class="btn light" href="contact.html">Request a selection</a></div></div></section>
"""

page(
    "filter-press-feed.html",
    "Filter Press Feed Pumps — Constant Pressure, 83%+ Efficiency | DALIAN HONGSHI TECHNOLOGY",
    "V5 five-plunger filter press feed pumps: 100–400 m³/h at 0.8–1.5 MPa, 30–60% solids, 83%+ efficiency, shorter cycles and drier cake than centrifugal feed pumps.",
    fp_body,
    active="applications.html",
)

# ---------------------------------------------------------------- TAILINGS
tail_body = f"""
{crumbs([("index.html", "Home"), ("applications.html", "Applications"), ("tailings-transport.html", "Tailings Transport")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Application · mining &amp; coal</p>
    <h1>Tailings and coal slime pumps where wear life is the economics</h1>
    <p class="lead">High density, fine solids, continuous duty. The cost of a tailings pump is not the purchase price — it is the rebuilds, the downtime and the electricity.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="gap:56px;align-items:start">
    <div class="prose">
      <h2>Why centrifugal units fail here</h2>
      <p>A centrifugal slurry pump works by accelerating the slurry to impeller tip speed. At 30%+ solids, that velocity is exactly what erodes the impeller, volute and liner. Wear life of 15 days to 6 months is normal, and every rebuild costs production time.</p>
      <h2>What the V5 does differently</h2>
      <p>The five-plunger design moves slurry at low velocity, in discrete volumes. Abrasion is limited to the plunger surface, valve seats and seals — all consumables with published service intervals.</p>
      <ul>
        <li>Ceramic plungers for abrasive solids</li>
        <li>Alloy valve seats to hold volumetric efficiency</li>
        <li>Wear parts 4,000 h+, overhaul 30,000 h+</li>
        <li>Mechanical drive — no hydraulic oil circuit to maintain</li>
      </ul>
      <div class="callout"><p><strong>Efficiency:</strong> above 83% against 25–50% for a worn centrifugal slurry pump. On a 250 m³/h duty at 120 m head, that difference is the difference between a manageable power bill and an unacceptable one.</p></div>
    </div>
    <div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Parameter</th><th>V5</th></tr></thead>
          <tbody>
            <tr><td>Flow</td><td class="num">100–400 m³/h</td></tr>
            <tr><td>Head</td><td class="num">≤150 m</td></tr>
            <tr><td>Solids concentration</td><td class="num">30–60% wt</td></tr>
            <tr><td>Efficiency</td><td class="num">&gt;83%</td></tr>
            <tr><td>Wear parts</td><td class="num">4,000 h+</td></tr>
            <tr><td>Overhaul</td><td class="num">30,000 h+</td></tr>
          </tbody>
        </table>
      </div>
      <div class="card" style="margin-top:24px">
        <h3>Send with the enquiry</h3>
        <ul class="checks">
          <li>Solids concentration and specific gravity</li>
          <li>Particle size distribution (d50, d90)</li>
          <li>Flow and pipeline length / elevation</li>
          <li>pH and temperature</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="tight"><div class="wrap"><div class="band"><div><h2>Calculate the energy difference first</h2><p>Our calculator compares a plunger pump with a centrifugal unit at your own duty point and electricity price.</p></div><a class="btn light" href="calculator.html">Open the calculator</a></div></div></section>
"""

page(
    "tailings-transport.html",
    "Tailings & Coal Slime Pumps — 30–60% Solids, 83%+ Efficiency | DALIAN HONGSHI TECHNOLOGY",
    "V5 five-plunger pumps for tailings and coal slime transport: 100–400 m³/h, 30–60% solids, 83%+ efficiency, 4,000 h wear parts, on-site maintenance.",
    tail_body,
    active="applications.html",
)

# ---------------------------------------------------------------- WATER INJECTION
wi_body = f"""
{crumbs([("index.html", "Home"), ("applications.html", "Applications"), ("water-injection.html", "Water Injection")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Application · oil &amp; gas</p>
    <h1>Oilfield water injection pumps at 0.3 kWh/m³·MPa</h1>
    <p class="lead">Multistage centrifugal injection pumps typically run at 0.5–0.8 kWh/m³·MPa. Our seven-plunger machines run at 0.3 — and do not need a separate lubrication skid.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="gap:56px;align-items:start">
    <div class="prose">
      <h2>The number that decides the project</h2>
      <p>Injection stations run continuously for years. A difference of 0.2–0.5 kWh/m³·MPa is not a rounding error; on a 300 m³/h station at 20 MPa it is roughly 2,900–7,300 MWh a year.</p>
      <p>Multistage centrifugal pumps also have to go back to the factory for overhaul, which means either a spare train or an outage. Plunger pumps are maintained in place.</p>
      <h2>Configuration</h2>
      <ul>
        <li><strong>UDZ 600 seven-plunger</strong>, up to 600 m³/h at 300–630 m head — replaces a 500 m³/h multistage centrifugal pump with one unit</li>
        <li><strong>VFD or fixed speed</strong>, depending on reservoir pressure strategy</li>
        <li><strong>Smart control</strong>: automatic regulation, condition monitoring, fault diagnosis, remote telemetry</li>
        <li><strong>Skid packaging</strong> with suction stabiliser, relief valve and instrumentation</li>
      </ul>
      <div class="callout"><p><strong>Field reference:</strong> Shengli Oilfield, Wanggang injection station — seven-plunger unit commissioned August 2023, in continuous service since. Specific power 0.3 kWh/m³·MPa.</p></div>
    </div>
    <div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Parameter</th><th>Typical</th></tr></thead>
          <tbody>
            <tr><td>Flow</td><td class="num">120–500 m³/h</td></tr>
            <tr><td>Discharge pressure</td><td class="num">16–25 MPa</td></tr>
            <tr><td>Specific power</td><td class="num">0.3 kWh/m³·MPa</td></tr>
            <tr><td>Efficiency</td><td class="num">&gt;90%</td></tr>
            <tr><td>Lubrication skid</td><td>Not required</td></tr>
            <tr><td>Overhaul</td><td class="num">30,000 h+, in place</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<section class="tight"><div class="wrap"><div class="band"><div><h2>Evaluating an injection upgrade?</h2><p>Send station flow, injection pressure and current specific power. We will model the annual energy difference.</p></div><a class="btn light" href="contact.html">Talk to us</a></div></div></section>
"""

page(
    "water-injection.html",
    "Oilfield Water Injection Pumps — 0.3 kWh/m³·MPa | DALIAN HONGSHI TECHNOLOGY",
    "Seven-plunger oilfield water injection pumps: 120–500 m³/h at 16–25 MPa, specific power 0.3 kWh/m³·MPa, no lubrication skid, in-place overhaul.",
    wi_body,
    active="applications.html",
)

# ---------------------------------------------------------------- CALCULATOR
calc_css = """<style>
.tabs{display:flex;gap:8px;margin-bottom:22px;flex-wrap:wrap}
.tabs button{border:1px solid #ccd8df;background:#fff;padding:10px 16px;border-radius:9px;font:inherit;font-weight:700;font-size:14px;cursor:pointer;color:#16303f}
.tabs button.active{background:#0c1a26;color:#fff;border-color:#0c1a26}
.formula{background:#fff;border:1px solid #dde5ea;border-radius:12px;padding:18px 22px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:14px;color:#16303f;overflow-x:auto}
</style>"""

calc_body = f"""
{crumbs([("index.html", "Home"), ("calculator.html", "Calculator")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Engineering tools</p>
    <h1>Pump sizing &amp; energy saving calculator</h1>
    <p class="lead">Two calculations we run on every project: what a duty point costs in shaft power, and what changes when a centrifugal pump is replaced by a plunger pump. Everything runs in your browser — no data is sent anywhere.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="tabs">
      <button data-tab="energy" class="active">Energy &amp; payback</button>
      <button data-tab="slurry">Slurry duty check</button>
    </div>

    <div data-panel="energy">
      <div class="calc">
        <div class="calc-form">
          <div class="field"><label for="e_q">Flow rate Q (m³/h)</label><input id="e_q" type="number" value="250" min="1" step="1"><div class="hint">Volume flow at duty point</div></div>
          <div class="field"><label for="e_h">Total head H (m)</label><input id="e_h" type="number" value="800" min="1" step="10"><div class="hint">Discharge head minus suction head, including pipe losses</div></div>
          <div class="field"><label for="e_rho">Fluid density (kg/m³)</label><input id="e_rho" type="number" value="1000" min="500" step="10"></div>
          <div class="field"><label for="e_eff">New pump efficiency (%)</label><input id="e_eff" type="number" value="90" min="30" max="98" step="1"><div class="hint">90% is the published figure for the TL range</div></div>
          <div class="field"><label for="e_eff_old">Existing pump efficiency (%)</label><input id="e_eff_old" type="number" value="55" min="10" max="95" step="1"><div class="hint">Use the measured or nameplate value; 45–65% is common for a worn multistage unit</div></div>
          <div class="field"><label for="e_hours">Operating hours per year</label><input id="e_hours" type="number" value="8000" min="100" step="100"></div>
          <div class="field"><label for="e_price">Electricity price (US$/kWh)</label><input id="e_price" type="number" value="0.08" min="0.01" step="0.01"></div>
          <div class="field"><label for="e_capex">Installed cost of new pump (US$)</label><input id="e_capex" type="number" value="150000" min="0" step="1000"><div class="hint">Optional — used only for simple payback</div></div>
        </div>
        <div class="calc-out">
          <h3>Results</h3>
          <div class="kv"><span>Hydraulic power</span><b id="o_ph">—</b></div>
          <div class="kv"><span>New pump shaft power</span><b id="o_pnew">—</b></div>
          <div class="kv"><span>Existing pump shaft power</span><b id="o_pold">—</b></div>
          <div class="kv"><span>New pump energy</span><b id="o_kwh">—</b></div>
          <div class="kv"><span>New pump energy cost</span><b id="o_cost">—</b></div>
          <div class="kv hl"><span>Annual saving</span><b id="o_save">—</b></div>
          <div class="kv hl"><span>Simple payback</span><b id="o_payback">—</b></div>
          <div class="kv"><span>CO₂ avoided</span><b id="o_co2">—</b></div>
          <p class="note" id="e_hint"></p>
        </div>
      </div>
      <div class="formula" style="margin-top:22px">
        P<sub>hyd</sub> = ρ · g · Q · H / 3.6×10⁶  [kW, Q in m³/h] &nbsp;·&nbsp; P<sub>shaft</sub> = P<sub>hyd</sub> / η &nbsp;·&nbsp; CO₂ factor 0.581 kg/kWh
      </div>
    </div>

    <div data-panel="slurry" style="display:none">
      <div class="calc">
        <div class="calc-form">
          <div class="field"><label for="s_q">Slurry flow Q (m³/h)</label><input id="s_q" type="number" value="250" min="1" step="1"></div>
          <div class="field"><label for="s_h">Head H (m)</label><input id="s_h" type="number" value="120" min="1" step="5"></div>
          <div class="field"><label for="s_c">Solids concentration (% by weight)</label><input id="s_c" type="number" value="35" min="0" max="80" step="1"><div class="hint">Pulp density as a mass fraction</div></div>
          <div class="field"><label for="s_sg">Solids specific gravity</label><input id="s_sg" type="number" value="2.7" min="1.1" max="8" step="0.1"><div class="hint">2.7 for typical rock / coal tailings</div></div>
          <div class="field"><label for="s_eff">Pump efficiency (%)</label><input id="s_eff" type="number" value="83" min="30" max="98" step="1"></div>
          <div class="field"><label for="s_hours">Operating hours per year</label><input id="s_hours" type="number" value="8000" min="100" step="100"></div>
          <div class="field"><label for="s_price">Electricity price (US$/kWh)</label><input id="s_price" type="number" value="0.08" min="0.01" step="0.01"></div>
        </div>
        <div class="calc-out">
          <h3>Results</h3>
          <div class="kv"><span>Mixture density</span><b id="o_mix">—</b></div>
          <div class="kv"><span>Mixture specific gravity</span><b id="o_sg_mix">—</b></div>
          <div class="kv"><span>Hydraulic power</span><b id="o_sph">—</b></div>
          <div class="kv hl"><span>Shaft power</span><b id="o_sshaft">—</b></div>
          <div class="kv"><span>Annual energy</span><b id="o_skwh">—</b></div>
          <div class="kv"><span>Annual energy cost</span><b id="o_scost">—</b></div>
          <p class="note" id="s_rec"></p>
        </div>
      </div>
      <div class="formula" style="margin-top:22px">
        ρ<sub>mix</sub> = 1 / (c/ρ<sub>s</sub> + (1−c)/ρ<sub>w</sub>) &nbsp;·&nbsp; c = solids mass fraction &nbsp;·&nbsp; P<sub>shaft</sub> = ρ<sub>mix</sub>·g·Q·H / (3.6×10⁶ · η)
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap prose">
    <h2>How to read the result</h2>
    <p>These are screening numbers, not a selection. They assume clean-fluid power with the efficiency you enter, and they ignore NPSH, viscosity correction and motor margin. A real selection adds 10–15% motor margin and checks the suction condition.</p>
    <h3>What usually surprises people</h3>
    <p>The shaft power of a worn centrifugal pump is often 1.6–2× the new pump — not because the motor is oversized, but because efficiency has fallen away from the design point. Measured input power is the single most useful number you can give us.</p>
    <h3>Payback assumptions</h3>
    <p>Simple payback only. It ignores maintenance savings (typically 30–50% of the energy saving on abrasive duties), downtime and the residual value of the old unit — so the real payback is usually shorter than shown.</p>
  </div>
</section>
"""

page(
    "calculator.html",
    "Pump Sizing & Energy Saving Calculator | DALIAN HONGSHI TECHNOLOGY",
    "Free pump calculator: hydraulic and shaft power, annual energy cost, savings versus a centrifugal pump, simple payback, and a slurry duty check with mixture density.",
    calc_body,
    active="calculator.html",
    extra_head=calc_css,
)

# ---------------------------------------------------------------- ABOUT
about_body = f"""
{crumbs([("index.html", "Home"), ("about.html", "About")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">About us</p>
    <h1>An engineering team that started with the pump, not the catalogue</h1>
    <p class="lead">{CONFIG['brand']} supplies high-pressure reciprocating plunger pumps and slurry pumps worldwide, with export operations handled from Dalian, Liaoning, China.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="gap:56px;align-items:start">
    <div class="prose">
      <h2>Background</h2>
      <p>The company was founded in 2018 in Pudong, Shanghai, as part of the Tongji Nanhui Science Park group. Product development draws on the Sichuan Machinery Research &amp; Design Institute (established 1957), a state-owned engineering institute with design and EPC qualifications across mechanical, municipal, petrochemical and power sectors.</p>
      <p>Our engineering center works on high-speed direct drive and low-speed high-torque drive machines — the two architectures behind every pump and fan we supply.</p>
      <h2>What we have delivered</h2>
      <ul>
        <li><strong>Boiler feed</strong> — 120 t/h and 130/160 t/h units replacing multistage centrifugal feed pumps in industrial boilers, 21% and 19% energy saving.</li>
        <li><strong>Mine dewatering</strong> — three pump houses at −50, −250 and −500 m, six machines replacing 24 centrifugal units, 22–37% saving.</li>
        <li><strong>Coke dry quenching waste-heat boiler</strong> — feed pump replacement, 26.7% saving, 3.2-year payback.</li>
        <li><strong>Oilfield injection</strong> — seven-plunger station at Shengli Oilfield, specific power 0.3 kWh/m³·MPa.</li>
      </ul>
      <h2>How we work</h2>
      <p>Most of our projects start with a measured duty point rather than a specification. We ask for flow, pressure, hours and a power reading, then propose a machine and a number. If the saving is not there, we say so — a pump that cannot pay for itself is not a project.</p>
    </div>
    <div>
      <div class="card">
        <h3>At a glance</h3>
        <div class="kv" style="color:var(--ink);border-color:var(--line)"><span class="muted">Founded</span><b>2018, Shanghai</b></div>
        <div class="kv" style="color:var(--ink);border-color:var(--line)"><span class="muted">Product range</span><b>12–600 m³/h · 200–3,150 m head · to 70 MPa</b></div>
        <div class="kv" style="color:var(--ink);border-color:var(--line)"><span class="muted">Pump efficiency</span><b>&gt;90%</b></div>
        <div class="kv" style="color:var(--ink);border-color:var(--line)"><span class="muted">Overhaul interval</span><b>30,000 h+</b></div>
        <div class="kv" style="color:var(--ink);border:0"><span class="muted">Markets</span><b>Mining · power · oil &amp; gas</b></div>
      </div>
      <div class="card" style="margin-top:20px">
        <h3>Engineering support</h3>
        <ul class="checks">
          <li>Duty-point selection and curve review</li>
          <li>Retrofit layout against existing piping</li>
          <li>Commissioning and operator training</li>
          <li>Spare-parts programme with wear intervals</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="tight"><div class="wrap"><div class="band"><div><h2>Working on an export project?</h2><p>We can quote FOB Dalian / FOB Shanghai or CIF, with English datasheets, curves and packing lists.</p></div><a class="btn light" href="contact.html">Contact sales</a></div></div></section>
"""

page(
    "about.html",
    "About DALIAN HONGSHI TECHNOLOGY — Reciprocating Pump Engineering, Shanghai",
    "Shanghai-based manufacturer of multi-plunger reciprocating pumps and slurry pumps, backed by the Sichuan Machinery Research & Design Institute. Delivered projects in boiler feed, mine dewatering and oilfield injection.",
    about_body,
    active="about.html",
)

# ---------------------------------------------------------------- CONTACT
contact_body = f"""
{crumbs([("index.html", "Home"), ("contact.html", "Contact")])}
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Send a duty point, get a selection</h1>
    <p class="lead">Flow, head or pressure, fluid, temperature and operating hours. If you are replacing an existing pump, add the model and a measured power reading — that is enough for us to size the replacement and estimate the saving.</p>
  </div>
</section>

<section>
  <div class="wrap grid-2" style="gap:56px;align-items:start">
    <div>
      <form class="enquiry" action="https://formsubmit.co/18041136555@189.cn" method="POST">
        <div><label class="small" for="name">Name</label><input id="name" name="name" required></div>
        <div><label class="small" for="company">Company</label><input id="company" name="company"></div>
        <div><label class="small" for="email">Email</label><input id="email" name="email" type="email" required></div>
        <div><label class="small" for="country">Country</label><input id="country" name="country"></div>
        <div class="full"><label class="small" for="duty">Duty point</label><textarea id="duty" name="duty" placeholder="Flow m³/h · head m or pressure MPa · fluid · solids % · temperature · hours per year · existing pump model"></textarea></div>
        <div class="full"><button class="btn" type="submit">Send enquiry</button></div>
      </form>
      <p class="small" style="margin-top:14px">The form opens a confirmation step on first use (anti-spam). Prefer email? Write to <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>.</p>
    </div>
    <div>
      <div class="card">
        <h3>Direct</h3>
        <div class="kv" style="color:var(--ink);border-color:var(--line)"><span class="muted">Email</span><b><a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a></b></div>
        <div class="kv" style="color:var(--ink);border-color:var(--line)"><span class="muted">Phone / WeChat ID</span><b>{CONFIG['phone']}</b></div>
        <div class="kv" style="color:var(--ink);border-color:var(--line)"><span class="muted">Microsoft Teams</span><b><a href="mailto:{CONFIG['teams']}">{CONFIG['teams']}</a></b></div>
        <div class="kv" style="color:var(--ink);border:0"><span class="muted">Location</span><b>{CONFIG['address']}</b></div>
      </div>
      <div class="card" style="margin-top:20px;text-align:center">
        <h3 style="text-align:left">WeChat</h3>
        <img src="{CONFIG['wechat_qr']}" alt="WeChat QR code — Zero Carbon Assistant" style="width:180px;height:180px;border-radius:8px;display:block;margin:0 auto 10px">
        <p class="small" style="margin:0">Scan to add us on WeChat, or search the ID <strong>{CONFIG['phone']}</strong>.<br>
        No WhatsApp in this market — please use <strong>Microsoft Teams</strong> ({CONFIG['teams']}) or email for calls.</p>
      </div>
      <div class="card" style="margin-top:20px">
        <h3>What happens next</h3>
        <ul class="checks">
          <li>We review the duty point within one working day</li>
          <li>You get a model, a curve and a budgetary price</li>
          <li>If a site visit or measured data is needed, we say so up front</li>
        </ul>
      </div>
      <div class="card" style="margin-top:20px">
        <h3>Trade terms</h3>
        <p class="small" style="margin:0">FOB Dalian / FOB Shanghai or CIF. English datasheets, GA drawings, curves, packing list and test reports supplied with every export order.</p>
      </div>
    </div>
  </div>
</section>
"""

page(
    "contact.html",
    "Contact — Request a Pump Quotation | DALIAN HONGSHI TECHNOLOGY",
    "Send your pump duty point for a selection and budgetary price. High-pressure plunger pumps and slurry pumps, FOB Dalian / FOB Shanghai or CIF, English documentation.",
    contact_body,
    active="contact.html",
)

# ---------------------------------------------------------------- 404
notfound = f"""<section class="page-head"><div class="wrap"><h1>Page not found</h1><p class="lead">That page does not exist. Try the product pages or send us your duty point.</p><p style="margin-top:24px"><a class="btn" href="index.html">Back to home</a></p></div></section>"""
page("404.html", "Page not found | DALIAN HONGSHI TECHNOLOGY", "Page not found.", notfound)

# ---------------------------------------------------------------- sitemap + robots
urls = [
    ("", "1.0", "weekly"),
    ("plunger-pumps.html", "0.9", "monthly"),
    ("slurry-pumps.html", "0.9", "monthly"),
    ("applications.html", "0.8", "monthly"),
    ("mine-dewatering.html", "0.7", "monthly"),
    ("filter-press-feed.html", "0.7", "monthly"),
    ("tailings-transport.html", "0.7", "monthly"),
    ("water-injection.html", "0.7", "monthly"),
    ("calculator.html", "0.8", "monthly"),
    ("about.html", "0.6", "yearly"),
    ("contact.html", "0.8", "yearly"),
]
today = date.today().isoformat()
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, pri, freq in urls:
    sm.append(f"  <url><loc>{CONFIG['domain']}/{u}</loc><lastmod>{today}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
sm.append("</urlset>")
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sm))

with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {CONFIG['domain']}/sitemap.xml\n")

print("done")
