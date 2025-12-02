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
