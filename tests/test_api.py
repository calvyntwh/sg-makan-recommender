import os
import sys

# Add the parent directory to Python path so we can import backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_api_health_and_data_seeding():
    """Test that the dishes endpoint works and database is seeded."""
    response = client.get("/dishes")
    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    assert len(dishes) > 0

    # Verify dish structure
    first_dish = dishes[0]
    required_fields = [
        "name",
        "price",
        "cuisine",
        "spiciness",
        "is_halal",
        "is_vegetarian",
    ]
    for field in required_fields:
        assert field in first_dish

    # Verify data types
    assert isinstance(first_dish["price"], (int, float))
    assert isinstance(first_dish["spiciness"], int)
    assert isinstance(first_dish["is_halal"], bool)
    assert isinstance(first_dish["is_vegetarian"], bool)


def test_recommendation_endpoint_basic():
    """Test basic recommendation endpoint functionality."""
    prefs = {
        "budget": 15.0,
        "cuisine": "Chinese",
        "spiciness": 4,
        "is_halal": False,
        "is_vegetarian": False,
    }
    response = client.post("/recommend", json=prefs)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)

    # Test recommendation structure if any are returned
    if recommendations:
        rec = recommendations[0]
        assert "dish" in rec
        assert "score" in rec
        assert "reasons" in rec
        assert isinstance(rec["score"], (int, float))
        assert isinstance(rec["reasons"], list)


def test_recommendation_vegetarian_preference():
    """Test recommendation with vegetarian preference."""
    prefs = {
        "budget": 20.0,
        "cuisine": "any",
        "spiciness": 3,
        "is_halal": False,
        "is_vegetarian": True,
    }
    response = client.post("/recommend", json=prefs)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)

    # If recommendations are returned, they should respect vegetarian preference
    for rec in recommendations:
        if rec["dish"]["is_vegetarian"] is False:
            # This would be a bug - vegetarian user getting non-veg recommendations
            dish_name = rec["dish"]["name"]
            error_msg = f"Non-vegetarian dish {dish_name} recommended to vegetarian"
            assert False, error_msg


def test_recommendation_halal_preference():
    """Test recommendation with halal preference."""
    prefs = {
        "budget": 25.0,
        "cuisine": "any",
        "spiciness": 5,
        "is_halal": True,
        "is_vegetarian": False,
    }
    response = client.post("/recommend", json=prefs)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)

    # If recommendations are returned, they should respect halal preference
    for rec in recommendations:
        if rec["dish"]["is_halal"] is False:
            # This would be a bug - halal user getting non-halal recommendations
            dish_name = rec["dish"]["name"]
            assert False, f"Non-halal dish {dish_name} recommended to halal user"


def test_highly_restrictive_filtering():
    """Test recommendation with very specific criteria."""
    prefs = {
        "budget": 10.0,
        "cuisine": "Indian",
        "spiciness": 8,
        "is_halal": True,
        "is_vegetarian": True,
    }
    response = client.post("/recommend", json=prefs)
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)

    # Response can be empty list (valid outcome)
    # If any dishes returned, they must strictly match criteria
    for rec in recommendations:
        dish = rec["dish"]
        assert dish["is_halal"], f"Non-halal dish recommended: {dish['name']}"
        assert dish["is_vegetarian"], f"Non-veg dish: {dish['name']}"


def test_recommendation_budget_limits():
    """Test recommendations with different budget constraints."""
    # Low budget test
    low_budget_prefs = {
        "budget": 8.0,
        "cuisine": "any",
        "spiciness": 3,
        "is_halal": False,
        "is_vegetarian": False,
    }
    response = client.post("/recommend", json=low_budget_prefs)
    assert response.status_code == 200

    # High budget test
    high_budget_prefs = {
        "budget": 40.0,
        "cuisine": "any",
        "spiciness": 3,
        "is_halal": False,
        "is_vegetarian": False,
    }
    response = client.post("/recommend", json=high_budget_prefs)
    assert response.status_code == 200


def test_recommendation_cuisine_specific():
    """Test recommendations for specific cuisines."""
    cuisines = ["Chinese", "Malay", "Indian", "Local"]

    for cuisine in cuisines:
        prefs = {
            "budget": 20.0,
            "cuisine": cuisine,
            "spiciness": 4,
            "is_halal": False,
            "is_vegetarian": False,
        }
        response = client.post("/recommend", json=prefs)
        assert response.status_code == 200
        recommendations = response.json()
        assert isinstance(recommendations, list)


