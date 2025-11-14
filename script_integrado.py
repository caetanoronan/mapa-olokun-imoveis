import pandas as pd
from geopy.geocoders import Nominatim
import folium
import time
import branca


class ColetorImoveisAutomatico:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="coletor_imoveis")

    def _gerar_dados_ficticios(self):
        return [
            {
                'tipo': 'Casa',
                'endereco': 'Rua das Flores, 100, Florianópolis',
                'area': '200m²',
                'quartos': 3,
                'banheiros': 2,
                'vagas': 2,
                'valor': 'R$ 550.000',
                'fotos': 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400',
                'descricao': 'Linda casa com jardim e garagem'
            },
            {
                'tipo': 'Apartamento',
                'endereco': 'Avenida Beira Mar, 500, Florianópolis',
                'area': '70m²',
                'quartos': 2,
                'banheiros': 1,
                'vagas': 1,
                'valor': 'R$ 300.000',
                'fotos': 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400',
                'descricao': 'Apartamento com vista para o mar'
            },
            {
                'tipo': 'Sala Comercial',
                'endereco': 'Rua XV de Novembro, 20, Centro, Florianópolis',
                'area': '40m²',
                'quartos': 0,
                'banheiros': 1,
                'vagas': 0,
                'valor': 'R$ 1.200/mês',
                'fotos': 'https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=400',
                'descricao': 'Sala comercial bem localizada'
            },
            {
                'tipo': 'Terreno',
                'endereco': 'Estrada Geral, Ratones, Florianópolis',
                'area': '500m²',
                'quartos': 0,
                'banheiros': 0,
                'vagas': 0,
                'valor': 'R$ 150.000',
                'fotos': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=400',
                'descricao': 'Terreno plano para construção'
            },
            {
                'tipo': 'Galpão Industrial',
                'endereco': 'Rodovia SC-401, km 5, Florianópolis',
                'area': '600m²',
                'quartos': 0,
                'banheiros': 2,
                'vagas': 5,
                'valor': 'R$ 850.000',
                'fotos': 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=400',
                'descricao': 'Galpão industrial com doca'
            }
        ]

    def geocodificar_imoveis(self, imoveis):
        for imovel in imoveis:
            try:
                location = self.geolocator.geocode(imovel['endereco'])
                time.sleep(1)  # Rate limiting
                if location:
                    imovel['lat'] = location.latitude
                    imovel['lon'] = location.longitude
                else:
                    imovel['lat'] = -27.5954
                    imovel['lon'] = -48.5480
            except Exception:
                imovel['lat'] = -27.5954
                imovel['lon'] = -48.5480
        return imoveis

    def criar_mapa_automatico(self):
        imoveis = self._gerar_dados_ficticios()
        imoveis = self.geocodificar_imoveis(imoveis)

        mapa = folium.Map(location=[-27.5954, -48.5480], zoom_start=12, min_zoom=10, max_zoom=18)

        # Cabeçalho profissional
        header_html = """
        <style>
            .header {
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 10000;
                background: rgba(255, 255, 255, 0.95);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                font-family: 'Arial', sans-serif;
                max-width: 300px;
            }
            .header h2 {
                margin: 0 0 10px 0;
                color: #2c3e50;
                font-size: 20px;
            }
            .header p {
                margin: 5px 0;
                font-size: 14px;
                color: #34495e;
            }
            .header .contact {
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px solid #ecf0f1;
            }
        </style>
        <div class="header">
            <h2>🏠 Olokun Imóveis</h2>
            <p><strong>Especialistas em imóveis em Florianópolis</strong></p>
            <div class="contact">
                <p>📞 (48) 99999-9999</p>
                <p>📧 contato@olokunimoveis.com.br</p>
                <p>📍 Rua Principal, 123 - Centro, Florianópolis/SC</p>
            </div>
        </div>
        """
        mapa.get_root().html.add_child(folium.Html(header_html))

        # Título central
        title_html = """
        <style>
            .map-title {
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 9999;
                background: rgba(255,255,255,0.9);
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 18px;
                color: #2c3e50;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
        </style>
        <div class="map-title">Mapa Interativo de Imóveis - Florianópolis</div>
        """
        mapa.get_root().html.add_child(folium.Html(title_html))

        cores = {
            'Casa': '#1f77b4',
            'Apartamento': '#2ca02c',
            'Sala Comercial': '#ff7f0e',
            'Terreno': '#d62728',
            'Galpão Industrial': '#9467bd'
        }

        grupos = {}
        for tipo in cores.keys():
            grupos[tipo] = folium.FeatureGroup(name=tipo, show=True)
            grupos[tipo].add_to(mapa)

        for imovel in imoveis:
            popup_html = f"""
            <div style="width:280px; font-family:Arial, sans-serif;">
                <h4 style="margin:0 0 10px 0; color:#2c3e50;">{imovel['tipo']}</h4>
                <img src="{imovel['fotos']}" width="260" style="border-radius:5px; margin-bottom:10px;">
                <p style="margin:5px 0;"><strong>Endereço:</strong> {imovel['endereco']}</p>
                <p style="margin:5px 0;"><strong>Área:</strong> {imovel['area']}</p>
                <p style="margin:5px 0;"><strong>Quartos:</strong> {imovel['quartos']}</p>
                <p style="margin:5px 0;"><strong>Banheiros:</strong> {imovel['banheiros']}</p>
                <p style="margin:5px 0;"><strong>Vagas:</strong> {imovel['vagas']}</p>
                <p style="margin:5px 0; font-size:16px; color:#e74c3c;"><strong>Valor:</strong> {imovel['valor']}</p>
                <p style="margin:10px 0; font-style:italic; color:#7f8c8d;">{imovel['descricao']}</p>
                <button onclick="window.open('mailto:contato@olokunimoveis.com.br?subject=Interesse em {imovel['tipo']} - {imovel['endereco']}')" style="background:#3498db; color:white; border:none; padding:8px 16px; border-radius:4px; cursor:pointer;">📧 Entrar em Contato</button>
            </div>
            """

            cor = cores.get(imovel['tipo'], '#999999')
            icon_html = f"""
                <div style="background:{cor};width:20px;height:20px;border-radius:50%;border:2px solid #fff;box-shadow:0 2px 4px rgba(0,0,0,.3);transform:translate(-10px,-10px);"></div>
            """

            folium.Marker([imovel['lat'], imovel['lon']], popup=folium.Popup(popup_html, max_width=300), tooltip=f"{imovel['tipo']} - {imovel['valor']}", icon=folium.DivIcon(html=icon_html)).add_to(grupos[imovel['tipo']])

        # Legenda interativa
        items = ''
        for tipo, cor in cores.items():
            items += f"<li style='list-style:none;margin-bottom:6px;display:flex;align-items:center;cursor:pointer;' onclick=\"toggleLayerByName('{tipo}')\"><span style='display:inline-block;width:14px;height:14px;background-color:{cor};border-radius:50%;margin-right:8px;box-shadow:0 1px 2px rgba(0,0,0,.25)'></span>{tipo}</li>"

        legend_html = f"""
        <div style='position:absolute;bottom:10px;right:10px;z-index:9999;background:white;padding:12px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);font-size:14px;max-width:200px;'>
            <b>🏠 Tipos de Imóvel</b>
            <ul style='padding-left:0;margin:8px 0 0 0'>{items}</ul>
            <p style="margin:10px 0 0 0; font-size:12px; color:#7f8c8d;">Clique para mostrar/ocultar</p>
        </div>

        <script>
        function toggleLayerByName(name){{
            var labels = document.querySelectorAll('.leaflet-control-layers-overlays label');
            for (var i=0;i<labels.length;i++){{
                var label = labels[i];
                if(label && label.innerText && label.innerText.trim() === name){{
                    var input = label.previousElementSibling;
                    if(input && input.type === 'checkbox') input.click();
                    break;
                }}
            }}
        }}
        </script>
        """

        folium.LayerControl(collapsed=False).add_to(mapa)
        mapa.get_root().html.add_child(folium.Html(legend_html))

        # Rodapé
        footer_html = """
        <style>
            .footer {
                position: absolute;
                bottom: 10px;
                left: 10px;
                z-index: 9999;
                background: rgba(255, 255, 255, 0.9);
                padding: 8px 12px;
                border-radius: 6px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                font-size: 12px;
                color: #7f8c8d;
            }
        </style>
        <div class="footer">
            © 2025 Olokun Imóveis - Todos os direitos reservados
        </div>
        """
        mapa.get_root().add_child(folium.Element(footer_html))

        mapa.save('mapa_imobiliaria_automatico.html')

        df = pd.DataFrame(imoveis)
        df.to_csv('dados_imoveis.csv', index=False)

        print("Mapa profissional criado!")
        print(f"Total de imóveis: {len(imoveis)}")
        return imoveis


if __name__ == '__main__':
    coletor = ColetorImoveisAutomatico()
    coletor.criar_mapa_automatico()
