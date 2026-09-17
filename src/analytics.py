import pandas as pd
from pathlib import Path


# Project path
base_path = Path(__file__).resolve().parent.parent
data_path = base_path / "data" / "processed"


# Load data
trucks = pd.read_csv(data_path / "trucks.csv")
trips = pd.read_csv(data_path / "trips.csv")
maintenance = pd.read_csv(data_path / "maintenance.csv")


# -----------------------------
# Fleet Overview
# -----------------------------

print("\n--- Fleet Overview ---")
print("Total trucks:", len(trucks))
print("Total trips:", len(trips))
print("Total distance:", round(trips["distance_km"].sum(), 2), "km")


# -----------------------------
# Fuel Analysis
# -----------------------------

trips["fuel_efficiency"] = (
    trips["distance_km"] / trips["fuel_liters"]
)

print("\n--- Fuel Analysis ---")
print(
    "Average fuel efficiency:",
    round(trips["fuel_efficiency"].mean(), 2),
    "km/l"
)


# -----------------------------
# Delivery Analysis
# -----------------------------

on_time = (trips["delivery_status"] == "On Time").sum()
total_trips = len(trips)

on_time_percentage = on_time / total_trips * 100

print("\n--- Delivery Analysis ---")
print("On-time delivery:", round(on_time_percentage, 2), "%")


# -----------------------------
# Maintenance Analysis
# -----------------------------

print("\n--- Maintenance Analysis ---")
print("Maintenance records:", len(maintenance))
print(
    "Total repair cost: ₹",
    round(maintenance["repair_cost"].sum(), 2)
)
print(
    "Total downtime:",
    round(maintenance["downtime_hours"].sum(), 2),
    "hours"
)


# -----------------------------
# Truck Performance
# -----------------------------

truck_performance = trips.groupby("truck_id").agg(
    total_trips=("trip_id", "count"),
    total_distance=("distance_km", "sum"),
    avg_fuel_efficiency=("fuel_efficiency", "mean")
).reset_index()

print("\n--- Top 5 Trucks by Distance ---")
print(
    truck_performance
    .sort_values("total_distance", ascending=False)
    .head(5)
)
