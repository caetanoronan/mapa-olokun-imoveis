import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

def buscar_imoveis_olx(cidade='florianopolis', tipo='imoveis', max_imoveis=10):
    '''
    Busca imóveis na OLX usando web scraping
    '''
    url = f'https://sc.olx.com.br/{cidade}/{tipo}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        # Adicionar delay para simular comportamento humano
        time.sleep(random.uniform(1, 3))

        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status da requisição: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            imoveis = []

            # Tentar diferentes seletores CSS que a OLX pode usar
            anuncios = soup.find_all(['div', 'li'], class_=re.compile(r'.*sc-.*'))[:max_imoveis]

            print(f"Encontrados {len(anuncios)} possíveis anúncios")

            for anuncio in anuncios:
                try:
                    # Extrair título
                    titulo_elem = anuncio.find('h2') or anuncio.find('a', class_=re.compile(r'.*title.*'))
                    titulo = titulo_elem.text.strip() if titulo_elem else 'Título não encontrado'

                    # Extrair preço
                    preco_elem = anuncio.find('span', class_=re.compile(r'.*price.*')) or anuncio.find('span', text=re.compile(r'R\$'))
                    preco = preco_elem.text.strip() if preco_elem else 'Preço não encontrado'

                    # Extrair link
                    link_elem = anuncio.find('a')
                    link = link_elem.get('href') if link_elem else '#'
                    if link and not str(link).startswith('http'):
                        link = 'https://olx.com.br' + str(link)

                    # Pular se não tem título ou preço válido
                    if titulo == 'Título não encontrado' or preco == 'Preço não encontrado':
                        continue

                    imovel = {
                        'titulo': titulo,
                        'preco': preco,
                        'link': link,
                        'localizacao': f'{cidade}, SC',
                        'fonte': 'OLX',
                        'tipo': 'real'
                    }

                    imoveis.append(imovel)

                except Exception as e:
                    continue

            return imoveis

    except Exception as e:
        print(f'Erro na busca OLX: {e}')

    return []

