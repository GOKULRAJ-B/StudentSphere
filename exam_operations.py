
from datetime import datetime

from database import (
    students_collection,
    exam_records_collection
)


def add_exam_record(record):
    student = students_collection.find_one(
        {"student_id": record["student_id"]}
    )

    if not student:
        print("Error: Student does not exist.")
        return

    if record["marks_obtained"] > record["maximum_marks"]:
        print("Error: Marks cannot exceed maximum marks.")
        return

    if record["marks_obtained"] < 0:
        print("Error: Marks cannot be negative.")
        return

    record["exam_date"] = datetime.now()

    exam_records_collection.insert_one(record)
    print("Exam record added successfully!")


def view_exam_history(student_id):
    records = exam_records_collection.find(
        {"student_id": student_id}
    ).sort("exam_date", 1)

    found = False

    for record in records:
        found = True
        print("-" * 40)
        print("Subject:", record["subject"])
        print("Exam:", record["exam_name"])
        print(
            "Marks:",
            f'{record["marks_obtained"]}/{record["maximum_marks"]}'
        )
        print(
            "Attendance:",
            f'{record["attendance_percentage"]}%'
        )
        print("Date:", record.get("exam_date", "Not available"))

    if not found:
        print("No exam records found for this student.")





def subject_averages(student_id):
    pipeline = [
        {"$match": {"student_id": student_id}},
        {
            "$group": {
                "_id": "$subject",
                "average_marks": {
                    "$avg": {
                        "$multiply": [
                            {
                                "$divide": [
                                    "$marks_obtained",
                                    "$maximum_marks"
                                ]
                            },
                            100
                        ]
                    }
                },
                "exam_count": {"$sum": 1}
            }
        },
        {"$sort": {"average_marks": -1}}
    ]

    results = exam_records_collection.aggregate(pipeline)

    found = False

    for result in results:
        found = True
        print(
            f'{result["_id"]}: '
            f'{result["average_marks"]:.2f}% '
            f'({result["exam_count"]} exams)'
        )

    if not found:
        print("No exam data available.")





def identify_weak_subjects(student_id, threshold=60):
    pipeline = [
        {"$match": {"student_id": student_id}},
        {
            "$group": {
                "_id": "$subject",
                "average_percentage": {
                    "$avg": {
                        "$multiply": [
                            {
                                "$divide": [
                                    "$marks_obtained",
                                    "$maximum_marks"
                                ]
                            },
                            100
                        ]
                    }
                }
            }
        },
        {"$match": {"average_percentage": {"$lt": threshold}}}
    ]

    results = list(exam_records_collection.aggregate(pipeline))

    if not results:
        print("No weak subjects found.")
        return

    print("Subjects needing improvement:")

    for result in results:
        print(
            f'{result["_id"]}: '
            f'{result["average_percentage"]:.2f}%'
        )
