// frontend/src/components/OrderForm.tsx
import { useState } from 'react';
import axios from 'axios';

export const OrderForm = () => {
  const [form, setForm] = useState({
    title: '',
    description: '',
    budget_min: '',
    budget_max: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Сначала войдите!');
      return;
    }
    await axios.post('http://127.0.0.1:8000/api/v1/orders/create/', form, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert('Заказ создан!');
    window.location.reload();
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-4 bg-white rounded shadow mb-6">
      <h3 className="text-xl font-bold mb-4">Создать заказ</h3>
      <input 
        type="text" 
        placeholder="Название заказа"
        className="w-full p-2 border mb-3"
        value={form.title}
        onChange={e => setForm({...form, title: e.target.value})}
        required
      />
      <textarea 
        placeholder="Описание"
        className="w-full p-2 border mb-3"
        value={form.description}
        onChange={e => setForm({...form, description: e.target.value})}
        rows={3}
        required
      />
      <div className="flex gap-3 mb-3">
        <input 
          type="number" 
          placeholder="Бюджет от"
          className="w-1/2 p-2 border"
          value={form.budget_min}
          onChange={e => setForm({...form, budget_min: e.target.value})}
          required
        />
        <input 
          type="number" 
          placeholder="Бюджет до"
          className="w-1/2 p-2 border"
          value={form.budget_max}
          onChange={e => setForm({...form, budget_max: e.target.value})}
          required
        />
      </div>
      <button type="submit" className="bg-green-500 text-white px-6 py-2 rounded">
        Создать заказ
      </button>
    </form>
  );
};