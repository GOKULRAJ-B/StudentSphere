import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "studentsphere"

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

try:
    client.admin.command("ping")
    db = client[DATABASE_NAME]

    students_df = pd.read_csv(
        "data/synthetic_students.csv"
    )
    exams_df = pd.read_csv(
        "data/synthetic_exam_records.csv"
    )

    students = db["synthetic_students"]
    exams = db["synthetic_exam_records"]

    for student in students_df.to_dict("records"):
        students.update_one(
            {"student_id": student["student_id"]},
            {"$set": student},
            upsert=True
        )

    for record in exams_df.to_dict("records"):
        exams.update_one(
            {
                "student_id": record["student_id"],
                "subject": record["subject"],
                "exam_name": record["exam_name"],
            },
            {"$set": record},
            upsert=True
        )

    students.create_index(
        "student_id",
        unique=True
    )
    exams.create_index(
        [
            ("student_id", 1),
            ("subject", 1),
            ("exam_name", 1),
        ],
        unique=True
    )

    print("Synthetic data imported successfully!")
    print("Students:", students.count_documents({}))
    print("Exam records:", exams.count_documents({}))

finally:
    client.close()
