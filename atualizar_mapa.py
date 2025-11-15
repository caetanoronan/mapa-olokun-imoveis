import json

# Carregar imóveis da OLX
with open('imoveis_olx.json', 'r', encoding='utf-8') as f:
    imoveis_olx = json.load(f)

# Imóveis fictícios da Olokun (mantidos para demonstração)
imoveis_olokun = [
    {
        "tipo": "Casa",
        "endereco": "Rua das Flores, 100, Florianópolis",
        "lat": -27.4305001,
        "lng": -48.4659858,
        "cor": "#1f77b4",
        "area": "200m²",
        "quartos": 3,
        "banheiros": 2,
        "vagas": 2,
        "valor": "R$ 550.000",
        "descricao": "Linda casa com jardim e garagem",
        "foto": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=300",
        "fonte": "Olokun Imóveis"
    },
    {
        "tipo": "Apartamento",
        "endereco": "Avenida Beira Mar, 500, Florianópolis",
        "lat": -27.6023224,
        "lng": -48.6026133,
        "cor": "#2ca02c",
        "area": "70m²",
        "quartos": 2,
        "banheiros": 1,
        "vagas": 1,
        "valor": "R$ 300.000",
        "descricao": "Apartamento com vista para o mar",
        "foto": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=300",
        "fonte": "Olokun Imóveis"
    },
    {
        "tipo": "Sala Comercial",
        "endereco": "Rua XV de Novembro, 20, Centro, Florianópolis",
        "lat": -27.597,
        "lng": -48.549,
        "cor": "#ff7f0e",
        "area": "40m²",
        "quartos": 0,
        "banheiros": 1,
        "vagas": 0,
        "valor": "R$ 1.200/mês",
        "descricao": "Sala comercial bem localizada",
        "foto": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=300",
        "fonte": "Olokun Imóveis"
    },
    {
        "tipo": "Terreno",
        "endereco": "Estrada Geral, Ratones, Florianópolis",
        "lat": -27.5045161,
        "lng": -48.4903989,
        "cor": "#d62728",
        "area": "500m²",
        "quartos": 0,
        "banheiros": 0,
        "vagas": 0,
        "valor": "R$ 150.000",
        "descricao": "Terreno plano para construção",
        "foto": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300",
        "fonte": "Olokun Imóveis"
    },
    {
        "tipo": "Galpão Industrial",
        "endereco": "Rodovia SC-401, km 5, Florianópolis",
        "lat": -27.5401647,
        "lng": -48.5054413,
        "cor": "#9467bd",
        "area": "600m²",
        "quartos": 0,
        "banheiros": 2,
        "vagas": 5,
        "valor": "R$ 850.000",
        "descricao": "Galpão industrial com doca",
        "foto": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=300",
        "fonte": "Olokun Imóveis"
    }
]

# Combinar imóveis
todos_imoveis = imoveis_olokun + imoveis_olx

print(f"Total de imóveis: {len(todos_imoveis)}")
print(f"Imóveis Olokun: {len(imoveis_olokun)}")
print(f"Imóveis OLX: {len(imoveis_olx)}")

