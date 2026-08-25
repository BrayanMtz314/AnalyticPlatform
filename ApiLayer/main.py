from fastapi import FastAPI, Query
from routers import analyticsRoutes


app = FastAPI()
app.include_router(analyticsRoutes.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}