
from database import students_collection, exam_records_collection

students = [
    {
        "student_id": "STU1003",
        "name": "Kavin Raj",
        "age": 20,
        "department": "CSE",
        "course": "Data Science",
        "enrollment_year": 2025,
        "subjects": ["Python", "MongoDB", "Statistics"],
        "active": True
    },
    {
        "student_id": "STU1004",
        "name": "Meena Devi",
        "age": 21,
        "department": "CSE",
        "course": "AI",
        "enrollment_year": 2024,
        "subjects": ["Python", "MongoDB", "Statistics"],
        "active": True
    },
    {
        "student_id": "STU1005",
        "name": "Rahul Kumar",
        "age": 20,
        "department": "IT",
        "course": "Data Science",
        "enrollment_year": 2025,
        "subjects": ["Python", "MongoDB", "Statistics"],
        "active": True
    }
]

exam_scores = {
    "STU1001": {
        "Python": [65, 72, 82],
        "MongoDB": [70, 76, 80],
        "Statistics": [55, 60, 64]
    },
    "STU1003": {
        "Python": [75, 80, 85],
        "MongoDB": [72, 78, 84],
        "Statistics": [68, 72, 76]
    },
    "STU1004": {
        "Python": [40, 48, 52],
        "MongoDB": [45, 50, 55],
        "Statistics": [35, 42, 48]
    },
    "STU1005": {
        "Python": [90, 92, 95],
        "MongoDB": [85, 90, 94],
        "Statistics": [80, 86, 90]
    }
}

for student in students:
    students_collection.update_one(
        {"student_id": student["student_id"]},
        {"$setOnInsert": student},
        upsert=True
    )

exam_names = ["Exam 1", "Exam 2", "Exam 3"]

for student_id, subjects in exam_scores.items():
    for subject, scores in subjects.items():
        for index, marks in enumerate(scores):
            exam_records_collection.update_one(
                {
                    "student_id": student_id,
                    "subject": subject,
                    "exam_name": exam_names[index]
                },
                {
                    "$setOnInsert": {
                        "student_id": student_id,
                        "subject": subject,
                        "exam_name": exam_names[index],
                        "marks_obtained": marks,
                        "maximum_marks": 100,
                        "attendance_percentage": 75 + index * 5
                    }
                },
                upsert=True
            )

print("Sample data inserted or already present.")
