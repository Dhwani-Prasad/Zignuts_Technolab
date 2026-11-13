# TaskPro – Personal Task Management App

TaskPro is a full-stack personal task management web application built with **Django**, **Django REST Framework (DRF)**, **JWT Authentication (SimpleJWT)**, and **MySQL**. Users can register, log in, and manage their personal tasks. Each user has strict data isolation and can only see and manage their own tasks.

---

## 🌟 Key Features

### 👤 User Management & Security
- **JWT Token-Based Authentication**: Built with `djangorestframework-simplejwt` using access and refresh tokens.
- **User Registration**: Register with username, email, and password confirmation with instant validation.
- **Strict Data Isolation**: Tasks are tied to the logged-in user; users can never see, edit, or delete another user's tasks.
- **Protected Endpoints**: DRF permission classes (`IsAuthenticated`, `IsTaskOwner`) guard every API route.

### 📋 Task Management
- **Create Task**: Set title, description, due date, priority (`Low`, `Medium`, `High`), and status (`Pending`, `Completed`).
- **View Task List**: Clean, responsive dashboard cards with priority badges, status badges, and intelligent due date indicators (Overdue, Due Today, Tomorrow, Upcoming).
- **Filter by Status**: Seamless tabs to view `All Tasks`, `Pending`, or `Completed`.
- **Search & Priority Filtering**: Instant debounced search by task title or description, plus dropdown filter for priorities.
- **Date-Based Sorting**: Default sorting by due date ascending (earliest first), with options to toggle latest first, priority, or newest created.
- **Edit & Delete**: Full task editing via modal and delete confirmation prompt.
- **Quick Complete**: One-click toggle between pending and completed with visual strike-through feedback.
- **Dashboard Metrics**: Real-time stats cards showing Total Tasks, Pending, Completed, and High Priority counts.

### 💻 Modern Frontend
- Responsive UI built with **Tailwind CSS** and **Font Awesome 6**.
- Clean client-side architecture using the **Fetch API** (`/static/js/api.js`).
- Automatic JWT token storage in `localStorage` with silent token refresh on 401 expiration.
- Toast notifications for success alerts and inline error handling.

---

## 🏗️ Tech Stack

- **Backend**: Python 3.12, Django 5.x / 6.x, Django REST Framework
- **Authentication**: `djangorestframework-simplejwt` (JWT tokens)
- **Database**: MySQL 8.0 (configured via `pymysql` with SQLite fallback)
- **Frontend**: HTML5, Tailwind CSS (CDN), Vanilla JavaScript (ES6+ Fetch API), Font Awesome

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.10+ and MySQL installed.

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Database Configuration
You can configure MySQL credentials in `.env`:
```env
DB_ENGINE=mysql
DB_NAME=taskpro_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_FALLBACK_SQLITE=True
```

#### Automatic Database Initialization
To automatically create the MySQL database and apply migrations:
```powershell
python setup_mysql.py
```

Or apply migrations manually:
```powershell
python manage.py makemigrations tasks
python manage.py migrate
```

### 4. Run the Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
- **Application URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Register**: [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
- **Login**: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
- **Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Automated Tests

Run the comprehensive test suite (16 tests covering auth, CRUD, isolation, filters, sorting):
```powershell
python manage.py test tasks
```

---

## 📡 API Reference

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register a new user | No |
| `POST` | `/api/auth/login/` | Obtain JWT access & refresh tokens | No |
| `POST` | `/api/auth/refresh/` | Refresh access token | No |
| `GET` | `/api/auth/me/` | Get current logged-in user info | Yes (Bearer token) |

### Task Endpoints
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/tasks/` | List current user's tasks (supports `?search=`, `?status=`, `?priority=`, `?ordering=`) | Yes |
| `POST` | `/api/tasks/` | Create a new task | Yes |
| `GET` | `/api/tasks/{id}/` | Retrieve task details | Yes |
| `PUT` | `/api/tasks/{id}/` | Update full task | Yes |
| `PATCH` | `/api/tasks/{id}/` | Partially update task | Yes |
| `DELETE` | `/api/tasks/{id}/` | Delete task | Yes |
| `PATCH` | `/api/tasks/{id}/complete/` | Mark task as completed | Yes |
| `PATCH` | `/api/tasks/{id}/toggle/` | Toggle between pending and completed | Yes |
| `GET` | `/api/tasks/stats/` | Retrieve user dashboard stats (total, pending, completed, high) | Yes |

---

## 📁 Project Directory Structure
```
Django TaskPro/
├── manage.py
├── setup_mysql.py
├── requirements.txt
├── .env
├── .env.example
├── README.md
├── taskpro/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
│       └── 0001_initial.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── static/
    └── js/
        ├── api.js
        └── dashboard.js
```
