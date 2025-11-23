import { useEffect, useState } from "react"

interface Props {
  supplierId: number
  onClose: () => void
}

export default function ContactModal({ supplierId, onClose }: Props) {
  const [contacts, setContacts] = useState<{ contact_email: string; contact_phone: string } | null>(null)

  useEffect(() => {
    const token = localStorage.getItem("token")
    fetch(`http://127.0.0.1:8000/api/v1/suppliers/${supplierId}/contacts/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setContacts)
      .catch(() => alert("Ошибка загрузки контактов"))
  }, [supplierId])

  if (!contacts) return <p className="p-4">Загрузка...</p>

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 max-w-sm w-full">
        <h3 className="text-lg font-semibold mb-4">Контакты</h3>
        <p><strong>Email:</strong> {contacts.contact_email}</p>
        <p><strong>Телефон:</strong> {contacts.contact_phone}</p>
        <button onClick={onClose} className="mt-4 bg-gray-600 text-white px-4 py-2 rounded">
          Закрыть
        </button>
      </div>
    </div>
  )
}