## Books API with FastAPI

This project is a backend API built with FastAPI, PostgreSQL, JWT Authentication, Redis, Celery, and more — for managing books, users, authentication, and reviews.

#### Features
- CRUD operations for Books, Users, and Reviews

- User registration with bcrypt password hashing

- JWT-based authentication (access & refresh tokens)

- Token revocation using Redis for logout security

- Role-based access control (RBAC)

- Async database operations with SQLAlchemy + asyncpg

- Background tasks with Celery (e.g., sending emails)

- Middleware for CORS, trusted hosts, and centralized error handling

#### Skills Showcased

| 🔧 Skill                | 💡 Application in Project                                                  |
|------------------------|-----------------------------------------------------------------------------|
| `FastAPI (Async)`      | Built all endpoints using async def for high performance                   |
| `JWT Auth`             | Secure login + refresh system using JWT and Redis-based blacklisting       |
| `SQLAlchemy ORM`       | Async ORM with relationships, joins, query optimization                    |
| `PostgreSQL`           | Used for structured, relational data storage                               |
| `Alembic`              | Auto-generates & tracks DB migrations                                       |
| `Redis`                | Caching & JWT blacklist storage                                            |
| `Celery`               | Handles background email tasks asynchronously                              |
| `RBAC`                 | Admin/user roles and permissions via dependency injection                  |
| `Security Best Practices` | Password hashing, token expiry, CORS config, input validation          |

#### Setup & Run
1. Clone 
```bash
git clone https://github.com/yourusername/books.git
cd books
```

2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run FastAPI
```bash
fastapi dev src/
```

5. POSTGRESQL Setup
```bash
CREATE USER sindh WITH PASSWORD 'Sindhu';
CREATE DATABASE bookly_db OWNER sindh;
```
    Connect 
        ```bash
        psql -U sindh -d bookly_db
        ```
6. Alembic Migrations
```bash
alembic init -t async migrations
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```
7. Start Redis
```bash
docker run --name redis -p 6379:6379 -d redis
docker ps
```
8. Start Celery Worker(fr background tasks)
```bash
celery -A app.celery_tasks.c_app worker --loglevel=info
```

#### Authentication Flow
- Register with email & password (hashed via bcrypt)

- Login → get access & refresh JWT tokens

- Use access token in Authorization header (Bearer <token>)

- Logout adds tokens to Redis blacklist to revoke access

- Refresh tokens to get new access tokens

#### MIDDLEWARE

- CORS Middleware (allow frontend on localhost:3000)

- TrustedHostMiddleware (restrict hosts)

- Error handlers for consistent API responses

##### Some tips

- Use selectinload() + scalars().first() to fix async loading errors

- Always hash passwords before storing

- Store JWT secret securely

- Revoke JWT tokens with Redis on logout

- Offload slow tasks (emails, notifications) with Celery