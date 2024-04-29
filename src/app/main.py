from fastapi import FastAPI
from .routers import exercise_analysis


app = FastAPI()
app.include_router(exercise_analysis.router) 


@app.get("/")
async def root():
    return {"message": "Api Content"}
