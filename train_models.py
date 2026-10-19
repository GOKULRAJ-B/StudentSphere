from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "student-mat.csv"
MODEL_DIR = BASE_DIR / "models"


def load_real_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\nDownload the UCI Student Performance dataset, extract it, "
            "and copy student-mat.csv into the project's data folder."
        )
    df = pd.read_csv(DATA_PATH, sep=";")
    required = {"G1", "G2", "G3"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    df = df[["G1", "G2", "G3"]].copy()
    for col in ["G1", "G2", "G3"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["G1", "G2", "G3"])

    df["G1_percentage"] = df["G1"] * 5.0
    df["G2_percentage"] = df["G2"] * 5.0
    df["G3_percentage"] = df["G3"] * 5.0
   
    df["average_percentage"] = (df["G1_percentage"] + df["G2_percentage"]) / 2.0

    def category(pct):
        if pct < 50:
            return "At Risk"
        if pct < 75:
            return "Needs Improvement"
        return "Good"

    df["performance"] = df["G3_percentage"].apply(category)
    return df.reset_index(drop=True)


def train_classifier(df):

    features = ["average_percentage"]
    X, y = df[features], df["performance"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    evaluation_model = DecisionTreeClassifier(max_depth=3, random_state=42, class_weight="balanced")
    evaluation_model.fit(X_train, y_train)
    predictions = evaluation_model.predict(X_test)
 
    print(f"Usable records: {len(df)}")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Test accuracy: {accuracy_score(y_test, predictions):.4f}")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Target: category derived from G3; input: average of G1 and G2.")

    final_model = DecisionTreeClassifier(max_depth=3, random_state=42, class_weight="balanced")
    final_model.fit(X, y)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "model": final_model,
        "features": features,
        "source": "UCI Student Performance Dataset - student-mat.csv",
        "target": "Performance category derived from G3 percentage",
    }, MODEL_DIR / "performance_model.joblib")
    print(f"Saved: {MODEL_DIR / 'performance_model.joblib'}")


def train_regressor(df):
    features = ["previous_percentage", "current_percentage"]
    X = pd.DataFrame({
        "previous_percentage": df["G1_percentage"],
        "current_percentage": df["G2_percentage"],
    })
    y = df["G3_percentage"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    evaluation_model = LinearRegression().fit(X_train, y_train)
    predictions = evaluation_model.predict(X_test)
    print("\n--- Real-Data Regression Evaluation ---")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"MAE: {mean_absolute_error(y_test, predictions):.4f} percentage points")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, predictions)):.4f} percentage points")
    print(f"R² score: {r2_score(y_test, predictions):.4f}")
    print("Inputs: G1 and G2 percentages; target: G3 percentage.")

    final_model = LinearRegression().fit(X, y)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "model": final_model,
        "features": features,
        "source": "UCI Student Performance Dataset - student-mat.csv",
        "target": "G3 percentage predicted from G1 and G2 percentages",
    }, MODEL_DIR / "marks_regression.joblib")
    print(f"Saved: {MODEL_DIR / 'marks_regression.joblib'}")


def main():
    df = load_real_data()
    print("Loaded real student records from the UCI dataset.")
    print(f"Usable rows: {len(df)}")
    print("\nPerformance category counts:")
    print(df["performance"].value_counts().to_string())
    train_classifier(df)
    train_regressor(df)
    print("\nTraining complete. Back up the old model files before replacing them.")
  


if __name__ == "__main__":
    main()
