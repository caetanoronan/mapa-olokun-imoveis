import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

def buscar_imoveis_vivareal(cidade='florianopolis', estado='santa-catarina', max_imoveis=10):
    '''
    Busca imóveis no Viva Real para ALUGUEL usando web scraping
    '''
    url = f'https://www.vivareal.com.br/aluguel/{estado}/{cidade}/'
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
        print(f"Status da requisição Viva Real: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            imoveis = []

            # Seletores para Viva Real
            anuncios = soup.find_all('article', class_=re.compile(r'.*property-card.*'))[:max_imoveis]

            print(f"Encontrados {len(anuncios)} possíveis anúncios no Viva Real")

            for anuncio in anuncios:
                try:
                    # Extrair título
                    titulo_elem = anuncio.find('span', class_=re.compile(r'.*property-card__title.*')) or anuncio.find('h2')
                    titulo = titulo_elem.text.strip() if titulo_elem else 'Título não encontrado'

                    # Extrair preço
                    preco_elem = anuncio.find('div', class_=re.compile(r'.*property-card__price.*'))
                    preco = preco_elem.text.strip() if preco_elem else 'Preço não encontrado'

                    # Extrair link
                    link_elem = anuncio.find('a', class_=re.compile(r'.*property-card__content-link.*'))
                    link = link_elem.get('href') if link_elem else '#'
                    if link and not str(link).startswith('http'):
                        link = 'https://www.vivareal.com.br' + str(link)

                    # Extrair localização
                    local_elem = anuncio.find('span', class_=re.compile(r'.*property-card__address.*'))
                    localizacao = local_elem.text.strip() if local_elem else f'{cidade}, {estado}'

                    # Extrair área, quartos, etc.
                    detalhes = anuncio.find_all('li', class_=re.compile(r'.*property-card__detail.*'))
                    area = quartos = banheiros = vagas = 'N/A'
                    for detalhe in detalhes:
                        text = detalhe.text.strip()
                        if 'm²' in text:
                            area = text
                        elif 'Quartos' in text or 'Quarto' in text:
                            quartos = re.search(r'\d+', text).group() if re.search(r'\d+', text) else 0
                        elif 'Banheiros' in text or 'Banheiro' in text:
                            banheiros = re.search(r'\d+', text).group() if re.search(r'\d+', text) else 0
                        elif 'Vagas' in text or 'Vaga' in text:
                            vagas = re.search(r'\d+', text).group() if re.search(r'\d+', text) else 0

                    # Pular se não tem título ou preço válido
                    if titulo == 'Título não encontrado' or preco == 'Preço não encontrado':
                        continue

                    imovel = {
                        'titulo': titulo,
                        'preco': preco,
                        'link': link,
                        'localizacao': localizacao,
                        'fonte': 'Viva Real',
                        'tipo': 'real',
                        'area': area,
                        'quartos': quartos,
                        'banheiros': banheiros,
                        'vagas': vagas
                    }

                    imoveis.append(imovel)

                except Exception as e:
                    continue

            return imoveis

    except Exception as e:
        print(f'Erro na busca Viva Real: {e}')

    return []

def dados_simulados_vivareal():
    '''
    Retorna dados simulados mas realistas do Viva Real para ALUGUEL quando o scraping falha
    '''
    return [
        {
            "titulo": "Apartamento 2 quartos Centro - Vista parcial mar",
            "preco": "R$ 3.500/mês",
            "link": "https://www.vivareal.com.br/imovel/apartamento-2-quartos-centro-vista-parcial-mar-65m2-2vagas-garagem-101234567/",
            "localizacao": "Centro, Florianópolis - SC",
            "fonte": "Viva Real",
            "tipo": "simulado",
            "lat": -27.596123,
            "lng": -48.549456,
            "cor": "#e74c3c",
            "area": "65m²",
            "quartos": 2,
            "banheiros": 1,
            "vagas": 2,
            "foto": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=300"
        },
        {
            "titulo": "Casa 3 quartos Lagoa da Conceição - Próximo ao mar",
            "preco": "R$ 4.500/mês",
            "link": "https://www.vivareal.com.br/imovel/casa-3-quartos-lagoa-conceicao-proximo-mar-180m2-2vagas-garagem-101234568/",
            "localizacao": "Lagoa da Conceição, Florianópolis - SC",
            "fonte": "Viva Real",
            "tipo": "simulado",
            "lat": -27.575678,
            "lng": -48.460123,
            "cor": "#27ae60",
            "area": "180m²",
            "quartos": 3,
            "banheiros": 2,
            "vagas": 2,
            "foto": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=300"
        },
        {
            "titulo": "Sala comercial Rua Felipe Schmidt - Centro Executivo",
            "preco": "R$ 8.000/mês",
            "link": "https://www.vivareal.com.br/imovel/sala-comercial-rua-felipe-schmidt-centro-executivo-50m2-101234569/",
            "localizacao": "Centro, Florianópolis - SC",
            "fonte": "Viva Real",
            "tipo": "simulado",
            "lat": -27.596789,
            "lng": -48.549012,
            "cor": "#f39c12",
            "area": "50m²",
            "quartos": 0,
            "banheiros": 1,
            "vagas": 0,
            "foto": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=300"
        },
        {
            "titulo": "Terreno 400m² Santo Antônio de Lisboa",
            "preco": "R$ 1.200/mês",
            "link": "https://www.vivareal.com.br/imovel/terreno-400m2-santo-antonio-lisboa-101234570/",
            "localizacao": "Santo Antônio de Lisboa, Florianópolis - SC",
            "fonte": "Viva Real",
            "tipo": "simulado",
            "lat": -27.506789,
            "lng": -48.518456,
            "cor": "#9b59b6",
            "area": "400m²",
            "quartos": 0,
            "banheiros": 0,
            "vagas": 0,
            "foto": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=300"
        },
        {
            "titulo": "Apartamento 1 quarto Jurerê - Praia particular",
            "preco": "R$ 6.500/mês",
            "link": "https://www.vivareal.com.br/imovel/apartamento-1-quarto-jurere-praia-particular-45m2-1vaga-garagem-101234571/",
            "localizacao": "Jurerê, Florianópolis - SC",
            "fonte": "Viva Real",
            "tipo": "simulado",
            "lat": -27.450123,
            "lng": -48.480456,
            "cor": "#1abc9c",
            "area": "45m²",
            "quartos": 1,
            "banheiros": 1,
            "vagas": 1,
            "foto": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=300"
        },
        {
            "titulo": "Casa 4 quartos Campeche - Lazer completo",
            "preco": "R$ 7.000/mês",
            "link": "https://www.vivareal.com.br/imovel/casa-4-quartos-campeche-lazer-completo-240m2-2vagas-garagem-101234572/",
            "localizacao": "Campeche, Florianópolis - SC",
            "fonte": "Viva Real",
            "tipo": "simulado",
            "lat": -27.670456,
            "lng": -48.480789,
            "cor": "#e67e22",
            "area": "240m²",
            "quartos": 4,
            "banheiros": 3,
            "vagas": 2,
            "foto": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=300"
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
    # Tentar buscar imóveis reais no Viva Real
    imoveis_vr = buscar_imoveis_vivareal('florianopolis', 'santa-catarina', 8)

    # Se não conseguiu dados reais, usar dados simulados
    if not imoveis_vr:
        print("Não foi possível obter dados reais do Viva Real. Usando dados simulados realistas...")
        imoveis_vr = dados_simulados_vivareal()
    else:
        print(f'Encontrados {len(imoveis_vr)} imóveis reais no Viva Real:')

        # Adicionar coordenadas aos imóveis
        for i, imovel in enumerate(imoveis_vr, 1):
            # Tentar geocodificar baseado na localização
            lat, lng = geocodificar_endereco(imovel['localizacao'])

            if lat and lng:
                imovel['lat'] = lat
                imovel['lng'] = lng
                imovel['cor'] = '#e74c3c'  # Vermelho para Viva Real
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
    with open('imoveis_vivareal.json', 'w', encoding='utf-8') as f:
        json.dump(imoveis_vr, f, ensure_ascii=False, indent=2)

    print(f"Dados salvos em imoveis_vivareal.json ({len(imoveis_vr)} imóveis)")