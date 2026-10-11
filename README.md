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

## Running with Docker

1. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Replace `SECRET_KEY` with your own secure Django secret key.

3. Build and start the application:

   ```bash
   docker compose up --build
   ```

4. Open the API at `http://localhost:8000/api/`.

5. Create a superuser if needed:

   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. Add sample data if the database is empty:

   ```bash
   docker compose exec web python manage.py seed
   ```

### JWT Authentication

- `POST /api/token/` — obtain access and refresh tokens.
- `POST /api/token/refresh/` — refresh an access token.
- `POST /api/token/verify/` — verify a token.

Authenticated requests use the header:

`Authorization: Bearer <access_token>`