import datetime

def get_menu():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Här skriver du in veckans meny manuellt på måndagar om du vill ha full kontroll
    menu_data = [
        {
            "name": "1. Blues Restaurang",
            "info": "Johanneshov | 150 kr",
            "items": ["Pepparrotskött", "Köttbullar", "Stekt strömming", "Nasi Goreng", "Pasta Carbonara"],
            "url": "https://bluesrestaurang.se/veckans-lunchmeny"
        },
        {
            "name": "2. Noll Ettan",
            "info": "Hammarby Sjöstad | 155 kr",
            "items": ["Wallenbergare", "Stekt torskfilé", "Svamprisotto", "Veckans Pasta: Scampi"],
            "url": "https://nollettan.se/"
        },
        {
            "name": "3. Vi går till Marie",
            "info": "Johanneshov | ca 150 kr",
            "items": ["Veckans Långkok", "Lammköttbullar", "Kantarellpasta", "Dubbla smörrebröd"],
            "url": "https://tillmarie.se/meny/#lunch"
        }
    ]

    html = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Lunchmenyn</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; padding: 15px; background: #f0f2f5; }}
            .card {{ background: white; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h2 {{ color: #1877f2; margin: 0; font-size: 1.1em; }}
            .info {{ font-size: 0.8em; color: #65676b; margin-bottom: 10px; }}
            ul {{ padding-left: 20px; margin: 10px 0; font-size: 0.95em; }}
            .btn {{ display: block; background: #e7f3ff; color: #1877f2; text-align: center; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">🍴 Lunchmenyn</h1>
        <p style="text-align:center; font-size:0.8em;">Uppdaterad: {now}</p>
    """

    for rest in menu_data:
        items_html = "".join([f"<li>{item}</li>" for item in rest['items']])
        html += f"""
        <div class="card">
            <h2>{rest['name']}</h2>
            <div class="info">{rest['info']}</div>
            <ul>{items_html}</ul>
            <a href="{rest['url']}" class="btn">Öppna originalmenyn</a>
        </div>
        """

    html += "</body></html>"
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    get_menu()
        
