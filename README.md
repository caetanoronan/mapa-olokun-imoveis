# Mapa Interativo – Imobiliária (Protótipo)

Aplicação web com React + Vite + Leaflet para visualização de imóveis em um mapa, com filtros por tipo e faixa de preço.

## Como rodar localmente (Windows PowerShell)

Pré-requisitos: Node.js 18+ e npm.

```powershell
# Dentro da pasta do projeto
npm install
npm run dev
# Abra o link mostrado (geralmente http://localhost:5173)
```

## Build de produção

```powershell
npm run build
npm run preview
```

## Deploy (Link público)

Você pode publicar facilmente em um destes serviços:

- Vercel (recomendado):
  1. Crie uma conta em https://vercel.com e instale o Vercel CLI (opcional).
  2. Faça login e importe o repositório do GitHub (ou use `vercel` no terminal).
  3. A plataforma detecta Vite automaticamente. Deploy sai com um URL público.

- GitHub Pages:
  1. Faça o build: `npm run build`.
  2. Publique a pasta `dist/` na branch `gh-pages` (pode usar a action `peaceiris/actions-gh-pages`).
  3. Ative Pages no repositório e use o link gerado.

## Estrutura

- `src/components/MapView.jsx` – Mapa e popups
- `src/components/Filters.jsx` – Filtros por tipo e preço
- `src/data/properties.js` – Dataset demonstrativo (5 tipos de imóveis)

## Créditos

- Mapas: OpenStreetMap
- Biblioteca de mapas: Leaflet + React-Leaflet

## Observações

- As imagens e links de tour/contato são placeholders. Substitua pelos seus.
- Para geocodificar endereços reais, sugere-se usar um serviço (Nominatim, Mapbox Geocoding, etc.) e gravar as coordenadas no dataset.
