import requests
from bs4 import BeautifulSoup
import datetime

def get_menu():
    urls = {
        "Blues": "https://bluesrestaurang.se/veckans-lunchmeny",
        "Noll Ettan": "https://nollettan.se/",
        "O'Learys": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/",
        "Mukbang": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/"
    }
    
    html_content = "<html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    html_content += "<style>body{font-family:sans-serif;padding:20px;line-height:1.6;} h2{color:#2c3e50;border-bottom:2px solid #eee;}</style></head><body>"
    html_content += f"<h1>Lunchmenyer {datetime.date.today()}</h1>"

    for name, url in urls.items():
        try:
            res = requests.get(url, timeout=10)
            res.encoding = 'utf-8'
            html_content += f"<h2>{name}</h2><p><a href='{url}'>Länk till meny</a></p>"
            # Här läggs förenklad text till (för enkelhetens skull i version 1)
            html_content += "<div>(Se länk för detaljerad meny just nu)</div>"
        except:
            html_content += f"<h2>{name}</h2><p>Kunde inte hämta menyn.</p>"

    html_content += "</body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    get_menu()
  
