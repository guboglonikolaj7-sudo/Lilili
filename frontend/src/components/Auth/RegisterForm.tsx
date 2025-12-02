import React, { useState } from 'react';
import { authAPI } from '../../api/api';
import { useNavigate } from 'react-router-dom';

export const RegisterForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '', password: '', password_confirm: '', first_name: '', last_name: '', company_name: '', country: '', city: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.password_confirm) {
      setError('ароли не совпадают');
      return;
    }
    try {
      await authAPI.register(formData);
      setSuccess(true);
      setError('');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'шибка регистрации');
    }
  };

  if (success) {
    return <div className="max-w-md mx-auto mt-10 p-6 bg-green-100 rounded-lg"><h2 className="text-2xl font-bold text-green-800">егистраци€ успешна!</h2><p className="text-green-600">ереход на страницу входа...</p></div>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">егистраци€ в Lilili B2B</h2>
      {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div><label className="block mb-2 font-medium">Email *</label><input type="email" name="email" value={formData.email} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" required /></div>
          <div><label className="block mb-2 font-medium">ароль *</label><input type="password" name="password" value={formData.password} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" required /></div>
          <div><label className="block mb-2 font-medium">одтвердите пароль *</label><input type="password" name="password_confirm" value={formData.password_confirm} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" required /></div>
          <div><label className="block mb-2 font-medium">м€</label><input type="text" name="first_name" value={formData.first_name} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">амили€</label><input type="text" name="last_name" value={formData.last_name} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">омпани€</label><input type="text" name="company_name" value={formData.company_name} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">—трана</label><input type="text" name="country" value={formData.country} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">ород</label><input type="text" name="city" value={formData.city} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
        </div>
        <button type="submit" className="w-full bg-indigo-600 text-white py-3 rounded-lg font-bold hover:bg-indigo-700">арегистрироватьс€</button>
      </form>
    </div>
  );
};
