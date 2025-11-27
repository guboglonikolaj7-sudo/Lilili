// frontend/src/App.tsx
import { useCallback, useEffect, useMemo, useState } from 'react';
import LoginForm from './components/LoginForm';
import { OrderList } from './components/OrderList';
import { OrderForm } from './components/OrderForm';
import SupplierList from './components/SupplierList';
import ChatModal from './components/ChatModal';
import { SearchBar } from './components/SearchBar';

const PRIORITY_COUNTRIES = [
  'Китай',
  'Турция',
  'Индия',
  'Россия',
  'Казахстан',
  'Узбекистан',
  'Кыргызстан',
  'Азербайджан',
];

function App() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  const [selectedOrderId, setSelectedOrderId] = useState<number | null>(null);
  const [search, setSearch] = useState('');
  const [country, setCountry] = useState('');

  useEffect(() => {
    setToken(localStorage.getItem('token'));
  }, []);

  const handleLogin = useCallback(() => {
    setToken(localStorage.getItem('token'));
  }, []);

  const handleLogout = useCallback(() => {
    localStorage.removeItem('token');
    setToken(null);
  }, []);

  const isAuthenticated = useMemo(() => Boolean(token), [token]);

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-4 py-4 flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="uppercase text-xs font-semibold text-emerald-600 tracking-widest">
              Постащик.ру • Supplier Trust Platform
            </p>
            <h1 className="text-2xl font-bold text-slate-900">Проверка поставщиков</h1>
            <p className="text-sm text-slate-500">
              Автоматические запросы в ФССП, РНП, ЕГРЮЛ и локальные реестры Китая, Турции, Индии, стран СНГ
            </p>
          </div>
          {isAuthenticated && (
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-semibold text-red-600 border border-red-200 rounded-lg hover:bg-red-50 transition"
            >
              Выйти
            </button>
          )}
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
        {!isAuthenticated ? (
          <div className="max-w-lg mx-auto bg-white p-6 rounded-2xl shadow-sm">
            <LoginForm onLogin={handleLogin} />
          </div>
        ) : (
          <>
            <section className="bg-white rounded-2xl shadow-sm p-6">
              <div className="flex flex-col gap-4">
                <div>
                  <h2 className="text-xl font-semibold">Поиск и фильтры</h2>
                  <p className="text-sm text-slate-500">
                    Настройте страну и ключевые слова для быстрого отбора поставщиков
                  </p>
                </div>
                <SearchBar
                  search={search}
                  setSearch={setSearch}
                  country={country}
                  setCountry={setCountry}
                  countries={PRIORITY_COUNTRIES}
                />
              </div>
            </section>

            <section className="grid gap-6 lg:grid-cols-2">
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <h2 className="text-xl font-semibold mb-4">Создать заказ</h2>
                <OrderForm />
              </div>
              <div className="bg-white rounded-2xl shadow-sm p-6">
                <OrderList onOpenChat={setSelectedOrderId} />
              </div>
            </section>

            <SupplierList searchTerm={search} country={country} />
          </>
        )}
      </main>

      {selectedOrderId && (
        <ChatModal orderId={selectedOrderId} onClose={() => setSelectedOrderId(null)} />
      )}
    </div>
  );
}

export default App;