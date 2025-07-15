from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .ai_system import RecommendationEngine
from .database import create_db_and_tables, engine, seed_database
from .models import Dish, UserPreferences


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    create_db_and_tables()
    seed_database()
    yield
    # on shutdown


app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")


@app.get("/dishes", response_model=List[Dish])
def get_all_dishes():
    with Session(engine) as session:
        dishes = session.exec(select(Dish)).all()
        return dishes


@app.post("/recommend")
def get_recommendations(prefs: UserPreferences):
    with Session(engine) as session:
        dishes = session.exec(select(Dish)).all()
        engine_instance = RecommendationEngine(
            dishes=list(dishes), user_prefs=prefs.model_dump()
        )
        recommendations = engine_instance.get_recommendations()
        return recommendations
