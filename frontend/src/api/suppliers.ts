import axios from 'axios';
import type {
  PaginatedResponse,
  Supplier,
  SupplierListFilters,
  VerificationCheck,
} from '../types';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 30000,
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const fetchSuppliers = (params?: SupplierListFilters) =>
  API.get<PaginatedResponse<Supplier> | Supplier[]>('/suppliers/', {
    params,
  }).then((r) => r.data);

export const verifySupplier = (supplierId: number) =>
  API.post<{ task_id: string; message: string }>(
    `/suppliers/${supplierId}/verify/`,
  ).then((r) => r.data);

export const fetchVerificationChecks = (supplierId: number) =>
  API.get<VerificationCheck[]>(
    `/suppliers/${supplierId}/verification_checks/`,
  ).then((r) => r.data);

export const fetchSupplierContacts = (supplierId: number) =>
  API.get<{ contact_email: string; contact_phone: string; name: string }>(
    `/suppliers/${supplierId}/contacts/`,
  ).then((r) => r.data);