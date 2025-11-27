# Проверка поставщиков

Документ описывает полную цепочку автоматической верификации поставщиков и производителей в проекте **Поставщик.ру**.

## 1. API‑ключи и переменные окружения

Добавьте значения в `backend/.env` (см. пример файла `.env.example`):

| Ключ              | Где получить                                                                 | Назначение                             |
|-------------------|------------------------------------------------------------------------------|----------------------------------------|
| `FSSP_API_KEY`    | [api-fssp.gov.ru](https://api-fssp.gov.ru/developers/)                       | Проверка исполнительных производств    |
| `NEWDB_API_KEY`   | API ЕИС/РНП или коммерческие зеркала (zakupki/new-rusprofile)                | Проверка в реестре недобросовестных    |
| `FNS_API_KEY`     | [api-fns.ru](https://api-fns.ru/) или официальный сервис ЕГРЮЛ               | Проверка регистрации и статуса         |

При dev-запуске переменные можно оставить пустыми — сервис перейдёт в детерминированный mock-режим, сохранив структуру ответа.

## 2. Как запустить пайплайн

```bash
# 1. Redis для каналов, Celery и WebSocket
redis-server

# 2. Backend + Celery
cd backend
python manage.py migrate
python manage.py runserver
celery -A config worker -l info

# 3. Frontend
cd ../frontend
npm run dev
```

Параметры Celery берутся из настроек `CELERY_BROKER_URL`/`CELERY_RESULT_BACKEND` (по умолчанию `redis://127.0.0.1:6379/0`).

## 3. Endpoints

| Метод | URL                                             | Описание                                      |
|-------|--------------------------------------------------|-----------------------------------------------|
| GET   | `/api/v1/suppliers/`                            | Список поставщиков + последний чек            |
| POST  | `/api/v1/suppliers/<id>/verify/`                | Запустить проверку выбранного поставщика      |
| GET   | `/api/v1/suppliers/<id>/verification_checks/`   | История проверок                               |
| GET   | `/api/v1/suppliers/<id>/contacts/`              | Контакты (только авторизованный доступ)       |
| POST  | `/api/v1/suppliers/verify_all/`                 | Массовая проверка всех активных поставщиков   |

### Примеры запросов

```bash
# Получить страницу поставщиков
curl -H "Authorization: Bearer <JWT>" http://127.0.0.1:8000/api/v1/suppliers/

# Запустить проверку
curl -X POST -H "Authorization: Bearer <JWT>" http://127.0.0.1:8000/api/v1/suppliers/5/verify/

# История проверок
curl -H "Authorization: Bearer <JWT>" http://127.0.0.1:8000/api/v1/suppliers/5/verification_checks/
```

## 4. Поток данных

1. Frontend вызывает `POST /verify/`.
2. Django создает `VerificationCheck` и ставит задачу Celery.
3. Celery обращается к внешним реестрам (или mock) через `VerificationService`.
4. Результаты и баллы сохраняются в `VerificationCheck`, а агрегированные значения попадают в модель `Supplier`.
5. Web/REST клиент может polling'ом получить статус через `GET /suppliers/` или историю проверок.

## 5. Диагностика

- Логи Celery (`celery -A config worker -l info`) покажут ошибки подключений.
- Убедитесь, что Redis запущен и доступен по `REDIS_URL`.
- Если API возвращает 429 — добавьте rate limiting/key rotation на стороне поставщиков данных.

