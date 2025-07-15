"""AI System combining fuzzy logic and expert systems for food recommendations."""

import json
from typing import Any, Dict, List, Optional, Tuple

from experta import MATCH, DefFacts, Fact, KnowledgeEngine, Rule
from fuzzy_expert.inference import DecompositionalInference
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.variable import FuzzyVariable

from .config import settings, scoring_config
from .logging_config import logger
from .models import Dish


# Global fuzzy system cache to avoid recreation
_fuzzy_system_cache: Optional[Tuple[Any, Dict[str, Any], List[Any]]] = None


def get_fuzzy_system():
    """Get cached fuzzy logic system or create new one."""
    global _fuzzy_system_cache
    if _fuzzy_system_cache is None:
        _fuzzy_system_cache = create_fuzzy_system()
    return _fuzzy_system_cache


def create_fuzzy_system():
    """Create fuzzy logic system using fuzzy-expert library."""
    try:
        config = load_fuzzy_config()
        logger.debug("Creating fuzzy logic system with config: %s", config)

        # Create fuzzy variables
        budget_var = FuzzyVariable(
            universe_range=tuple(config["budget"]["universe_range"]),
            terms=config["budget"]["terms"],
        )

        spiciness_var = FuzzyVariable(
            universe_range=tuple(config["spiciness"]["universe_range"]),
            terms=config["spiciness"]["terms"],
        )

        recommendation_var = FuzzyVariable(
            universe_range=tuple(config["recommendation_score"]["universe_range"]),
            terms=config["recommendation_score"]["terms"],
        )

        # Create comprehensive fuzzy rules
        rules = [
            # Budget-Spiciness combinations
            FuzzyRule(
                premise=[("budget", "low"), ("spiciness", "mild")],
                consequence=[("recommendation_score", "high")],
            ),
            FuzzyRule(
                premise=[("budget", "low"), ("spiciness", "medium")],
                consequence=[("recommendation_score", "medium")],
            ),
            FuzzyRule(
                premise=[("budget", "low"), ("spiciness", "spicy")],
                consequence=[("recommendation_score", "medium")],
            ),
            FuzzyRule(
                premise=[("budget", "medium"), ("spiciness", "mild")],
                consequence=[("recommendation_score", "medium")],
            ),
            FuzzyRule(
                premise=[("budget", "medium"), ("spiciness", "medium")],
                consequence=[("recommendation_score", "high")],
            ),
            FuzzyRule(
                premise=[("budget", "medium"), ("spiciness", "spicy")],
                consequence=[("recommendation_score", "medium")],
            ),
            FuzzyRule(
                premise=[("budget", "high"), ("spiciness", "mild")],
                consequence=[("recommendation_score", "low")],
            ),
            FuzzyRule(
                premise=[("budget", "high"), ("spiciness", "medium")],
                consequence=[("recommendation_score", "medium")],
            ),
            FuzzyRule(
                premise=[("budget", "high"), ("spiciness", "spicy")],
                consequence=[("recommendation_score", "high")],
            ),
        ]

        # Create inference system
        variables = {
            "budget": budget_var,
            "spiciness": spiciness_var,
            "recommendation_score": recommendation_var,
        }

        inference_system = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="min",
            composition_operator="max",
            production_link="max",
            defuzzification_operator="centroid",
        )

        logger.info("Fuzzy logic system created successfully")
        return inference_system, variables, rules

    except Exception as e:
        logger.error("Failed to create fuzzy system: %s", e)
        raise


def load_fuzzy_config():
    """Load fuzzy logic configuration from JSON file."""
    try:
        with open(settings.fuzzy_config_path) as f:
            config = json.load(f)
        logger.debug("Loaded fuzzy config from %s", settings.fuzzy_config_path)
        return config
    except FileNotFoundError:
        logger.error("Fuzzy config file not found: %s", settings.fuzzy_config_path)
        raise
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in fuzzy config: %s", e)
        raise


def fuzzy_engine(inputs: Dict[str, float]) -> Dict[str, float]:
    """Enhanced fuzzy logic engine with proper error handling."""
    try:
        # For now, use the robust simple inference implementation
        # This can be extended to use fuzzy-expert when needed
        result = simple_fuzzy_inference(inputs)
        logger.debug("Fuzzy inference result for inputs %s: %s", inputs, result)
        return result

    except Exception as e:
        logger.warning("Fuzzy inference failed: %s, using fallback", e)
        return {"recommendation_score": 0.0}


