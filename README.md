# Singapore Makan Recommender

An AI-powered food recommendation system for Singapore cuisine, combining fuzzy logic and expert systems to provide personalized dining suggestions.

## Quick Start

1. Install dependencies: `uv sync`
2. Run the server: `uv run uvicorn backend.main:app --reload`
3. Open your browser to: `http://127.0.0.1:8000/`

## Features

- **Hybrid AI System**: Combines fuzzy logic for preference matching with expert system rules
- **Comprehensive Database**: 50+ authentic Singapore dishes with detailed attributes
- **Dietary Preferences**: Supports halal, vegetarian, and cuisine-specific filtering
- **Smart Scoring**: Considers budget, spiciness tolerance, and personal preferences
- **Web Interface**: Clean, responsive frontend for easy interaction
- **RESTful API**: Well-documented FastAPI backend with automatic validation

## Prerequisites

This project requires Python 3.9 or higher. You can download it from [python.org](https://www.python.org/downloads/).

This project requires `uv` to be installed. You can install it with the following command:

```bash
pip install uv
```

## Running the Application

1. **Install Dependencies:**
   ```bash
   uv sync
   ```

2. **Run the FastAPI Server:**
   ```bash
   uv run uvicorn backend.main:app --reload
   ```
   The server will start on port 8000. The application will be available at:
   - **Web Interface**: `http://127.0.0.1:8000/` (Main application)
   - **API Documentation**: `http://127.0.0.1:8000/docs` (Swagger UI)
   - **API Endpoints**: `http://127.0.0.1:8000/dishes` and `http://127.0.0.1:8000/recommend`

3. **That's it!** FastAPI now serves both the frontend and API.

## Troubleshooting

### Server Issues
- **Port already in use**: If port 8000 is busy, specify a different port:
  ```bash
  uv run uvicorn backend.main:app --reload --port 8001
  ```
  Then access the app at `http://127.0.0.1:8001/`

- **Dependencies not found**: Make sure you've run `uv sync` to install all dependencies

- **Database errors**: The SQLite database (`singapore_food.db`) is automatically created when the server starts if it doesn't exist. If you encounter issues:
  - Check if the file exists and has proper permissions
  - To reset the database, delete `singapore_food.db` and restart the server
  - The server will automatically detect and reuse existing databases

## Development & Quality Assurance

### Prerequisites

The development dependencies are automatically installed with:
```bash
uv sync
```

### Linting & Formatting

* **Check for linting errors:**
    ```bash
    uv run ruff check .
    ```
* **Automatically format the code:**
    ```bash
    uv run ruff format .
    ```

### Running Tests

* **Execute the automated test suite:**
    ```bash
    uv run pytest
    ```

* **Run tests with verbose output:**
    ```bash
    uv run pytest -v
    ```

## API Endpoints

- **GET `/dishes`** - Retrieve all available dishes
- **POST `/recommend`** - Get personalized recommendations based on preferences

### Example API Usage

```bash
# Get all dishes
curl http://127.0.0.1:8000/dishes

# Get recommendations
curl -X POST http://127.0.0.1:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 15.0,
    "cuisine": "Chinese",
    "spiciness": 4,
    "is_halal": false,
    "is_vegetarian": false
  }'
```

## Project Structure

```
sg-makan-recc/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Data models
│   ├── database.py      # Database setup and seeding
│   └── ai_system.py     # Fuzzy logic and expert system
├── frontend/
│   └── index.html       # Web interface
├── tests/
│   ├── test_api.py      # API endpoint tests
│   └── test_ai_system.py # AI system tests
└── singapore_food.db    # SQLite database (auto-generated)
```

## Technologies Used

- **Backend**: FastAPI, SQLModel, Uvicorn
- **AI/ML**: Experta (expert systems), fuzzy-expert (fuzzy logic)
- **Frontend**: AlpineJS, TailwindCSS
- **Database**: SQLite
- **Testing**: pytest
- **Code Quality**: Ruff (linting & formatting)
- **Package Management**: UV