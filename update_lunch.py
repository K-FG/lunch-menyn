"""Bygger index.html med dagens lunch för restaurangerna på WSP-listan.

Källor:
- Statiska sidor och PDF hämtas med requests.
- Sidor som renderas med JavaScript (GHB, Tant Maja, Indian Garden) hämtas
  via Firecrawl-API:t. Kräver hemligheten FIRECRAWL_API_KEY. Saknas den visas
  bara en länk för dessa restauranger.
- Om något fel uppstår för en restaurang visas länken och ett meddelande,
  så att resten av sidan ändå byggs.
"""
import datetime
import html
import io
import os
import re

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Stockholm")
WEEKDAYS = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
FIRECRAWL_KEY = os.environ.get("FIRECRAWL_API_KEY", "")

# Restaurangerna från https://bit.ly/lunchwsp (sites.google.com/view/lunchwsp)
RESTAURANTS = [
    {"name": "BankOmat Seaside", "brand": "#4a4a48", "url": "https://restaurangbankomat.se/lunch/", "source": "html", "wordmark": "BankOmat", "wordmark_style": "plain"},
    {"name": "GHB German Beer Hall", "brand": "#b7791f", "url": "https://www.kvartersmenyn.se/index.php/rest/16965", "source": "firecrawl", "logo": "https://www.kvmcdn.se/images/logos_small/16965.jpg"},
    {"name": "Tant Maja & Fröken Emilia", "brand": "#2f6f6a", "url": "https://www.tantmajaochfrokenemilia.se/lunch-meny", "source": "firecrawl_images", "logo": "https://www.tantmajaochfrokenemilia.se/tenants/tantmaja/logo.jpg"},
    {"name": "Indian Garden", "brand": "#8a3b1f", "url": "https://indiangarden.nu/locations/liljeholmen", "source": "firecrawl_block", "logo": "https://indiangarden.nu/image/catalog/Background/logo.png", "chip": True},
    {"name": "Haandi curry & streetfood", "brand": "#890405", "url": "https://haandi.se/wp-content/uploads/2025/06/Lunchmeny.pdf", "source": "pdf", "logo": "https://haandi.se/favicon.ico", "chip": True},
    {"name": "Marrakech", "brand": "#2a1f14", "url": "https://marrakechrestaurang.se/meny", "source": "info", "logo": "https://marrakechrestaurang.se/assets/marrakech-logo-CE9fafJE.png",
     "info": "Lunchbuffé efter vikt, 19,90 kr per hekto, mån–fre 10.30–13.30. Bröd och kaffe ingår."},
    {"name": "Mackverket", "brand": "#32373c", "url": "https://www.mackverket.se/surdegsmackor-stockholm/", "source": "info",
     "info": "Surdegsmackor, inte en dagsmeny. Samma sortiment varje dag."},
]

DAY_RE = re.compile(r"^\W*(Måndag|Tisdag|Onsdag|Torsdag|Fredag|Lördag|Söndag)\W*$", re.IGNORECASE | re.MULTILINE)
SKIP_RE = re.compile(
    r"kr\b|:-|Ingår|Hemlagad|ALLERGEN|!\[|^\[|https?://|vecka|öppet|pris|©|cookie|powered|"
    r"^\d{1,2} \w+\.?$|^\W*$|^\d+:?\W*$",
    re.IGNORECASE,
)


def fetch_html_text(url):
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text("\n")