def simple_fuzzy_inference(inputs: Dict[str, float]) -> Dict[str, float]:
    """Simplified but robust fuzzy inference implementation."""
    try:
        config = load_fuzzy_config()

        budget = inputs.get("budget", 0)
        spiciness = inputs.get("spiciness", 0)

        # Calculate membership values for budget
        budget_low = fuzzy_membership(budget, *config["budget"]["terms"]["low"])
        budget_medium = fuzzy_membership(budget, *config["budget"]["terms"]["medium"])
        budget_high = fuzzy_membership(budget, *config["budget"]["terms"]["high"])

        # Calculate membership values for spiciness
        spice_mild = fuzzy_membership(spiciness, *config["spiciness"]["terms"]["mild"])
        spice_medium = fuzzy_membership(spiciness, *config["spiciness"]["terms"]["medium"])
        spice_spicy = fuzzy_membership(spiciness, *config["spiciness"]["terms"]["spicy"])

        # Apply fuzzy rules using min-max inference
        rules_activation = {
            "high": max(
                min(budget_low, spice_mild),      # Rule 1: low budget + mild -> high
                min(budget_medium, spice_medium), # Rule 5: medium budget + medium -> high
                min(budget_high, spice_spicy),    # Rule 9: high budget + spicy -> high
            ),
            "medium": max(
                min(budget_low, spice_medium),    # Rule 2: low budget + medium -> medium
                min(budget_low, spice_spicy),     # Rule 3: low budget + spicy -> medium
                min(budget_medium, spice_mild),   # Rule 4: medium budget + mild -> medium
                min(budget_medium, spice_spicy),  # Rule 6: medium budget + spicy -> medium
                min(budget_high, spice_medium),   # Rule 8: high budget + medium -> medium
            ),
            "low": min(budget_high, spice_mild),  # Rule 7: high budget + mild -> low
        }

        # Defuzzification using weighted average
        score_values = {"high": 8.0, "medium": 5.0, "low": 2.0}
        total_activation = sum(rules_activation.values())
        
        if total_activation > 0:
            score = sum(
                activation * score_values[level] 
                for level, activation in rules_activation.items()
            ) / total_activation
        else:
            score = 0.0

        # Ensure score is in valid range
        score = max(0, min(10, score))

        return {"recommendation_score": score}

    except Exception as e:
        logger.error("Simple fuzzy inference failed: %s", e)
        return {"recommendation_score": 0.0}


def fuzzy_membership(value: float, low: float, mid: float, high: float) -> float:
    """Calculate membership value for a triangular fuzzy set."""
    if value <= low:
        return 1.0 if value == low else 0.0
    elif value <= mid:
        return (value - low) / (mid - low) if mid != low else 1.0
    elif value <= high:
        return (high - value) / (high - mid) if high != mid else 1.0
    else:
        return 0.0


# --- Expert System Classes ---
class UserPreferences(Fact):
    """Fact representing user preferences."""
    pass


class DishCandidate(Fact):
    """Fact representing a dish candidate for recommendation."""
    pass


class ScoredDish(Fact):
    """Fact representing a dish with its calculated score."""
    pass


