import pandas as pd
import mysql.connector
from pathlib import Path
from getpass import getpass


# Project paths
base_path = Path(__file__).resolve().parent.parent
data_path = base_path / "data" / "processed"


# MySQL connection
password = getpass("Enter MySQL password: ")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="fleet_intelligence"
)

cursor = db.cursor()


def load_csv(file_name, table_name):
    file_path = data_path / file_name
    df = pd.read_csv(file_path)

    # Convert date columns
    for column in df.columns:
        if "date" in column:
            df[column] = pd.to_datetime(df[column]).dt.date

    # Replace NaN with None for MySQL
    df = df.where(pd.notnull(df), None)

    columns = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))

    query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
    """

    data = [tuple(row) for row in df.itertuples(index=False, name=None)]

    cursor.executemany(query, data)
    db.commit()

    print(f"{table_name}: {len(df)} rows inserted")


# Load parent tables first because of foreign keys
load_csv("routes.csv", "routes")
load_csv("trucks.csv", "trucks")
load_csv("trips.csv", "trips")
load_csv("maintenance.csv", "maintenance")


cursor.close()
db.close()

print("All CSV files loaded into MySQL!")