# Gerar JavaScript para o mapa
js_code = f"""
// Dados dos imóveis
var imoveis = {json.dumps(todos_imoveis, ensure_ascii=False, indent=2)};

// Criar camadas para cada fonte
var layers = {{
    olokun: L.layerGroup(),
    olx: L.layerGroup()
}};

console.log('Camadas criadas:', Object.keys(layers));

// Adicionar marcadores
imoveis.forEach(function(imovel, index) {{
    console.log('Processando imóvel', index + 1, ':', imovel.titulo || imovel.tipo);

    var tipoLayer = imovel.fonte === 'OLX' ? 'olx' : 'olokun';

    var marker = L.circleMarker([imovel.lat, imovel.lng], {{
        color: imovel.cor,
        fillColor: imovel.cor,
        fillOpacity: 0.8,
        radius: imovel.fonte === 'OLX' ? 6 : 8,  // Marcadores menores para OLX
        weight: 2
    }});

    console.log('Marcador criado para coordenadas:', imovel.lat, imovel.lng);

    var popupContent;
    if (imovel.fonte === 'OLX') {{
        popupContent = `
            <div style="width:280px; font-family:Arial, sans-serif;">
                <div style="background:#ff6b35; color:white; padding:4px 8px; border-radius:3px; display:inline-block; font-size:10px; margin-bottom:6px;">OLX</div>
                <h4 style="margin:0 0 8px 0; color:#2c3e50; font-size:14px;">${{imovel.titulo}}</h4>
                <img src="${{imovel.foto}}" width="260" height="160" style="border-radius:3px; margin-bottom:8px; object-fit:cover;">
                <p style="margin:3px 0; font-size:12px;"><strong>Localização:</strong> ${{imovel.localizacao}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Área:</strong> ${{imovel.area}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Quartos:</strong> ${{imovel.quartos}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Banheiros:</strong> ${{imovel.banheiros}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Vagas:</strong> ${{imovel.vagas}}</p>
                <p style="margin:3px 0; font-size:16px; color:#e74c3c; font-weight:bold;"><strong>Valor:</strong> ${{imovel.preco || imovel.valor}}</p>
                <a href="${{imovel.link}}" target="_blank" style="background:#ff6b35; color:white; border:none; padding:8px 16px; border-radius:3px; cursor:pointer; font-size:12px; text-decoration:none; display:inline-block; margin-top:8px;">Ver na OLX</a>
            </div>
        `;
    }} else {{
        popupContent = `
            <div style="width:250px; font-family:Arial, sans-serif;">
                <div style="background:#3498db; color:white; padding:4px 8px; border-radius:3px; display:inline-block; font-size:10px; margin-bottom:6px;">Olokun Imóveis</div>
                <h4 style="margin:0 0 8px 0; color:#2c3e50; font-size:14px;">${{imovel.tipo}}</h4>
                <img src="${{imovel.foto}}" width="230" height="150" style="border-radius:3px; margin-bottom:8px; object-fit:cover;">
                <p style="margin:3px 0; font-size:12px;"><strong>Endereço:</strong> ${{imovel.endereco}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Área:</strong> ${{imovel.area}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Quartos:</strong> ${{imovel.quartos}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Banheiros:</strong> ${{imovel.banheiros}}</p>
                <p style="margin:3px 0; font-size:12px;"><strong>Vagas:</strong> ${{imovel.vagas}}</p>
                <p style="margin:3px 0; font-size:14px; color:#e74c3c;"><strong>Valor:</strong> ${{imovel.valor}}</p>
                <p style="margin:6px 0; font-style:italic; color:#7f8c8d; font-size:11px;">${{imovel.descricao}}</p>
                <button onclick="window.open('mailto:contato@olokunimoveis.com.br?subject=Interesse em ${{imovel.tipo}} - ${{imovel.endereco}}')" style="background:#3498db; color:white; border:none; padding:6px 12px; border-radius:3px; cursor:pointer; font-size:11px;">📧 Contato</button>
            </div>
        `;
    }}

    marker.bindPopup(popupContent);
    marker.addTo(layers[tipoLayer]);
    console.log('Marcador adicionado à layer:', tipoLayer);
}});

console.log('Adicionando camadas ao mapa...');
// Adicionar camadas ao mapa inicialmente
Object.values(layers).forEach(function(layer) {{
    layer.addTo(map);
}});

console.log('Adicionando controle de camadas...');
// Adicionar controle de camadas
L.control.layers(null, {{
    "🏢 Olokun Imóveis": layers.olokun,
    "🟠 OLX": layers.olx
}}, {{collapsed: false}}).addTo(map);

console.log('Mapa inicializado com', imoveis.length, 'imóveis totais!');
"""

# Ler o arquivo HTML atual
with open('docs/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Substituir a seção do JavaScript
# Encontrar onde começa o script dos imóveis
start_marker = "// Dados dos imóveis"
end_marker = "// Função para alternar camadas"

start_pos = html_content.find(start_marker)
end_pos = html_content.find(end_marker)

if start_pos != -1 and end_pos != -1:
    new_html = html_content[:start_pos] + js_code + html_content[end_pos:]
else:
    print("Não foi possível encontrar os marcadores no HTML")
    exit(1)

# Salvar o novo HTML
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Mapa atualizado com imóveis reais da OLX!")
print(f"Total de imóveis no mapa: {len(todos_imoveis)}")
print(f"- Olokun Imóveis: {len(imoveis_olokun)} imóveis")
print(f"- OLX: {len(imoveis_olx)} imóveis")