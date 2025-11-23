import { useEffect, useState, useRef } from 'react';

interface Message {
  id: number;
  content: string;
  sender: string;
  timestamp: string;
}

interface Props {
  orderId: number;
  onClose: () => void;
}

export const ChatModal = ({ orderId, onClose }: Props) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [message, setMessage] = useState('');
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    ws.current = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${orderId}/?token=${token}`);
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, {
        id: Date.now(),
        content: data.message,
        sender: data.sender,
        timestamp: data.timestamp
      }]);
    };

    ws.current.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.current.onclose = () => {
      console.log('WebSocket closed');
    };

    return () => {
      ws.current?.close();
    };
  }, [orderId]);

  const sendMessage = () => {
    if (!message.trim()) return;
    ws.current?.send(JSON.stringify({ message }));
    setMessage('');
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl mx-4 h-3/4 flex flex-col">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Чат по заказу #{orderId}</h2>
          <button onClick={onClose} className="text-red-500 hover:text-red-700 text-2xl">
            ×
          </button>
        </div>

        <div className="border rounded flex-1 p-4 mb-4 overflow-y-auto bg-gray-50">
          {messages.map(msg => (
            <div key={msg.id} className="mb-3 p-3 bg-white rounded shadow">
              <span className="font-semibold text-blue-600">{msg.sender}:</span>
              <p className="text-gray-800 mt-1">{msg.content}</p>
              <span className="text-xs text-gray-500">{msg.timestamp}</span>
            </div>
          ))}
          {messages.length === 0 && (
            <p className="text-gray-500 text-center">Начните общение...</p>
          )}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Введите сообщение..."
            value={message}
            onChange={e => setMessage(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && sendMessage()}
          />
          <button
            onClick={sendMessage}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-lg font-medium transition-colors"
          >
            Отправить
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatModal;
