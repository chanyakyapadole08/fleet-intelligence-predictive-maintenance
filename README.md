# Fleet Intelligence & Predictive Maintenance

An end-to-end fleet analytics and predictive maintenance project built using Python, SQL, MySQL, Machine Learning and Streamlit.

## Project Overview

This project analyzes simulated truck fleet data to understand fleet utilization, fuel efficiency, delivery performance and maintenance activity.

A Logistic Regression model is also used as a proof-of-concept to classify trucks into maintenance risk categories based on fleet and operational features.

## Objectives

* Analyze overall fleet performance
* Measure truck utilization and distance traveled
* Analyze fuel efficiency
* Monitor delivery performance
* Analyze maintenance cost and downtime
* Identify trucks with higher maintenance risk
* Build an interactive Streamlit dashboard

## Tech Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* SQL
* MySQL
* Scikit-learn
* Streamlit
* Git & GitHub

## Dataset

The project uses simulated fleet operation data generated using Python.

The dataset contains:

* 100 trucks
* 3,000 trips
* 500 maintenance records
* 8 routes

### Main Data Files

* `trucks.csv` - Truck information
* `trips.csv` - Trip and delivery information
* `maintenance.csv` - Maintenance records
* `routes.csv` - Route information

## Project Workflow

```text
Raw Fleet Data
      ↓
Data Generation
      ↓
Data Cleaning
      ↓
MySQL Database
      ↓
SQL Analysis
      ↓
Fleet Analytics
      ↓
Feature Engineering
      ↓
Predictive Maintenance Model
      ↓
Streamlit Dashboard
```

## How to Run

### 1. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/chanyakyapadole08/fleet-intelligence-predictive-maintenance.git
```

Open the project folder:

```bash
cd fleet-intelligence-predictive-maintenance
```

### 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Required Libraries

Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Generate Fleet Dataset

Generate the simulated fleet data:

```bash
python src/data_generator.py
```

This creates the following files inside `data/raw/`:

* `trucks.csv`
* `trips.csv`
* `maintenance.csv`
* `routes.csv`

### 5. Clean the Data

Run the data-cleaning script:

```bash
python src/data_cleaning.py
```

The cleaned files are saved inside:

```text
data/processed/
```

### 6. Set Up MySQL Database

Make sure MySQL Server is installed and running.

Open MySQL and create the database:

```sql
CREATE DATABASE fleet_intelligence;
USE fleet_intelligence;
```

Create the required tables according to the project database schema.

The SQL analysis queries are available in:

```text
sql/fleet_analysis.sql
```

### 7. Load Data into MySQL

Run the MySQL loading script:

```bash
python src/load_to_mysql.py
```

The script loads the processed CSV data into the MySQL database.

### 8. Run Fleet Analytics

Run the Python analytics script:

```bash
python src/analytics.py
```

This performs basic fleet, fuel, delivery and maintenance analysis.

### 9. Run Predictive Maintenance Model

Run the machine learning model:

```bash
python src/prediction.py
```

The model uses Logistic Regression to classify trucks into maintenance-risk categories and displays evaluation metrics such as:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

### 10. Run the Streamlit Dashboard

Start the interactive dashboard:

```bash
streamlit run dashboard/app.py
```

The dashboard provides:

* Fleet Overview
* Fuel Analytics
* Delivery Performance
* Maintenance Analytics
* Maintenance Risk Prediction
* Truck-level details

The dashboard will open in your web browser.
