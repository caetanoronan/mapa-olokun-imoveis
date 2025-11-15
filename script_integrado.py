import pandas as pd
from geopy.geocoders import Nominatim
import folium
import time
import branca
import json


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

    def carregar_dados_olx(self):
        """Carrega dados da OLX do arquivo JSON"""
        try:
            with open('imoveis_olx.json', 'r', encoding='utf-8') as f:
                dados_olx = json.load(f)

            imoveis_olx = []
            for imovel in dados_olx:
                imovel_olx = {
                    'tipo': 'OLX',
                    'titulo': imovel.get('titulo', 'Título não disponível'),
                    'endereco': imovel.get('localizacao', 'Localização não disponível'),
                    'area': imovel.get('area', 'N/A'),
                    'quartos': imovel.get('quartos', 0),
                    'banheiros': imovel.get('banheiros', 0),
                    'vagas': imovel.get('vagas', 0),
                    'valor': imovel.get('preco', 'Preço não disponível'),
                    'fotos': imovel.get('foto', 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400'),
                    'descricao': f"Imóvel da OLX - {imovel.get('titulo', '')}",
                    'link': imovel.get('link', '#'),
                    'fonte': 'OLX',
                    'lat': imovel.get('lat', -27.5954),
                    'lon': imovel.get('lng', -48.5480),
                    'cor': imovel.get('cor', '#3498db')
                }
                imoveis_olx.append(imovel_olx)

            return imoveis_olx
        except FileNotFoundError:
            print("Arquivo imoveis_olx.json não encontrado. Usando apenas dados da Olokun.")
            return []
        except Exception as e:
            print(f"Erro ao carregar dados OLX: {e}")
            return []

    def geocodificar_imoveis(self, imoveis):
        for imovel in imoveis:
            # Pula geocodificação se já tem coordenadas (caso OLX)
            if 'lat' in imovel and 'lon' in imovel and imovel['lat'] != -27.5954:
                continue

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
        # Carrega dados da Olokun
        imoveis_olokun = self._gerar_dados_ficticios()
        imoveis_olokun = self.geocodificar_imoveis(imoveis_olokun)

        # Carrega dados da OLX
        imoveis_olx = self.carregar_dados_olx()

        # Combina todos os imóveis
        todos_imoveis = imoveis_olokun + imoveis_olx

        mapa = folium.Map(location=[-27.5954, -48.5480], zoom_start=12, min_zoom=10, max_zoom=18)

        # Título central simples
        title_html = """
        <div style="position:absolute;top:10px;left:50%;transform:translateX(-50%);z-index:9999;background:rgba(255,255,255,0.9);padding:8px 16px;border-radius:8px;font-weight:bold;font-size:16px;color:#2c3e50;">
            Mapa de Imóveis - Florianópolis
        </div>
        """
        mapa.get_root().html.add_child(folium.Html(title_html))

        # Cores para diferentes tipos
        cores = {
            'Casa': '#1f77b4',
            'Apartamento': '#2ca02c',
            'Sala Comercial': '#ff7f0e',
            'Terreno': '#d62728',
            'Galpão Industrial': '#9467bd',
            'OLX': '#3498db'
        }

        # Cria grupos de camadas
        grupos = {}
        for tipo in cores.keys():
            grupos[tipo] = folium.FeatureGroup(name=tipo, show=True)
            grupos[tipo].add_to(mapa)

        for imovel in todos_imoveis:
            # Determina o tipo para o grupo
            tipo_grupo = imovel.get('tipo', 'OLX')
            if tipo_grupo not in cores:
                tipo_grupo = 'OLX'

            # Cria popup simples
            if imovel.get('fonte') == 'OLX':
                popup_html = f"""
                <div style="width:200px;">
                    <h5>{imovel['titulo']}</h5>
                    <p><b>Local:</b> {imovel['endereco']}</p>
                    <p><b>Valor:</b> {imovel['valor']}</p>
                    <p><b>Área:</b> {imovel['area']}</p>
                    <button onclick="window.open('{imovel['link']}')">Ver na OLX</button>
                </div>
                """
            else:
                popup_html = f"""
                <div style="width:200px;">
                    <h5>{imovel['tipo']}</h5>
                    <p><b>Endereço:</b> {imovel['endereco']}</p>
                    <p><b>Valor:</b> {imovel['valor']}</p>
                    <p><b>Área:</b> {imovel['area']}</p>
                    <button onclick="window.open('mailto:contato@olokunimoveis.com.br?subject=Interesse')">Contato</button>
                </div>
                """

            cor = imovel.get('cor', cores.get(tipo_grupo, '#999999'))
            icon_html = f'<div style="background:{cor};width:15px;height:15px;border-radius:50%;border:2px solid #fff;"></div>'

            folium.Marker([imovel['lat'], imovel['lon']], popup=popup_html, tooltip=f"{imovel.get('titulo', imovel.get('tipo', 'Imóvel'))} - {imovel['valor']}", icon=folium.DivIcon(html=icon_html)).add_to(grupos[tipo_grupo])

        # Controle de camadas simples
        folium.LayerControl(collapsed=False).add_to(mapa)

        mapa.save('mapa_imobiliaria_automatico.html')

        df = pd.DataFrame(imoveis_olokun)
        df.to_csv('dados_imoveis.csv', index=False)

        print("Mapa simplificado criado!")
        print(f"Total de imóveis: {len(todos_imoveis)}")
        print(f"Imóveis Olokun: {len(imoveis_olokun)}")
        print(f"Imóveis OLX: {len(imoveis_olx)}")
        return todos_imoveis


if __name__ == '__main__':
    coletor = ColetorImoveisAutomatico()
    coletor.criar_mapa_automatico()
