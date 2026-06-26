from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from typing import List
import io

from database import get_db
from models import Exam, ExamExercise, Exercise
from schemas import ExamCreate, ExamOut, AddExerciseToExam, AutoGenerateRequest
from exam_generator import generate_exam
from exporters import export_to_pdf, export_to_docx
# from services.exam_generator import generate_exam
# from services.exporters import export_to_pdf, export_to_docx

router = APIRouter(prefix="/api/exams", tags=["exams"])


def _get_exam_or_404(exam_id: int, db: Session) -> Exam:
    exam = (
        db.query(Exam)
        .options(
            joinedload(Exam.exam_exercises).joinedload(ExamExercise.exercise)
        )
        .filter(Exam.id == exam_id)
        .first()
    )
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


# ── CRUD ──────────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ExamOut])
def list_exams(db: Session = Depends(get_db)):
    return (
        db.query(Exam)
        .options(
            joinedload(Exam.exam_exercises).joinedload(ExamExercise.exercise)
        )
        .order_by(Exam.created_at.desc())
        .all()
    )


@router.post("/", response_model=ExamOut, status_code=201)
def create_exam(payload: ExamCreate, db: Session = Depends(get_db)):
    exam = Exam(**payload.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.get("/{exam_id}", response_model=ExamOut)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    return _get_exam_or_404(exam_id, db)


@router.delete("/{exam_id}", status_code=204)
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    db.delete(exam)
    db.commit()


# ── Exercise management inside an exam ───────────────────────────────────────

@router.post("/{exam_id}/exercises", response_model=ExamOut)
def add_exercise_to_exam(
    exam_id: int,
    payload: AddExerciseToExam,
    db: Session = Depends(get_db)
):
    exam = _get_exam_or_404(exam_id, db)

    # Prevent duplicate exercises in the same exam
    already = any(
        ee.exercise_id == payload.exercise_id
        for ee in exam.exam_exercises
    )
    if already:
        raise HTTPException(
            status_code=400,
            detail="This exercise is already in the exam"
        )

    exercise = db.query(Exercise).filter(Exercise.id == payload.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    order = payload.order if payload.order is not None else len(exam.exam_exercises)
    ee = ExamExercise(exam_id=exam_id, exercise_id=payload.exercise_id, order=order)
    db.add(ee)
    db.commit()
    return _get_exam_or_404(exam_id, db)


@router.delete("/{exam_id}/exercises/{exercise_id}", response_model=ExamOut)
def remove_exercise_from_exam(
    exam_id: int,
    exercise_id: int,
    db: Session = Depends(get_db)
):
    ee = (
        db.query(ExamExercise)
        .filter(
            ExamExercise.exam_id == exam_id,
            ExamExercise.exercise_id == exercise_id
        )
        .first()
    )
    if not ee:
        raise HTTPException(status_code=404, detail="Exercise not in this exam")
    db.delete(ee)
    db.commit()
    return _get_exam_or_404(exam_id, db)


# ── Auto-generation ───────────────────────────────────────────────────────────

@router.post("/generate", response_model=ExamOut, status_code=201)
def auto_generate_exam(
    payload: AutoGenerateRequest,
    db: Session = Depends(get_db)
):
    try:
        exam = generate_exam(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _get_exam_or_404(exam.id, db)


# ── Export ────────────────────────────────────────────────────────────────────

@router.get("/{exam_id}/export/pdf")
def export_exam_pdf(exam_id: int, db: Session = Depends(get_db)):
    exam = _get_exam_or_404(exam_id, db)
    pdf_bytes = export_to_pdf(exam)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="exam_{exam_id}.pdf"'
        }
    )


@router.get("/{exam_id}/export/docx")
def export_exam_docx(exam_id: int, db: Session = Depends(get_db)):
    exam = _get_exam_or_404(exam_id, db)
    docx_bytes = export_to_docx(exam)
    return StreamingResponse(
        io.BytesIO(docx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="exam_{exam_id}.docx"'
        }
    )
