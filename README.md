# 📝 English Exam Builder

A FastAPI admin app for creating, managing, and exporting English language exams.

---

## 🚀 Setup

### 1. Prerequisites
- Python 3.11+
- PostgreSQL running locally (or via Docker)

### 2. Create the database
```sql
CREATE DATABASE exam_db;
```

### 3. Install dependencies
```bash
cd exam_app
pip install -r requirements.txt
```

### 4. Configure database URL (optional)
By default the app connects to:
```
postgresql://postgres:password@localhost:5432/exam_db
```
Override via environment variable:
```bash
export DATABASE_URL="postgresql://user:pass@host:5432/exam_db"
```

### 5. Seed grammar exercises
```bash
python seed.py
```
This inserts 16 ready-made grammar exercises (multiple choice, fill-in-the-blank, error correction, sentence transformation).

### 6. Run the server
```bash
uvicorn main:app --reload
```

Open → **http://localhost:8000**

---

## 🗂️ Pages

| URL | Description |
|-----|-------------|
| `/` | Dashboard — all exams + stats |
| `/exams/new` | Create exam (manual or auto-generate) |
| `/exams/{id}` | Exam detail — view, add/remove exercises, export |
| `/exercises` | Exercise bank — browse all exercises |

## 🔌 API (JSON)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exams/` | List all exams |
| POST | `/api/exams/` | Create blank exam |
| GET | `/api/exams/{id}` | Get exam with exercises |
| DELETE | `/api/exams/{id}` | Delete exam |
| POST | `/api/exams/{id}/exercises` | Add exercise to exam |
| DELETE | `/api/exams/{id}/exercises/{ex_id}` | Remove exercise from exam |
| POST | `/api/exams/generate` | Auto-generate exam |
| GET | `/api/exams/{id}/export/pdf` | Download PDF |
| GET | `/api/exams/{id}/export/docx` | Download Word |
| GET | `/api/exercises/` | List exercises (filter: ?category=grammar) |
| POST | `/api/exercises/` | Create exercise |
| PUT | `/api/exercises/{id}` | Update exercise |
| DELETE | `/api/exercises/{id}` | Delete exercise |

Interactive docs → **http://localhost:8000/docs**

---

## ⚡ Auto-Generate Example (API)

```json
POST /api/exams/generate
{
  "title": "Mixed B1 Test",
  "level": "B1",
  "grammar": 4,
  "vocabulary": 1,
  "reading": 1,
  "writing": 1
}
```

Picks exercises randomly without repeating any within the exam.

---

## 📁 Project Structure

```
exam_app/
├── main.py               # FastAPI app + UI routes
├── database.py           # PostgreSQL connection
├── models.py             # SQLAlchemy ORM models
├── schemas.py            # Pydantic schemas
├── seed.py               # Sample grammar exercises
├── requirements.txt
├── routers/
│   ├── exams.py          # Exam CRUD + export + auto-gen
│   └── exercises.py      # Exercise CRUD
├── services/
│   ├── exam_generator.py # Random selection logic
│   └── exporters.py      # PDF & DOCX export
├── templates/            # Jinja2 HTML templates
└── static/               # CSS + JS
```

---

## 🗺️ Roadmap

- [ ] Create exercises from the UI
- [ ] Vocabulary / Reading / Writing exercise types
- [ ] Student-facing exam view (read-only, printable)
- [ ] Answer key toggle on export
- [ ] Search & filter exercises
