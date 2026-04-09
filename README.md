# Student Project Tracker

A full-stack AI-powered API system built with FastAPI, MySQL, JWT authentication, a machine learning model, Docker, and a Streamlit frontend. Deployed live on Render.

---

## What This Project Does

This system allows users to:
- Register and log in securely
- Create, view, update, and delete student projects
- Use an AI model to automatically classify a project description into a category (AI, Web, Data Science, or Mobile)

---

## Live Links

| Service | URL |
|--------|-----|
| Frontend | https://student-tracker-frontend-34zp.onrender.com |
| API Docs | https://student-tracker-api-ql07.onrender.com/docs |

---

## Project Structure

```
student-tracker/
├── main.py            # FastAPI app — all endpoints
├── database.py        # Database connection
├── models.py          # Database tables (User, Project)
├── schemas.py         # Request/response shapes
├── auth.py            # JWT login and password hashing
├── train_model.py     # ML model training script
├── app.py             # Streamlit frontend
├── Dockerfile         # Docker image for the API
├── docker-compose.yml # Runs API + database together
├── requirements.txt   # Python dependencies
└── .env               # Environment variables (not uploaded to GitHub)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI (Python) |
| Database | MySQL (local) / PostgreSQL (production) |
| ORM | SQLAlchemy |
| Authentication | JWT (JSON Web Tokens) |
| Password Hashing | bcrypt via passlib |
| ML Model | scikit-learn (TF-IDF + Naive Bayes) |
| Frontend | Streamlit |
| Containerization | Docker + docker-compose |
| Deployment | Render |

---

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/aakwadwo/student-tracker.git
cd student-tracker
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up MySQL
Make sure MySQL is running locally, then create the database:
```bash
mysql -u root -p
```
```sql
CREATE DATABASE student_tracker;
exit
```

### 5. Create a `.env` file
Create a file called `.env` in the project folder:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=student_tracker
SECRET_KEY=your-secret-key
```

### 6. Train the ML model
```bash
python train_model.py
```
This creates a `model.pkl` file used by the `/predict` endpoint.

### 7. Start the API
```bash
uvicorn main:app --reload
```
API runs at: http://127.0.0.1:8000
Swagger docs at: http://127.0.0.1:8000/docs

### 8. Start the frontend (in a separate terminal)
```bash
streamlit run app.py
```
Frontend runs at: http://localhost:8501

---

## How to Run with Docker

Make sure Docker Desktop is running, then:
```bash
docker-compose up --build
```
This starts both the API and a MySQL database in containers.

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Create a new user account |
| POST | `/login` | Login and receive a JWT token |

### Projects (all require login)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | Get all projects |
| POST | `/projects` | Create a new project |
| PUT | `/projects/{id}` | Update a project |
| DELETE | `/projects/{id}` | Delete a project |

### AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Predict the category of a project description |

---

## How the AI Model Works

1. `train_model.py` trains a text classifier on labeled project descriptions
2. The model uses TF-IDF to convert text into numbers and Naive Bayes to classify
3. It can predict 4 categories: **AI**, **Web**, **Data Science**, **Mobile**
4. The trained model is saved as `model.pkl`
5. When the API starts, it loads `model.pkl` into memory
6. When a request hits `POST /predict`, the description is passed to the model and a category is returned instantly

Example:
```json
Input:  { "description": "AI system for healthcare" }
Output: { "description": "AI system for healthcare", "category": "AI" }
```

---

## Authentication Flow

1. User registers via `POST /register` — password is hashed with bcrypt
2. User logs in via `POST /login` — receives a JWT access token
3. Token is included in the header of all protected requests
4. Server decodes the token to verify the user before allowing access
5. Without a valid token, all project endpoints return `401 Unauthorized`

---

## Deployment (Render)

The app is deployed on [Render](https://render.com) using two services:

- **Web Service** — runs the FastAPI backend
- **Web Service** — runs the Streamlit frontend
- **PostgreSQL** — free managed database on Render

Environment variable `DATABASE_URL` is set on Render to connect to the PostgreSQL database automatically.

---

## Phases Completed

| Phase | What Was Built |
|-------|---------------|
| Phase 1 | Basic FastAPI app with CRUD endpoints |
| Phase 2 | MySQL database integration with SQLAlchemy |
| Phase 3 | JWT authentication and protected routes |
| Phase 4 | ML model trained and served via /predict |
| Phase 5 | Dockerized with docker-compose |
| Phase 6 | Streamlit frontend |
| Phase 7 | Live deployment on Render |

---

## Author

Kwadwo Amoah Asumadu — built as part of a FastAPI to AI Deployment learning project.
