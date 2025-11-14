# Relatório – Mapa Interativo para Imobiliária Digital

## 1. Plataforma Utilizada
O protótipo foi desenvolvido como uma aplicação web usando **React (Vite)** para a interface e **Leaflet + React-Leaflet** para visualização geográfica. Os tiles do mapa são fornecidos pelo OpenStreetMap. Esta abordagem permite alta customização, integração futura com APIs e fácil publicação (Vercel / GitHub Pages).

## 2. Etapas de Criação
1. Definição do objetivo de negócio: facilitar a descoberta e comparação de imóveis.
2. Estruturação inicial do projeto (Vite + React) e instalação das dependências de mapa.
3. Criação de um dataset demonstrativo com cinco tipos distintos de imóveis, incluindo atributos chave (tipo, endereço, coordenadas, áreas, dormitórios, banheiros, vagas, preço, links).
4. Implementação do componente de mapa (`MapView.jsx`) exibindo marcadores e popups detalhados.
5. Implementação de filtros dinâmicos por tipo de imóvel, faixa de preço, transação (venda/aluguel) e mínimo de dormitórios (`Filters.jsx`).
6. Adição de clusterização de marcadores, ícones SVG personalizados por tipo, legenda recolhível e contador de imóveis filtrados.
7. Aplicação da paleta ColorBrewer BuGn para visual consistente e limites de zoom (min 10, max 18).
8. Ajustes de layout responsivo e estilização para facilitar navegação.
9. Criação de documentação (`README.md`) e deste relatório.
10. Preparação para deploy: projeto pronto para ser importado em Vercel e gerar URL público.

## 3. Tipos de Imóveis Representados
- Casa residencial (5 exemplares)
- Apartamento (5 exemplares)
- Sala comercial (5 exemplares)
- Terreno (5 exemplares)
- Galpão industrial (5 exemplares)

Total: 25 imóveis demonstrativos, cada um com atributos relevantes: localização, áreas, dormitórios, banheiros, vagas, tipo de transação (venda/aluguel), valor, foto e links de contato/tour.

## 4. Valor para o Negócio
O mapa interativo agrega valor ao processo comercial da imobiliária ao:
- Centralizar informações antes dispersas em planilhas e documentos físicos.
- Melhorar a experiência do usuário através de navegação geográfica intuitiva com ícones visuais por tipo.
- Acelerar a comparação entre opções (filtros avançados por tipo, preço, transação e dormitórios).
- Reduzir tempo de atendimento inicial disponibilizando detalhes completos e links de contato/tour.
- Criar base para métricas futuras (ex.: cliques por região, interesse por faixa de preço) e extensão com funcionalidades como desenho de área de interesse ou integração com CRM.

## 5. Funcionalidades Implementadas
- Mapa interativo com tiles OpenStreetMap.
- Marcadores clusterizados com ícones SVG personalizados por tipo de imóvel.
- Popups detalhados com fotos, atributos e links.
- Filtros por tipo, preço, transação e dormitórios.
- Legenda recolhível no mapa.
- Contador dinâmico de imóveis filtrados no cabeçalho.
- Design responsivo com paleta BuGn.
- Limites de zoom para melhor usabilidade.

## 6. Link Público
O mapa está publicado em: [INSIRA O LINK DO VERCEL AQUI, ex: https://mapa-olokun-imoveis.vercel.app]

## 7. Próximas Melhorias (Sugestões)
- Geocodificação automática de novos endereços.
- Integração com API para dados em tempo real.
- Modo de comparação lado a lado.
- Filtros adicionais (banheiros, vagas, área).
- Análise de dados (estatísticas de visualizações).

## 8. Exportação
Para entregar em PDF: abra este arquivo e exporte usando sua IDE ou converta via uma ferramenta como `pandoc`:

```
pandoc Mapa_Imobiliaria_CaetanoRonan.md -o Mapa_Imobiliaria_CaetanoRonan.pdf
```

---
Relatório gerado em: 2025-11-14