import React, { useMemo, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import MarkerClusterGroup from 'react-leaflet-cluster';
import L from 'leaflet';

// Fix default marker icons with Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).toString(),
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).toString(),
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).toString(),
});

export default function MapView({ properties }) {
  const center = useMemo(() => ({ lat: -27.5954, lng: -48.5480 }), []); // Florianópolis
  const [isLegendExpanded, setIsLegendExpanded] = useState(true);
  const [tilesLoaded, setTilesLoaded] = useState(false);

  // Build a custom color icon per type using DivIcon + CSS classes
  const iconsByType = useMemo(() => {
    const toKey = (type) => {
      if (!type) return 'default';
      if (type.toLowerCase().startsWith('casa')) return 'casa';
      if (type.toLowerCase().startsWith('apart')) return 'apartamento';
      if (type.toLowerCase().startsWith('sala')) return 'sala';
      if (type.toLowerCase().startsWith('terreno')) return 'terreno';
      if (type.toLowerCase().startsWith('galp')) return 'galpao';
      return 'default';
    };

    const svgFor = (key) => {
      switch (key) {
        case 'casa':
          return '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 3 3 10v11h6v-6h6v6h6V10z"/></svg>';
        case 'apartamento':
          return '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M4 3h10v18H4zM16 9h4v12h-4zM6 5v2h2V5zm0 4v2h2V9zm0 4v2h2v-2zm4-8v2h2V5zm0 4v2h2V9zm0 4v2h2v-2z"/></svg>';
        case 'sala':
          return '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M3 3h18v6H3zm2 8h14v10H5z"/></svg>';
        case 'terreno':
          return '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M3 5h18v4H3zm0 6h18v8H3z"/></svg>';
        case 'galpao':
          return '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2 2 9v13h6v-6h8v6h6V9z"/></svg>';
        default:
          return '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><circle cx="12" cy="12" r="10"/></svg>';
      }
    };

    const uniqueTypes = Array.from(new Set(properties.map(p => p.type)));
    const map = {};
    uniqueTypes.forEach((t) => {
      const key = toKey(t);
      map[t] = L.divIcon({
        className: 'cm-wrapper',
        html: `<div class=\"cm cm--${key}\">${svgFor(key)}</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -28],
      });
    });
    if (!map.default) {
      map.default = L.divIcon({ className: 'cm-wrapper', html: `<div class=\"cm cm--default\">${svgFor('default')}</div>`, iconSize: [32,32], iconAnchor: [16,32], popupAnchor: [0,-28] });
    }
    return map;
  }, [properties]);

  return (
    <MapContainer
      center={center}
      zoom={12}
      minZoom={10}
      maxZoom={18}
      style={{ height: '100%', width: '100%' }}
      scrollWheelZoom
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        eventHandlers={{
          tileload: () => setTilesLoaded(true),
          tileerror: () => setTilesLoaded(false),
        }}
      />
      <div className="legend">
        <div className="legend__header">
          <h4>Legenda</h4>
          <button
            className="legend__toggle"
            onClick={() => setIsLegendExpanded(!isLegendExpanded)}
            title={isLegendExpanded ? 'Recolher legenda' : 'Expandir legenda'}
          >
            {isLegendExpanded ? '−' : '+'}
          </button>
        </div>
        {isLegendExpanded && (
          <ul>
            <li><span className="cm cm--casa legend__icon"></span> Casa residencial</li>
            <li><span className="cm cm--apartamento legend__icon"></span> Apartamento</li>
            <li><span className="cm cm--sala legend__icon"></span> Sala comercial</li>
            <li><span className="cm cm--terreno legend__icon"></span> Terreno</li>
            <li><span className="cm cm--galpao legend__icon"></span> Galpão industrial</li>
          </ul>
        )}
      </div>
      <MarkerClusterGroup chunkedLoading maxClusterRadius={60} disableClusteringAtZoom={16}>
        {properties.map((p) => (
          <Marker key={p.id} position={[p.lat, p.lng]} icon={iconsByType[p.type] || iconsByType.default}>
            <Popup>
              <div className="popup">
                <img src={p.photo} alt={p.title} className="popup__img" />
                <div className="popup__body">
                  <h3 className="popup__title">{p.title}</h3>
                  <p className="popup__subtitle">{p.type} • {p.address}</p>
                  <ul className="popup__list">
                    {p.areaBuilt !== null && (
                      <li><strong>Área construída:</strong> {p.areaBuilt.toLocaleString('pt-BR')} m²</li>
                    )}
                    {p.areaLot !== null && (
                      <li><strong>Área do terreno:</strong> {p.areaLot.toLocaleString('pt-BR')} m²</li>
                    )}
                    {p.bedrooms !== null && (
                      <li><strong>Dormitórios:</strong> {p.bedrooms}</li>
                    )}
                    {p.bathrooms !== null && (
                      <li><strong>Banheiros:</strong> {p.bathrooms}</li>
                    )}
                    {p.parking !== null && (
                      <li><strong>Vagas:</strong> {p.parking}</li>
                    )}
                    <li><strong>Valor:</strong> {p.priceType === 'aluguel' ? 'Aluguel' : 'Venda'} • R$ {p.price.toLocaleString('pt-BR')}</li>
                  </ul>
                  <div className="popup__links">
                    {p.tour && <a href={p.tour} target="_blank" rel="noreferrer">Tour virtual</a>}
                    {p.contact && <a href={p.contact} target="_blank" rel="noreferrer">Contato</a>}
                  </div>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MarkerClusterGroup>
      <div className="debug-overlay">Marcadores: {properties.length} • Tiles: {tilesLoaded ? 'OK' : 'Carregando'}</div>
    </MapContainer>
  );
}
