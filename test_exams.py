
from exam_operations import (
    subject_averages,
    identify_weak_subjects
)

student_id = "STU1001"

print("Subject Averages:")
subject_averages(student_id)

print("\nWeak Subject Analysis:")
identify_weak_subjects(student_id)

print("\nTesting with a higher threshold of 90%:")
identify_weak_subjects(student_id, threshold=90)