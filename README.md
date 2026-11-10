# Gym Booking API

Gym Booking API is a backend application built with Django and Django REST Framework.

The application allows users to view trainers and gym classes, create bookings, search and filter data, and manage their own records.

## Technologies

- Python
- Django
- Django REST Framework
- django-filter
- SQLite

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd gym-booking-api
```
Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Create .env based on .env.example.

Run migrations:
```bash
python manage.py migrate
```
Add sample data:
```bash
python manage.py seed
```
Run the server:
```bash
python manage.py runserver
```
## API Endpoints
| Method | URL | Description | Access |
|---|---|---|---|
| GET | /api/classes/ | List gym classes | Everyone |
| POST | /api/classes/ | Create gym class | Authenticated |
| GET | /api/classes/<id>/ | Gym class details | Everyone |
| PATCH | /api/classes/<id>/ | Update gym class | Owner |
| DELETE | /api/classes/<id>/ | Delete gym class | Owner |
| GET | /api/classes/available/ | Classes with available places | Everyone |
| GET | /api/trainers/ | List trainers | Everyone |
| GET | /api/trainers/<id>/ | Trainer details | Everyone |
| GET | /api/bookings/ | List bookings | Everyone |
| POST | /api/bookings/ | Create booking | Authenticated |
| PATCH | /api/bookings/<id>/ | Update booking | Owner |
| DELETE | /api/bookings/<id>/ | Delete booking | Owner |

## Filtering
Filter classes by trainer:
```blash
/api/classes/?trainer=1
```
Search:
```blash
/api/classes/?search=yoga
```
Ordering:
```blash
/api/classes/?ordering=-date
```

## Running with Docker and PostgreSQL

This project uses Django REST Framework, JWT authentication, PostgreSQL 17, and Docker Compose.

### Requirements

- Docker
- Docker Compose
- A local `.env` file configured from `.env.example`

### Start the application

```bash
docker compose up --build
```

Docker Compose starts two services:

- `web` — Django REST API
- `db` — PostgreSQL 17

The Django service waits until PostgreSQL is healthy and then applies database migrations automatically.

### Create an admin user

```bash
docker compose exec web python manage.py createsuperuser
```

### Add sample data

```bash
docker compose exec web python manage.py seed
```

### Check PostgreSQL

```bash
docker compose exec db psql -U app_user -d app_db
```

Inside `psql`:

```sql
\dt
SELECT * FROM gym_trainer;
SELECT * FROM gym_gymclass;
```

### API

The API is available at:

`http://localhost:8000/api/`

JWT login endpoint:

`http://localhost:8000/api/token/`

### Stop containers

```bash
docker compose down
```

PostgreSQL data is stored in the `postgres_data` Docker volume and persists across normal container restarts.