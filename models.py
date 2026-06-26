from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class Category(str, enum.Enum):
    grammar = "grammar"
    vocabulary = "vocabulary"
    reading = "reading"
    writing = "writing"


class ExerciseType(str, enum.Enum):
    # Grammar
    multiple_choice = "multiple_choice"
    fill_in_the_blank = "fill_in_the_blank"
    error_correction = "error_correction"
    sentence_transformation = "sentence_transformation"
    # Vocabulary (future)
    word_matching = "word_matching"
    definition_match = "definition_match"
    # Reading (future)
    comprehension_questions = "comprehension_questions"
    true_false = "true_false"
    # Writing (future)
    guided_writing = "guided_writing"
    essay = "essay"


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(SAEnum(Category), nullable=False)
    exercise_type = Column(SAEnum(ExerciseType), nullable=False)
    instructions = Column(Text, nullable=False)
    content = Column(JSON, nullable=False)   # flexible per exercise type
    difficulty = Column(String(50), default="medium")  # easy / medium / hard
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    exam_exercises = relationship("ExamExercise", back_populates="exercise")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    level = Column(String(50), nullable=True)   # A1, A2, B1, B2, C1, C2
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    exam_exercises = relationship(
        "ExamExercise", back_populates="exam",
        order_by="ExamExercise.order", cascade="all, delete-orphan"
    )


class ExamExercise(Base):
    __tablename__ = "exam_exercises"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    order = Column(Integer, nullable=False, default=0)

    exam = relationship("Exam", back_populates="exam_exercises")
    exercise = relationship("Exercise", back_populates="exam_exercises")
