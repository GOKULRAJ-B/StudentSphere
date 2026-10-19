
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

SEED = 42
random.seed(SEED)

NUM_STUDENTS = 1000
SUBJECTS = ["Python", "MongoDB", "Statistics"]
NUM_EXAMS = 5

OUTPUT_DIR = Path(__file__).parent
STUDENTS_FILE = OUTPUT_DIR / "synthetic_students.csv"
EXAMS_FILE = OUTPUT_DIR / "synthetic_exam_records.csv"


def generate_dataset():
    students = []
    exam_records = []

    for i in range(1, NUM_STUDENTS + 1):
        student_id = f"STU{i:04d}"

        ability = random.gauss(70, 12)
        ability = max(25, min(95, ability))

        students.append({
            "student_id": student_id,
            "name": f"Student {i:04d}",
            "age": random.randint(17, 23),
            "department": "CSE",
            "year": random.randint(1, 4),
        })

        subject_ability = {
            subject: random.gauss(ability, 7)
            for subject in SUBJECTS
        }

        for subject in SUBJECTS:
            previous_percentage = None

            for exam_number in range(1, NUM_EXAMS + 1):
               
                progress = (exam_number - 1) * random.uniform(0.5, 2.0)
                percentage = (
                    subject_ability[subject]
                    + progress
                    + random.gauss(0, 6)
                )
                percentage = round(
                    max(0, min(100, percentage)), 2
                )

                max_marks = 100
                marks_obtained = round(
                    percentage * max_marks / 100, 2
                )

                exam_records.append({
                    "student_id": student_id,
                    "subject": subject,
                    "exam_name": f"Exam {exam_number}",
                    "marks_obtained": marks_obtained,
                    "max_marks": max_marks,
                    "exam_date": (
                        datetime(2025, 1, 1)
                        + timedelta(days=exam_number * 30)
                    ).isoformat(),
                })

                previous_percentage = percentage

    pd.DataFrame(students).to_csv(
        STUDENTS_FILE, index=False
    )
    pd.DataFrame(exam_records).to_csv(
        EXAMS_FILE, index=False
    )

    print("Synthetic dataset generated successfully!")
    print(f"Students: {len(students)}")
    print(f"Exam records: {len(exam_records)}")
    print(f"Students CSV: {STUDENTS_FILE}")
    print(f"Exam records CSV: {EXAMS_FILE}")


if __name__ == "__main__":
    generate_dataset()
