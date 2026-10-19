from pathlib import Path
import re
import joblib
import pandas as pd
from database import exam_records_collection

MODEL_DIR = Path(__file__).resolve().parent / "models"
CLASSIFIER_PATH = MODEL_DIR / "performance_model.joblib"
REGRESSOR_PATH = MODEL_DIR / "marks_regression.joblib"


def _load_model(path, display_name):
    if not path.exists():
        print(f"{display_name} model not found. Run train_models.py first.")
        return None
    try:
        return joblib.load(path)
    except (OSError, EOFError, ValueError) as exc:
        print(f"Could not load {display_name} model: {exc}")
        return None


def predict_performance(average_percentage, exam_count=None, subject_count=None):

    saved = _load_model(CLASSIFIER_PATH, "Performance classification")
    if saved is None:
        return
    features = saved["features"]
    values = {"average_percentage": float(average_percentage)}
    try:
        row = pd.DataFrame([[values[name] for name in features]], columns=features)
    except KeyError as exc:
        print(f"Model expects an unsupported feature: {exc}")
        return
    result = saved["model"].predict(row)[0]
    print("\nPredicted Performance:", result)


def predict_student_performance(student_id):
    records = list(exam_records_collection.find(
        {"student_id": student_id},
        {"_id": 0, "marks_obtained": 1, "maximum_marks": 1, "subject": 1},
    ))
    if not records:
        print("No exam records found for this student.")
        return
    percentages, subjects = [], set()
    for record in records:
        try:
            marks, maximum = float(record["marks_obtained"]), float(record["maximum_marks"])
        except (KeyError, TypeError, ValueError):
            continue
        if maximum <= 0:
            continue
        percentages.append(marks / maximum * 100)
        if record.get("subject"):
            subjects.add(record["subject"])
    if not percentages:
        print("No valid exam records available.")
        return
    average = sum(percentages) / len(percentages)
    print(f"\nStudent ID: {student_id}")
    print(f"Average Percentage: {average:.2f}%")
    print(f"Exam Records: {len(percentages)}")
    print(f"Subjects: {len(subjects)}")
    predict_performance(average, len(percentages), len(subjects))


def predict_next_exam_marks(student_id, subject):
    records = list(exam_records_collection.find(
        {"student_id": student_id, "subject": subject, "exam_name": {"$regex": r"^Exam\s+\d+$"}},
        {"_id": 0, "exam_name": 1, "marks_obtained": 1, "maximum_marks": 1},
    ))
    history = []
    for record in records:
        match = re.fullmatch(r"Exam\s+(\d+)", str(record.get("exam_name", "")))
        if not match:
            continue
        try:
            marks, maximum = float(record["marks_obtained"]), float(record["maximum_marks"])
        except (KeyError, TypeError, ValueError):
            continue
        if maximum > 0:
            history.append((int(match.group(1)), marks / maximum * 100))
    history.sort(key=lambda pair: pair[0])
    if len(history) < 2:
        print("At least two sequential exam records are required.")
        return
    numbers = [item[0] for item in history]
    if len(numbers) != len(set(numbers)):
        print("Duplicate exam numbers found. Please check the records.")
        return
    saved = _load_model(REGRESSOR_PATH, "Next-exam regression")
    if saved is None:
        return
    previous, current = history[-2][1], history[-1][1]
    values = {"previous_percentage": previous, "current_percentage": current}
    features = saved["features"]
    try:
        row = pd.DataFrame([[values[name] for name in features]], columns=features)
    except KeyError as exc:
        print(f"Model expects an unsupported feature: {exc}")
        return
    prediction = float(saved["model"].predict(row)[0])
    prediction = max(0.0, min(100.0, prediction))
    print(f"\nStudent ID: {student_id}")
    print(f"Subject: {subject}")
    print(f"Next exam: Exam {history[-1][0] + 1}")
    print(f"Previous exam percentage: {previous:.2f}%")
    print(f"Most recent exam percentage: {current:.2f}%")
    print(f"Estimated percentage: {prediction:.2f}%")


if __name__ == "__main__":
    student_id = input("Enter Student ID: ").strip()
    predict_student_performance(student_id)
    subject = input("\nEnter subject for next-exam estimation: ").strip()
