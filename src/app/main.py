from fastapi import FastAPI
from .routers import exercise_analysis
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(exercise_analysis.router) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Api Content"}
