# LocalLink Backend API

> A RESTful API built with Flask and SQLAlchemy for the LocalLink local services marketplace.

[![Python](https://img.shields.io/badge/Python-3.8-blue?style=flat-square)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green?style=flat-square)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange?style=flat-square)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)

## Related Repositories

| Repository | Description |
|------------|-------------|
| **[LocalLink-Frontend](https://github.com/MrNawir/LocalLink-Frontend)** | React frontend application |
| **[LocalLink-Backend](https://github.com/MrNawir/LocalLink-Backend)** | Flask API (this repo) |

## Live Demo

**[View Live App](https://locallink.dpdns.org)**

### Deployment Details

The live demo is hosted on a **Debian 13 (Trixie) VPS** with the following setup:

- **Web Server**: Nginx (reverse proxy)
- **Process Manager**: systemd services for backend and frontend
- **Domain**: Free subdomain from [digitalplat.org](https://domain.digitalplat.org)
- **CDN/Security**: Cloudflare proxy for SSL and DDoS protection

---

## Contributors

### Backend Team
| Name | Role |
|------|------|
| Ibrahim Abdu | Backend Developer |
| Esther Nekesa | Backend Developer |
| Julius Mutinda | Backend Developer |

### Frontend Team
| Name | Role |
|------|------|
| Abdimalik Kulow | Frontend Developer |
| Megan Mumbi | Frontend Developer |
| Abdullahi Omar | Frontend Developer |

---

## Features

- **RESTful API** - Full CRUD operations for services, categories, bookings, and users
- **JWT Authentication** - Secure token-based authentication with Flask-JWT-Extended
- **Password Hashing** - Bcrypt encryption for secure password storage
- **Role-Based Access** - Client, Provider, and Admin roles with protected endpoints
- **SQLite Database** - Lightweight, file-based database for easy development
- **CORS Enabled** - Cross-origin requests supported for frontend integration
- **Seed Data** - Pre-populated with realistic demo data and high-quality images

## Tech Stack

- **Framework**: Flask 3.0
- **ORM**: Flask-SQLAlchemy
- **Database**: SQLite
- **Authentication**: Flask-JWT-Extended + Flask-Bcrypt
- **CORS**: Flask-CORS

---

## Quick Start (Local Development)

> Complete setup in under 5 minutes.

### Prerequisites

- **Python 3.8+** (check with `python3 --version`)
- **pip** (Python package manager)
- **Node.js 18+** (for frontend - check with `node --version`)

### Step 1: Clone Both Repositories

```bash
# Create project folder
mkdir LocalLink && cd LocalLink

# Clone backend
git clone https://github.com/MrNawir/LocalLink-Backend.git
cd LocalLink-Backend

# Switch to development branch
git checkout ibrahim/dev
```

### Step 2: Install Backend Dependencies

```bash
# Option A: Using pipenv (recommended)
pip install pipenv
pipenv install
pipenv shell

# Option B: Using pip directly
pip install -r requirements.txt
```

### Step 3: Initialize Database & Seed Data

```bash
# Create database tables
python -c "from config import app, db; from models import *; app.app_context().push(); db.create_all()"

# Seed with demo data
python seed.py
```

### Step 4: Start the Backend Server

```bash
python app.py
```

Backend running at `http://localhost:5555`

### Step 5: Setup Frontend (New Terminal)

```bash
# Navigate to frontend
cd ../
git clone https://github.com/MrNawir/LocalLink-Frontend.git
cd LocalLink-Frontend
git checkout ibrahim/dev

# Install and run
cd client
npm install
npm run dev
```

Frontend running at `http://localhost:5173`

---

## Test Accounts

| Role | Email | Password | Dashboard |
|------|-------|----------|-----------|
| **Admin** | admin@locallink.com | admin123 | `/admin` |
| **Provider** | provider0@example.com | password123 | `/provider` |
| **Client** | client0@example.com | password123 | `/dashboard` |

---

## API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |
| GET | `/categories/:id` | Get single category |
| GET | `/services` | List all services |
| GET | `/services/:id` | Get single service |
| GET | `/users` | List all users |

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/me` | Get current user profile |
| PATCH | `/auth/me` | Update profile |
| POST | `/auth/change-password` | Change password |

### Protected Endpoints (Require JWT)

| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| POST | `/bookings` | Create booking | Any |
| GET | `/auth/my-bookings` | Get user's bookings | Client |
| PATCH | `/auth/my-bookings/:id` | Cancel/reschedule | Client |
| GET | `/provider/bookings` | Get provider's gigs | Provider |
| PATCH | `/provider/bookings/:id` | Update gig status | Provider |
| GET | `/admin/users` | List all users | Admin |
| PATCH | `/admin/users/:id` | Update user role | Admin |
| DELETE | `/admin/users/:id` | Delete user | Admin |

---

## Project Structure

```
LocalLink-Backend/
├── app.py          # Main application with API routes
├── auth.py         # Authentication blueprint (JWT, roles)
├── config.py       # Flask configuration and extensions
├── models.py       # SQLAlchemy models (User, Service, Category, Booking)
├── seed.py         # Database seeding script with demo data
├── Pipfile         # Python dependencies (pipenv)
├── requirements.txt # Python dependencies (pip)
└── README.md
```

## Database Models

```
User (id, username, email, password_hash, role, is_active, image_url)
  └── role: 'client' | 'provider' | 'admin'

Category (id, name, image_url)
  └── has many Services

Service (id, title, description, price, image_url, provider_id, category_id)
  └── belongs to User (provider) and Category

Booking (id, service_id, client_id, date, status, notes, location, contact_phone)
  └── status: 'pending' | 'confirmed' | 'completed' | 'cancelled'
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pipenv install` or `pip install -r requirements.txt` |
| Database errors | Delete `instance/locallink.db` and re-run seed |
| CORS errors | Ensure backend runs on port 5555, frontend on 5173 |
| JWT errors | Token expired - login again to get new token |

---

## License

This project is part of a school project for educational purposes.

**LocalLink Team - 2026**