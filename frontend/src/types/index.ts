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
  description?: string;
}

export type VerificationStatus =
  | 'not_started'
  | 'in_progress'
  | 'completed'
  | 'failed';

export type VerificationRiskLevel = 'low' | 'medium' | 'high' | null;

export interface VerificationSourceSnapshot {
  status: 'ok' | 'warning' | 'error' | 'unknown';
  score: number | null;
  details?: string;
  payload?: Record<string, unknown> | null;
}

export interface VerificationCheck {
  id: number;
  supplier: number;
  country: string;
  status: VerificationStatus;
  fssp_score: number | null;
  rnp_score: number | null;
  egrul_score: number | null;
  licenses_score: number | null;
  overall_score: number | null;
  is_verified: boolean;
  risk_level: VerificationRiskLevel;
  error_message?: string | null;
  checked_sources: Record<string, VerificationSourceSnapshot>;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Supplier {
  id: number;
  name: string;
  country: string;
  city: string;
  description: string;
  logo?: string | null;
  logo_url?: string | null;
  video_url?: string | null;
  moq: number;
  contact_email?: string | null;
  contact_phone?: string | null;
  category: Category | null;
  logistics_options: LogisticsCompany[];
  created_at: string;
  verification_status: VerificationStatus;
  verification_score?: number | null;
  is_verified: boolean;
  last_verified_at?: string | null;
  latest_check?: VerificationCheck | null;
}

export interface SupplierListFilters {
  search?: string;
  country?: string;
  page?: number;
}

export interface Order {
  id: number;
  title: string;
  description: string;
  category_name: string;
  buyer_email: string;
  budget_min?: number | string | null;
  budget_max?: number | string | null;
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
