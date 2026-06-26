from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Exercise, Category
from schemas import ExerciseCreate, ExerciseOut

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


@router.get("/", response_model=List[ExerciseOut])
def list_exercises(
    category: Optional[Category] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Exercise)
    if category:
        q = q.filter(Exercise.category == category)
    return q.order_by(Exercise.created_at.desc()).all()


@router.post("/", response_model=ExerciseOut, status_code=201)
def create_exercise(payload: ExerciseCreate, db: Session = Depends(get_db)):
    exercise = Exercise(**payload.model_dump())
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.get("/{exercise_id}", response_model=ExerciseOut)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.put("/{exercise_id}", response_model=ExerciseOut)
def update_exercise(
    exercise_id: int,
    payload: ExerciseCreate,
    db: Session = Depends(get_db)
):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    for key, value in payload.model_dump().items():
        setattr(exercise, key, value)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(exercise)
    db.commit()
