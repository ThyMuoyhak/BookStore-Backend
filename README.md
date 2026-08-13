# Book Store Backend API

FastAPI backend for the Book Store with PostgreSQL database.

## Features

- **Book**: title, category, description, price, discount price, multiple images
- **Authentication**: signup, login, JWT token-based auth

## Tech Stack

- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **JWT** - Authentication

## Project Structure

```
Backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py      # Signup, Login, Me
│   │   │   └── books.py     # Book CRUD
│   │   └── deps.py          # DB session & auth dependencies
│   ├── core/
│   │   ├── config.py        # Settings (.env)
│   │   ├── database.py      # SQLAlchemy engine/session
│   │   └── security.py      # Password hashing & JWT
│   ├── crud/
│   │   ├── book.py
│   │   └── user.py
│   ├── models/
│   │   ├── book.py          # Book + BookImage
│   │   └── user.py          # User
│   ├── schemas/
│   │   ├── book.py
│   │   └── user.py
│   └── main.py              # FastAPI app entry
├── .env                     # Environment variables
├── .gitignore
└── requirements.txt
```

## Setup

1. **Create virtual environment**

```bash
cd Backend
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure `.env`**

Edit `.env` with your database connection from Render.

> ⚠️ **Important:** The `dpg-d9u8r9740ujc73fq4pt0-a` hostname in the sample below is Render's **internal** hostname and only works inside Render's network. For **local** development, copy your **External Database URL** from Render and use that host instead.

```
# Replace with YOUR password and host (from Render's External Database URL)
DATABASE_URL=postgresql://bookstore_q5pc_user:YOUR_PASSWORD@dpg-d9u8r9740ujc73fq4pt0-a.oregon-postgres.render.com:5432/bookstore_q5pc
```

4. **Run the server**

```bash
python run.py
```

Or alternatively:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## API Endpoints

### Authentication

| Method | Endpoint          | Description             |
|--------|-------------------|-------------------------|
| POST   | `/api/auth/signup` | Register a new user     |
| POST   | `/api/auth/login`  | Login (returns JWT)     |
| GET    | `/api/auth/me`     | Get current user (auth) |

### Books

| Method | Endpoint      | Description                      |
|--------|---------------|----------------------------------|
| GET    | `/api/books`  | List books (filter by category/search, paginated) |
| GET    | `/api/books/{id}` | Get a single book           |
| POST   | `/api/books`  | Create a book (auth)             |
| PUT    | `/api/books/{id}` | Update a book (auth)         |
| DELETE | `/api/books/{id}` | Delete a book (auth)         |

### Health

| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| GET    | `/api/health`  | Health check         |

## Example Payloads

### Signup

```json
POST /api/auth/signup
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "secret123",
  "full_name": "John Doe"
}
```

### Login

```json
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secret123
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Create Book

```json
POST /api/books
Authorization: Bearer <token>

{
  "title": "Clean Code",
  "category": "Programming",
  "description": "A handbook of agile software craftsmanship.",
  "price": 45.99,
  "discount_price": 39.99,
  "images": [
    { "image_url": "https://example.com/cover.jpg", "is_primary": 1 },
    { "image_url": "https://example.com/back.jpg", "is_primary": 0 }
  ]
}
```

### List Books with Filters

```
GET /api/books?category=Programming&search=clean&skip=0&limit=20
```
