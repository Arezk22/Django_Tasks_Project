# Django Tasks Project

A full-stack web application built with **Django 6** that combines a task management system with a student records module, featuring both a traditional web interface and a REST API.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Authentication](#authentication)

---

## Overview

Django Tasks Project is a multi-app Django project with two main modules:

- **Tasks App** — A personal task manager where users can create, view, update, and delete tasks, with support for status tracking (Pending / In Progress / Done) and priority levels.
- **Students App** — A simple CRUD module for managing student records including department and course enrollment data.

The project also exposes a full-featured **REST API** (built with Django REST Framework) for programmatic access to the Tasks module.

---

## Features

### Tasks App

- User registration and login with session-based authentication
- Each user sees only their own tasks (data isolation)
- Admin users can view and manage **all** tasks across all users
- Create, read, update, and delete tasks
- Task fields: title, description, status, priority, completion flag, and due date
- Tasks grouped by status on the list view

### Students App

- Full CRUD operations for student records
- Fields: first name, last name, age (18–28), course name, department (IT / CS / IS)
- Flash messages on create, update, and delete

### REST API (Tasks)

- Token-based and session-based authentication
- Function-based views, Class-based views (APIView), and ViewSets — all three patterns implemented
- Filtering by `completed` and `priority`
- Search across `title` and `description`
- Ordering by `created_at` and `due_date`
- Pagination (5 items per page)
- Custom actions:
  - `GET /api/v1/tasks/summary/` — returns task statistics (total, completed, pending, in progress, done)
  - `POST /api/v1/tasks/{id}/mark_status/` — updates only the status of a specific task
- Custom permission: `IsOwnerOrAdmin` — only the task owner or an admin can access/modify a task

---

## Project Structure

```
Django_Tasks_Project/
│
├── manage.py
├── requirements.txt
│
├── mysite/                     # Project configuration
│   ├── settings.py
│   ├── urls.py                 # Root URL dispatcher
│   ├── wsgi.py
│   └── asgi.py
│
├── tasks/                      # Tasks application
│   ├── models.py               # Task model
│   ├── views.py                # Web views (login, register, CRUD)
│   ├── forms.py                # TaskForm
│   ├── urls.py                 # Web URL patterns
│   ├── admin.py
│   ├── templates/tasks/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── task_list.html
│   │   ├── task_form.html
│   │   ├── task_details.html
│   │   └── task_confirm_delete.html
│   └── api/
│       ├── views.py            # FBV, CBV, and ViewSet API views
│       ├── serializers.py      # TaskSerializer
│       ├── permissions.py      # IsOwnerOrAdmin permission
│       └── urls.py             # API URL patterns
│
└── students/                   # Students application
    ├── models.py               # Student model
    ├── views.py                # CRUD views
    ├── forms.py                # StudentForm
    ├── urls.py                 # URL patterns
    ├── admin.py
    └── templates/students/
        ├── base.html
        ├── student_list.html
        ├── student_form.html
        └── student_confirm_delete.html
```

---

## Tech Stack

| Layer     | Technology                       |
| --------- | -------------------------------- |
| Backend   | Python 3, Django 6.0.5           |
| API       | Django REST Framework 3.17.1     |
| Filtering | django-filter 25.2               |
| Database  | SQLite (default)                 |
| Frontend  | Django Templates + HTML          |
| Auth      | Django built-in auth + DRF Token |

---

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/Arezk22/Django_Tasks_Project.git
cd Django_Tasks_Project
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Apply migrations**

```bash
python manage.py migrate
```

**5. Create a superuser (admin)**

```bash
python manage.py createsuperuser
```

**6. Run the development server**

```bash
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`

---

## Usage

| URL                      | Description                |
| ------------------------ | -------------------------- |
| `/tasks/`                | Task list (requires login) |
| `/tasks/create/`         | Create a new task          |
| `/tasks/update/<id>/`    | Edit a task                |
| `/tasks/delete/<id>/`    | Delete a task              |
| `/tasks/details/<id>/`   | View task details          |
| `/tasks/login/`          | Login page                 |
| `/tasks/register/`       | Register new user          |
| `/tasks/logout/`         | Logout                     |
| `/students/`             | Student list               |
| `/students/add/`         | Add a new student          |
| `/students/edit/<id>/`   | Edit a student             |
| `/students/delete/<id>/` | Delete a student           |
| `/admin/`                | Django admin panel         |

---

## API Reference

Base URL: `/api/v1/`

### Get Auth Token

```
POST /api/v1/token/
Body: { "username": "...", "password": "..." }
```

### Tasks Endpoints (ViewSet)

| Method | Endpoint                          | Description                     |
| ------ | --------------------------------- | ------------------------------- |
| GET    | `/api/v1/tasks/`                  | List all tasks for current user |
| POST   | `/api/v1/tasks/`                  | Create a new task               |
| GET    | `/api/v1/tasks/<id>/`             | Get task details                |
| PUT    | `/api/v1/tasks/<id>/`             | Full update of a task           |
| PATCH  | `/api/v1/tasks/<id>/`             | Partial update of a task        |
| DELETE | `/api/v1/tasks/<id>/`             | Delete a task                   |
| GET    | `/api/v1/tasks/summary/`          | Get task count statistics       |
| POST   | `/api/v1/tasks/<id>/mark_status/` | Update task status only         |

### Query Parameters (on list endpoint)

| Parameter   | Example              | Description              |
| ----------- | -------------------- | ------------------------ |
| `completed` | `?completed=true`    | Filter by completion     |
| `priority`  | `?priority=high`     | Filter by priority       |
| `search`    | `?search=meeting`    | Search title/description |
| `ordering`  | `?ordering=due_date` | Sort results             |

---

## Authentication

The API supports two authentication methods:

- **Token Authentication** — obtain a token via `POST /api/v1/token/` and send it in the header:
  ```
  Authorization: Token <your_token_here>
  ```
- **Session Authentication** — used automatically when accessing the API through the browser.

### Permissions

- Regular users can only access their own tasks.
- Staff/admin users can access and manage all tasks.
- Unauthenticated requests to protected endpoints return `401 Unauthorized`.

---

## Data Models

### Task

| Field         | Type          | Description                        |
| ------------- | ------------- | ---------------------------------- |
| `title`       | CharField     | Task title (max 200 chars)         |
| `description` | TextField     | Optional description               |
| `status`      | CharField     | `pending` / `in_progress` / `done` |
| `priority`    | CharField     | `low` / `medium` / `high`          |
| `completed`   | BooleanField  | Completion flag (default: False)   |
| `due_date`    | DateField     | Optional due date                  |
| `user`        | ForeignKey    | Linked to Django User              |
| `created_at`  | DateTimeField | Auto-set on creation               |
| `updated_at`  | DateTimeField | Auto-updated on save               |

### Student

| Field         | Type          | Description                    |
| ------------- | ------------- | ------------------------------ |
| `f_name`      | CharField     | First name                     |
| `l_name`      | CharField     | Last name (optional)           |
| `age`         | IntegerField  | Age (18–28, validated)         |
| `course_name` | CharField     | Optional course name           |
| `dept_name`   | CharField     | Department: `it` / `cs` / `is` |
| `enrolled_at` | DateTimeField | Auto-set on enrollment         |

---

## Author

**Ahmed Rezk** — [@Arezk22](https://github.com/Arezk22)
