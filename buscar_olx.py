import requests
from bs4 import BeautifulSoup
import json
import re

def buscar_imoveis_olx(cidade='florianopolis', tipo='imoveis', max_imoveis=10):
    '''
    Busca imóveis na OLX usando web scraping
    '''
    url = f'https://sc.olx.com.br/{cidade}/{tipo}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
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
                    preco_elem = anuncio.find('span', class_=re.compile(r'.*price.*')) or anuncio.find('span', string=re.compile(r'R\$'))
                    preco = preco_elem.text.strip() if preco_elem else 'Preço não encontrado'

                    # Extrair link
                    link_elem = anuncio.find('a')
                    link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else '#'
                    if not link.startswith('http'):
                        link = 'https://olx.com.br' + link

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
    # Buscar imóveis na OLX
    imoveis_olx = buscar_imoveis_olx('florianopolis', 'imoveis', 5)

    print(f'Encontrados {len(imoveis_olx)} imóveis na OLX:')

    # Adicionar coordenadas aos imóveis
    for i, imovel in enumerate(imoveis_olx, 1):
        # Tentar geocodificar baseado no título (que geralmente contém bairro)
        lat, lng = geocodificar_endereco(f"{imovel['titulo']}, Florianópolis, SC")

        if lat and lng:
            imovel['lat'] = lat
            imovel['lng'] = lng
        else:
            # Coordenadas padrão para o centro de Florianópolis se não conseguir geocodificar
            imovel['lat'] = -27.597
            imovel['lng'] = -48.549

        print(f'{i}. {imovel["titulo"]}')
        print(f'   Preço: {imovel["preco"]}')
        print(f'   Coordenadas: {imovel["lat"]}, {imovel["lng"]}')
        print(f'   Link: {imovel["link"]}')
        print()

    # Salvar em JSON para usar no mapa
    with open('imoveis_olx.json', 'w', encoding='utf-8') as f:
        json.dump(imoveis_olx, f, ensure_ascii=False, indent=2)

    print("Dados salvos em imoveis_olx.json")