import { useMemo } from 'react';
import {
  FiAlertCircle,
  FiCheckCircle,
  FiRefreshCw,
  FiShield,
} from 'react-icons/fi';
import clsx from 'clsx';
import type { Supplier } from '../types';

const SOURCE_LABELS: Record<string, string> = {
  fssp: 'ФССП',
  rnp: 'РНП',
  egrul: 'ЕГРЮЛ',
  licenses: 'Лицензии',
};

const getScoreColor = (score?: number | null) => {
  if (typeof score !== 'number') {
    return 'text-gray-500';
  }
  if (score >= 0.85) return 'text-emerald-600';
  if (score >= 0.65) return 'text-amber-500';
  return 'text-rose-500';
};

interface SupplierCardProps {
  supplier: Supplier;
  onVerify: (supplierId: number) => void;
  verifying?: boolean;
  onShowContacts?: (supplierId: number) => void;
}

export const SupplierCard = ({
  supplier,
  onVerify,
  verifying,
  onShowContacts,
}: SupplierCardProps) => {
  const imagePath = supplier.logo_url ?? supplier.logo ?? null;
  const imageSrc =
    imagePath && imagePath.startsWith('http')
      ? imagePath
      : imagePath
        ? `http://127.0.0.1:8000${imagePath}`
        : null;
  const latestCheck = supplier.latest_check ?? null;
  const score = supplier.verification_score ?? latestCheck?.overall_score ?? null;
  const statusLabel = useMemo(() => {
    switch (supplier.verification_status) {
      case 'completed':
        return supplier.is_verified ? 'Проверен' : 'Результат есть';
      case 'in_progress':
        return 'Проверяем...';
      case 'failed':
        return 'Ошибка проверки';
      default:
        return 'Не проверен';
    }
  }, [supplier.is_verified, supplier.verification_status]);

  const sourceBadges = useMemo(() => {
    const sources = ['fssp', 'rnp', 'egrul', 'licenses'];
    return sources.map((source) => {
      const snapshot = latestCheck?.checked_sources?.[source] ?? null;
      const status = snapshot?.status ?? 'unknown';
      const baseClasses =
        'inline-flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full';
      const color =
        status === 'ok'
          ? 'bg-emerald-50 text-emerald-700'
          : status === 'warning'
            ? 'bg-amber-50 text-amber-700'
            : status === 'error'
              ? 'bg-rose-50 text-rose-700'
              : 'bg-gray-100 text-gray-600';
      return (
        <span key={source} className={clsx(baseClasses, color)}>
          <FiShield />
          {SOURCE_LABELS[source] ?? source.toUpperCase()}
          {typeof snapshot?.score === 'number' && (
            <span className="font-semibold">
              {(snapshot.score * 100).toFixed(0)}%
            </span>
          )}
        </span>
      );
    });
  }, [latestCheck]);

  return (
    <div className="border rounded-xl p-5 shadow-sm bg-white hover:shadow-lg transition flex flex-col gap-3">
      {imageSrc ? (
        <img
          src={imageSrc}
          alt={supplier.name}
          className="h-32 w-full object-contain rounded-lg bg-gray-50"
        />
      ) : (
        <div className="h-32 w-full rounded-lg bg-gray-100 flex items-center justify-center text-gray-400 text-sm uppercase tracking-wide">
          медиа нет
        </div>
      )}

      <div className="flex items-start justify-between gap-2">
        <div>
          <h2 className="font-semibold text-lg">{supplier.name}</h2>
          <p className="text-sm text-gray-600">
            {supplier.country}, {supplier.city}
          </p>
        </div>
        <div className="text-right">
          <p className={clsx('text-sm font-semibold', getScoreColor(score))}>
            {typeof score === 'number'
              ? `${(score * 100).toFixed(0)}%`
              : 'нет данных'}
          </p>
          <p className="text-xs text-gray-500">{statusLabel}</p>
        </div>
      </div>

      {supplier.category?.name && (
        <span className="inline-flex w-fit bg-blue-50 text-blue-700 text-xs px-3 py-1 rounded-full">
          {supplier.category.name}
        </span>
      )}
      <p className="text-sm text-gray-700 min-h-[3.5rem] overflow-hidden text-ellipsis">
        {supplier.description}
      </p>
      <p className="text-sm">
        MOQ: <span className="font-semibold">{supplier.moq} шт.</span>
      </p>

      <div className="flex flex-wrap gap-2">{sourceBadges}</div>

      {latestCheck?.completed_at && (
        <p className="text-xs text-gray-500">
          Проверено: {new Date(latestCheck.completed_at).toLocaleString('ru-RU')}
        </p>
      )}

      <div className="mt-auto flex flex-wrap gap-3">
        <button
          type="button"
          onClick={() => onVerify(supplier.id)}
          disabled={verifying}
          className={clsx(
            'flex-1 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition',
            verifying
              ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
              : 'bg-emerald-600 text-white hover:bg-emerald-700',
          )}
        >
          {verifying ? <FiRefreshCw className="animate-spin" /> : <FiCheckCircle />}
          {verifying ? 'Проверяем...' : 'Проверить'}
        </button>
        {onShowContacts && (
          <button
            type="button"
            onClick={() => onShowContacts(supplier.id)}
            className="px-3 py-2 rounded-lg text-sm font-medium border border-gray-200 text-gray-700 hover:bg-gray-50 flex-1"
          >
            Контакты
          </button>
        )}
      </div>

      {latestCheck?.error_message && (
        <div className="flex items-start gap-2 text-xs text-rose-600 bg-rose-50 px-3 py-2 rounded-lg">
          <FiAlertCircle className="mt-0.5" />
          {latestCheck.error_message}
        </div>
      )}
    </div>
  );
};