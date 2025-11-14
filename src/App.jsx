import React, { useMemo, useState } from 'react';
import MapView from './components/MapView.jsx';
import Filters from './components/Filters.jsx';
import properties from './data/properties.js';

export default function App() {
  const [selectedTypes, setSelectedTypes] = useState([]); // empty => all
  const [priceRange, setPriceRange] = useState([0, 10000000]);
  const [transactionTypes, setTransactionTypes] = useState([]); // [] => todas (venda/aluguel)
  const [minBedrooms, setMinBedrooms] = useState(0); // 0 => qualquer

  const filtered = useMemo(() => {
    return properties.filter((p) => {
      const typeOk = selectedTypes.length === 0 || selectedTypes.includes(p.type);
      const priceOk = p.price >= priceRange[0] && p.price <= priceRange[1];
      const transactionOk = transactionTypes.length === 0 || transactionTypes.includes(p.priceType);
      const bedroomsOk = minBedrooms === 0 || (p.bedrooms !== null && p.bedrooms >= minBedrooms);
      return typeOk && priceOk && transactionOk && bedroomsOk;
    });
  }, [selectedTypes, priceRange, transactionTypes, minBedrooms]);

  const allTypes = useMemo(() => {
    const set = new Set(properties.map((p) => p.type));
    return Array.from(set);
  }, []);

  return (
    <div className="app">
      <header className="app__header">
        <h1>Olokun Imoveis</h1>
        <p>Exibindo {filtered.length} imóveis. Visualize imóveis por tipo, transação e faixa de preço. Use os filtros para comparar e planejar visitas.</p>
      </header>
      <div className="app__content">
        <aside className="sidebar">
          <Filters
            allTypes={allTypes}
            selectedTypes={selectedTypes}
            onTypesChange={setSelectedTypes}
            priceRange={priceRange}
            onPriceRangeChange={setPriceRange}
            transactionTypes={transactionTypes}
            onTransactionTypesChange={setTransactionTypes}
            minBedrooms={minBedrooms}
            onMinBedroomsChange={setMinBedrooms}
          />
        </aside>
        <main className="main">
          <MapView properties={filtered} />
        </main>
      </div>
      <footer className="app__footer">
        <small>Dados demonstrativos. Tiles © OpenStreetMap contributors.</small>
      </footer>
    </div>
  );
}