def test_recommendation_spiciness_levels():
    """Test recommendations with different spiciness preferences."""
    for spice_level in [0, 3, 6, 10]:
        prefs = {
            "budget": 15.0,
            "cuisine": "any",
            "spiciness": spice_level,
            "is_halal": False,
            "is_vegetarian": False,
        }
        response = client.post("/recommend", json=prefs)
        assert response.status_code == 200
        recommendations = response.json()
        assert isinstance(recommendations, list)


def test_invalid_request_budget_string():
    """Test API validation with invalid budget type."""
    prefs = {
        "budget": "cheap",  # Invalid: should be float
        "cuisine": "Chinese",
        "spiciness": 4,
        "is_halal": False,
        "is_vegetarian": False,
    }
    response = client.post("/recommend", json=prefs)
    assert response.status_code == 422  # Validation error


def test_invalid_request_missing_fields():
    """Test API validation with missing required fields."""
    incomplete_prefs = {
        "budget": 15.0,
        # Missing other required fields
    }
    response = client.post("/recommend", json=incomplete_prefs)
    # Should handle missing fields gracefully or return validation error
    assert response.status_code in [200, 422]


def test_invalid_request_out_of_range():
    """Test API validation with out-of-range values."""
    prefs = {
        "budget": -10.0,  # Invalid: negative budget
        "cuisine": "Chinese",
        "spiciness": 15,  # Invalid: beyond 0-10 range
        "is_halal": False,
        "is_vegetarian": False,
    }
    response = client.post("/recommend", json=prefs)
    # Should handle gracefully
    assert response.status_code in [200, 422]


def test_api_concurrent_requests():
    """Test that the API can handle multiple concurrent requests."""
    import threading

    results = []

    def make_request():
        prefs = {
            "budget": 20.0,
            "cuisine": "any",
            "spiciness": 5,
            "is_halal": False,
            "is_vegetarian": False,
        }
        response = client.post("/recommend", json=prefs)
        results.append(response.status_code)

    # Create multiple threads
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=make_request)
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # All requests should succeed
    assert all(status == 200 for status in results)
    assert len(results) == 5


# --- Enhanced Real-world Scenario Tests ---


def test_budget_conscious_student_scenario():
    """
    SCENARIO: Budget-conscious student looking for affordable meals.
    """
    # Student with limited budget
    request_data = {
        "budget": 5.0,
        "cuisine": "any",
        "spiciness": 3,
        "is_halal": False,
        "is_vegetarian": False,
    }
    
    response = client.post("/recommend", json=request_data)
    assert response.status_code == 200
    
    recommendations = response.json()
    assert len(recommendations) >= 1, "Should get recommendations for budget-conscious student"
    
    # All recommendations should be within budget
    for rec in recommendations:
        dish_price = rec["dish"]["price"]
        assert dish_price <= 5.0, f"Dish price {dish_price} exceeds budget of 5.0"
    
    # Should have base compatibility scores (fuzzy logic working)
    assert any("Base compatibility score" in rec["reasons"] for rec in recommendations), \
        "Should have fuzzy logic base scores"


def test_spicy_food_lover_scenario():
    """
    SCENARIO: User who loves spicy food with medium budget.
    """
    request_data = {
        "budget": 12.0,
        "cuisine": "any", 
        "spiciness": 8,  # Loves spicy food
        "is_halal": False,
        "is_vegetarian": False,
    }
    
    response = client.post("/recommend", json=request_data)
    assert response.status_code == 200
    
    recommendations = response.json()
    assert len(recommendations) >= 1, "Should get recommendations for spicy food lover"
    
    # Should have base compatibility scores
    base_scores_present = any("Base compatibility score" in rec["reasons"] for rec in recommendations)
    assert base_scores_present, "Fuzzy logic should provide base compatibility scores"


def test_halal_vegetarian_family_scenario():
    """
    SCENARIO: Family looking for halal and vegetarian options.
    """
    request_data = {
        "budget": 15.0,
        "cuisine": "Malay",
        "spiciness": 4,
        "is_halal": True,
        "is_vegetarian": True,
    }
    
    response = client.post("/recommend", json=request_data)
    assert response.status_code == 200
    
    recommendations = response.json()
    
    if recommendations:  # If we have matching dishes
        for rec in recommendations:
            dish = rec["dish"]
            reasons = rec["reasons"]
            
            # If dish is both halal and vegetarian, should have both bonuses
            if dish["is_halal"] and dish["is_vegetarian"]:
                assert "Is Halal" in reasons, "Should have halal bonus"
                assert "Is Vegetarian" in reasons, "Should have vegetarian bonus"
                
                # Score should be high with multiple bonuses
                assert rec["score"] > 3.0, "Score should be high with multiple bonuses"


