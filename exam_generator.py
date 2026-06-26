import random
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Exercise, Exam, ExamExercise, Category
from schemas import AutoGenerateRequest


def generate_exam(db: Session, request: AutoGenerateRequest) -> Exam:
    """
    Creates an Exam by randomly picking exercises per category
    without repeating any exercise within the same exam.
    """
    category_counts = {
        Category.grammar: request.grammar,
        Category.vocabulary: request.vocabulary,
        Category.reading: request.reading,
        Category.writing: request.writing,
    }

    selected_exercises: list[Exercise] = []

    for category, count in category_counts.items():
        if count <= 0:
            continue

        available = (
            db.query(Exercise)
            .filter(Exercise.category == category)
            .all()
        )

        if len(available) < count:
            raise ValueError(
                f"Not enough '{category}' exercises in the database. "
                f"Requested {count}, available {len(available)}."
            )

        picked = random.sample(available, count)
        selected_exercises.extend(picked)

    # Shuffle final list so categories aren't all grouped together
    random.shuffle(selected_exercises)

    # Persist exam
    exam = Exam(
        title=request.title,
        description=request.description,
        level=request.level,
    )
    db.add(exam)
    db.flush()  # get exam.id before adding children

    for idx, exercise in enumerate(selected_exercises):
        ee = ExamExercise(exam_id=exam.id, exercise_id=exercise.id, order=idx)
        db.add(ee)

    db.commit()
    db.refresh(exam)
    return exam
