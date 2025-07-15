import os
import sys

import pytest

# Add the parent directory to Python path so we can import backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import DATABASE_URL, create_db_and_tables, seed_database


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    # Create the database and tables
    create_db_and_tables()
    # Seed the database
    seed_database()
    yield
    # Teardown the database
    import os

    os.remove(DATABASE_URL.replace("sqlite:///", ""))
