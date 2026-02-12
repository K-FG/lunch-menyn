import requests
from bs4 import BeautifulSoup
import datetime

def get_menu():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Restaurangernas data och skrap-logik
    restaurants = [
        {
            "name": "1. Blues Restaurang",
            "url": "https://bluesrestaurang.se/veckans-lunchmeny",
            "info": "Johanneshov | 11:00-14:00",
            "search_term": "Onsdag" # Kan ändras till dagens veckodag
        },
        {
            "name": "2. Noll Ettan",
            "url": "https://nollettan.se/",
            "info": "Hammarby Sjöstad | 11:00-14:00",
            "search_term": "Onsdag"
        },
        {
            "name": "3. Vi går till Marie",
            "url": "https://tillmarie.se/meny/#lunch",
            "info": "Johanneshov | 10:30-16:00",
            "items": ["Långkok på högrev", "Lammköttbullar", "Kantarellpasta", "Dubbla smörrebröd"]
        },
        {
            "name": "4. Mukbang (Food & Co)",
            "url": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/",
            "info": "Johanneshov | 11:00-14:15",
            "items": ["Stekt chorizo m. tryffelcréme", "Sydfransk fiskgryta", "Pastagratäng"]
        },
        {
            "name": "5. O'Learys Tolv Stockholm",
            "url": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/",
            "info": "Tele2 Arena | 10:30-14:00",
            "items": ["Köttbullar m. gräddsås", "Spättarullader", "Halloumibiffar"]
        },
        {
            "name": "6. Partymakarna",
            "url": "https://www.partymakarna.se/#alacarte",
            "info": "Slakthusområdet | 09:30-14:00",
            "items": ["Fiskgryta m. lax", "Fylld fläskschnitzel", "Kycklingfilé"]
        }
    ]

    html = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: -apple-system, sans-serif; padding: 10px; background: #f0f2f5; }}
            .card {{ background: white; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            h2 {{ color: #1877f2; margin: 0 0 5px 0; font-size: 1.1em; }}
            .info {{ font-size: 0.8em; color: #65676b; margin-bottom: 10px; }}
            ul {{ padding-left: 20px; margin: 0; font-size: 0.9em; }}
            .btn {{ display: block; background: #e7f3ff; color: #1877f2; text-align: center; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">🍴 Lunchmenyn</h1>
        <p style="text-align:center; font-size:0.8em;">Uppdaterad: {now}</p>
    """

    for rest in restaurants:
        content = ""
        if "items" in rest:
            content = "".join([f"<li>{item}</li>" for item in rest['items']])
        else:
            try:
                # Enkel skrapning för Blues och Noll Ettan
                r = requests.get(rest['url'], headers=headers, timeout=10)
                soup = BeautifulSoup(r.text, 'html.parser')
                text = soup.get_text()
                if rest['search_term'] in text:
                    # Försöker klippa ut en bit av texten runt dagens rätt
                    idx = text.find(rest['search_term'])
                    content = f"<li>{text[idx:idx+200]}...</li>"
                else:
                    content = "<li>Se hemsida för dagens rätter</li>"
            except:
                content = "<li>Kunde inte hämta rätter automatiskt</li>"

        html += f"""
        <div class="card">
            <h2>{rest['name']}</h2>
            <div class="info">{rest['info']}</div>
            <ul>{content}</ul>
            <a href="{rest['url']}" class="btn">Öppna originalmenyn</a>
        </div>
        """

    html += "</body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    get_menu()
        
