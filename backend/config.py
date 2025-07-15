"""Configuration management for the Singapore Makan Recommender."""

import os
from typing import Dict


class Settings:
    """Application settings with environment variable support using Pydantic v2 approach."""
    
    def __init__(self):
        # Database settings
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///singapore_food.db")
        self.database_file: str = os.getenv("DATABASE_FILE", "singapore_food.db")
        
        # Recommendation settings
        self.max_recommendations: int = int(os.getenv("MAX_RECOMMENDATIONS", "3"))
        
        # Scoring configuration
        self.cuisine_bonus: float = float(os.getenv("CUISINE_BONUS", "1.0"))
        self.halal_bonus: float = float(os.getenv("HALAL_BONUS", "2.0"))
        self.vegetarian_bonus: float = float(os.getenv("VEGETARIAN_BONUS", "2.0"))
        self.meal_type_bonus: float = float(os.getenv("MEAL_TYPE_BONUS", "5.0"))
        
        # API settings
        self.api_host: str = os.getenv("API_HOST", "127.0.0.1")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        
        # Fuzzy logic settings
        self.fuzzy_config_path: str = os.getenv("FUZZY_CONFIG_PATH", "backend/fuzzy_config.json")
        
        # Logging settings
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")


class ScoringConfig:
    """Centralized scoring configuration to avoid magic numbers."""
    
    def __init__(self, settings: Settings):
        self.CUISINE_BONUS = settings.cuisine_bonus
        self.HALAL_BONUS = settings.halal_bonus
        self.VEGETARIAN_BONUS = settings.vegetarian_bonus
        self.MEAL_TYPE_BONUS = settings.meal_type_bonus
        
    def get_all_bonuses(self) -> Dict[str, float]:
        """Get all bonus values as a dictionary."""
        return {
            "cuisine": self.CUISINE_BONUS,
            "halal": self.HALAL_BONUS,
            "vegetarian": self.VEGETARIAN_BONUS,
            "meal_type": self.MEAL_TYPE_BONUS,
        }


# Global settings instance
settings = Settings()
scoring_config = ScoringConfig(settings)
