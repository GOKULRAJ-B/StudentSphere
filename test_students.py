
from student_operations import (
    add_student,
    search_student,
    delete_student
)

student = {
    "student_id": "STU1002",
    "name": "Priya Sharma",
    "age": 21,
    "department": "CSE",
    "course": "Data Science",
    "enrollment_year": 2025,
    "subjects": ["Python", "MongoDB"],
    "active": True
}

print("Adding test student...")
add_student(student)

print("\nBefore Deletion:")
search_student("STU1002")

print("\nDeleting test student...")
delete_student("STU1002")

print("\nAfter Deletion:")
search_student("STU1002")