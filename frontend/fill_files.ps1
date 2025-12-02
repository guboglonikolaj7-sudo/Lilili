# fill_files.ps1

# Определяем содержимое файлов
$files = @{
    "src\api\api.ts" = @'
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцептор для JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/users/login/', { email, password }),
  
  register: (data: any) =>
    api.post('/users/register/', data),
};

export const suppliersAPI = {
  getSuppliers: () => api.get('/suppliers/'),
  getSupplier: (id: number) => api.get(`/suppliers/${id}/`),
};

export const rfqAPI = {
  getRFQs: () => api.get('/orders/'),
  createRFQ: (data: any) => api.post('/orders/', data),
};
'@

    "src\types\types.ts" = @'
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  company_name?: string;
  country?: string;
  city?: string;
}

export interface Supplier {
  id: number;
  name: string;
  country: string;
  city: string;
  description: string;
  logo?: string;
  moq: number;
  verification_score?: number;
}

export interface RFQ {
  id: number;
  title: string;
  description: string;
  category: string;
  budget: number;
  deadline: string;
  status: 'active' | 'closed';
}
'@

    "src\components\Layout\Header.tsx" = @'
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.reload();
  };

  return (
    <header className="bg-indigo-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold hover:text-indigo-200">
          Lilili B2B Platform
        </Link>
        <nav className="flex items-center space-x-6">
          <Link to="/suppliers" className="hover:text-indigo-200 transition">
            Поставщики
          </Link>
          <Link to="/rfq" className="hover:text-indigo-200 transition">
            Закупки
          </Link>
          {isLoggedIn ? (
            <>
              <Link to="/profile" className="hover:text-indigo-200 transition">
                Профиль
              </Link>
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg transition"
              >
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-indigo-200 transition">
                Войти
              </Link>
              <Link
                to="/register"
                className="bg-white text-indigo-600 px-4 py-2 rounded-lg hover:bg-indigo-50 transition font-bold"
              >
                Регистрация
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};
'@

    "src\components\Auth\LoginForm.tsx" = @'
import React, { useState } from 'react';
import { authAPI } from '../../api/api';
import { useNavigate } from 'react-router-dom';

export const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await authAPI.login(formData.email, formData.password);
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      navigate('/profile');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка входа');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Вход в систему</h2>
      {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block mb-2">Email</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} className="w-full px-3 py-2 border rounded" required />
        </div>
        <div className="mb-4">
          <label className="block mb-2">Пароль</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} className="w-full px-3 py-2 border rounded" required />
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
          Войти
        </button>
      </form>
    </div>
  );
};
'@

    "src\components\Auth\RegisterForm.tsx" = @'
import React, { useState } from 'react';
import { authAPI } from '../../api/api';
import { useNavigate } from 'react-router-dom';

export const RegisterForm: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    company_name: '',
    country: '',
    city: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.password_confirm) {
      setError('Пароли не совпадают');
      return;
    }
    try {
      await authAPI.register(formData);
      setSuccess(true);
      setError('');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка регистрации');
    }
  };

  if (success) {
    return <div className="max-w-md mx-auto mt-10 p-6 bg-green-100 rounded-lg"><h2 className="text-2xl font-bold text-green-800">Регистрация успешна!</h2><p className="text-green-600">Переход на страницу входа...</p></div>;
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Регистрация в Lilili B2B</h2>
      {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div><label className="block mb-2 font-medium">Email *</label><input type="email" name="email" value={formData.email} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" required /></div>
          <div><label className="block mb-2 font-medium">Пароль *</label><input type="password" name="password" value={formData.password} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" required /></div>
          <div><label className="block mb-2 font-medium">Подтвердите пароль *</label><input type="password" name="password_confirm" value={formData.password_confirm} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" required /></div>
          <div><label className="block mb-2 font-medium">Имя</label><input type="text" name="first_name" value={formData.first_name} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">Фамилия</label><input type="text" name="last_name" value={formData.last_name} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">Компания</label><input type="text" name="company_name" value={formData.company_name} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">Страна</label><input type="text" name="country" value={formData.country} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
          <div><label className="block mb-2 font-medium">Город</label><input type="text" name="city" value={formData.city} onChange={handleChange} className="w-full px-3 py-2 border rounded-lg" /></div>
        </div>
        <button type="submit" className="w-full bg-indigo-600 text-white py-3 rounded-lg font-bold hover:bg-indigo-700">Зарегистрироваться</button>
      </form>
    </div>
  );
};
'@

    "src\pages\LoginPage.tsx" = @'
import React from 'react';
import { LoginForm } from '../components/Auth/LoginForm';

export const LoginPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <LoginForm />
    </div>
  );
};
'@

    "src\pages\RegisterPage.tsx" = @'
import React from 'react';
import { RegisterForm } from '../components/Auth/RegisterForm';

export const RegisterPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <RegisterForm />
    </div>
  );
};
'@

    "src\pages\Home.tsx" = @'
import React from 'react';
import { Link } from 'react-router-dom';

export const Home: React.FC = () => {
  return (
    <div className="text-center py-16">
      <h1 className="text-6xl font-bold text-indigo-600 mb-6">Lilili B2B Platform</h1>
      <p className="text-xl text-gray-700 mb-8 max-w-3xl mx-auto">
        Найдите проверенных поставщиков из 83 категорий. Создавайте закупки, получайте предложения, общайтесь в real-time чате.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 my-16">
        {[
          { number: '10,000+', label: 'Верифицированных поставщиков' },
          { number: '83', label: 'Категории товаров' },
          { number: 'Real-time', label: 'Чат с поставщиками' },
        ].map((stat) => (
          <div key={stat.label} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition">
            <h3 className="text-3xl font-bold text-indigo-600 mb-2">{stat.number}</h3>
            <p className="text-gray-600">{stat.label}</p>
          </div>
        ))}
      </div>
      <div className="space-x-4">
        <Link to="/suppliers" className="bg-indigo-600 text-white px-8 py-4 rounded-xl text-lg hover:bg-indigo-700 transition shadow-lg">
          Найти поставщиков
        </Link>
        <Link to="/rfq" className="bg-green-600 text-white px-8 py-4 rounded-xl text-lg hover:bg-green-700 transition shadow-lg">
          Создать закупку
        </Link>
      </div>
    </div>
  );
};
'@

    "src\App.tsx" = @'
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Header } from './components/Layout/Header';
import { Home } from './pages/Home';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { SuppliersPage } from './pages/SuppliersPage';
import { ProfilePage } from './pages/ProfilePage';
import { RFQPage } from './pages/RFQPage';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/suppliers" element={<SuppliersPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/rfq" element={<RFQPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
'@
}

# Заполняем файлы
foreach ($file in $files.Keys) {
    $content = $files[$file]
    $path = Join-Path $PWD.Path $file
    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
    Write-Host "✅ $file заполнен"
}

Write-Host "🎉 Все файлы созданы и заполнены!"

Remove-Item fill_files.ps1