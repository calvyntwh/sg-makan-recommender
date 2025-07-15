from typing import List, Optional

from sqlmodel import JSON, Column, Field, SQLModel


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
