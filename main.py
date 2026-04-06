from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Project, User
from schemas import ProjectCreate, ProjectUpdate, ProjectResponse, UserCreate, UserResponse, Token
from auth import hash_password, verify_password, create_access_token, get_current_user
from typing import List
import pickle
from pydantic import BaseModel as PydanticBaseModel


# Load the ML model
with open("model.pkl", "rb") as f:
    ml_model = pickle.load(f)

# Input schema for prediction
class PredictRequest(PydanticBaseModel):
    description: str

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Project Tracker")


# --- REGISTER ---
@app.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# --- LOGIN ---
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- GET all projects (protected) ---
@app.get("/projects", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Project).all()


# --- POST create a project (protected) ---
@app.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = Project(
        title=project.title,
        description=project.description,
        status=project.status
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


# --- PUT update a project (protected) ---
@app.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, update: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if update.title is not None:
        project.title = update.title
    if update.description is not None:
        project.description = update.description
    if update.status is not None:
        project.status = update.status
    db.commit()
    db.refresh(project)
    return project


# --- DELETE a project (protected) ---
@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": f"Project {project_id} deleted"}


# --- POST predict project category ---
@app.post("/predict")
def predict_category(request: PredictRequest):
    prediction = ml_model.predict([request.description])[0]
    return {
        "description": request.description,
        "category": prediction
    }