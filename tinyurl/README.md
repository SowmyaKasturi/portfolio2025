# 🔗 TinyURL - Flask-Based URL Shortener

This is a complete backend implementation of a URL shortener service, built with **Flask**, featuring persistent storage, caching, and multiple authentication methods. Inspired by real-world services like TinyURL, this app is structured to reflect production-grade backend design and development.

---

## ✅ Features Implemented

### 🧱 Core Functionality
- URL shortening using hash-based slugs
- Redirect logic to the original URL
- Auto-handling of duplicates and edge cases

### 🗃️ Storage
- In-memory logic → upgraded to SQLite using SQLAlchemy
- Full model: `id`, `original_url`, `hashcode`, `created_at`

### ⚡ Caching
- `lru_cache` (local memory cache) for fast repeated lookups
- Redis integration for scalable, multi-process caching

### 🔐 Authentication
Multiple authentication layers implemented:
- ✅ **API Key Auth** via `X-API-Key` header
- ✅ **Basic Auth** using HTTP Authorization headers
- ✅ **JWT Auth** for stateless, token-based API protection

> Frontend or API clients are expected to request a token from `/login` and include it in headers using:
> ```
> Authorization: Bearer <token>
> ```

---

## 🛠️ Technologies Used

| Stack Piece    | Tool          |
|----------------|---------------|
| Language       | Python 3.8    |
| Web Framework  | Flask         |
| ORM            | SQLAlchemy    |
| Caching        | Redis         |
| Auth Tokens    | PyJWT         |
| HTTP Testing   | Postman       |
| Containerization (next) | Docker  |

---

## 🧪 Development Flow

### 1. Run the app
```bash
python app.py

