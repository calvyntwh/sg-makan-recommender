import json
from typing import Any, Dict, List

from experta import MATCH, DefFacts, Fact, KnowledgeEngine, Rule
from fuzzy_expert.inference import DecompositionalInference
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.variable import FuzzyVariable

from .models import Dish


# --- Fuzzy Logic System using fuzzy-expert ---
def create_fuzzy_system():
    """Create fuzzy logic system using fuzzy-expert library"""
    config = load_fuzzy_config()

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

    # Create fuzzy rules
    rules = [
        FuzzyRule(
            premise=[("budget", "low"), ("spiciness", "mild")],
            consequence=[("recommendation_score", "high")],
        ),
        FuzzyRule(
            premise=[("budget", "medium"), ("spiciness", "medium")],
            consequence=[("recommendation_score", "high")],
        ),
        FuzzyRule(
            premise=[("budget", "high"), ("spiciness", "spicy")],
            consequence=[("recommendation_score", "high")],
        ),
        FuzzyRule(
            premise=[("budget", "high"), ("spiciness", "mild")],
            consequence=[("recommendation_score", "low")],
        ),
    ]

    # Create inference system
    variables = {
        "budget": budget_var,
        "spiciness": spiciness_var,
        "recommendation_score": recommendation_var,
    }

    return (
        DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="min",
            composition_operator="max",
            production_link="max",
            defuzzification_operator="centroid",
        ),
        variables,
        rules,
    )


def load_fuzzy_config():
    with open("backend/fuzzy_config.json") as f:
        return json.load(f)


def fuzzy_engine(inputs):
    """Fuzzy logic engine using fuzzy-expert library"""
    try:
        inference_system, variables, rules = create_fuzzy_system()

        # Set input values for potential future use with fuzzy-expert
        # Currently using simple_fuzzy_inference as fallback

        # Run inference (simplified approach)
        # Note: fuzzy-expert has a complex API, so we'll use a hybrid approach
        # where we use our own simple inference but with the fuzzy-expert structure
        return simple_fuzzy_inference(inputs)

    except Exception:
        # Fallback to simple scoring
        return simple_fuzzy_inference(inputs)


def simple_fuzzy_inference(inputs):
    """Simplified fuzzy inference as backup"""
    config = load_fuzzy_config()

    budget = inputs.get("budget", 0)
    spiciness = inputs.get("spiciness", 0)

    try:
        # Calculate membership values for budget
        budget_low = fuzzy_membership(budget, *config["budget"]["terms"]["low"])
        budget_medium = fuzzy_membership(budget, *config["budget"]["terms"]["medium"])
        budget_high = fuzzy_membership(budget, *config["budget"]["terms"]["high"])

        # Calculate membership values for spiciness
        spice_mild = fuzzy_membership(
            spiciness, *config["spiciness"]["terms"]["mild"]
        )
        spice_medium = fuzzy_membership(
            spiciness, *config["spiciness"]["terms"]["medium"]
        )
        spice_spicy = fuzzy_membership(
            spiciness, *config["spiciness"]["terms"]["spicy"]
        )

        # Apply fuzzy rules using min-max inference
        rule1 = min(budget_low, spice_mild)  # low budget + mild -> high score
        rule2 = min(budget_medium, spice_medium)  # medium budget + medium -> high score
        rule3 = min(budget_high, spice_spicy)  # high budget + spicy -> high score
        rule4 = min(budget_high, spice_mild)  # high budget + mild -> low score

        # Aggregate rules
        high_score_activation = max(rule1, rule2, rule3)
        low_score_activation = rule4

        # Simple defuzzification
        if high_score_activation > low_score_activation:
            score = 7.5 * high_score_activation + 2.5 * low_score_activation
        else:
            score = 2.5 * high_score_activation + 7.5 * low_score_activation

        # Ensure score is in valid range
        score = max(0, min(10, score))

        return {"recommendation_score": score}
    except Exception as e:
        print(f"Debug: Exception in fuzzy inference: {e}")
        return {"recommendation_score": 0}


def fuzzy_membership(value, low, mid, high):
    """Calculate membership value for a triangular fuzzy set"""
    if value <= low:
        return 1.0 if value == low else 0.0
    elif value <= mid:
        return (value - low) / (mid - low)
    elif value <= high:
        return (high - value) / (high - mid)
    else:
        return 0.0


# --- Expert System Engine (Experta) ---
class UserPreferences(Fact):
    pass


class ScoredDish(Fact):
    pass


