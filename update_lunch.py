import requests
from bs4 import BeautifulSoup
import datetime

def get_menu():
    now = datetime.datetime.now()
    # Hanterar svensk tid och dag
    weekdays = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
    today_swe = weekdays[now.weekday()]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
    
    restaurants = [
        {"name": "Blues Restaurang", "url": "https://bluesrestaurang.se/veckans-lunchmeny"},
        {"name": "Noll Ettan", "url": "https://nollettan.se/"},
        {"name": "Vi går till Marie", "url": "https://tillmarie.se/meny/#lunch"},
        {"name": "Mukbang (Food & Co)", "url": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/"},
        {"name": "O'Learys Tolv", "url": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/"},
        {"name": "Partymakarna", "url": "https://www.partymakarna.se/#alacarte"}
    ]

    html_head = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: -apple-system, sans-serif; padding: 15px; background: #f8f9fa; color: #333; }}
            .card {{ background: white; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #007bff; }}
            h2 {{ margin: 0 0 10px 0; font-size: 1.2rem; color: #0056b3; }}
            ul {{ padding-left: 20px; margin: 0; }}
            li {{ margin-bottom: 8px; font-size: 0.95rem; }}
            .btn {{ display: block; background: #007bff; color: white; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; margin-top: 15px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🍴 Lunch i Johanneshov</h1>
            <p>{today_swe} {now.strftime('%d %b')}</p>
        </div>
    """

    body_content = ""
    for rest in restaurants:
        items = "<li>Klicka nedan för att se dagens meny.</li>"
        # Här kan vi bygga ut med Gemini API-anrop senare för Hostinger-versionen
        
        body_content += f"""
        <div class="card">
            <h2>{rest['name']}</h2>
            <ul>{items}</ul>
            <a href="{rest['url']}" class="btn">Visa Hemsida</a>
        </div>
        """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_head + body_content + "</body></html>")

if __name__ == "__main__":
    get_menu()
        
