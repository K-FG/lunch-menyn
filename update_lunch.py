import requests
from bs4 import BeautifulSoup
import datetime

def get_menu():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Header för att se ut som en riktig webbläsare
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Restaurang-inställningar
    restaurants = {
        "Blues Restaurang": "https://bluesrestaurang.se/veckans-lunchmeny",
        "Noll Ettan": "https://nollettan.se/",
        "Vi går till Marie": "https://tillmarie.se/meny/#lunch",
        "Mukbang": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/",
        "O'Learys Tolv": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/",
        "Partymakarna": "https://www.partymakarna.se/#alacarte"
    }

    html_output = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lunchmenyn</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; padding: 15px; background: #f0f2f5; color: #1c1e21; }}
            .card {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            h2 {{ color: #1877f2; margin-top: 0; border-bottom: 1px solid #ddd; padding-bottom: 10px; }}
            .menu-text {{ font-size: 0.95em; white-space: pre-wrap; margin: 15px 0; }}
            .btn {{ display: block; background: #1877f2; color: white; text-align: center; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; }}
            .status {{ font-size: 0.8em; color: #65676b; text-align: center; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">🍴 Lunchmenyn</h1>
        <div class="status">Uppdaterad: {now}</div>
    """

    for name, url in restaurants.items():
        menu_content = ""
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Olika strategier för olika sidor
            if "blues" in url:
                # Hittar texten för Blues
                menu_content = soup.find('div', {'class': 'et_pb_module'}).get_text(separator='\n')[:500] + "..."
            elif "nollettan" in url:
                # Hittar texten för Noll Ettan
                menu_content = soup.get_text().split("Onsdag")[1].split("Torsdag")[0] if "Onsdag" in soup.get_text() else "Se meny via länk."
            else:
                menu_content = "Klicka på knappen nedan för att se dagens aktuella meny direkt på hemsidan."
                
        except Exception as e:
            menu_content = "Kunde inte hämta texten automatiskt just nu."

        html_output += f"""
        <div class="card">
            <h2>{name}</h2>
            <div class="menu-text">{menu_content}</div>
            <a href="{url}" class="btn">Öppna originalmenyn</a>
        </div>
        """

    html_output += "</body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_output)

if __name__ == "__main__":
    get_menu()
        
