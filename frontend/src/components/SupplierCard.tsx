import React from "react";

export interface Supplier {
  id: number;
  name: string;
  country: string;
  city: string;
  logo: string | null;
  moq: number;
  description?: string;
  category: { name: string };
}

export const SupplierCard: React.FC<{ s: Supplier }> = ({ s }) => (
  <div className="border rounded p-4 w-72 shadow hover:shadow-lg transition">
    {s.logo && (
      <img
        src={`http://127.0.0.1:8000${s.logo}`}
        alt={s.name}
        className="h-32 w-full object-contain mb-2"
      />
    )}
    <h2 className="font-bold text-lg">{s.name}</h2>
    <p className="text-sm text-gray-600">
      {s.country}, {s.city}
    </p>
    <p className="text-sm">MOQ: {s.moq} шт.</p>
    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mt-2">
      {s.category.name}
    </span>
  </div>
);