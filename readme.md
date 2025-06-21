# 📚 Bookly: Asynchronous Book Review API

Bookly is a modern, production-ready RESTful API for a book review web service. It demonstrates best practices in asynchronous Python development, robust authentication, scalable database management, and cloud-native patterns. The project is designed for extensibility, maintainability, and security, leveraging industry-standard tools and libraries.

---

## 🗂️ Table of Contents

- [✨ Overview](#-overview)
- [🏛️ Architecture](#-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Setup & Installation](#-setup--installation)
- [🗄️ Database Migrations](#-database-migrations)
- [🚀 Running the Application](#-running-the-application)
- [📖 API Documentation](#-api-documentation)
- [🧪 Testing & Quality](#-testing--quality)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

---

## ✨ Overview

Bookly provides endpoints for user authentication, book management, and review submission. It is built with FastAPI for high performance and asynchronous I/O, SQLModel for ORM, and Alembic for migrations. JWT-based authentication and Redis-backed token revocation ensure secure session management. The project is suitable for cloud deployment and scalable microservice architectures.

---

## 🏛️ Architecture

- **API Layer:** FastAPI serves as the entry point, providing async endpoints and automatic OpenAPI documentation.
- **Authentication:** JWT tokens are issued and validated for secure, stateless authentication. Redis is used for token blocklisting (revocation).
- **Database:** SQLModel (built on SQLAlchemy) provides ORM capabilities, with PostgreSQL as the recommended backend.
- **Migrations:** Alembic manages schema migrations, ensuring safe and versioned database changes.
- **Background Tasks:** Celery is used for asynchronous tasks such as sending emails, with Redis as the broker.
- **Email:** FastAPI-Mail is integrated for transactional email delivery.

---

## 🛠️ Tech Stack

| Layer                | Technology/Library         | Purpose                                      |
|----------------------|---------------------------|----------------------------------------------|
| Language             | Python 3.11+              | Core programming language                    |
| Web Framework        | [FastAPI](https://fastapi.tiangolo.com/) | Async API framework with OpenAPI support     |
| ORM                  | [SQLModel](https://sqlmodel.tiangolo.com/) | Async ORM, type-safe models                  |
| Database             | PostgreSQL (recommended)  | Relational database                          |
| Migrations           | [Alembic](https://alembic.sqlalchemy.org/) | Database schema migrations                   |
| Auth                 | [PyJWT](https://pyjwt.readthedocs.io/) | JWT encoding/decoding                        |
| Caching/Blocklist    | [Redis](https://redis.io/) | Token revocation, Celery broker/backend      |
| Background Tasks     | [Celery](https://docs.celeryq.dev/) | Distributed task queue                       |
| Email                | [FastAPI-Mail](https://sabuhish.github.io/fastapi-mail/) | Transactional email delivery                 |
| Password Hashing     | [passlib](https://passlib.readthedocs.io/) | Secure password storage                      |
| Environment Config   | [pydantic-settings](https://docs.pydantic.dev/latest/integrations/settings/) | Typed config management                      |
| Testing              | [pytest](https://docs.pytest.org/) | Unit and integration testing                 |
| Linting/Formatting   | [Black](https://black.readthedocs.io/), [Ruff](https://docs.astral.sh/ruff/) | Code quality                                 |

---

## 📁 Project Structure

```
src/
├── __init__.py
├── celeryTask.py
├── config.py
├── errors.py
├── mail.py
├── middleware.py
├── auth/
│   ├── __init__.py
│   ├── dependencies.py
│   ├── routes.py
│   ├── schemas.py
│   ├── service.py
│   └── utils.py
├── books/
│   ├── __init__.py
│   ├── data.py
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
├── db/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── redis.py
└── reviews/
    ├── __init__.py
    ├── routes.py
    ├── schemas.py
    └── service.py
```

- **auth/**: User authentication, JWT, and authorization logic.
- **books/**: Book CRUD operations and schemas.
- **reviews/**: Review submission and retrieval.
- **db/**: Database models, session management, and Redis integration.
- **middleware.py**: CORS and custom logging middleware.
- **errors.py**: Centralized error handling and custom exceptions.
- **mail.py**: Email sending utilities.
- **celeryTask.py**: Celery worker and async email tasks.
- **config.py**: Environment and settings management.

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-org/bookly.git
   cd bookly
   ```
2. **Create a virtual environment and install dependencies:**
   ```sh
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   pip install -r requirement.txt
   ```
3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   JWT_SECRET=your_jwt_secret
   JWT_ALGORITHM=HS256
   REDIS_URL=redis://localhost:6379/0
   MAIL_USERNAME=your_email@example.com
   MAIL_PASSWORD=your_email_password
   MAIL_FROM=your_email@example.com
   MAIL_PORT=587
   MAIL_SERVER=smtp.example.com
   MAIL_FROM_NAME=Bookly
   DOMAIN=localhost:8000
   ```
4. **Start Redis with Docker:**
   ```sh
   docker run -d --name redis-server -p 6379:6379 redis
   ```

---

## 🗄️ Database Migrations

1. **Initialize the database (first run):**
   ```sh
   alembic upgrade head
   ```
2. **Create a new migration after model changes:**
   ```sh
   alembic revision --autogenerate -m "Describe your change"
   alembic upgrade head
   ```

---

## 🚀 Running the Application

1. **Start the FastAPI server:**
   ```sh
   uvicorn src:app --reload
   ```
2. **Start the Celery worker (for background tasks):**
   ```sh
   celery -A src.celeryTask.c_app worker --loglevel=info
   ```

---

## 📖 API Documentation

Once running, access the interactive API docs at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testing & Quality

- **Unit tests:**
  ```sh
  pytest
  ```
- **Linting & formatting:**
  ```sh
  black .
  ruff check .
  ```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

MIT License

---

## ✨ Credits
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database: SQLAlchemy/SQLModel
- Migrations: Alembic
- Testing: Pytest, Faker
- Task Queue: Celery
- Caching: Redis

---

For questions or support, please contact the maintainers or open an issue.