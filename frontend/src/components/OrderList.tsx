// frontend/src/components/OrderList.tsx
import { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import clsx from 'clsx';
import type { Order } from '../types';

interface Props {
  onOpenChat?: (orderId: number) => void;
  className?: string;
}

const toNumber = (value?: number | string | null) => {
  if (typeof value === 'number') return value;
  if (typeof value === 'string' && value.trim().length) {
    const parsed = Number(value);
    return Number.isNaN(parsed) ? undefined : parsed;
  }
  return undefined;
};

const formatBudget = (min?: number | string | null, max?: number | string | null) => {
  const minNumber = toNumber(min);
  const maxNumber = toNumber(max);
  if (typeof minNumber !== 'number' && typeof maxNumber !== 'number') {
    return 'Бюджет не указан';
  }
  const formatter = new Intl.NumberFormat('ru-RU');
  if (typeof minNumber === 'number' && typeof maxNumber === 'number') {
    return `${formatter.format(minNumber)} – ${formatter.format(maxNumber)} ₽`;
  }
  if (typeof minNumber === 'number') {
    return `от ${formatter.format(minNumber)} ₽`;
  }
  return `до ${formatter.format(maxNumber as number)} ₽`;
};

export const OrderList = ({ onOpenChat, className }: Props) => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setLoading(true);
    axios
      .get('http://127.0.0.1:8000/api/v1/orders/', {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
      .then((res) => {
        const payload = res.data;
        const normalized = Array.isArray(payload)
          ? payload
          : payload?.results ?? [];
        setOrders(normalized);
        setError(null);
      })
      .catch((err) => {
        console.error(err);
        setError('Не удалось загрузить список заказов');
      })
      .finally(() => setLoading(false));
  }, []);

  const content = useMemo(() => {
    if (loading) {
      return <div className="text-center p-4">Загрузка...</div>;
    }
    if (error) {
      return (
        <div className="text-center p-4 text-red-600 bg-red-50 rounded">
          {error}
        </div>
      );
    }
    if (!orders.length) {
      return (
        <div className="text-center p-4 text-gray-500 bg-white rounded shadow">
          Активных заказов пока нет
        </div>
      );
    }
    return (
      <div className="space-y-4">
        {orders.map((order) => (
          <div key={order.id} className="bg-white shadow-md rounded-lg p-6">
            <h3 className="text-xl font-semibold">{order.title}</h3>
            <p className="text-gray-600 mt-2">{order.description}</p>
            <div className="flex flex-wrap justify-between gap-4 mt-4">
              <span className="text-green-600 font-bold">
                Бюджет:{' '}
                {formatBudget(
                  order.budget_min as number | string | null,
                  order.budget_max as number | string | null,
                )}
              </span>
              {typeof onOpenChat === 'function' && (
                <button
                  onClick={() => onOpenChat(order.id)}
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
                >
                  Перейти в чат
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    );
  }, [error, loading, onOpenChat, orders]);

  return (
    <section className={clsx('space-y-4', className)}>
      <h2 className="text-2xl font-bold">Активные заказы</h2>
      {content}
    </section>
  );
};