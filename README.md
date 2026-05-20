# My First Django Project

A simple Django web application built as part of a learning project.
The project includes two main Django apps:

- `tasks` for task management with login, registration, and CRUD operations
- `students` for managing student records with basic CRUD operations

It also includes a Django REST Framework API for tasks, with token authentication support.

## Features

- Task management
  - List tasks
  - Create, update, delete tasks
  - View task details
  - User login, logout, and registration
- Student management
  - List students
  - Add new students
  - Edit student records
  - Delete students
- REST API for tasks
  - API endpoints under `/api/v1/`
  - Token authentication via `/api/v1/token/`
- Uses SQLite database by default

## Requirements

- Python 3.11 or compatible
- Django 6.0.5
- Django REST Framework 3.17.1
- django-filter 25.2
- asgiref 3.11.1
- sqlparse 0.5.5
- tzdata 2026.2

Install using:

```bash
python -m pip install -r requirements.txt
```

## Setup

1. Navigate to the project directory:
   ```bash
   cd e:\Iti6month\Django\Day 01\my_first_project
   ```
2. Apply migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

- Open `http://127.0.0.1:8000/tasks/` for the task management app.
- Open `http://127.0.0.1:8000/students/` for the student management app.
- Open `http://127.0.0.1:8000/admin/` for the Django admin site.
- Use `/api/v1/` to access task API endpoints.
- Use `/api/v1/token/` to obtain an authentication token.

## Project Structure

- `mysite/` - Django project configuration
  - `settings.py` - project settings
  - `urls.py` - root URL routing
- `tasks/` - task management app
  - `views.py` - task views and authentication
  - `urls.py` - task app routes
  - `templates/tasks/` - task-related HTML templates
  - `api/` - Django REST Framework API definitions
- `students/` - student management app
  - `views.py` - student views
  - `urls.py` - student app routes
  - `templates/students/` - student-related HTML templates
- `db.sqlite3` - SQLite database file

## Notes

- `DEBUG` is enabled in settings. Do not use this configuration for production.
- Database changes are stored in `db.sqlite3`.
- The project uses Django's built-in authentication system.
