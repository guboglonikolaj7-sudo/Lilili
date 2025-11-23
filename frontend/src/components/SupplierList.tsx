import { useEffect, useState } from "react"
import axios from "axios"

interface Supplier {
  id: number
  name: string
  country: string
  city: string
  moq: number
  category: { name: string }
}

interface SupplierListProps {
  onSelectContact?: (supplierId: number) => void
}

export default function SupplierList({ onSelectContact }: SupplierListProps = {}) {
  const [suppliers, setSuppliers] = useState<Supplier[]>([])

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/v1/suppliers/")
      .then(res => setSuppliers(res.data))
      .catch(err => console.error(err))
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {suppliers.map(s => (
        <div key={s.id} className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold">{s.name}</h3>
          <p className="text-gray-600">{s.country}, {s.city}</p>
          <p className="text-sm text-gray-500">Мин. заказ: {s.moq}</p>
          <p className="text-sm text-blue-600">{s.category.name}</p>

          {onSelectContact && (
            <button
              onClick={() => onSelectContact(s.id)}
              className="mt-3 bg-blue-600 text-white px-4 py-2 rounded"
            >
              Показать контакты
            </button>
          )}
        </div>
      ))}
    </div>
  )
}