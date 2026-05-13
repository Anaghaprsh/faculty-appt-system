# 📅 DevOps-Enabled Faculty Availability and Appointment Management System

**Group 5 | Department of Computer Science**
| Student | USN |
|---|---|
| Anagha H Prashanth | 1DT23CS019 |
| Amisha AR | 1DT23CS015 |
| Chinmayi Padmaraj | 1DT23CS044 |

---

## 📌 Project Overview

A RESTful web application built with **Flask** that allows students to:
- View faculty availability and time slots
- Book appointments with faculty members
- Manage and track bookings

The project follows a full **DevOps lifecycle** using Git, GitHub Actions, Docker, and PyTest.

---

## 🛠️ Tools Used

| Tool | Purpose |
|---|---|
| **Git** | Version control — branching, commits, pull requests |
| **GitHub Actions** | CI/CD pipeline — auto-test and auto-deploy on push |
| **Docker** | Containerize the Flask app for consistent deployment |
| **PyTest** | Automated unit & integration testing (10 test cases) |

---

## 📁 Project Structure

```
faculty-appt-system/
├── app/
│   ├── __init__.py
│   └── app.py               # Flask REST API
├── tests/
│   ├── __init__.py
│   └── test_app.py          # PyTest test suite (10 tests)
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions pipeline
├── Dockerfile               # Multi-stage Docker build
├── requirements.txt
└── README.md
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API home / status |
| GET | `/health` | Health check |
| GET | `/api/faculty` | List all faculty |
| GET | `/api/faculty/<id>` | Get faculty by ID |
| GET | `/api/faculty/<id>/availability` | Get available slots |
| POST | `/api/appointments` | Book an appointment |
| GET | `/api/appointments` | View all appointments |

---

## 🧪 Running Tests (PyTest)

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

**Test Results:** 10/10 PASSED ✅

---

## 🐳 Running with Docker

```bash
# Build the image
docker build --target production -t faculty-appt-system .

# Run the container
docker run -p 5000:5000 faculty-appt-system

# App will be live at: http://localhost:5000
```

---

## ⚙️ GitHub Actions CI/CD Pipeline

The pipeline triggers automatically on every `push` to `main` or `develop`:

```
Push to GitHub
     │
     ▼
┌─────────────┐
│  Job 1      │  Run PyTest suite
│  TEST       │  → Uploads test results as artifact
└──────┬──────┘
       │ (on success)
       ▼
┌─────────────┐
│  Job 2      │  Build Docker image
│  DOCKER     │  → Push to DockerHub with SHA tag
└──────┬──────┘
       │ (on main branch only)
       ▼
┌─────────────┐
│  Job 3      │  Deploy to production server
│  DEPLOY     │
└─────────────┘
```

---

## 📖 Git Workflow

```bash
# Clone the repo
git clone https://github.com/<username>/faculty-appt-system.git

# Create a feature branch
git checkout -b feature/add-cancel-appointment

# Make changes, then commit
git add .
git commit -m "feat: add cancel appointment endpoint"

# Push and open Pull Request
git push origin feature/add-cancel-appointment
```

Branches used:
- `main` — production-ready code
- `develop` — integration branch
- `feature/*` — individual features per student