class RecommendationEngine(KnowledgeEngine):
    """Expert system engine for food recommendations using a simpler, more reliable approach."""

    def __init__(self, dishes: List[Dish], user_prefs: Dict[str, Any]):
        super().__init__()
        self.dishes = dishes
        self.user_prefs = user_prefs
        self.scored_dishes = []
        logger.info("Initialized RecommendationEngine with %d dishes", len(dishes))

    @DefFacts()
    def _initial_facts(self):
        """Initialize facts in the knowledge base."""
        yield UserPreferences(**self.user_prefs)

    @Rule(UserPreferences(budget=MATCH.budget, spiciness=MATCH.spiciness))
    def calculate_recommendations(self, budget, spiciness):
        """Calculate all recommendations in a single rule to avoid fact management complexity."""
        logger.debug("Calculating recommendations for budget=%.2f, spiciness=%d", budget, spiciness)
        
        self.scored_dishes = []  # Reset scored dishes
        
        for dish in self.dishes:
            # Apply budget filtering: exclude dishes that exceed user's budget
            if dish.price > budget:
                continue

            # Get fuzzy logic score based on budget and spiciness preferences
            fuzzy_result = fuzzy_engine({
                "budget": budget, 
                "spiciness": spiciness
            })
            base_score = fuzzy_result.get("recommendation_score", 0.0)
            
            reasons = []
            final_score = base_score

            if base_score > 0:
                reasons.append("Base compatibility score")

            # Apply expert system bonuses
            user_prefs = self.user_prefs

            # Cuisine matching bonus
            if (user_prefs.get("cuisine", "any").lower() == "any" or 
                user_prefs.get("cuisine", "").lower() == dish.cuisine.lower()):
                final_score += scoring_config.CUISINE_BONUS
                reasons.append(f"Matches cuisine: {dish.cuisine}")

            # Halal bonus
            if user_prefs.get("is_halal", False) and dish.is_halal:
                final_score += scoring_config.HALAL_BONUS
                reasons.append("Is Halal")

            # Vegetarian bonus
            if user_prefs.get("is_vegetarian", False) and dish.is_vegetarian:
                final_score += scoring_config.VEGETARIAN_BONUS
                reasons.append("Is Vegetarian")

            # Meal type bonus
            meal_type = user_prefs.get("meal_type")
            if meal_type and meal_type.lower() == dish.meal_type.lower():
                final_score += scoring_config.MEAL_TYPE_BONUS
                reasons.append(f"Matches meal type: {dish.meal_type}")

            # Only include dishes that have some positive score (fuzzy or expert bonus)
            if final_score > 0:
                self.scored_dishes.append({
                    "dish": dish.model_dump(),
                    "score": final_score,
                    "reasons": reasons,
                })
                logger.debug("Scored dish %s: %.2f points", dish.name, final_score)

    def get_recommendations(self) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Get top recommendations using the expert system with enhanced metadata."""
        try:
            # Track initial metrics
            total_candidates = len(self.dishes)
            
            # Reset and run the expert system
            self.reset()
            self.scored_dishes = []  # Clear previous results
            self.run()

            # Determine which filters were applied
            filters_applied = []
            filtered_count = len([d for d in self.dishes if self._dish_passes_filters(d)])
            
            if any(dish.price > self.user_prefs['budget'] for dish in self.dishes):
                filters_applied.append("budget")
            if self.user_prefs['cuisine'].lower() != 'any':
                filters_applied.append("cuisine")
            if self.user_prefs['is_halal']:
                filters_applied.append("halal")
            if self.user_prefs['is_vegetarian']:
                filters_applied.append("vegetarian")

            # Create metadata
            metadata = {
                "total_candidates": total_candidates,
                "filtered_candidates": filtered_count,
                "scoring_method": "fuzzy_logic_with_expert_system",
                "filters_applied": filters_applied,
                "suggestions": None
            }

            if not self.scored_dishes:
                logger.warning("No recommendations found for preferences: %s", self.user_prefs)
                
                # Generate helpful suggestions
                metadata["suggestions"] = self._generate_suggestions(filters_applied)
                
                return [], metadata

            # Sort by score and return top recommendations
            sorted_recommendations = sorted(
                self.scored_dishes, 
                key=lambda x: x["score"], 
                reverse=True
            )

            top_recommendations = sorted_recommendations[:settings.max_recommendations]
            
            logger.info(
                "Generated %d recommendations from %d candidates", 
                len(top_recommendations), 
                len(self.scored_dishes)
            )
            
            return top_recommendations, metadata

        except Exception as e:
            logger.error("Error generating recommendations: %s", e)
            metadata = {
                "total_candidates": len(self.dishes) if hasattr(self, 'dishes') else 0,
                "filtered_candidates": 0,
                "scoring_method": "fuzzy_logic_with_expert_system",
                "filters_applied": [],
                "suggestions": "An error occurred while generating recommendations. Please try again."
            }
            return [], metadata
    
    def _dish_passes_filters(self, dish) -> bool:
        """Check if a dish passes all user filters."""
        # Budget filter
        if dish.price > self.user_prefs['budget']:
            return False
        
        # Cuisine filter
        if (self.user_prefs['cuisine'].lower() != 'any' and 
            dish.cuisine.lower() != self.user_prefs['cuisine'].lower()):
            return False
        
        # Dietary restrictions
        if self.user_prefs['is_halal'] and not dish.is_halal:
            return False
            
        if self.user_prefs['is_vegetarian'] and not dish.is_vegetarian:
            return False
        
        return True
    
    def _generate_suggestions(self, filters_applied: list) -> str:
        """Generate helpful suggestions when no recommendations are found."""
        suggestions = []
        
        if "budget" in filters_applied:
            suggestions.append("try increasing your budget")
        
        if "cuisine" in filters_applied:
            suggestions.append("consider trying 'any' cuisine type")
        
        if "halal" in filters_applied:
            suggestions.append("expand to include non-halal options if acceptable")
        
        if "vegetarian" in filters_applied:
            suggestions.append("consider non-vegetarian options if acceptable")
        
        if not suggestions:
            return "Try adjusting your preferences for more options."
        
        return "To find more options, " + " or ".join(suggestions) + "."
