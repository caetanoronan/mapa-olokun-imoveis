import folium
import pandas as pd
from geopy.geocoders import Nominatim
# branca MacroElement not needed for title injection; folium.Element is used instead

class MapaImobiliaria:
    def __init__(self, min_zoom=10, max_zoom=18, zoom_start=12):
        """Cria a instancia do mapa com limites de zoom padrao.

        min_zoom: limite de zoom (quanto menor, mais afastado / menor escala)
        max_zoom: limite de aproximacao (quanto maior, mais aproximado / maior escala)
        zoom_start: zoom inicial ao abrir o mapa
        """
        self.geolocator = Nominatim(user_agent="imobiliaria_digital")
        # Aplicar limites de zoom
        self.mapa = folium.Map(
            location=[-27.5954, -48.5480],
            zoom_start=zoom_start,
            min_zoom=min_zoom,
            max_zoom=max_zoom,
    )
    # Adicionar um titulo default
    self.adicionar_titulo("Olokun Imóveis")
    
    def carregar_dados(self, arquivo_csv):
        """Carrega dados de um CSV"""
        return pd.read_csv(arquivo_csv)
    
    def geocodificar(self, endereco):
        """Converte endereço em coordenadas"""
        try:
            location = self.geolocator.geocode(endereco + ", Florianópolis, SC")
            return location.latitude, location.longitude
        except:
            return None, None
    
    def criar_mapa(self, dados):
        """Cria o mapa com os dados dos imóveis"""
        # Usamos cores em hex para melhor controle de contraste
        cores = {
            'Casa': '#1f77b4',         # azul
            'Apartamento': '#2ca02c',  # verde
            'Sala Comercial': '#ff7f0e',# laranja
            'Terreno': '#d62728',      # vermelho
            'Galpão Industrial': '#9467bd' # roxo
        }

        # Criar feature groups para cada tipo para permitir filtragem
        grupos = {}
        for tipo in cores.keys():
            grupos[tipo] = folium.FeatureGroup(name=tipo, show=True)
            grupos[tipo].add_to(self.mapa)

    for _, imovel in dados.iterrows():
            lat, lon = self.geocodificar(imovel['endereco'])
            
            if lat and lon:
                popup_html = f"""
                <b>{imovel['tipo']}</b><br>
                <b>Endereço:</b> {imovel['endereco']}<br>
                <b>Área:</b> {imovel['area']}<br>
                <b>Quartos:</b> {imovel['quartos']}<br>
                <b>Banheiros:</b> {imovel['banheiros']}<br>
                <b>Vagas:</b> {imovel['vagas']}<br>
                <b>Valor:</b> {imovel['valor']}<br>
                <a href="{imovel['fotos']}" target="_blank">📸 Ver Fotos</a>
                """
                
                # Usar um DivIcon para aplicar cores hex personalizadas nos marcadores
                cor = cores.get(imovel['tipo'], '#999999')
                icon_html = f"""
                    <div style="background:{cor};width:18px;height:18px;border-radius:50%;border:2px solid #fff;box-shadow:0 1px 2px rgba(0,0,0,.6);transform:translate(-9px,-9px);"></div>
                """

                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=imovel['tipo'],
                    icon=folium.DivIcon(html=icon_html)
                ).add_to(grupos[imovel['tipo']])
        # Adicionar controle de camadas e legenda interativa
        folium.LayerControl(collapsed=False).add_to(self.mapa)
        self.adicionar_legenda(cores, interactive=True)
    
    def salvar_mapa(self, nome_arquivo='mapa_imobiliaria.html'):
        """Salva o mapa em HTML"""
        self.mapa.save(nome_arquivo)
        print(f"Mapa salvo como {nome_arquivo}")

    def adicionar_titulo(self, titulo: str):
        """Adiciona um titulo no topo do mapa (overlay HTML)."""
        # Template com CSS para exibir o titulo centralizado no topo do mapa
        title_html = f"""
        <style>
            .map-title {{
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 9999;
                background-color: rgba(255, 255, 255, 0.85);
                padding: 6px 12px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 5px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            }}
        </style>
        <div class="map-title">{titulo}</div>
        """

        # Insere o titulo no HTML do mapa
        self.mapa.get_root().html.add_child(folium.Element(title_html))

    def adicionar_legenda(self, cores: dict, interactive: bool=False):
        """Gera uma legenda no topo direito com as cores dos tipos de imóvel.

        cores: dicionário tipo->cor (ex. 'Casa': 'blue')
        """
        items = ""
        for tipo, cor in cores.items():
            # cria um pequeno circulo colorido e o texto do tipo
            if interactive:
                items += f"<li onclick=\"toggleLayerByName('{tipo}')\" style='list-style:none;margin-bottom:6px;display:flex;align-items:center;cursor:pointer;'><span style='display:inline-block;width:14px;height:14px;background-color:{cor};border-radius:50%;margin-right:8px;box-shadow:0 1px 2px rgba(0,0,0,.25)'></span>{tipo}</li>"
            else:
                items += f"<li style='list-style:none;margin-bottom:6px;display:flex;align-items:center;'><span style='display:inline-block;width:14px;height:14px;background-color:{cor};border-radius:50%;margin-right:8px;box-shadow:0 1px 2px rgba(0,0,0,.25)'></span>{tipo}</li>"

        legend_html = f"""
        <div style="position: absolute; bottom: 10px; right: 10px; z-index:9999; background:white; padding:8px 12px; border-radius:6px; box-shadow:0 2px 6px rgba(0,0,0,0.15); font-size:13px">
            <b>Legenda</b>
            <ul style='padding-left:0;margin:6px 0 0 0'>{items}</ul>
        </div>
        """

        # script para tornar a legenda clicavel: procura o label do LayerControl e clica no checkbox
        if interactive:
            legend_html += """
            <script>
            function toggleLayerByName(name){
                var labels = document.querySelectorAll('.leaflet-control-layers-overlays label');
                for (var i=0;i<labels.length;i++){
                    var label = labels[i];
                    if(label && label.innerText && label.innerText.trim() === name){
                        var input = label.previousElementSibling;
                        if(input && input.type === 'checkbox') input.click();
                        break;
                    }
                }
            }
            </script>
            """

        self.mapa.get_root().html.add_child(folium.Element(legend_html))

# Uso do script
if __name__ == "__main__":
    # Dados de exemplo
    dados_imoveis = pd.DataFrame({
        'tipo': ['Casa', 'Apartamento', 'Sala Comercial', 'Terreno', 'Galpão Industrial'],
        'endereco': [
            'Rua das Flores, 100',
            'Avenida Beira Mar, 500', 
            'Rua XV de Novembro, 20',
            'Estrada Geral, s/n',
            'Rodovia SC-401, km 5'
        ],
        'area': ['200m²', '70m²', '40m²', '500m²', '600m²'],
        'quartos': [3, 2, 0, 0, 0],
        'banheiros': [2, 1, 1, 0, 2],
        'vagas': [2, 1, 0, 0, 5],
        'valor': ['R$ 550.000', 'R$ 300.000', 'R$ 1.200/mês', 'R$ 150.000', 'R$ 850.000'],
        'fotos': [
            'https://exemplo.com/foto1.jpg',
            'https://exemplo.com/foto2.jpg',
            'https://exemplo.com/foto3.jpg', 
            'https://exemplo.com/foto4.jpg',
            'https://exemplo.com/foto5.jpg'
        ]
    })
    
    # Criar mapa
    mapa_imobiliaria = MapaImobiliaria()
    mapa_imobiliaria.criar_mapa(dados_imoveis)
    mapa_imobiliaria.salvar_mapa()