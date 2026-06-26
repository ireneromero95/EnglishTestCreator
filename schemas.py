from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime
from models import Category, ExerciseType


# ── Exercise ──────────────────────────────────────────────────────────────────

class ExerciseBase(BaseModel):
    title: str
    category: Category
    exercise_type: ExerciseType
    instructions: str
    content: Any          # dict structure varies by type
    difficulty: Optional[str] = "medium"


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseOut(ExerciseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Exam ──────────────────────────────────────────────────────────────────────

class ExamExerciseOut(BaseModel):
    order: int
    exercise: ExerciseOut

    class Config:
        from_attributes = True


class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    level: Optional[str] = None


class ExamCreate(ExamBase):
    pass


class ExamOut(ExamBase):
    id: int
    created_at: datetime
    exam_exercises: List[ExamExerciseOut] = []

    class Config:
        from_attributes = True


# ── Auto-generation request ───────────────────────────────────────────────────

class AutoGenerateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    level: Optional[str] = None
    grammar: int = 0
    vocabulary: int = 0
    reading: int = 0
    writing: int = 0


# ── Add exercise to exam ──────────────────────────────────────────────────────

class AddExerciseToExam(BaseModel):
    exercise_id: int
    order: Optional[int] = None
