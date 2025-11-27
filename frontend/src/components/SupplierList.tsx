import { useCallback, useEffect, useMemo, useState } from 'react';
import type { Supplier, SupplierListFilters } from '../types';
import { fetchSuppliers, verifySupplier } from '../api/suppliers';
import { SupplierCard } from './SupplierCard';

interface SupplierListProps {
  searchTerm?: string;
  country?: string;
  onSelectContact?: (supplierId: number) => void;
}

const normalizeSuppliers = (payload: Supplier[] | { results?: Supplier[] }) => {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (payload?.results) {
    return payload.results;
  }
  return [];
};

export default function SupplierList({
  searchTerm,
  country,
  onSelectContact,
}: SupplierListProps) {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [verifyingId, setVerifyingId] = useState<number | null>(null);

  const loadSuppliers = useCallback(() => {
    setLoading(true);
    const params: SupplierListFilters = {};
    if (searchTerm?.trim()) {
      params.search = searchTerm.trim();
    }
    if (country) {
      params.country = country;
    }
    fetchSuppliers(params)
      .then((data) => {
        setSuppliers(normalizeSuppliers(data as Supplier[] | { results?: Supplier[] }));
        setError(null);
      })
      .catch((err) => {
        console.error(err);
        setError('Не удалось загрузить поставщиков');
      })
      .finally(() => setLoading(false));
  }, [country, searchTerm]);

  useEffect(() => {
    loadSuppliers();
  }, [loadSuppliers]);

  const handleVerify = useCallback(
    (supplierId: number) => {
      setVerifyingId(supplierId);
      verifySupplier(supplierId)
        .then(() => {
          setSuppliers((prev) =>
            prev.map((s) =>
              s.id === supplierId
                ? {
                    ...s,
                    verification_status: 'in_progress',
                  }
                : s,
            ),
          );
        })
        .catch((err) => {
          console.error(err);
          setError('Ошибка запуска проверки. Повторите попытку.');
        })
        .finally(() => setVerifyingId(null));
    },
    [],
  );

  const content = useMemo(() => {
    if (loading) {
      return (
        <div className="col-span-full text-center text-gray-500">Загрузка...</div>
      );
    }
    if (error) {
      return (
        <div className="col-span-full text-center text-red-600 bg-red-50 rounded p-4">
          {error}
        </div>
      );
    }
    if (!suppliers.length) {
      return (
        <div className="col-span-full text-center text-gray-500 bg-white rounded-lg shadow p-6">
          Поставщики не найдены. Попробуйте изменить параметры фильтрации.
        </div>
      );
    }
    return suppliers.map((supplier) => (
      <SupplierCard
        key={supplier.id}
        supplier={supplier}
        onVerify={handleVerify}
        verifying={verifyingId === supplier.id}
        onShowContacts={onSelectContact}
      />
    ));
  }, [error, handleVerify, loading, onSelectContact, suppliers, verifyingId]);

  return (
    <section>
      <header className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-2xl font-semibold">Поставщики</h2>
          <p className="text-sm text-gray-500">
            Автоматическая проверка по реестрам Китая, Турции, Индии, стран СНГ и РФ
          </p>
        </div>
      </header>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {content}
      </div>
    </section>
  );
}
