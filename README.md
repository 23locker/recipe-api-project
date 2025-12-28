# Recipe API

## О проекте

Бэкенд приложение для работы с рецептами на FastAPI. Можешь просматривать рецепты, фильтровать по калориям и категориям, заменять ингредиенты если их нет, парсить цены из магазина Пятерочка.

## Recipe API Project

Сервис для управления рецептами, ингредиентами и категориями с поддержкой кэширования и очередей сообщений.

## Технологический стек

### Backend

- **Язык:** Python 3.12+
- **Фреймворк:** FastAPI
- **ORM:** Tortoise-ORM
- **Базы данных:**
  - PostgreSQL (основное хранилище)
  - MongoDB (дополнительные данные)
  - Redis (кэширование)
- **Брокер сообщений:** RabbitMQ (через aio-pika)
- **Миграции:** Aerich / Alembic

### Frontend

- **Фреймворк:** Vue 3
- **Сборка:** Vite
- **Управление состоянием:** Pinia
- **Стилизация:** Tailwind CSS
- **HTTP-клиент:** Axios

## Запуск проекта

Для управления проектом рекомендуется использовать `Makefile`.

### 1. Предварительные требования

- Docker и Docker Compose
- Python 3.12 (рекомендуется использовать `uv`)
- Node.js и npm

---

### Режим PROD (Основной)

1.  **Инфраструктура:**
    ```bash
    make prod-up
    ```
2.  **Backend:**
    - Настройте `.env` (используйте `.env.example`).
    - Установите зависимости в `backend/`: `uv sync` (или `pip install -r requirements.txt`).
    - Примените миграции: `aerich upgrade`.
    - Заполните данными: `make seed-prod`.
    - Запустите: `uvicorn app.main:app --reload` (в директории `backend`).

---

### Режим TEST (Для разработки и тестов)

1.  **Инфраструктура:**
    ```bash
    make test-up
    ```
    _Примечание: используется `docker-compose-test.yml`, порты не конфликтуют с PROD._
2.  **Backend:**
    - Создайте `backend/.env.test` на основе `.env.test.example`.
    - Заполните данными: `make seed-test`.
    - Запустите тесты: `make test`.

---

### 4. Настройка Frontend

Перейдите в директорию `frontend`:

```bash
cd frontend
npm install
npm run dev
```

### 4. Настройка Frontend

Перейдите в директорию `frontend`:

```bash
cd frontend
npm install
npm run dev
```

## Тестирование

Для запуска тестов бэкенда:

```bash
pytest
```
