from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from sqlmodel import Session, select

from .ai_system import RecommendationEngine
from .database import create_db_and_tables, engine, seed_database
from .logging_config import logger
from .models import Dish, UserPreferences, RecommendationResponse, RecommendationMetadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    try:
        logger.info("Starting up Singapore Makan Recommender...")
        create_db_and_tables()
        seed_database()
        logger.info("Startup completed successfully")
    except Exception as e:
        logger.error("Failed to start up application: %s", e)
        raise
    
    yield
    
    # on shutdown
    logger.info("Shutting down Singapore Makan Recommender...")


app = FastAPI(
    title="Singapore Makan Recommender",
    description="AI-powered food recommendation system for Singapore cuisine",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def read_root():
    """Serve the main web interface."""
    return FileResponse("frontend/index.html")


@app.get("/dishes", response_model=List[Dish])
def get_all_dishes():
    """Get all available dishes from the database."""
    try:
        with Session(engine) as session:
            dishes = session.exec(select(Dish)).all()
            logger.debug("Retrieved %d dishes from database", len(dishes))
            return dishes
    except Exception as e:
        logger.error("Failed to retrieve dishes: %s", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve dishes")


@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(prefs: UserPreferences):
    """Get personalized food recommendations based on user preferences."""
    try:
        logger.info("Generating recommendations for preferences: %s", prefs.model_dump())
        
        with Session(engine) as session:
            dishes = session.exec(select(Dish)).all()
            
            if not dishes:
                logger.warning("No dishes found in database")
                raise HTTPException(status_code=404, detail="No dishes available")
            
            engine_instance = RecommendationEngine(
                dishes=list(dishes), 
                user_prefs=prefs.model_dump()
            )
            recommendations, metadata = engine_instance.get_recommendations()
            
            # Create the enhanced response
            if not recommendations:
                logger.info("No recommendations found for user preferences")
                return RecommendationResponse(
                    recommendations=[],
                    metadata=RecommendationMetadata(**metadata),
                    success=True,
                    message="No dishes match your current preferences. " + (metadata.get("suggestions", ""))
                )
            
            logger.info("Generated %d recommendations", len(recommendations))
            return RecommendationResponse(
                recommendations=recommendations,
                metadata=RecommendationMetadata(**metadata),
                success=True,
                message=f"Found {len(recommendations)} great recommendations for you!"
            )
            
    except ValidationError as e:
        logger.warning("Invalid user preferences: %s", e)
        raise HTTPException(status_code=422, detail=str(e))
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error("Unexpected error generating recommendations: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
