import folium
from folium.plugins import MarkerCluster
import json
from geopy.geocoders import Nominatim
import time

# Carregar dados do Viva Real
try:
    with open('imoveis_vivareal.json', 'r', encoding='utf-8') as f:
        imoveis_vr = json.load(f)
except FileNotFoundError:
    imoveis_vr = []

# Dados dos imóveis Olokun
imoveis_olokun = [
    {
        "titulo": "Casa Centro",
        "preco": "R$ 550.000",
        "endereco": "Rua das Flores, 100, Florianópolis",
        "lat": -27.596123,
        "lng": -48.549456,
        "tipo": "Casa",
        "fonte": "Olokun Imóveis"
    },
    {
        "titulo": "Apartamento Beira Mar",
        "preco": "R$ 300.000",
        "endereco": "Avenida Beira Mar, 500, Florianópolis",
        "lat": -27.597234,
        "lng": -48.550567,
        "tipo": "Apartamento",
        "fonte": "Olokun Imóveis"
    }
]

# Geocodificar imóveis do Viva Real se necessário
geolocator = Nominatim(user_agent="mapa_imoveis")
for imovel in imoveis_vr:
    if 'lat' not in imovel or 'lng' not in imovel:
        try:
            location = geolocator.geocode(imovel['localizacao'])
            time.sleep(1)  # Rate limiting
            if location:
                imovel['lat'] = location.latitude
                imovel['lng'] = location.longitude
            else:
                imovel['lat'] = -27.5954
                imovel['lng'] = -48.5480
        except:
            imovel['lat'] = -27.5954
            imovel['lng'] = -48.5480

# Combinar todos os imóveis
todos_imoveis = imoveis_olokun + imoveis_vr

# Criar mapa centrado em Florianópolis
mapa = folium.Map(
    location=[-27.5954, -48.5480],
    zoom_start=13,
    tiles='OpenStreetMap'
)

# Criar grupos de camadas para legenda
grupo_olokun = folium.FeatureGroup(name='🏠 Olokun Imóveis (Venda)', show=True)
grupo_vivareal = folium.FeatureGroup(name='🏢 Viva Real (Aluguel)', show=True)

# Adicionar marcadores para Olokun (venda)
for imovel in imoveis_olokun:
    # Criar popup com informações
    popup_html = f"""
    <div style="width: 250px; font-family: Arial, sans-serif;">
        <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{imovel['titulo']}</h4>
        <p style="margin: 5px 0;"><strong>Preço:</strong> {imovel['preco']}</p>
        <p style="margin: 5px 0;"><strong>Endereço:</strong> {imovel['endereco']}</p>
        <p style="margin: 5px 0;"><strong>Tipo:</strong> {imovel['tipo']}</p>
        <p style="margin: 5px 0;"><strong>Fonte:</strong> {imovel['fonte']}</p>
        <button onclick="window.open('mailto:contato@olokunimoveis.com.br?subject=Interesse em {imovel['titulo']}')"
                style="background: #3498db; color: white; border: none; padding: 8px 16px;
                       border-radius: 4px; cursor: pointer; margin-top: 10px;">
            📧 Entrar em Contato
        </button>
    </div>
    """

    folium.Marker(
        location=[imovel['lat'], imovel['lng']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=imovel['titulo'],
        icon=folium.Icon(color='blue', icon='home', prefix='fa')
    ).add_to(grupo_olokun)

# Adicionar marcadores para Viva Real (aluguel)
for imovel in imoveis_vr:
    # Criar popup com informações
    popup_html = f"""
    <div style="width: 250px; font-family: Arial, sans-serif;">
        <h4 style="margin: 0 0 10px 0; color: #e74c3c;">{imovel['titulo']}</h4>
        <p style="margin: 5px 0;"><strong>Preço:</strong> {imovel['preco']}</p>
        <p style="margin: 5px 0;"><strong>Local:</strong> {imovel['localizacao']}</p>
        <p style="margin: 5px 0;"><strong>Área:</strong> {imovel.get('area', 'N/A')}</p>
        <p style="margin: 5px 0;"><strong>Quartos:</strong> {imovel.get('quartos', 'N/A')}</p>
        <p style="margin: 5px 0;"><strong>Fonte:</strong> {imovel['fonte']}</p>
        <button onclick="window.open('{imovel['link']}')"
                style="background: #e74c3c; color: white; border: none; padding: 8px 16px;
                       border-radius: 4px; cursor: pointer; margin-top: 10px;">
            🏠 Ver no Viva Real (Aluguel)
        </button>
    </div>
    """

    folium.Marker(
        location=[imovel['lat'], imovel['lng']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=imovel['titulo'],
        icon=folium.Icon(color='red', icon='building', prefix='fa')
    ).add_to(grupo_vivareal)

# Adicionar grupos ao mapa
grupo_olokun.add_to(mapa)
grupo_vivareal.add_to(mapa)

# Adicionar controle de camadas
folium.LayerControl(collapsed=False).add_to(mapa)# Adicionar título
title_html = '''
<div style="position: fixed; top: 10px; left: 50px; z-index: 1000;
            background-color: rgba(255, 255, 255, 0.9); padding: 10px;
            border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
    <h3 style="margin: 0; color: #2c3e50;">🏠 Mapa de Imóveis - Florianópolis</h3>
    <p style="margin: 5px 0 0 0; font-size: 14px;">Legenda: Azul=Venda | Vermelho=Aluguel</p>
    <p style="margin: 2px 0 0 0; font-size: 12px;">Total: {} imóveis</p>
</div>
'''.format(len(todos_imoveis))

mapa.get_root().html.add_child(folium.Element(title_html))

# Salvar mapa
mapa.save('mapa_georreferenciado.html')

print(f"Mapa de aluguel georreferenciado criado com sucesso! {len(todos_imoveis)} imóveis adicionados.")
print(f"Olokun: {len(imoveis_olokun)} imóveis")
print(f"Viva Real (Aluguel): {len(imoveis_vr)} imóveis")
print("Arquivo salvo como: mapa_georreferenciado.html")