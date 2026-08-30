# Restaurant Management System

A backend-based Restaurant Management System developed using Django and Django REST Framework.

## Features

- Menu Management
- Restaurant Table Management
- Table Reservations
- Order Management
- Inventory Management
- Automatic Inventory Updates
- Table Availability Checking
- REST APIs
- Django Admin Panel

## Technologies

- Python
- Django
- Django REST Framework
- SQLite

## API Endpoints

- GET /api/menu/
- GET /api/tables/
- GET /api/reservations/
- POST /api/reservations/
- GET /api/orders/
- POST /api/orders/
- GET /api/inventory/
- POST /api/inventory/

## How to Run

1. Clone the repository.
2. Open the Task-3-Restaurant-Management folder.
3. Create a virtual environment.
4. Install dependencies using:

   pip install -r requirements.txt

5. Run migrations:

   python manage.py migrate

6. Start the server:

   python manage.py runserver

7. Open:

   http://127.0.0.1:8000/

## Admin Panel

Admin panel:

http://127.0.0.1:8000/admin/