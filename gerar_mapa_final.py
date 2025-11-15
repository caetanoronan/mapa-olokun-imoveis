import json

# Carregar dados
with open('imoveis_olx.json', 'r', encoding='utf-8') as f:
    imoveis_olx = json.load(f)

# Imóveis Olokun simples
imoveis_olokun = [
    {
        "titulo": "Casa Centro",
        "preco": "R$ 550.000",
        "endereco": "Rua das Flores, 100, Florianópolis",
        "lat": -27.5954,
        "lng": -48.5480
    },
    {
        "titulo": "Apartamento Beira Mar",
        "preco": "R$ 300.000",
        "endereco": "Avenida Beira Mar, 500, Florianópolis",
        "lat": -27.6023,
        "lng": -48.6026
    }
]

# Gerar JavaScript para os marcadores
js_marcadores = []

# Marcadores OLX
for imovel in imoveis_olx:
    marcador = f"""
    L.marker([{imovel['lat']}, {imovel['lng']}])
        .addTo(map)
        .bindPopup(`
            <div style="width:200px;">
                <h5>{imovel['titulo']}</h5>
                <p><b>Preço:</b> {imovel['preco']}</p>
                <p><b>Local:</b> {imovel['localizacao']}</p>
                <button onclick="window.open('{imovel['link']}')">Ver na OLX</button>
            </div>
        `)
        .bindTooltip("{imovel['titulo']}");
    """
    js_marcadores.append(marcador)

# Marcadores Olokun
for imovel in imoveis_olokun:
    marcador = f"""
    L.marker([{imovel['lat']}, {imovel['lng']}])
        .addTo(map)
        .bindPopup(`
            <div style="width:200px;">
                <h5>{imovel['titulo']}</h5>
                <p><b>Preço:</b> {imovel['preco']}</p>
                <p><b>Endereço:</b> {imovel['endereco']}</p>
                <button onclick="window.open('mailto:contato@olokunimoveis.com.br')">Contato</button>
            </div>
        `)
        .bindTooltip("{imovel['titulo']}");
    """
    js_marcadores.append(marcador)

# Template HTML
html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Mapa de Imóveis - Florianópolis</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
    <style>
        #map {{ height: 100vh; width: 100vw; margin: 0; padding: 0; }}
        body {{ margin: 0; padding: 0; }}
        .header {{
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h3>🏠 Olokun Imóveis</h3>
        <p>Mapa Interativo - Florianópolis</p>
        <p>Total: {len(imoveis_olx) + len(imoveis_olokun)} imóveis</p>
    </div>
    <div id="map"></div>

    <script>
        // Inicializar mapa
        var map = L.map('map').setView([-27.5954, -48.5480], 12);

        // Adicionar tile layer
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap contributors'
        }}).addTo(map);

        // Adicionar marcadores
        {"".join(js_marcadores)}

        console.log('Mapa carregado com {len(imoveis_olx) + len(imoveis_olokun)} imóveis');
    </script>
</body>
</html>"""

# Salvar arquivo
with open('mapa_final.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Mapa final criado com {len(imoveis_olx) + len(imoveis_olokun)} imóveis!")