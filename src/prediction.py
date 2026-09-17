import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score
from sklearn.metrics import recall_score, f1_score
from sklearn.metrics import confusion_matrix


# Project path
base_path = Path(__file__).resolve().parent.parent
data_path = base_path / "data" / "processed"


# Load data
trucks = pd.read_csv(data_path / "trucks.csv")
trips = pd.read_csv(data_path / "trips.csv")


# Create trip features
trip_features = trips.groupby("truck_id").agg(
    trip_count=("trip_id", "count"),
    total_distance=("distance_km", "sum")
).reset_index()


# Combine truck and trip data
data = trucks.merge(
    trip_features,
    on="truck_id",
    how="left"
)

data = data.fillna(0)


# Create maintenance risk
data["maintenance_risk"] = (
    (data["truck_age_years"] >= 8) |
    (data["total_mileage_km"] >= 180000)
).astype(int)


# Features used by model
features = [
    "truck_age_years",
    "total_mileage_km",
    "capacity_tons",
    "trip_count",
    "total_distance"
]

X = data[features]
y = data["maintenance_risk"]


# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Train Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


# Make predictions
predictions = model.predict(X_test)


# Calculate evaluation metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)


print("\n--- Predictive Maintenance Model ---")
print("Accuracy:", round(accuracy, 2))
print("Precision:", round(precision, 2))
print("Recall:", round(recall, 2))
print("F1 Score:", round(f1, 2))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))