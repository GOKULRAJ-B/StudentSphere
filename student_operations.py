from database import students_collection


def add_student(student):
    if students_collection.find_one(
        {"student_id": student["student_id"]}
    ):
        print("Error: Student ID already exists.")
        return

    students_collection.insert_one(student)
    print("Student added successfully!")


def view_all_students():
    students = students_collection.find().sort("student_id", 1)

    found = False

    for student in students:
        found = True
        print("-" * 40)
        print("Student ID:", student["student_id"])
        print("Name:", student["name"])
        print("Department:", student["department"])
        print("Course:", student["course"])

    if not found:
        print("No students found.")

def search_student(student_id):
    student = students_collection.find_one(
        {"student_id": student_id}
    )

    if student:
        print("\nStudent Found")
        print("-" * 30)

        for key, value in student.items():
            print(f"{key}: {value}")
    else:
        print("Student not found.")


def update_student(student_id, updates):
    result = students_collection.update_one(
        {"student_id": student_id},
        {"$set": updates}
    )

    if result.matched_count == 0:
        print("Student not found.")
    elif result.modified_count == 0:
        print("No changes made.")
    else:
        print("Student updated successfully!")

def delete_student(student_id):
    result = students_collection.delete_one(
        {"student_id": student_id}
    )

    if result.deleted_count == 1:
        print("Student deleted successfully!")
    else:
        print("Student not found.")
