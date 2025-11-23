// frontend/src/App.tsx
import { useState, useEffect } from 'react';
import LoginForm from './components/LoginForm';
import { OrderList } from './components/OrderList';
import { OrderForm } from './components/OrderForm';
import SupplierList from './components/SupplierList';
import ChatModal from './components/ChatModal';

function App() {
  const [token, setToken] = useState<string | null>(null);
  const [selectedOrderId, setSelectedOrderId] = useState<number | null>(null);

  useEffect(() => {
    setToken(localStorage.getItem('token'));
  }, []);

  const handleLogin = () => {
    setToken(localStorage.getItem('token'));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm p-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">📦 ПОСТАВЩИК.РУ</h1>
          {token && (
            <button onClick={handleLogout} className="text-red-500 hover:text-red-700">
              Выйти
            </button>
          )}
        </div>
      </header>
      <main className="py-6">
        {!token ? (
          <LoginForm onLogin={handleLogin} />
        ) : (
          <>
            <OrderForm />
            <OrderList onOpenChat={setSelectedOrderId} />
            <SupplierList />
          </>
        )}
        {selectedOrderId && (
          <ChatModal orderId={selectedOrderId} onClose={() => setSelectedOrderId(null)} />
        )}
      </main>
    </div>
  );
}

export default App;