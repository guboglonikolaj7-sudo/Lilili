1. справь App.tsx: восстанови layout (header+main grid), контролируй token, добавь logout, используй SearchBar из components.
2. SupplierCard.tsx: убери выражение s.moq && s.logo, добавь Boolean, выведи проверку (score, badge, кнопка «роверить», react-icons).
3. OrderList.tsx: типизируй onOpenChat, убери дублирование, обработай пустой список и ошибки загрузки.
4. settings.py: устрани дубли CHANNEL_LAYERS/INSTALLED_APPS, добавь API-ключи, CELERY_BROKER_URL/CELERY_RESULT_BACKEND.
5. urls.py: подключи SupplierViewSet через router и убери лишние JWT endpoints.