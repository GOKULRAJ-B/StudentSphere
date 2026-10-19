from student_operations import (
    add_student,
    view_all_students,
    search_student,
    update_student,
    delete_student
)

from predictions import predict_student_performance
from predictions import predict_next_exam_marks

from exam_operations import (
    add_exam_record,
    view_exam_history,
    subject_averages,
    identify_weak_subjects
)

def main():
    while True:
        print("\n===== StudentSphere =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Add Exam Record")
        print("7. View Exam History")
        print("8. Subject Averages")
        print("9. Identify Weak Subjects")
        print("10. Predict Student Performance")
        print("11. Estimate Next Exam Marks")
        print("12. Exit")
        

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            student = {
                "student_id": input("Student ID: ").strip(),
                "name": input("Name: ").strip(),
                "age": int(input("Age: ")),
                "department": input("Department: ").strip(),
                "course": input("Course: ").strip(),
                "enrollment_year": int(
                    input("Enrollment Year: ")
                ),
                "subjects": [
                    s.strip()
                    for s in input(
                        "Subjects (comma-separated): "
                    ).split(",")
                    if s.strip()
                ],
                "active": True
            }
            add_student(student)

        elif choice == "2":
            view_all_students()

        elif choice == "3":
            student_id = input("Student ID: ").strip()
            search_student(student_id)

        elif choice == "4":
            student_id = input("Student ID: ").strip()
            field = input(
                "Field to update (name, age, department, course): "
            ).strip()

            if field not in {
                "name", "age", "department", "course"
            }:
                print("Invalid field.")
                continue

            value = input("New value: ").strip()

            if field == "age":
                try:
                    value = int(value)
                except ValueError:
                    print("Age must be a number.")
                    continue

            update_student(student_id, {field: value})

        elif choice == "5":
            student_id = input(
                "Student ID to delete: "
            ).strip()
            delete_student(student_id)
            
        elif choice == "6":
            record = {
                "student_id": input("Student ID: ").strip(),
                "subject": input("Subject: ").strip(),
                "exam_name": input("Exam Name: ").strip(),
                "marks_obtained": float(
                    input("Marks Obtained: ")
                ),
                "maximum_marks": float(
                    input("Maximum Marks: ")
                ),
                "attendance_percentage": float(
                    input("Attendance Percentage: ")
                )
            }
            add_exam_record(record)

        elif choice in ("7", "8", "9"):
            student_id = input("Student ID: ").strip()

            if choice == "7":
                view_exam_history(student_id)
            elif choice == "8":
                subject_averages(student_id)
            else:
                identify_weak_subjects(student_id)

        elif choice == "10":
            student_id = input("Enter Student ID: ").strip()
            predict_student_performance(student_id)

        elif choice == "11":
            student_id = input("Enter Student ID: ").strip()
            subject = input("Enter Subject: ").strip()
            predict_next_exam_marks(student_id, subject)

        elif choice == "12":
            print("Thank you for using StudentSphere!")
            break


        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