def test_specific_cuisine_preference_scenario():
    """
    SCENARIO: User with strong cuisine preference.
    """
    cuisines_to_test = ["Chinese", "Indian", "Malay"]
    
    for cuisine in cuisines_to_test:
        request_data = {
            "budget": 10.0,
            "cuisine": cuisine,
            "spiciness": 5,
            "is_halal": False,
            "is_vegetarian": False,
        }
        
        response = client.post("/recommend", json=request_data)
        assert response.status_code == 200
        
        recommendations = response.json()
        
        if recommendations:  # If we have dishes of this cuisine
            for rec in recommendations:
                dish = rec["dish"]
                reasons = rec["reasons"]
                
                # Should match requested cuisine
                assert dish["cuisine"] == cuisine, f"Expected {cuisine} cuisine"
                
                # Should have cuisine bonus
                cuisine_bonus_present = any("cuisine" in r.lower() for r in reasons)
                assert cuisine_bonus_present, f"Should have cuisine bonus for {cuisine}"


def test_regression_roti_prata_scenario():
    """
    REGRESSION TEST: The exact scenario that revealed the original bug.
    """
    request_data = {
        "budget": 5,
        "cuisine": "Indian",
        "spiciness": 5,
        "is_halal": False,
        "is_vegetarian": False,
    }
    
    response = client.post("/recommend", json=request_data)
    assert response.status_code == 200
    
    recommendations = response.json()
    assert len(recommendations) >= 1, "Should get recommendations"
    
    # Look for Roti Prata specifically
    roti_prata_found = False
    for rec in recommendations:
        if "Roti Prata" in rec["dish"]["name"]:
            roti_prata_found = True
            
            # Should have both base score and cuisine bonus
            reasons = rec["reasons"]
            assert "Base compatibility score" in reasons, \
                "Roti Prata should have base fuzzy score"
            assert any("cuisine" in r.lower() for r in reasons), \
                "Roti Prata should have cuisine bonus"
            
            # Score should be reasonable 
            score = rec["score"]
            assert score > 1.5, f"Roti Prata score should be > 1.5, got {score}"
            break
    
    # Roti Prata should appear for this scenario
    assert roti_prata_found, "Roti Prata should be recommended for this scenario"


def test_edge_case_exact_budget_match():
    """
    SCENARIO: User budget exactly matches dish price.
    """
    # Look for dishes that cost exactly $5
    all_dishes_response = client.get("/dishes")
    assert all_dishes_response.status_code == 200
    
    all_dishes = all_dishes_response.json()
    five_dollar_dishes = [dish for dish in all_dishes if dish["price"] == 5.0]
    
    if five_dollar_dishes:  # If we have $5 dishes
        request_data = {
            "budget": 5.0,  # Exact match
            "cuisine": "any",
            "spiciness": 3,
            "is_halal": False,
            "is_vegetarian": False,
        }
        
        response = client.post("/recommend", json=request_data)
        assert response.status_code == 200
        
        recommendations = response.json()
        
        # Should include the $5 dishes
        recommended_prices = [rec["dish"]["price"] for rec in recommendations]
        assert 5.0 in recommended_prices, "Should include dishes that exactly match budget"


