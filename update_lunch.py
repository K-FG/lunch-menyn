import datetime

def get_menu():
    # Enkel lista på dina restauranger
    restaurants = [
        {"name": "Blues Restaurang", "url": "https://bluesrestaurang.se/veckans-lunchmeny"},
        {"name": "Noll Ettan", "url": "https://nollettan.se/"},
        {"name": "Vi går till Marie", "url": "https://tillmarie.se/meny/#lunch"},
        {"name": "Mukbang", "url": "https://www.compass-group.se/restauranger-och-menyer/foodandco/mukbang/"},
        {"name": "O'Learys Tolv", "url": "https://olearys.com/sv-se/tolv-stockholm/food/lunchmeny/"},
        {"name": "Partymakarna", "url": "https://www.partymakarna.se/#alacarte"}
    ]
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Skapar en mobilvänlig webbsida
    html = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mina Lunchställen</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; padding: 20px; background-color: #f6f8fa; color: #24292e; }}
            h1 {{ text-align: center; font-size: 1.5rem; margin-bottom: 5px; }}
            .date {{ text-align: center; font-size: 0.8rem; color: #57606a; margin-bottom: 25px; }}
            .card {{ background: white; border: 1px solid #d0d7de; border-radius: 6px; padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            .card h2 {{ margin: 0 0 12px 0; font-size: 1.1rem; }}
            .btn {{ display: block; background-color: #0969da; color: white; padding: 12px; border-radius: 6px; text-decoration: none; text-align: center; font-weight: 600; font-size: 0.9rem; }}
            .btn:active {{ background-color: #0550ae; }}
        </style>
    </head>
    <body>
        <h1>🍴 Lunchmenyn</h1>
        <div class="date">Senast uppdaterad: {now}</div>
    """
    
    for rest in restaurants:
        html += f"""
        <div class="card">
            <h2>{rest['name']}</h2>
            <a href="{rest['url']}" class="btn">Se dagens meny</a>
        </div>
        """
        
    html += "</body></html>"
    
    # Detta steg skapar filen som fattas
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Succé! index.html har skapats.")

if __name__ == "__main__":
    get_menu()
    
