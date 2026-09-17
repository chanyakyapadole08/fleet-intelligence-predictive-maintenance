import streamlit as st
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression

# Project path
base_path = Path(__file__).resolve().parent.parent
data_path = base_path / "data" / "processed"


# Load data
trucks = pd.read_csv(data_path / "trucks.csv")
trips = pd.read_csv(data_path / "trips.csv")
maintenance = pd.read_csv(data_path / "maintenance.csv")


# Page settings
st.set_page_config(
    page_title="Fleet Intelligence",
    page_icon="🚛",
    layout="wide"
)


st.title("🚛 Fleet Intelligence & Predictive Maintenance")
st.write("Fleet analytics and maintenance monitoring dashboard")


# -----------------------------
# Sidebar Filter
# -----------------------------

st.sidebar.header("Filters")

truck_types = ["All"] + sorted(trucks["truck_type"].unique())

selected_type = st.sidebar.selectbox(
    "Truck Type",
    truck_types
)

if selected_type != "All":
    filtered_trucks = trucks[
        trucks["truck_type"] == selected_type
    ]
else:
    filtered_trucks = trucks


# -----------------------------
# Fleet KPIs
# -----------------------------

st.header("Fleet Overview")

total_trucks = len(filtered_trucks)

filtered_ids = filtered_trucks["truck_id"]

filtered_trips = trips[
    trips["truck_id"].isin(filtered_ids)
]

filtered_maintenance = maintenance[
    maintenance["truck_id"].isin(filtered_ids)
]

total_trips = len(filtered_trips)
total_distance = filtered_trips["distance_km"].sum()
total_maintenance = len(filtered_maintenance)


col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Trucks", total_trucks)
col2.metric("Total Trips", total_trips)
col3.metric("Distance (km)", f"{total_distance:,.0f}")
col4.metric("Maintenance Records", total_maintenance)


# -----------------------------
# Fuel Analysis
# -----------------------------

st.header("⛽ Fuel Analytics")

filtered_trips["fuel_efficiency"] = (
    filtered_trips["distance_km"] /
    filtered_trips["fuel_liters"]
)

avg_efficiency = filtered_trips["fuel_efficiency"].mean()

st.metric(
    "Average Fuel Efficiency",
    f"{avg_efficiency:.2f} km/l"
)

fuel_by_truck = (
    filtered_trips
    .groupby("truck_id")["fuel_efficiency"]
    .mean()
    .sort_values(ascending=False)
)

st.subheader("Fuel Efficiency by Truck")

st.bar_chart(fuel_by_truck)


# -----------------------------
# Delivery Analysis
# -----------------------------

st.header("📦 Delivery Performance")

delivery_count = (
    filtered_trips["delivery_status"]
    .value_counts()
)

st.bar_chart(delivery_count)


on_time = (
    filtered_trips["delivery_status"] == "On Time"
).sum()

if total_trips > 0:
    on_time_percentage = on_time / total_trips * 100
else:
    on_time_percentage = 0

st.metric(
    "On-Time Delivery",
    f"{on_time_percentage:.2f}%"
)


# -----------------------------
# Maintenance Analysis
# -----------------------------

st.header("🔧 Maintenance Analytics")

col1, col2 = st.columns(2)

total_cost = filtered_maintenance["repair_cost"].sum()
total_downtime = filtered_maintenance["downtime_hours"].sum()

col1.metric(
    "Total Repair Cost",
    f"₹{total_cost:,.0f}"
)

col2.metric(
    "Total Downtime",
    f"{total_downtime:,.0f} hours"
)


maintenance_by_type = (
    filtered_maintenance["maintenance_type"]
    .value_counts()
)

st.subheader("Maintenance by Type")

st.bar_chart(maintenance_by_type)

# -----------------------------
# Maintenance Risk Prediction
# -----------------------------

st.header("⚠️ Maintenance Risk Prediction")

# Create truck-level trip features
trip_features = trips.groupby("truck_id").agg(
    trip_count=("trip_id", "count"),
    total_distance=("distance_km", "sum")
).reset_index()

risk_data = trucks.merge(
    trip_features,
    on="truck_id",
    how="left"
)

risk_data = risk_data.fillna(0)

# Create training target using age and mileage
risk_data["maintenance_risk"] = (
    (risk_data["truck_age_years"] >= 8) |
    (risk_data["total_mileage_km"] >= 180000)
).astype(int)

features = [
    "truck_age_years",
    "total_mileage_km",
    "capacity_tons",
    "trip_count",
    "total_distance"
]

X = risk_data[features]
y = risk_data["maintenance_risk"]

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Predict risk
risk_data["risk_prediction"] = model.predict(X)

risk_data["Maintenance Risk"] = risk_data[
    "risk_prediction"
].map({
    0: "Low",
    1: "High"
})
high_risk = (risk_data["Maintenance Risk"] == "High").sum()
low_risk = (risk_data["Maintenance Risk"] == "Low").sum()

col1, col2 = st.columns(2)

col1.metric("High Risk Trucks", high_risk)
col2.metric("Low Risk Trucks", low_risk)

risk_count = risk_data["Maintenance Risk"].value_counts()

st.subheader("Maintenance Risk Distribution")
st.bar_chart(risk_count)
st.dataframe(
    risk_data[
        [
            "truck_id",
            "truck_age_years",
            "total_mileage_km",
            "trip_count",
            "total_distance",
            "Maintenance Risk"
        ]
    ],
    use_container_width=True
)
# -----------------------------
# Truck Table
# -----------------------------

st.header("🚚 Truck Details")

st.dataframe(
    filtered_trucks[
        [
            "truck_id",
            "truck_type",
            "truck_age_years",
            "total_mileage_km",
            "capacity_tons",
            "fuel_type",
            "status"
        ]
    ],
    use_container_width=True
)