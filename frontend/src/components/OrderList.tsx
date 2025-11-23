// frontend/src/components/OrderList.tsx
import { useEffect, useState } from 'react';
import axios from 'axios';

interface Order {
  id: number;
  title: string;
  description: string;
  budget_min: string;
  budget_max: string;
}

interface Props {
  onOpenChat?: (orderId: number) => void;
}

export const OrderList = ({ onOpenChat }: Props) => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/v1/orders/')
      .then(res => setOrders(res.data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center p-4">Загрузка...</div>;

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-6">Активные заказы</h2>
      {orders.map(order => (
        <div key={order.id} className="bg-white shadow-md rounded-lg p-6 mb-4">
          <h3 className="text-xl font-semibold">{order.title}</h3>
          <p className="text-gray-600 mt-2">{order.description}</p>
          <div className="flex justify-between mt-4">
            <span className="text-green-600 font-bold">
              Бюджет: {order.budget_min} - {order.budget_max} ₽
            </span>
            {onOpenChat && (
              <button
                onClick={() => onOpenChat(order.id)}
                className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              >
                Перейти в чат
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};