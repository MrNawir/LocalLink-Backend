# LocalLink Backend API

A RESTful API built with Flask and SQLAlchemy for the LocalLink local services marketplace.

![Python](https://img.shields.io/badge/Python-3.8-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-green)
![SQLite](https://img.shields.io/badge/SQLite-3-orange)

## Features

- **RESTful API** - Full CRUD operations for services, categories, bookings, and users
- **SQLite Database** - Lightweight, file-based database for easy development
- **CORS Enabled** - Cross-origin requests supported for frontend integration
- **Seed Data** - Pre-populated with realistic demo data and high-quality images

## Tech Stack

- **Framework**: Flask
- **ORM**: Flask-SQLAlchemy
- **Database**: SQLite
- **Migrations**: Flask-Migrate
- **CORS**: Flask-CORS

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |
| GET | `/categories/:id` | Get single category |
| POST | `/categories` | Create category |
| PATCH | `/categories/:id` | Update category |
| DELETE | `/categories/:id` | Delete category |
| GET | `/services` | List all services |
| GET | `/services/:id` | Get single service |
| POST | `/services` | Create service |
| PATCH | `/services/:id` | Update service |
| DELETE | `/services/:id` | Delete service |
| GET | `/bookings` | List all bookings |
| POST | `/bookings` | Create booking |
| PATCH | `/bookings/:id` | Update booking status |
| GET | `/users` | List all users |

## Installation

### Prerequisites
- Python 3.8.13 (recommended via pyenv)
- pipenv

### Setup

1. **Install Python 3.8.13 with pyenv:**
   ```bash
   pyenv install 3.8.13
   pyenv local 3.8.13
   ```

2. **Install dependencies:**
   ```bash
   pipenv install
   ```

3. **Create database tables:**
   ```bash
   pipenv run python -c "from config import app, db; from models import *; app.app_context().push(); db.create_all()"
   ```

4. **Seed the database:**
   ```bash
   pipenv run python seed.py
   ```

5. **Run the server:**
   ```bash
   pipenv run python app.py
   ```

The API will be available at `http://localhost:5555`

## Project Structure

```
LocalLink-Backend/
├── app.py          # Main application with all API routes
├── config.py       # Flask configuration and extensions
├── models.py       # SQLAlchemy models (User, Service, Category, Booking)
├── seed.py         # Database seeding script
├── Pipfile         # Python dependencies
└── README.md
```

## Running as a Service

The backend can run as a systemd service for production:

```bash
sudo systemctl start locallink-backend
sudo systemctl enable locallink-backend
```

## Authors

LocalLink Team - School Project 2026