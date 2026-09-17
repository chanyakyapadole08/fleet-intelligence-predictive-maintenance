import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
np.random.seed(42)

# Project folders
base_path = Path(__file__).resolve().parent.parent
raw_path = base_path / "data" / "raw"
raw_path.mkdir(parents=True, exist_ok=True)


# -----------------------------
# 1. Generate Routes
# -----------------------------

routes = []

cities = [
    ("Nagpur", "Pune"),
    ("Nagpur", "Mumbai"),
    ("Pune", "Nashik"),
    ("Mumbai", "Nashik"),
    ("Nagpur", "Indore"),
    ("Pune", "Aurangabad"),
    ("Mumbai", "Pune"),
    ("Nagpur", "Amravati")
]

for i, (origin, destination) in enumerate(cities, start=1):
    distance = random.randint(250, 750)

    routes.append([
        f"R{i:03}",
        origin,
        destination,
        distance,
        random.choice(["Highway", "Mixed", "Urban"])
    ])

routes_df = pd.DataFrame(routes, columns=[
    "route_id", "origin", "destination", "distance_km", "route_type"
])


# -----------------------------
# 2. Generate Trucks
# -----------------------------

trucks = []

for i in range(1, 101):
    age = random.randint(1, 12)

    trucks.append([
        f"T{i:03}",
        random.choice(["Light", "Medium", "Heavy"]),
        age,
        random.randint(20000, 250000),
        random.choice([5, 10, 15, 20]),
        datetime.now() - timedelta(days=age * 365),
        random.choice(["Diesel", "CNG"]),
        f"D{random.randint(1, 50):03}",
        random.choice(["Active", "Active", "Active", "Inactive"])
    ])

trucks_df = pd.DataFrame(trucks, columns=[
    "truck_id",
    "truck_type",
    "truck_age_years",
    "total_mileage_km",
    "capacity_tons",
    "purchase_date",
    "fuel_type",
    "driver_id",
    "status"
])


# -----------------------------
# 3. Generate Trips
# -----------------------------

trips = []

for i in range(1, 3001):
    truck_id = random.choice(trucks_df["truck_id"].tolist())
    route = routes_df.sample(1).iloc[0]

    distance = route["distance_km"] + random.randint(-30, 30)
    fuel = round(distance / random.uniform(2.5, 4.5), 2)

    scheduled_time = round(distance / random.uniform(45, 60), 2)
    travel_time = round(scheduled_time * random.uniform(0.85, 1.25), 2)

    if travel_time <= scheduled_time:
        status = "On Time"
    else:
        status = "Late"

    trips.append([
        f"TR{i:04}",
        truck_id,
        trucks_df.loc[
            trucks_df["truck_id"] == truck_id, "driver_id"
        ].iloc[0],
        route["route_id"],
        datetime.now() - timedelta(days=random.randint(1, 365)),
        distance,
        fuel,
        round(random.uniform(2, route["distance_km"] / 100), 2),
        travel_time,
        scheduled_time,
        status
    ])

trips_df = pd.DataFrame(trips, columns=[
    "trip_id",
    "truck_id",
    "driver_id",
    "route_id",
    "trip_date",
    "distance_km",
    "fuel_liters",
    "load_tons",
    "travel_time_hours",
    "scheduled_time_hours",
    "delivery_status"
])


# -----------------------------
# 4. Generate Maintenance
# -----------------------------

maintenance = []

maintenance_types = [
    "Engine",
    "Brake",
    "Tyre",
    "Oil Change",
    "Electrical"
]

for i in range(1, 501):
    truck_id = random.choice(trucks_df["truck_id"].tolist())

    maintenance.append([
        f"M{i:04}",
        truck_id,
        datetime.now() - timedelta(days=random.randint(1, 365)),
        random.choice(maintenance_types),
        random.randint(1000, 30000),
        random.randint(2, 48)
    ])

maintenance_df = pd.DataFrame(maintenance, columns=[
    "maintenance_id",
    "truck_id",
    "maintenance_date",
    "maintenance_type",
    "repair_cost",
    "downtime_hours"
])


# -----------------------------
# Save CSV files
# -----------------------------

routes_df.to_csv(raw_path / "routes.csv", index=False)
trucks_df.to_csv(raw_path / "trucks.csv", index=False)
trips_df.to_csv(raw_path / "trips.csv", index=False)
maintenance_df.to_csv(raw_path / "maintenance.csv", index=False)

print("Dataset generated successfully!")
print("Routes:", len(routes_df))
print("Trucks:", len(trucks_df))
print("Trips:", len(trips_df))
print("Maintenance records:", len(maintenance_df))