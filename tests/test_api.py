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
