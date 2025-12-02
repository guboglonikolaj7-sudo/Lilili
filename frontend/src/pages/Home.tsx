import React from 'react';
import { Link } from 'react-router-dom';

export const Home: React.FC = () => {
  return (
    <div className="text-center py-16">
      <h1 className="text-6xl font-bold text-indigo-600 mb-6">Lilili B2B Platform</h1>
      <p className="text-xl text-gray-700 mb-8 max-w-3xl mx-auto">
        айдите проверенных поставщиков из 83 категорий. Создавайте закупки, получайте предложения, общайтесь в real-time чате.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 my-16">
        {[
          { number: '10,000+', label: 'ерифицированных поставщиков' },
          { number: '83', label: 'атегории товаров' },
          { number: 'Real-time', label: 'ат с поставщиками' },
        ].map((stat) => (
          <div key={stat.label} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
            <h3 className="text-3xl font-bold text-indigo-600 mb-2">{stat.number}</h3>
            <p className="text-gray-600">{stat.label}</p>
          </div>
        ))}
      </div>
      <div className="space-x-4">
        <Link to="/suppliers" className="bg-indigo-600 text-white px-8 py-4 rounded-xl text-lg hover:bg-indigo-700 transition shadow-lg">айти поставщиков</Link>
        <Link to="/rfq" className="bg-green-600 text-white px-8 py-4 rounded-xl text-lg hover:bg-green-700 transition shadow-lg">Создать закупку</Link>
      </div>
    </div>
  );
};
