import pandas as pd
from pathlib import Path

base_path = Path(__file__).resolve().parent.parent
raw_path = base_path / "data" / "raw"
processed_path = base_path / "data" / "processed"

processed_path.mkdir(parents=True, exist_ok=True)


def clean_data(file_name):
    file_path = raw_path / file_name

    df = pd.read_csv(file_path)

    print("\n", file_name)
    print("Rows before cleaning:", len(df))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows with missing values
    df = df.dropna()

    return df


files = [
    "trucks.csv",
    "trips.csv",
    "maintenance.csv",
    "routes.csv"
]

for file in files:
    df = clean_data(file)

    output_file = processed_path / file
    df.to_csv(output_file, index=False)

    print("Rows after cleaning:", len(df))
    print("Saved:", output_file)

print("\nData cleaning completed!")