def dados_simulados_olx():
    '''
    Retorna dados simulados mas realistas da OLX quando o scraping falha
    '''
    return [
        {
            "titulo": "Apartamento 2 quartos Centro - Excelente localização",
            "preco": "R$ 450.000",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/apartamento-2-quartos-centro-excelente-localizacao",
            "localizacao": "Centro, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.5972029,
            "lng": -48.5494815,
            "cor": "#3498db",
            "area": "65m²",
            "quartos": 2,
            "banheiros": 1,
            "vagas": 1,
            "foto": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=300"
        },
        {
            "titulo": "Casa 3 quartos Lagoa da Conceição - Vista para o mar",
            "preco": "R$ 850.000",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/casa-3-quartos-lagoa-conceicao-vista-mar",
            "localizacao": "Lagoa da Conceição, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.5697194,
            "lng": -48.4515809,
            "cor": "#e74c3c",
            "area": "180m²",
            "quartos": 3,
            "banheiros": 2,
            "vagas": 2,
            "foto": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=300"
        },
        {
            "titulo": "Sala comercial Rua XV de Novembro - Centro Histórico",
            "preco": "R$ 2.500/mês",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/sala-comercial-rua-xv-novembro-centro-historico",
            "localizacao": "Centro Histórico, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.5972029,
            "lng": -48.5494815,
            "cor": "#f39c12",
            "area": "45m²",
            "quartos": 0,
            "banheiros": 1,
            "vagas": 0,
            "foto": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=300"
        },
        {
            "titulo": "Terreno 300m² Santo Antônio de Lisboa",
            "preco": "R$ 180.000",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/terreno-300m2-santo-antonio-lisboa",
            "localizacao": "Santo Antônio de Lisboa, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.5061508,
            "lng": -48.5188698,
            "cor": "#27ae60",
            "area": "300m²",
            "quartos": 0,
            "banheiros": 0,
            "vagas": 0,
            "foto": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300"
        },
        {
            "titulo": "Galpão industrial 500m² Distrito Industrial",
            "preco": "R$ 750.000",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/galpao-industrial-500m2-distrito-industrial",
            "localizacao": "Distrito Industrial, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.5401647,
            "lng": -48.5054413,
            "cor": "#9b59b6",
            "area": "500m²",
            "quartos": 0,
            "banheiros": 2,
            "vagas": 4,
            "foto": "https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=300"
        },
        {
            "titulo": "Apartamento 1 quarto Jurerê Internacional",
            "preco": "R$ 320.000",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/apartamento-1-quarto-jurere-internacional",
            "localizacao": "Jurerê Internacional, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.46,
            "lng": -48.5,
            "cor": "#1abc9c",
            "area": "45m²",
            "quartos": 1,
            "banheiros": 1,
            "vagas": 1,
            "foto": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=300"
        },
        {
            "titulo": "Casa 4 quartos Campeche - Próximo à praia",
            "preco": "R$ 920.000",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/casa-4-quartos-campeche-proximo-praia",
            "localizacao": "Campeche, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.68,
            "lng": -48.49,
            "cor": "#e67e22",
            "area": "220m²",
            "quartos": 4,
            "banheiros": 3,
            "vagas": 2,
            "foto": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=300"
        },
        {
            "titulo": "Cobertura duplex Ingleses - Vista panorâmica",
            "preco": "R$ 1.200.000",
            "link": "https://www.olx.com.br/sc/florianopolis/imoveis/cobertura-duplex-ingleses-vista-panoramica",
            "localizacao": "Ingleses, Florianópolis, SC",
            "fonte": "OLX",
            "tipo": "simulado",
            "lat": -27.43,
            "lng": -48.39,
            "cor": "#34495e",
            "area": "150m²",
            "quartos": 3,
            "banheiros": 2,
            "vagas": 2,
            "foto": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=300"
        }
    ]

def geocodificar_endereco(endereco):
    '''
    Geocodifica um endereço para obter coordenadas
    '''
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': endereco,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'BR'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass

    return None, None

if __name__ == "__main__":
    # Tentar buscar imóveis reais na OLX
    imoveis_olx = buscar_imoveis_olx('florianopolis', 'imoveis', 8)

    # Se não conseguiu dados reais, usar dados simulados
    if not imoveis_olx:
        print("Não foi possível obter dados reais da OLX. Usando dados simulados realistas...")
        imoveis_olx = dados_simulados_olx()
    else:
        print(f'Encontrados {len(imoveis_olx)} imóveis reais na OLX:')

        # Adicionar coordenadas aos imóveis
        for i, imovel in enumerate(imoveis_olx, 1):
            # Tentar geocodificar baseado no título (que geralmente contém bairro)
            lat, lng = geocodificar_endereco(f"{imovel['titulo']}, Florianópolis, SC")

            if lat and lng:
                imovel['lat'] = lat
                imovel['lng'] = lng
                imovel['cor'] = '#3498db'  # Azul para imóveis reais
            else:
                # Coordenadas padrão para o centro de Florianópolis se não conseguir geocodificar
                imovel['lat'] = -27.597
                imovel['lng'] = -48.549
                imovel['cor'] = '#95a5a6'  # Cinza para imóveis sem coordenadas precisas

            print(f'{i}. {imovel["titulo"]}')
            print(f'   Preço: {imovel["preco"]}')
            print(f'   Coordenadas: {imovel["lat"]}, {imovel["lng"]}')
            print(f'   Link: {imovel["link"]}')
            print()

    # Salvar em JSON para usar no mapa
    with open('imoveis_olx.json', 'w', encoding='utf-8') as f:
        json.dump(imoveis_olx, f, ensure_ascii=False, indent=2)

    print(f"Dados salvos em imoveis_olx.json ({len(imoveis_olx)} imóveis)")