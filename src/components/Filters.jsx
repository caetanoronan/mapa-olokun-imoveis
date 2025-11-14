import React, { useMemo, useState } from 'react';

export default function Filters({
  allTypes,
  selectedTypes,
  onTypesChange,
  priceRange,
  onPriceRangeChange,
  transactionTypes,
  onTransactionTypesChange,
  minBedrooms,
  onMinBedroomsChange,
}) {
  const [min, max] = priceRange;
  const [localMin, setLocalMin] = useState(min);
  const [localMax, setLocalMax] = useState(max);

  const options = useMemo(() => allTypes.sort(), [allTypes]);

  function toggleType(type) {
    if (selectedTypes.includes(type)) {
      onTypesChange(selectedTypes.filter((t) => t !== type));
    } else {
      onTypesChange([...selectedTypes, type]);
    }
  }

  function applyPriceRange(e) {
    e.preventDefault();
    const m1 = Number(localMin) || 0;
    const m2 = Number(localMax) || 999999999;
    onPriceRangeChange([Math.min(m1, m2), Math.max(m1, m2)]);
  }

  function clearFilters() {
    onTypesChange([]);
    onPriceRangeChange([0, 10000000]);
    onTransactionTypesChange([]);
    onMinBedroomsChange(0);
    setLocalMin(0);
    setLocalMax(10000000);
  }

  return (
    <div className="filters">
      <h2>Filtros</h2>

      <section className="filters__section">
        <h3>Tipo de imóvel</h3>
        <div className="filters__list">
          {options.map((type) => (
            <label key={type} className="filters__checkbox">
              <input
                type="checkbox"
                checked={selectedTypes.includes(type)}
                onChange={() => toggleType(type)}
              />
              <span>{type}</span>
            </label>
          ))}
        </div>
      </section>

      <section className="filters__section">
        <h3>Transação</h3>
        <div className="filters__list">
          {['venda', 'aluguel'].map((tx) => (
            <label key={tx} className="filters__checkbox">
              <input
                type="checkbox"
                checked={transactionTypes.includes(tx)}
                onChange={() => {
                  if (transactionTypes.includes(tx)) {
                    onTransactionTypesChange(transactionTypes.filter((t) => t !== tx));
                  } else {
                    onTransactionTypesChange([...transactionTypes, tx]);
                  }
                }}
              />
              <span style={{ textTransform: 'capitalize' }}>{tx}</span>
            </label>
          ))}
          <button className="btn btn--ghost" onClick={() => onTransactionTypesChange([])}>Todos</button>
        </div>
      </section>

      <section className="filters__section">
        <h3>Dormitórios (mín.)</h3>
        <select
          value={minBedrooms}
          onChange={(e) => onMinBedroomsChange(Number(e.target.value))}
          style={{ width: '100%', padding: '6px 8px', border: '1px solid #ddd', borderRadius: '6px' }}
        >
          <option value={0}>Qualquer</option>
          <option value={1}>1+</option>
          <option value={2}>2+</option>
          <option value={3}>3+</option>
          <option value={4}>4+</option>
        </select>
      </section>

      <section className="filters__section">
        <h3>Faixa de preço (R$)</h3>
        <form onSubmit={applyPriceRange} className="filters__price">
          <input
            type="number"
            value={localMin}
            min={0}
            step={500}
            onChange={(e) => setLocalMin(e.target.value)}
            placeholder="Mín"
          />
          <span>—</span>
          <input
            type="number"
            value={localMax}
            min={0}
            step={500}
            onChange={(e) => setLocalMax(e.target.value)}
            placeholder="Máx"
          />
          <button type="submit">Aplicar</button>
        </form>
      </section>

      <div className="filters__actions">
        <button className="btn btn--ghost" onClick={clearFilters}>Limpar filtros</button>
      </div>
    </div>
  );
}
