"""
Run once to populate the DB with sample grammar exercises.
Usage: python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

EXERCISES = [
    # ── Multiple Choice ───────────────────────────────────────────────────────
    {
        "title": "Present Simple vs. Continuous (MC)",
        "category": "grammar",
        "exercise_type": "multiple_choice",
        "difficulty": "easy",
        "instructions": "Choose the correct option to complete the sentence.",
        "content": {
            "question": "She _____ to the gym every Monday.",
            "options": ["go", "goes", "is going", "has gone"],
            "answer": "B"
        }
    },
    {
        "title": "Past Simple – Regular Verbs (MC)",
        "category": "grammar",
        "exercise_type": "multiple_choice",
        "difficulty": "easy",
        "instructions": "Choose the correct past simple form.",
        "content": {
            "question": "They _____ the project last week.",
            "options": ["finish", "finishing", "finished", "have finished"],
            "answer": "C"
        }
    },
    {
        "title": "Conditional Type 1 (MC)",
        "category": "grammar",
        "exercise_type": "multiple_choice",
        "difficulty": "medium",
        "instructions": "Choose the best option to complete the first conditional sentence.",
        "content": {
            "question": "If it _____ tomorrow, we will cancel the picnic.",
            "options": ["rains", "will rain", "rained", "would rain"],
            "answer": "A"
        }
    },
    {
        "title": "Present Perfect vs. Past Simple (MC)",
        "category": "grammar",
        "exercise_type": "multiple_choice",
        "difficulty": "medium",
        "instructions": "Choose the most appropriate tense.",
        "content": {
            "question": "I _____ this movie three times already.",
            "options": ["saw", "have seen", "see", "had seen"],
            "answer": "B"
        }
    },
    {
        "title": "Passive Voice – Present (MC)",
        "category": "grammar",
        "exercise_type": "multiple_choice",
        "difficulty": "medium",
        "instructions": "Choose the correct passive form.",
        "content": {
            "question": "The report _____ every month by the manager.",
            "options": ["writes", "is written", "was written", "has written"],
            "answer": "B"
        }
    },
    # ── Fill in the Blank ─────────────────────────────────────────────────────
    {
        "title": "Articles (a / an / the) – Fill in",
        "category": "grammar",
        "exercise_type": "fill_in_the_blank",
        "difficulty": "easy",
        "instructions": "Fill in the blank with the correct article: a, an or the.",
        "content": {
            "sentence": "I saw _______ elephant at _______ zoo yesterday.",
            "answers": ["an", "the"]
        }
    },
    {
        "title": "Prepositions of Time – Fill in",
        "category": "grammar",
        "exercise_type": "fill_in_the_blank",
        "difficulty": "easy",
        "instructions": "Complete the sentence with the correct preposition: in, on, or at.",
        "content": {
            "sentence": "The meeting is _______ Monday _______ 3 o'clock _______ the afternoon.",
            "answers": ["on", "at", "in"]
        }
    },
    {
        "title": "Modal Verbs – Fill in",
        "category": "grammar",
        "exercise_type": "fill_in_the_blank",
        "difficulty": "medium",
        "instructions": "Fill in the blank with the correct modal verb (can, must, should, might).",
        "content": {
            "sentence": "You _______ see a doctor if the pain continues.",
            "answers": ["should"]
        }
    },
    {
        "title": "Future with 'will' or 'going to' – Fill in",
        "category": "grammar",
        "exercise_type": "fill_in_the_blank",
        "difficulty": "medium",
        "instructions": "Fill in with the correct future form of the verb in brackets.",
        "content": {
            "sentence": "Look at those dark clouds! It _______ (rain).",
            "answers": ["is going to rain"]
        }
    },
    {
        "title": "Comparative & Superlative – Fill in",
        "category": "grammar",
        "exercise_type": "fill_in_the_blank",
        "difficulty": "easy",
        "instructions": "Fill in with the comparative or superlative form of the adjective in brackets.",
        "content": {
            "sentence": "This is _______ (interesting) book I have ever read, and it is _______ (long) than the previous one.",
            "answers": ["the most interesting", "longer"]
        }
    },
    # ── Error Correction ──────────────────────────────────────────────────────
    {
        "title": "Identify the Grammar Error – Present Perfect",
        "category": "grammar",
        "exercise_type": "error_correction",
        "difficulty": "medium",
        "instructions": "Each sentence contains ONE grammar error. Find it and write the correct sentence.",
        "content": {
            "sentence": "She has went to Paris twice.",
            "error": "went",
            "correction": "gone"
        }
    },
    {
        "title": "Identify the Grammar Error – Subject-Verb Agreement",
        "category": "grammar",
        "exercise_type": "error_correction",
        "difficulty": "easy",
        "instructions": "Find and correct the error in subject-verb agreement.",
        "content": {
            "sentence": "The news are very shocking today.",
            "error": "are",
            "correction": "is"
        }
    },
    {
        "title": "Identify the Grammar Error – Reported Speech",
        "category": "grammar",
        "exercise_type": "error_correction",
        "difficulty": "hard",
        "instructions": "Find and correct the error in reported speech.",
        "content": {
            "sentence": "He said that he will call me the next day.",
            "error": "will",
            "correction": "would"
        }
    },
    # ── Sentence Transformation ───────────────────────────────────────────────
    {
        "title": "Active to Passive – Past Simple",
        "category": "grammar",
        "exercise_type": "sentence_transformation",
        "difficulty": "medium",
        "instructions": "Rewrite the sentence beginning with the word given, keeping the same meaning.",
        "content": {
            "original": "The chef cooked the meal.",
            "start_with": "The meal",
            "keyword": "was",
            "answer": "The meal was cooked by the chef."
        }
    },
    {
        "title": "Direct to Reported Speech",
        "category": "grammar",
        "exercise_type": "sentence_transformation",
        "difficulty": "hard",
        "instructions": "Rewrite the sentence in reported speech.",
        "content": {
            "original": '"I am tired," she said.',
            "start_with": "She said",
            "keyword": "that",
            "answer": "She said that she was tired."
        }
    },
    {
        "title": "Conditional Type 2 – Transformation",
        "category": "grammar",
        "exercise_type": "sentence_transformation",
        "difficulty": "hard",
        "instructions": "Complete the second sentence so it has a similar meaning using the word given.",
        "content": {
            "original": "I don't have enough money, so I can't buy that laptop.",
            "keyword": "If",
            "answer": "If I had enough money, I could buy that laptop."
        }
    },
    {
    "title": "Synonyms – Describing People (MC)",
    "category": "vocabulary",
    "exercise_type": "multiple_choice",
    "difficulty": "easy",
    "instructions": "Choose the word closest in meaning to the underlined word.",
    "content": {
        "question": "She is a very <u>generous</u> person.",
        "options": ["stingy", "giving", "shy", "strict"],
        "answer": "B"
    }
},
{
    "title": "Word in Context – Business Vocabulary (MC)",
    "category": "vocabulary",
    "exercise_type": "multiple_choice",
    "difficulty": "medium",
    "instructions": "Choose the word that best completes the sentence.",
    "content": {
        "question": "The two companies decided to _____ in order to reduce production costs.",
        "options": ["merge", "resign", "withdraw", "complain"],
        "answer": "A"
    }
},
{
    "title": "Short Passage – City Life (MC)",
    "category": "reading",
    "exercise_type": "multiple_choice",
    "difficulty": "medium",
    "instructions": "Read the passage and choose the correct answer.",
    "content": {
        "passage": "More people are choosing to live in cities than ever before. While cities offer better access to jobs, transport and entertainment, they also bring higher rents and more pollution. For this reason, some young professionals are starting to look for a balance between city convenience and a quieter lifestyle.",
        "question": "According to the passage, why are some young professionals reconsidering city life?",
        "options": [
            "Cities have fewer job opportunities",
            "They want better transport options",
            "They are looking for a balance with a quieter lifestyle",
            "Entertainment options are decreasing"
        ],
        "answer": "C"
    }
},
{
    "title": "Opinion Essay – Technology and Daily Life",
    "category": "writing",
    "exercise_type": "essay",
    "difficulty": "hard",
    "instructions": "Write a short essay giving your opinion on the topic below.",
    "content": {
        "prompt": "Some people believe technology has made our lives easier, while others think it has made daily life more stressful. Discuss both views and give your own opinion.",
        "min_words": 150,
        "max_words": 200,
        "sample_answer": "Technology has undoubtedly transformed daily life, bringing both convenience and new sources of stress. On one hand, tasks such as banking, shopping and communicating with others have become faster and more accessible thanks to smartphones and apps..."
    }
}
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(models.Exercise).count()
        if existing > 0:
            print(f"Database already has {existing} exercises. Skipping seed.")
            return

        for data in EXERCISES:
            exercise = models.Exercise(**data)
            db.add(exercise)
        db.commit()
        print(f"✅ Seeded {len(EXERCISES)} grammar exercises successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
