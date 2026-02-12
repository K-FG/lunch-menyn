import datetime

def get_menu():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Uppdaterad data för alla sex restauranger
    menu_data = [
        {
            "name": "1. Blues Restaurang",
            "info": "Johanneshov | 11:00-14:00 | 150 kr",
            "items": ["Pepparrotskött m. morötter", "Köttbullar m. gräddsås", "Stekt strömming", "Nasi Goreng", "Pasta Carbonara"],
            "url": "https://bluesrestaurang.se/veckans-lunchmeny"
        },
        {
            "name": "2. Noll Ettan",
            "info": "Hammarby Sjöstad | 11:00-14:00 | 155 kr",
            "items": ["Wallenbergare m. potatispuré", "Stekt torskfilé m. remoulad", "Svamprisotto", "Veckans Pasta: Scampi"],
            "url": "https://nollettan.se/"
        },
        {
            "name": "3. Vi går till Marie",
            "info": "Johanneshov | 10:30-16:00 | ca 150 kr",
            "items": ["Veckans Långkok (Högrev)", "Lammköttbullar m. fetaost", "Kantarellpasta", "Dubbla smörrebröd"],
            "url": "https://tillmarie.se/meny/#lunch"
        },
        {
            "name": "4. Mukbang (Food & Co)",
            "info": "Johanneshov | 11:00-14:15",
            "items": ["Stekt chorizo m. tryffelcréme", "Sydfransk fiskgryta m. aioli", "Veg: Pastagratäng m. belugalinser", "Broccolisoppa"],
            "url": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/"
        },
        {
            "name": "5. O'Learys Tolv Stockholm",
            "info": "Tele2 Arena | 10:30-14:00 | 139 kr",
            "items": ["Köttbullar m. gräddsås & lingon", "Spättarullader m. romsås", "Veg: Halloumi- & rödbetsbiffar"],
            "url": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/"
        },
        {
            "name": "6. Partymakarna",
            "info": "Slakthusområdet | 09:30-14:00",
            "items": ["Fiskgryta m. lax & räkor", "Fylld fläskschnitzel m. salvia", "Stekt kycklingfilé m. bbq-sås", "Asiatisk nudelsallad m. falafel"],
            "url": "https://www.partymakarna.se/#alacarte"
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
            body {{ font-family: -apple-system, system-ui, sans-serif; padding: 10px; background: #f0f2f5; color: #1c1e21; }}
            .header {{ text-align: center; padding: 20px 0; }}
            h1 {{ margin: 0; font-size: 1.5em; color: #1c1e21; }}
            .update-time {{ font-size: 0.8em; color: #65676b; }}
            .card {{ background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }}
            h2 {{ color: #1877f2; margin: 0 0 4px 0; font-size: 1.1em; }}
            .info {{ font-size: 0.8em; color: #65676b; margin-bottom: 12px; border-bottom: 1px solid #ebedf0; padding-bottom: 8px; }}
            ul {{ padding-left: 20px; margin: 10px 0; font-size: 0.95em; color: #050505; }}
            li {{ margin-bottom: 6px; }}
            .btn {{ display: block; background: #e7f3ff; color: #1877f2; text-align: center; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 0.9em; margin-top: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🍴 Mina Lunchställen</h1>
            <div class="update-time">Uppdaterad: {now}</div>
        </div>
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
        
