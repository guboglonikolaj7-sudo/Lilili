export interface User {
  id: number;
  email: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface LogisticsCompany {
  id: number;
  name: string;
  site: string;
}

export interface Supplier {
  id: number;
  name: string;
  country: string;
  city: string;
  description: string;
  logo?: string;
  logo_url?: string;
  video_url?: string;
  moq: number;
  contact_email?: string;
  contact_phone?: string;
  category: Category;
  logistics_options: LogisticsCompany[];
  created_at: string;
}

export interface Order {
  id: number;
  title: string;
  description: string;
  category_name: string;
  buyer_email: string;
  budget_min?: number;
  budget_max?: number;
  region: string;
  deadline: string;
  status: string;
  created_at: string;
  is_urgent: boolean;
  offers_count: number;
}

export interface Offer {
  id: number;
  price: number;
  delivery_days: number;
  comment?: string;
  supplier_email: string;
  supplier_id: number;
  created_at: string;
  is_selected: boolean;
}

export interface Message {
  id: number;
  content: string;
  sender_email: string;
  timestamp: string;
  is_read: boolean;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}


