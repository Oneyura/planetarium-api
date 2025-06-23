# 🌌 Planetarium API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

**REST API for managing planetarium shows, reservations, and tickets**

</div>

---

## 🎯 About Project

**Planetarium API** is a modern REST API for managing planetarium sessions and reservations. It supports show themes, astronomy shows, domes, sessions, reservations, and ticket validation.

---

## ✨ Features

### 🎥 Show Management

* CRUD operations for show themes and astronomy shows
* Filtering by title, description, or theme

### 🏛️ Dome Management

* CRUD for domes with seat and row configurations

### 📅 Show Sessions

* Sessions linked to domes and shows
* Filtering by title and date

### 🎟️ Reservations

* Authenticated users can create reservations
* Ticket validation for seat and row limits
* Prevention of seat duplication

### 🔐 Authentication

* JWT-based authentication
* Roles: user and admin

---

## 🚀 Quick Start

```bash
# 1. Clone repository
https://github.com/Oneyura/planetarium-api.git
cd planetarium-api

# 2. Create .env file
cp .env.example .env

# 3. Run with Docker (coming soon)
docker-compose up --build

# 4. Or run locally:
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🔧 API Endpoints

### Show Themes

```http
GET    /api/planetarium/show_themes/       # List all themes (auth: required)
POST   /api/planetarium/show_themes/       # Create new theme (auth: admin)
```

### Astronomy Shows

```http
GET    /api/planetarium/astronomy_shows/   # Show list with filters (auth: required)
POST   /api/planetarium/astronomy_shows/   # Create a show (auth: admin)
```

### Domes

```http
GET    /api/planetarium/planetarium_domes/ # List domes (auth: admin)
```

### Show Sessions

```http
GET    /api/planetarium/show_sessions/     # Get sessions (auth: required)
POST   /api/planetarium/show_sessions/     # Create session (auth: admin)
```

### Reservations

```http
GET    /api/planetarium/reservations/      # My reservations (auth: required)
POST   /api/planetarium/reservations/      # Book tickets (auth: required)
```

### Auth (JWT)

```http
POST   /api/auth/register/                 # Register
POST   /api/auth/token/                    # Obtain token
GET    /api/auth/me/                       # View current user
```

| Role     | Description                            |
| -------- | -------------------------------------- |
| 🔐 User  | Can view shows and create reservations |
| 👑 Admin | Full CRUD access for all resources     |

---

## 🛠️ Technologies

* Django 5.2
* Django REST Framework
* drf-spectacular (OpenAPI docs)
* PostgreSQL
* Docker (planned)
* JWT (SimpleJWT)

---

## ✅ Testing

```bash
# Run all tests
python manage.py test
```

Covers:

* CRUD for shows, domes, and sessions
* Reservation creation with ticket validation
* Validation of seat boundaries and duplicate protection

---

## 📞 Support

Issues and ideas? Please create an [Issue](https://github.com/Oneyura/planetarium-api/issues).

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ If you like this project, leave a star!**

Made with ❤️ for stars and planets ☄️

</div>
