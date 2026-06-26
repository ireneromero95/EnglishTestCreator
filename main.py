from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from database import engine, get_db
import models
from models import Exam, ExamExercise, Exercise, Category, ExerciseType
import exams, exercises

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Exam Builder", version="1.0.0")

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API routers
app.include_router(exams.router)
app.include_router(exercises.router)


# ── UI Routes ─────────────────────────────────────────────────────────────────

@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    all_exams = (
        db.query(Exam)
        .options(joinedload(Exam.exam_exercises))
        .order_by(Exam.created_at.desc())
        .all()
    )
    exercise_counts = {
        cat.value: db.query(Exercise).filter(Exercise.category == cat).count()
        for cat in Category
    }
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "exams": all_exams,
        "exercise_counts": exercise_counts,
    })


@app.get("/exams/new")
def new_exam_page(request: Request, db: Session = Depends(get_db)):
    all_exercises = db.query(Exercise).order_by(Exercise.category, Exercise.title).all()
    return templates.TemplateResponse("exam_create.html", {
        "request": request,
        "exercises": all_exercises,
        "categories": [c.value for c in Category],
    })


@app.get("/exams/{exam_id}")
def exam_detail_page(exam_id: int, request: Request, db: Session = Depends(get_db)):
    exam = (
        db.query(Exam)
        .options(joinedload(Exam.exam_exercises).joinedload(ExamExercise.exercise))
        .filter(Exam.id == exam_id)
        .first()
    )
    if not exam:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    all_exercises = db.query(Exercise).order_by(Exercise.category, Exercise.title).all()
    exam_exercise_ids = {ee.exercise_id for ee in exam.exam_exercises}

    return templates.TemplateResponse("exam_detail.html", {
        "request": request,
        "exam": exam,
        "all_exercises": all_exercises,
        "exam_exercise_ids": exam_exercise_ids,
    })

@app.get("/exercises/new")
def new_exercise_page(request: Request):
    return templates.TemplateResponse("exercise_create.html", {
        "request": request,
        "categories": [c.value for c in Category],
        "exercise_types": [t.value for t in ExerciseType],
    })


@app.get("/exercises")
def exercises_page(request: Request, db: Session = Depends(get_db)):
    all_exercises = db.query(Exercise).order_by(Exercise.category, Exercise.title).all()
    return templates.TemplateResponse("exercises.html", {
        "request": request,
        "exercises": all_exercises,
        "categories": [c.value for c in Category],
    })