def fetch_pdf_text(url):
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    reader = PdfReader(io.BytesIO(r.content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def fetch_firecrawl(url):
    if not FIRECRAWL_KEY:
        raise RuntimeError("FIRECRAWL_API_KEY saknas")
    r = requests.post(
        "https://api.firecrawl.dev/v1/scrape",
        headers={"Authorization": f"Bearer {FIRECRAWL_KEY}"},
        json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["data"]["markdown"]


def day_section(text, day):
    """Returnerar den längsta textbiten under veckodagens rubrik.

    Någon sida listar veckodagarna i en meny före själva rätterna, därför tar
    vi den längsta sektionen i stället för den första förekomsten.
    """
    matches = list(DAY_RE.finditer(text))
    best = ""
    for i, m in enumerate(matches):
        if m.group(1).lower() != day.lower():
            continue
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[m.end():end]
        if len(section) > len(best):
            best = section
    return best or None


def lunch_block_items(text):
    """Indian Garden: lunchrätterna står under '## LUNCH' och är desamma varje vardag."""
    i = text.find("## LUNCH")
    if i < 0:
        return []
    seg = text[i + len("## LUNCH"):]
    nxt = re.search(r"\n## ", seg)
    if nxt:
        seg = seg[:nxt.start()]
    names = re.findall(r"^#{3,6} (.+)$", seg, re.MULTILINE)
    out = []
    for n in names:
        n = re.sub(r"\s+", " ", n).strip()
        if n in out:  # lunchdelen slutar när samma rätt börjar om (nästa avsnitt)
            break
        out.append(n)
    return out[:15]


def image_names(section):
    """Tant Maja: rättens namn står på raden direkt efter bildraden ![...](...)."""
    lines = [l.strip() for l in section.splitlines()]
    out = []
    for i, line in enumerate(lines):
        if line.startswith("!["):
            for nxt in lines[i + 1:]:
                if nxt:
                    if nxt not in out:
                        out.append(nxt)
                    break
    return out[:15]


def dish_lines(section):
    out = []
    for line in section.splitlines():
        t = re.sub(r"[*_#>]+", " ", line)
        t = re.sub(r"\s+", " ", t).strip(" -·")
        if len(t) < 4 or len(t) > 160 or SKIP_RE.search(t):
            continue
        if t not in out:
            out.append(t)
    return out[:15]


def build_card(rest, today):
    name = html.escape(rest["name"])
    url = html.escape(rest["url"])
    items = []
    note = ""
    try:
        if rest["source"] == "info":
            note = rest["info"]
        elif rest["source"] == "pdf":
            items = dish_lines(fetch_pdf_text(rest["url"]))
            note = "Menyn är en PDF från juni 2025. Kontrollera att den fortfarande gäller."
        elif rest["source"] == "html":
            section = day_section(fetch_html_text(rest["url"]), today)
            items = dish_lines(section) if section else []
        elif rest["source"] == "firecrawl_block":
            if not FIRECRAWL_KEY:
                note = "Dagsmenyn kräver FIRECRAWL_API_KEY. Öppna länken för menyn."
            else:
                items = lunch_block_items(fetch_firecrawl(rest["url"]))
                note = "Samma lunchrätter varje vardag, 11–14."
        elif rest["source"] == "firecrawl_images":
            if not FIRECRAWL_KEY:
                note = "Dagsmenyn kräver FIRECRAWL_API_KEY. Öppna länken för menyn."
            else:
                section = day_section(fetch_firecrawl(rest["url"]), today)
                items = image_names(section) if section else []
        elif rest["source"] == "firecrawl":
            if not FIRECRAWL_KEY:
                note = "Dagsmenyn kräver FIRECRAWL_API_KEY. Öppna länken för menyn."
            else:
                section = day_section(fetch_firecrawl(rest["url"]), today)
                items = dish_lines(section) if section else []
    except Exception as exc:  # en restaurang får inte stoppa resten
        note = f"Kunde inte läsa menyn ({type(exc).__name__}). Öppna länken."

    if rest["source"] not in ("info", "pdf") and not items and not note:
        note = "Ingen dagsmeny hittades för idag. Öppna länken."

    body = ""
    if items:
        body = "<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in items) + "</ul>"
    if note:
        body += f"<p class='note'>{html.escape(note)}</p>"
    initials = "".join(w[0] for w in rest["name"].split()[:2]).upper()
    if rest.get("wordmark"):
        wm_cls = {"serif": "wordmark serif", "plain": "wordmark plain"}.get(rest.get("wordmark_style"), "wordmark")
        initials = None
    logo = ""
    if rest.get("logo"):
        cls = "logo chip" if rest.get("chip") else "logo"
        logo = f'<img class="{cls}" src="{html.escape(rest["logo"])}" alt="" onload="this.previousElementSibling.style.display=&#39;none&#39;" onerror="this.remove()">'
    if rest.get("wordmark"):
        wm_or_badge = f'<span class="{wm_cls}">{html.escape(rest["wordmark"])}</span>'
    else:
        wm_or_badge = f'<span class="badge">{html.escape(initials)}</span>'
    return f"""
        <div class="card" style="--brand: {rest.get('brand', '#1f4e79')}">
            <h2>{wm_or_badge}{logo}{name}</h2>
            {body}
            <a href="{url}" class="btn">Visa meny</a>
        </div>
        """


def get_menu():
    now = datetime.datetime.now(TZ)
    today = WEEKDAYS[now.weekday()]
    head = f"""<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: -apple-system, sans-serif; padding: 15px; background: #161615; color: #ecebe6; }}
        .card {{ background: #22221f; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); border-left: 5px solid #8fbde3; }}
        h2 {{ margin: 0 0 10px 0; font-size: 1.2rem; color: #8fbde3; }}
        ul {{ padding-left: 20px; margin: 0; }}
        li {{ margin-bottom: 8px; font-size: 0.95rem; }}
        .note {{ color: #a6a39a; font-size: 0.9rem; }}
        .btn {{ display: block; background: #2b5f8f; color: #ecebe6; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 15px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        :root {{ color-scheme: dark; }}
        .grid {{ display: grid; grid-template-columns: 1fr; gap: 0 20px; max-width: 1200px; margin: 0 auto; }}
        .grid .card {{ margin-bottom: 20px; }}
        .card {{ border-left-color: var(--brand, #8fbde3); }}
        .card h2 {{ color: var(--fg-h, #ecebe6); }}
        .card .btn {{ background: var(--brand, #2b5f8f); color: #fff; }}
        .wordmark {{ display: inline-flex; align-items: center; height: 28px; padding: 0 10px; border-radius: 6px; background: var(--brand, #4a4a48); color: #fff; font-weight: 800; letter-spacing: .08em; font-size: .72rem; text-transform: uppercase; margin-right: 8px; vertical-align: middle; white-space: nowrap; box-shadow: inset 0 -6px 0 rgba(255,255,255,.12); }}
        .wordmark.plain {{ text-transform: none; letter-spacing: .01em; font-size: .85rem; font-weight: 800; }}
        .wordmark.serif {{ font-family: Georgia, "Times New Roman", serif; font-style: italic; font-weight: 400; letter-spacing: 0; font-size: .85rem; text-transform: none; }}
        .badge {{ display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; background: var(--brand, #2c3e50); color: #fff; font-size: 0.7rem; font-weight: 700; margin-right: 8px; vertical-align: middle; }}
        .logo {{ width: auto; height: 28px; max-width: 80px; object-fit: contain; margin-right: 8px; vertical-align: middle; position: relative; }}
        .logo {{ background: var(--brand, #2c3e50); border-radius: 6px; padding: 3px 6px; box-sizing: content-box; }}
        .logo.chip {{ background: #f4f1ea; }}
        @media (min-width: 900px) {{ .grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }} }}
        .updated {{ color: #666; font-size: 0.85rem; margin-top: -8px; }}
        .standard {{ color: #666; font-size: 0.85rem; text-align: center; margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🍴 Lunch Marievik</h1>
        <p>{today} {now.strftime('%d %b %Y')}</p>
        <p class="updated">Uppdaterad {now.strftime('%d %b %Y kl %H:%M')}</p>
    </div>
"""
    cards = '<div class="grid">' + "".join(build_card(r, today) for r in RESTAURANTS) + "</div>"
    standard = (
        "<p class='standard'>Menyerna hämtas automatiskt från restaurangernas egna sidor "
        "vardagar kl 09:00. Kontrollera alltid hos restaurangen innan du går dit. "
        "Vi ansvarar inte för felaktigheter i menyerna. Klicka på \"Visa meny\" för att "
        "se hela menyn på restaurangens sida.</p>"
    )
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(head + cards + standard + "</body></html>")


if __name__ == "__main__":
    get_menu()
