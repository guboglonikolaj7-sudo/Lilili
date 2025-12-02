import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = Bearer ;
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
  getSupplier: (id: number) => api.get(/suppliers//),
};

export const rfqAPI = {
  getRFQs: () => api.get('/orders/'),
  createRFQ: (data: any) => api.post('/orders/', data),
};
