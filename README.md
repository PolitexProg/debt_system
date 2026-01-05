# 💸 Debt Tracker API

A professional asynchronous backend built with **FastAPI** and **SQLAlchemy 2.0** for tracking personal debts, loans, and financial balances across different currencies.

## 🚀 Key Architectural Features

* **Asynchronous Core:** Built with `asyncio` and `SQLAlchemy` (AsyncSession) for high-performance I/O operations.
* **Advanced User Management:** Integrated with `fastapi-users` using UUIDs for secure authentication.
* **Automated Summaries:** Built-in analytics to calculate net balances (owed to vs. owed by) grouped by currency using database-level aggregations (`func.sum`, `group_by`).
* **Relational Integrity:** * **User ↔ Settings:** One-to-one relationship for personalized app configurations.
* **User ↔ Debts:** One-to-many relationship with cascading deletions.


* **Scalable Service Layer:** Business logic is encapsulated in pure async functions, keeping routes lean and testable.

## 🛠 Tech Stack

* **Backend:** FastAPI (Python 3.10+)
* **ORM:** SQLAlchemy 2.0 (Declarative Base)
* **Auth:** FastAPI Users (UUID strategy)
* **Database:** PostgreSQL (recommended) / SQLite (async)
* **Validation:** Pydantic v2

## 📂 Business Logic Layers

### 1. Debt Management (`crud.py` / `services.py`)

Provides full CRUD capabilities for debt records. Includes strict ownership checks to ensure users can only access or modify their own data.

### 2. Financial Analytics

The `get_user_summary` service performs complex SQL aggregations to return a dashboard-ready summary:

* **Total Owed To:** Money you lent to others.
* **Total Owed By:** Money you borrowed.
* **Net Balance:** Your overall financial standing per currency.

### 3. User Settings

Automated "get-or-create" pattern for user preferences (default currency, notification reminders), ensuring a seamless onboarding experience for new users.

## 🔌 API Endpoints (Quick Overview)

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/debts/` | List all debts with filters (type, name) |
| `POST` | `/debts/` | Register a new debt/loan |
| `GET` | `/debts/summary` | Get currency-wise financial summary |
| `GET` | `/settings/` | Retrieve user preferences |
| `PATCH` | `/settings/` | Update default currency or reminders |

## ⚙️ Installation & Setup

1. **Clone & Environment:**

```bash
git clone <repo_url>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

2. **Database Migrations:**

```bash
alembic upgrade head

```

3. **Run Application:**

```bash
uvicorn app.main:app --reload

```

## 🧪 Testing

Run async tests using `pytest` and `httpx`:

```bash
pytest tests/

```

---

**Хотите, чтобы я помог вам реализовать Alembic-миграции или добавил middleware для автоматического создания настроек при регистрации пользователя?**
