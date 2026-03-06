# ✨ Stars Project — Telegram Mini App Ecosystem

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

**Stars Project** is a high-performance, full-stack Telegram Mini App ecosystem designed for gamified task execution and automated channel promotion. Built with a modern microservices architecture, it seamlessly integrates a React-based frontend with a powerful FastAPI backend and a real-time Aiogram Telegram bot.

---

## 🚀 Core Features

The application is divided into three primary modules, wrapped in a premium "Glassmorphism" UI with heavy haptic feedback for a native app feel.

### 💰 1. Earn Center (Task Execution)
* **Gamified Tasks:** Users earn internal currency ("Stars") by subscribing to targeted Telegram channels.
* **Frozen Balance System:** To prevent immediate unsubscribing, rewards are placed in a 72-hour hold (Frozen Balance).
* **Real-time Verification:** Instant subscription verification using Telegram Webhooks.

### 🚀 2. Boost Center (Ad Campaigns)
* **Self-Serve Advertising:** Users can spend their Stars or top up their Ad Balance to promote their own channels.
* **Automated Tracking:** The system automatically tracks the progress of the order and stops the campaign once the target subscriber count is reached.

### 👤 3. Profile Center
* **Financial Dashboard:** Manage Available Balance, Ad Balance, and Frozen Balance.
* **Referral System:** Built-in referral tracking with automated bonuses.
* **Strike & Penalty System:** Live tracking of user violations (see Anti-Fraud System below).

---

## 🛡️ Anti-Fraud & Strike System

implement a robust, webhook-driven anti-fraud system to ensure high-quality traffic for advertisers:

1.  **Event Listening:** The backend listens to Telegram's `chat_member` updates via Webhooks.
2.  **Leave Detection:** If a user leaves a sponsored channel before the 72-hour hold expires, the system catches the event instantly.
3.  **Penalty:** The user receives a **Strike**. Accumulating 5 strikes results in an automatic, permanent ban from the bot and the Mini App via custom `AuthMiddleware`.



---

## 🛠️ Technology Stack

### Backend
* **Framework:** FastAPI (Python 3.13)
* **Telegram API:** Aiogram 3.x (running in Webhook mode)
* **Database:** PostgreSQL with SQLAlchemy (Async ORM) & Alembic for migrations
* **Task Queue:** Celery + Redis for background processing and deferred tasks

### Frontend (Mini App)
* **Framework:** React 18 + Vite
* **Styling:** Custom CSS, Lucide Icons
* **Integration:** Telegram Web Apps API (`window.Telegram.WebApp`)

### Infrastructure
* **Containerization:** Fully Dockerized (Docker + Docker Compose)
* **Reverse Proxy:** Nginx (handled via external proxy manager)

---

## 📂 Project Structure (Monorepo)

```text
stars_project/
├── backend/                # FastAPI backend and Aiogram Bot
│   ├── app/                # API routes, ORM, Models, and Celery tasks
│   ├── tg_bot/             # Telegram bot handlers and middlewares
│   ├── alembic/            # Database migrations
│   ├── Dockerfile          # Backend container configuration
│   └── requirements.txt / pyproject.toml
├── frontend/               # React Mini App
│   ├── src/                # React components, pages, and API hooks
│   ├── Dockerfile          # Frontend container configuration
│   └── package.json
├── docker-compose.yml      # Multi-container orchestration
└── .env.example            # Environment variables template


⚙️ Quick Start (Docker)

The project is fully containerized. You can spin up the entire ecosystem (API, Bot, Database, Redis, Celery Workers, and Frontend) with a single command.
1. Environment Setup

Create a .env file in the root directory based on .env.example:
Bash

cp .env.example .env

Ensure you provide your BOT_TOKEN, WEBHOOK_URL, and Database credentials.
2. Build and Run
Bash

docker-compose up -d --build

3. Verify

    API Docs (Swagger): http://localhost:8000/docs

    Frontend: http://localhost:80 (or your mapped port)
