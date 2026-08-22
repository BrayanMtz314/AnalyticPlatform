from fastapi import FastAPI, Query
from data.mockData import dim_track, dim_customer, dim_employees, dim_date, fact_sales
from routers import analyticsRoutes


app = FastAPI()
app.include_router(analyticsRoutes.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/dim_track")
def get_dim_track():
    return dim_track

@app.get("/dim_customer")
def get_dim_customer():
    return dim_customer

@app.get("/dim_employees")
def get_dim_employees():
    return dim_employees

@app.get("/dim_date")
def get_dim_date():
    return dim_date

@app.get("/fact_sales")
def get_fact_sales():
    return fact_sales