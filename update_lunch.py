import requests
from bs4 import BeautifulSoup
import datetime

def get_menu():
    # Enkel lista på restauranger och deras länkar
    restaurants = [
        {"name": "Blues Restaurang", "url": "https://bluesrestaurang.se/veckans-lunchmeny"},
        {"name": "Noll Ettan", "url": "https://nollettan.se/"},
        {"name": "Vi går till Marie", "url": "https://tillmarie.se/meny/#lunch"},
        {"name": "Mukbang", "url": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/"},
        {"name": "O'Learys Tolv", "url": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/"},
        {"name": "Partymakarna", "url": "https://www.partymakarna.se/#alacarte"}
    ]
    
    # Skapa själva HTML-sidan
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dagens Lunch</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; padding: 20px; background: #f4f4f9; }}
            .card {{ background: white; padding: 15px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; }}
            h2 {{ margin: 0 0 10px 0; color: #007bff; }}
            a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
            .time {{ font-size: 0.8em; color: #666; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>Dagens Luncher</h1>
        <div class="time">Uppdaterad: {now}</div>
    """
    
    for rest in restaurants:
        html += f"""
        <div class="card">
            <h2>{rest['name']}</h2>
            <p><a href="{rest['url']}" target="_blank">👉 Se dagens meny här</a></p>
        </div>
        """
        
    html += "</body></html>"
    
    # Spara filen som index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html skapad!")

if __name__ == "__main__":
    get_menu()
      