def test_multiple_preference_combinations():
    """
    STRESS TEST: Test many different preference combinations.
    """
    budgets = [3.0, 5.0, 10.0, 20.0]
    spiciness_levels = [1, 3, 5, 7, 9]
    cuisines = ["any", "Chinese", "Indian", "Malay"]
    
    successful_requests = 0
    total_requests = 0
    
    for budget in budgets:
        for spiciness in spiciness_levels:
            for cuisine in cuisines:
                request_data = {
                    "budget": budget,
                    "cuisine": cuisine,
                    "spiciness": spiciness,
                    "is_halal": False,
                    "is_vegetarian": False,
                }
                
                response = client.post("/recommend", json=request_data)
                total_requests += 1
                
                assert response.status_code == 200, \
                    f"Request failed for budget={budget}, spiciness={spiciness}, cuisine={cuisine}"
                
                recommendations = response.json()
                assert isinstance(recommendations, list), "Should return list"
                
                # If we get recommendations, they should be valid
                if recommendations:
                    successful_requests += 1
                    for rec in recommendations:
                        assert "dish" in rec, "Recommendation should have dish"
                        assert "score" in rec, "Recommendation should have score"
                        assert "reasons" in rec, "Recommendation should have reasons"
                        
                        # Score should be positive
                        assert rec["score"] > 0, "Score should be positive"
                        
                        # Dish price should not exceed budget
                        assert rec["dish"]["price"] <= budget, \
                            f"Dish price {rec['dish']['price']} exceeds budget {budget}"
    
    # At least some combinations should return recommendations
    success_rate = successful_requests / total_requests
    assert success_rate > 0.3, f"Success rate too low: {success_rate:.2%}"


def test_fuzzy_score_consistency_via_api():
    """
    INTEGRATION TEST: Ensure fuzzy scores are consistent via API.
    """
    request_data = {
        "budget": 8.0,
        "cuisine": "Chinese",
        "spiciness": 4,
        "is_halal": False,
        "is_vegetarian": False,
    }
    
    # Make the same request multiple times
    scores_for_same_dishes = {}
    
    for _ in range(3):  # Test 3 times
        response = client.post("/recommend", json=request_data)
        assert response.status_code == 200
        
        recommendations = response.json()
        
        for rec in recommendations:
            dish_name = rec["dish"]["name"]
            score = rec["score"]
            
            if dish_name in scores_for_same_dishes:
                # Score should be identical for same dish with same preferences
                previous_score = scores_for_same_dishes[dish_name]
                assert abs(score - previous_score) < 0.001, \
                    f"Score inconsistency for {dish_name}: {score} vs {previous_score}"
            else:
                scores_for_same_dishes[dish_name] = score


def test_no_recommendations_scenario():
    """
    SCENARIO: User preferences that result in no matches.
    
    Tests graceful handling when no dishes meet criteria.
    """
    request_data = {
        "budget": 1.0,  # Unrealistically low budget
        "cuisine": "any",
        "spiciness": 5,
        "is_halal": False,
        "is_vegetarian": False,
    }
    
    response = client.post("/recommend", json=request_data)
    assert response.status_code == 200
    
    recommendations = response.json()
    assert isinstance(recommendations, list), "Should return empty list, not error"


def test_high_budget_gourmet_scenario():
    """
    SCENARIO: Wealthy user looking for premium options.
    
    Tests high budget scenarios and premium dish recommendations.
    """
    request_data = {
        "budget": 50.0,  # High budget
        "cuisine": "any",
        "spiciness": 2,   # Mild preference (often associated with premium dining)
        "is_halal": False,
        "is_vegetarian": False,
    }
    
    response = client.post("/recommend", json=request_data)
    assert response.status_code == 200
    
    recommendations = response.json()
    
    if recommendations:
        # Should have base compatibility scores
        base_scores_present = any("Base compatibility score" in rec["reasons"] for rec in recommendations)
        assert base_scores_present, "Should have fuzzy logic base scores for high budget scenario"


def test_response_structure_validation():
    """
    VALIDATION TEST: Ensure API responses have correct structure.
    
    This catches structural issues in recommendations.
    """
    request_data = {
        "budget": 10.0,
        "cuisine": "any",
        "spiciness": 5,
        "is_halal": False,
        "is_vegetarian": False,
    }
    
    response = client.post("/recommend", json=request_data)
    assert response.status_code == 200
    
    recommendations = response.json()
    assert isinstance(recommendations, list), "Response should be a list"
    
    for rec in recommendations:
        # Check required fields
        assert "dish" in rec, "Missing dish field"
        assert "score" in rec, "Missing score field"
        assert "reasons" in rec, "Missing reasons field"
        
        # Check dish structure
        dish = rec["dish"]
        required_dish_fields = ["name", "price", "cuisine", "spiciness", "is_halal", "is_vegetarian"]
        for field in required_dish_fields:
            assert field in dish, f"Missing dish field: {field}"
        
        # Check data types
        assert isinstance(rec["score"], (int, float)), "Score should be numeric"
        assert isinstance(rec["reasons"], list), "Reasons should be a list"
        assert isinstance(dish["price"], (int, float)), "Price should be numeric"
        assert isinstance(dish["spiciness"], int), "Spiciness should be integer"
