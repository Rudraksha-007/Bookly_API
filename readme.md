# Bookly

Bookly is a RESTful API for a book review web service. This project demonstrates skills in building asynchronous web APIs with FastAPI, JWT authentication, database migrations, and using SQLModel for ORM. The project also includes Redis integration for token revocation and uses Alembic for handling migrations.

## Features

- **User Authentication:** Sign-up, login, token refresh, and logout endpoints with JWT.
- **Book Management:** Create, read, update, and delete books.
- **Review System:** Add reviews for books with relationships between users and books.
- **Asynchronous Endpoints:** Fully async database operations using SQLModel.
- **Database Migrations:** Managed via Alembic for schema versioning.

## Tech Stack

- **Language:** Python
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ORM:** [SQLModel](https://sqlmodel.tiangolo.com/)
- **Database migration:** Alembic
- **Authentication:** JWT (using [PyJWT](https://pyjwt.readthedocs.io/))
- **Caching/Blocklisting:** Redis
- **Testing & Linting:** (Configured as needed)

## Project Structure

```
d:\Fast API\
├── alembic.ini
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── c283f4ad8b7b_init.py
│       ├── 38c84f1e3778_adds_password_hash_field.py
│       ├── 6bf688d68f54_.py
│       ├── dc2385c4d4d3_adding_review_table.py
│       └── e10f4973b9b7_adding_updated_at_attribute.py
└── src/
    ├── __init__.py  [View here](d:/Fast API/src/__init__.py)
    ├── config.py
    ├── auth/
    │   ├── __init__.py
    │   ├── dependencies.py
    │   ├── routes.py  [View here](d:/Fast API/src/auth/routes.py)
    │   ├── schemas.py
    │   └── service.py
    ├── books/
    │   ├── __init__.py
    │   ├── data.py
    │   ├── routes.py  [View here](d:/Fast API/src/books/routes.py)
    │   ├── schemas.py  [View here](d:/Fast API/src/books/schemas.py)
    │   └── service.py
    ├── db/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── models.py  [View here](d:/Fast API/src/db/models.py)
    │   └── redis.py
    └── reviews/
        ├── __init__.py
        ├── routes.py  [View here](d:/Fast API/src/reviews/routes.py)
        ├── schemas.py  [View here](d:/Fast API/src/reviews/schemas.py)
        └── service.py  [View here](d:/Fast API/src/reviews/service.py)

## Getting Started

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/yourusername/bookly.git
   cd bookly
   ```

2. **Create a Virtual Environment & Install Dependencies:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirement.txt
   ```

3. **Configure Environment Variables:**

   Create a `.env` file at the root directory with the following keys:
   
   ```
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   JWT_SECRET=your_jwt_secret
   JWT_ALGORITHM=HS256
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

4. **Run Database Migrations:**

   Use Alembic to upgrade or downgrade the database schema:

   ```sh
   alembic upgrade head
   ```

5. **Start the Application:**

   ```sh
   uvicorn src.__init__:app --reload
   ```

## API Documentation

Once the server is running, access the interactive API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Testing & Quality

- **Unit Testing:** Implement tests using your preferred framework (pytest recommended).
- **Static Analysis:** Use linters and formatters such as Black and Ruff.

## Conclusion

This project showcases an end-to-end REST API built with modern Python best practices. It integrates asynchronous programming, robust authentication, and relational database handling to create a scalable microservice.

---

Feel free to explore the code and reach out if you have any questions.