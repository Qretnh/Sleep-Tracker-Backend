
# SleepMate

**SleepMate** — бэкенд приложения для контроля и отслеживания качества сна.  
Собирает статистику, строит дашборды, генерирует ИИ-отчёты, позволяет ставить цели и напоминания.

---

## 🛠 Технологии

- **Язык:** Python  
- **Фреймворк:** FastAPI  
- **База данных:** PostgreSQL + SQLAlchemy  
- **Миграции:** Alembic  
- **Телеграм-бот:** Aiogram  
- **Очередь уведомлений:** RabbitMQ  
- **Интеграция с ИИ:** OpenAI через ProxyAPI  
- **Docker Compose:** оркестрация 6 контейнеров  

---

## 🏗 Архитектура

Контейнеры Docker Compose:

1. **backend** — основной бэкенд на FastAPI  
2. **db** — PostgreSQL  
3. **rabbitmq** — очередь уведомлений  
4. **producer** — сканирует БД и отправляет уведомления в очередь  
5. **consumer** — отправляет уведомления пользователям  
6. **bot** — Telegram бот для перехода в Mini App  

Все сервисы конфигурируются через `.env` в корне проекта.

---

## ⚡ Фичи

- **JWT авторизация** — безопасный доступ к API через токены.  
- **Распределённая архитектура** — бэкенд, база данных, очередь и бот работают в отдельных контейнерах, повышая отказоустойчивость.  
- **Телеграм-бот для Mini App** — пользователи получают уведомления, ставят цели и смотрят ИИ-отчёты.  
- **Интеграция с OpenAI через ProxyAPI** — генерация отчётов и подсказок на основе анализа сна.  
- **Конфиг через `.env`** — все ключи, URL и токены настраиваются через окружение.  
- **Миграции через Alembic** — изменения в БД версионируются и легко применяются.  
- **Логи в консоль Docker** — прозрачное логирование всех сервисов.  
- **Форматирование кода** — `black` и `isort` настроены для автоматической чистки кода.

---

## ⚙️ Настройка

1. Скопируйте `.env.example` в `.env` и заполните необходимые значения:  

```dotenv
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/sleepmate
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=sleepmate
POSTGRES_HOST=db
POSTGRES_PORT=5432

WEB_APP_URL=https://your-web-app-url
BOT_TOKEN=your-telegram-bot-token

JWT_SECRET=your-secret
JWT_ALGO=HS256
JWT_EXPIRE_MINUTES=1440

OPENAI_API_BASE_URL=https://api.proxyapi.ru/openai/v1
OPENAI_API_KEY=your-proxyapi-key
OPENAI_MODEL_NAME=gpt-5-mini

RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
NOTIFICATIONS_QUEUE=notifications
````

2. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

3. Запустите миграции:

```bash
make migrate
```

---

## 🧩 Команды бота

* `/start` — открывает веб-приложение.

---

## 🧹 Форматирование кода

* `black` — автоматическое форматирование кода
* `isort` — сортировка импортов

Для проверки и исправления кода:

```bash
black ./backend ./bot
isort ./backend ./bot
```

---

## 📜 Лицензия

Проект открыт для изучения и модификации.

```

