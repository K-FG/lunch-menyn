import requests
from bs4 import BeautifulSoup
import datetime

def get_menu():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Lista på restauranger och deras specifika skrap-logik
    restaurants = [
        {"name": "Blues Restaurang", "url": "https://bluesrestaurang.se/veckans-lunchmeny", "id": "blues"},
        {"name": "Noll Ettan", "url": "https://nollettan.se/", "id": "nollettan"},
        {"name": "Vi går till Marie", "url": "https://tillmarie.se/meny/#lunch", "id": "marie"},
        {"name": "Mukbang (Food & Co)", "url": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/", "id": "mukbang"},
        {"name": "O'Learys Tolv", "url": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/", "id": "olearys"},
        {"name": "Partymakarna", "url": "https://www.partymakarna.se/#alacarte", "id": "party"}
    ]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dagens Lunch</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; padding: 10px; background: #f0f2f5; color: #1c1e21; }}
            .card {{ background: white; border-radius: 12px; padding: 15px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }}
            h2 {{ color: #1877f2; margin: 0 0 5px 0; font-size: 1.1em; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            ul {{ padding-left: 20px; margin: 10px 0; font-size: 0.9em; }}
            li {{ margin-bottom: 8px; }}
            .btn {{ display: block; background: #e7f3ff; color: #1877f2; text-align: center; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.85em; }}
            .update-time {{ text-align: center; font-size: 0.7em; color: #65676b; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <h1 style="text-align:center; font-size:1.5em; margin-bottom:5px;">🍴 Johanneshov Lunch</h1>
        <div class="update-time">Uppdaterad: {now}</div>
    """

    for rest in restaurants:
        menu_items = []
        try:
            res = requests.get(rest['url'], headers=headers, timeout=15)
            soup = BeautifulSoup(res.content, 'html.parser')
            
            if rest['id'] == "blues":
                # Specifik logik för Blues
                days = soup.find_all('div', class_='et_pb_module')
                for d in days:
                    if "Torsdag" in d.text: # Ändra till aktuell dag dynamiskt vid behov
                        menu_items = [li.text.strip() for li in d.find_all('li')][:5]
                        break
            
            elif rest['id'] == "nollettan":
                # Specifik logik för Noll Ettan
                content = soup.find(string=lambda t: "Torsdag" in t)
                if content:
                    parent = content.find_parent('div')
                    menu_items = [p.text.strip() for p in parent.find_all('p') if len(p.text.strip()) > 5][:4]

            # Felsäker text om skrapning misslyckas för de andra
            if not menu_items:
                menu_items = ["Se dagens meny direkt på hemsidan via knappen nedan."]

        except Exception:
            menu_items = ["Kunde inte hämta menyn automatiskt just nu."]

        items_html = "".join([f"<li>{item}</li>" for item in menu_items])
        html_content += f"""
        <div class="card">
            <h2>{rest['name']}</h2>
            <ul>{items_html}</ul>
            <a href="{rest['url']}" class="btn">Öppna originalmenyn</a>
        </div>
        """

    html_content += "</body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    get_menu()
        
