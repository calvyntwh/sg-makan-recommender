from typing import List, Optional, Dict, Any

from sqlmodel import JSON, Column, Field, SQLModel
from pydantic import BaseModel


class Dish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    price: float
    cuisine: str
    spiciness: int
    meal_time: List[str] = Field(sa_column=Column(JSON))
    # NEW FIELD to better classify dishes
    meal_type: str  # e.g., "main_course", "side_dish", "dessert", "drink"
    attributes: List[str] = Field(sa_column=Column(JSON))
    is_halal: bool
    is_vegetarian: bool

    def __hash__(self):
        return hash(
            (
                self.name,
                self.price,
                self.cuisine,
                self.spiciness,
                self.is_halal,
                self.is_vegetarian,
                self.meal_type,
            )
        )


class UserPreferences(SQLModel, table=False):
    budget: float
    cuisine: str
    spiciness: int
    is_halal: bool
    is_vegetarian: bool
    meal_type: Optional[str] = None


class RecommendationMetadata(BaseModel):
    """Metadata about the recommendation process."""
    
    total_candidates: int = Field(description="Total dishes considered")
    filtered_candidates: int = Field(description="Dishes after filtering")
    scoring_method: str = Field(description="Method used for scoring")
    filters_applied: List[str] = Field(description="List of filters that were applied")
    suggestions: Optional[str] = Field(default=None, description="Helpful suggestions for user")


class RecommendationResponse(BaseModel):
    """Enhanced response model for recommendations."""
    
    recommendations: List[Dict[str, Any]] = Field(description="List of recommended dishes with scores")
    metadata: RecommendationMetadata = Field(description="Information about the recommendation process")
    success: bool = Field(description="Whether the request was successful")
    message: Optional[str] = Field(default=None, description="Additional message for the user")
