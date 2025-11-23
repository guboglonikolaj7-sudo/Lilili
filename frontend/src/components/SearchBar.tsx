import React from "react";

interface Props {
  search: string;
  setSearch: (v: string) => void;
  country: string;
  setCountry: (v: string) => void;
  countries: string[];
}

export const SearchBar: React.FC<Props> = ({
  search,
  setSearch,
  country,
  setCountry,
  countries,
}) => (
  <div className="flex flex-wrap gap-4 mb-6 items-center">
    <input
      type="text"
      placeholder="Поиск по названию / описанию"
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="border px-3 py-2 rounded w-64"
    />
    <select
      value={country}
      onChange={(e) => setCountry(e.target.value)}
      className="border px-3 py-2 rounded"
    >
      <option value="">Все страны</option>
      {countries.map((c) => (
        <option key={c} value={c}>
          {c}
        </option>
      ))}
    </select>
    <button
      onClick={() => (setSearch(""), setCountry(""))}
      className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
    >
      Сбросить
    </button>
  </div>
);