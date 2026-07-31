import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from preprocess import DataPreprocessor


# ==========================================================
# PATHS
# ==========================================================

DATASET_PATH = "dataset/Churn_Modelling.csv"

MODEL_FOLDER = "models"

MODEL_PATH = os.path.join(
    MODEL_FOLDER,
    "churn_model.pkl"
)

os.makedirs(MODEL_FOLDER, exist_ok=True)


# ==========================================================
# LOAD DATASET
# ==========================================================

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

processor = DataPreprocessor()

X, y = processor.prepare_dataset(DATASET_PATH)

print()

print("Dataset Loaded Successfully")

print("Rows :", len(X))

print("Columns :", len(X.columns))

print()

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

print("=" * 60)
print("Splitting Dataset...")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

print()

print("Training Records :", len(X_train))

print("Testing Records :", len(X_test))

print()

# ==========================================================
# RANDOM FOREST
# ==========================================================

print("=" * 60)
print("Training Random Forest...")
print("=" * 60)

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=12,

    random_state=42,

    n_jobs=-1

)

model.fit(

    X_train,

    y_train

)

print()

print("Training Completed.")

print()

# ==========================================================
# PREDICTION
# ==========================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    predictions

)

print("=" * 60)

print("MODEL ACCURACY")

print("=" * 60)

print(f"{accuracy * 100:.2f}%")

print()

print("=" * 60)

print("CLASSIFICATION REPORT")

print("=" * 60)

print(

    classification_report(

        y_test,

        predictions

    )

)

print("=" * 60)

print("CONFUSION MATRIX")

print("=" * 60)

print(

    confusion_matrix(

        y_test,

        predictions

    )

)

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print()

print("=" * 60)

print("TOP FEATURES")

print("=" * 60)

print(

    importance

)

# ==========================================================
# SAVE MODEL
# ==========================================================

joblib.dump(

    {

        "model": model,

        "encoders": processor.encoders,

        "features": processor.feature_columns

    },

    MODEL_PATH

)

print()

print("=" * 60)

print("MODEL SAVED SUCCESSFULLY")

print("=" * 60)

print(MODEL_PATH)

print("=" * 60)