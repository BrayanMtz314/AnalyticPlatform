import pandas as pd
from pathlib import Path

current_dir = Path(__file__).parent

# Load CSVs and instantly convert all column names to lowercase
dim_track = pd.read_csv(current_dir / 'DIM_TRACKS.csv').rename(columns=str.lower)
dim_customer = pd.read_csv(current_dir / 'DIM_CUSTOMER.csv').rename(columns=str.lower)
dim_employees = pd.read_csv(current_dir / 'DIM_EMPLOYEES.csv').rename(columns=str.lower)
dim_date = pd.read_csv(current_dir / 'DIM_DATES.csv').rename(columns=str.lower)
fact_sales = pd.read_csv(current_dir / 'FACT_SALES.csv').rename(columns=str.lower)