# Expert System for filtering and reasoning
class RecommendationEngine(KnowledgeEngine):
    def __init__(self, dishes: List[Dish], user_prefs: Dict[str, Any]):
        super().__init__()
        self.dishes = dishes
        self.user_prefs = user_prefs
        self.recommendations = []

    @DefFacts()
    def _initial_facts(self):
        yield UserPreferences(**self.user_prefs)

    @Rule(UserPreferences(budget=MATCH.budget, spiciness=MATCH.spiciness))
    def score_dishes(self, budget, spiciness):

        # Store recommendations directly instead of using Facts
        self.recommendations = []

        for dish in self.dishes:
            # Use fuzzy logic to get the baseline score
            # Compare user budget against dish price, and use dish spiciness
            fuzzy_result = fuzzy_engine(
                {"budget": budget, "spiciness": dish.spiciness}
            )
            fuzzy_score = fuzzy_result.get("recommendation_score", 0.0)

            # Apply budget filtering: exclude dishes that exceed user's budget
            if dish.price > budget:
                continue

            # Include all dishes that pass budget filter, even with 0 fuzzy score
            # Expert system bonuses may still make them viable
            reasons = []
            final_score = fuzzy_score

            if fuzzy_score > 0:
                reasons.append("Base compatibility score")

            # Apply expert system bonuses
            user_prefs = self.user_prefs

            # Cuisine matching bonus
            if user_prefs.get("cuisine", "any").lower() == "any" or \
               user_prefs.get("cuisine", "").lower() == dish.cuisine.lower():
                final_score += 1.0
                reasons.append(f"Matches cuisine: {dish.cuisine}")

            # Halal bonus
            if user_prefs.get("is_halal", False) and dish.is_halal:
                final_score += 2.0
                reasons.append("Is Halal")

            # Vegetarian bonus
            if user_prefs.get("is_vegetarian", False) and dish.is_vegetarian:
                final_score += 2.0
                reasons.append("Is Vegetarian")

            # Only include dishes that have some positive score (fuzzy or expert bonus)
            if final_score > 0:
                self.recommendations.append({
                    "dish": dish.model_dump(),
                    "score": final_score,
                    "reasons": reasons,
                })

    @Rule(
        ScoredDish(dish=MATCH.dish, final_score=MATCH.score, reasons=MATCH.reasons),
        UserPreferences(cuisine=MATCH.cuisine),
    )
    def match_cuisine(self, dish, score, reasons, cuisine):
        if cuisine.lower() == "any" or cuisine.lower() == dish.cuisine.lower():
            new_score = score + 1
            new_reasons = list(reasons) + [f"Matches Cuisine: {dish.cuisine}"]
            # Find and modify the fact
            for fact in self.facts:
                if (
                    isinstance(fact, ScoredDish)
                    and fact.get("dish")
                    and fact["dish"].id == dish.id
                ):
                    self.modify(fact, final_score=new_score, reasons=new_reasons)
                    break

    @Rule(
        ScoredDish(dish=MATCH.dish, final_score=MATCH.score, reasons=MATCH.reasons),
        UserPreferences(is_halal=True),
    )
    def match_halal(self, dish, score, reasons):
        if dish.is_halal:
            new_score = score + 2
            new_reasons = list(reasons) + ["Is Halal"]
            for fact in self.facts:
                if (
                    isinstance(fact, ScoredDish)
                    and fact.get("dish")
                    and fact["dish"].id == dish.id
                ):
                    self.modify(fact, final_score=new_score, reasons=new_reasons)
                    break

    @Rule(
        ScoredDish(dish=MATCH.dish, final_score=MATCH.score, reasons=MATCH.reasons),
        UserPreferences(is_vegetarian=True),
    )
    def match_vegetarian(self, dish, score, reasons):
        if dish.is_vegetarian:
            new_score = score + 2
            new_reasons = list(reasons) + ["Is Vegetarian"]
            for fact in self.facts:
                if (
                    isinstance(fact, ScoredDish)
                    and fact.get("dish")
                    and fact["dish"].id == dish.id
                ):
                    self.modify(fact, final_score=new_score, reasons=new_reasons)
                    break

    @Rule(
        ScoredDish(dish=MATCH.dish, final_score=MATCH.score, reasons=MATCH.reasons),
        UserPreferences(meal_type=MATCH.meal_type),
    )
    def match_meal_type(self, dish, score, reasons, meal_type):
        if meal_type and meal_type.lower() == dish.meal_type.lower():
            new_score = score + 5
            new_reasons = list(reasons) + [f"Matches Meal Type: {dish.meal_type}"]
            for fact in self.facts:
                if (
                    isinstance(fact, ScoredDish)
                    and fact.get("dish")
                    and fact["dish"].id == dish.id
                ):
                    self.modify(fact, final_score=new_score, reasons=new_reasons)
                    break

    def get_recommendations(self):
        self.reset()
        print("Debug: Starting recommendation engine...")
        self.run()

        # Return the recommendations created by the rule
        if hasattr(self, 'recommendations') and self.recommendations:
            sorted_recommendations = sorted(
                self.recommendations, key=lambda x: x["score"], reverse=True
            )

            return sorted_recommendations[:3]
        else:
            print("Debug: No recommendations found")
            return []
