# Singapore Makan Recommender

An AI-powered food recommendation system for Singapore cuisine, combining fuzzy logic and expert systems to provide personalized dining suggestions.

## Quick Start

1. **Install uv**: 
   ```bash
   pip install uv
   ```
   (See [Prerequisites](#prerequisites) for platform-specific instructions)

2. **Install dependencies**: 
   ```bash
   uv sync
   ```

3. **Run the server**: 
   ```bash
   uv run uvicorn backend.main:app --reload
   ```

4. **Open your browser to**: `http://127.0.0.1:8000/`

**Note**: If any command doesn't work, check the [Platform-Specific Setup](#platform-specific-setup) section and [Installation Troubleshooting](#installation-troubleshooting) for alternatives.

## What You Can Do

- **Get Personalized Recommendations**: Set your budget, cuisine preference, and spiciness tolerance
- **Filter by Diet**: Find Halal or Vegetarian options 
- **Budget-Conscious**: Get suggestions within your price range
- **Spice Level Control**: Adjust recommendations based on heat preference
- **Web & API Access**: Use the friendly web interface or integrate via REST API

## Features

- **Hybrid AI System**: Combines fuzzy logic for preference matching with expert system rules
- **Comprehensive Database**: 58 authentic Singapore dishes with detailed attributes
- **Dietary Preferences**: Supports halal, vegetarian, and cuisine-specific filtering
- **Smart Scoring**: Considers budget, spiciness tolerance, and personal preferences
- **Web Interface**: Clean, responsive frontend for easy interaction
- **RESTful API**: Well-documented FastAPI backend with automatic validation

## Prerequisites

### Python Requirements

This project requires Python 3.9 or higher. You can download it from [python.org](https://www.python.org/downloads/).

### Platform-Specific Setup

#### Windows

1. **Check if Python is installed:**
   ```cmd
   python --version
   ```
   If that doesn't work, try:
   ```cmd
   python3 --version
   ```
   Or:
   ```cmd
   py --version
   ```

2. **Install uv using pip:**
   ```cmd
   pip install uv
   ```
   If that doesn't work, try:
   ```cmd
   python -m pip install uv
   ```
   Or:
   ```cmd
   py -m pip install uv
   ```

3. **Verify uv installation:**
   ```cmd
   uv --version
   ```

#### macOS

1. **Check if Python is installed:**
   ```bash
   python3 --version
   ```
   Note: On macOS, use `python3` instead of `python` to avoid conflicts with the system Python 2.7.

2. **Install uv using pip:**
   ```bash
   pip3 install uv
   ```
   If you encounter permission issues, try:
   ```bash
   python3 -m pip install --user uv
   ```

3. **Verify uv installation:**
   ```bash
   uv --version
   ```

#### Linux

1. **Check if Python is installed:**
   ```bash
   python3 --version
   ```
   If Python is not installed, install it using your package manager:
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install python3 python3-pip
   
   # CentOS/RHEL/Fedora
   sudo yum install python3 python3-pip
   ```

2. **Install uv using pip:**
   ```bash
   pip3 install uv
   ```
   If you encounter permission issues, try:
   ```bash
   python3 -m pip install --user uv
   ```

3. **Verify uv installation:**
   ```bash
   uv --version
   ```

### Installation Verification

After installing uv, verify your setup by checking both Python and uv versions:

```bash
# Check Python version (use the command that worked for your platform)
python --version  # or python3 --version, or py --version

# Check uv version
uv --version
```

You should see:
- Python version 3.9 or higher
- uv version (latest available)

## Running the Application

### Step 1: Install Dependencies

Run the following command in your terminal/command prompt:

```bash
uv sync
```

**Verification:** You should see uv downloading and installing the required packages. The command should complete without errors.

### Step 2: Start the Server

Run the following command to start the FastAPI server:

```bash
uv run uvicorn backend.main:app --reload
```

**What to expect:** You should see output similar to:
```
INFO:     Will watch for changes in these directories: ['/path/to/sg-makan-recommender']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Access the Application

Once the server is running, the application will be available at:
- **Web Interface**: `http://127.0.0.1:8000/` (Main application)
- **API Documentation**: `http://127.0.0.1:8000/docs` (Swagger UI)
- **API Endpoints**: `http://127.0.0.1:8000/dishes` and `http://127.0.0.1:8000/recommend`

**Verification:** Open your web browser and navigate to `http://127.0.0.1:8000/`. You should see the Singapore Makan Recommender interface.

### Alternative Commands by Platform

If the standard commands don't work, try these platform-specific alternatives:

#### Windows
```cmd
# If uv command is not found, try:
python -m uv sync
python -m uv run uvicorn backend.main:app --reload

# Or with py launcher:
py -m uv sync
py -m uv run uvicorn backend.main:app --reload
```

#### macOS/Linux
```bash
# If uv command is not found, try:
python3 -m uv sync
python3 -m uv run uvicorn backend.main:app --reload
```

**That's it!** FastAPI now serves both the frontend and API.

## Installation Troubleshooting

### Common Python/pip Issues

#### "python is not recognized" or "command not found"
**Problem**: Python is not installed or not in your system PATH.

**Solutions**:
- **Windows**: Download Python from [python.org](https://www.python.org/downloads/) and ensure "Add to PATH" is checked during installation
- **macOS**: Install Python via [python.org](https://www.python.org/downloads/) or use Homebrew: `brew install python3`
- **Linux**: Install via package manager: `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (CentOS/RHEL)

#### "pip is not recognized" or command not found"
**Problem**: pip is not installed or not in your PATH.

**Solutions**:
```bash
# Try these alternatives:
python -m pip --version
python3 -m pip --version
py -m pip --version  # Windows only
```

If none work, install pip:
```bash
# Download get-pip.py and run:
python get-pip.py
# Or
python3 get-pip.py
```

#### Permission denied when installing uv
**Problem**: You don't have permission to install packages globally.

**Solutions**:
```bash
# Install for current user only:
pip install --user uv
python3 -m pip install --user uv

# Or use virtual environment (recommended):
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install uv
```

### uv-Specific Issues

#### "uv command not found" after installation
**Problem**: uv is installed but not in your PATH.

**Solutions**:
1. **Check if uv is installed**:
   ```bash
   python -m uv --version
   python3 -m uv --version
   py -m uv --version  # Windows
   ```

2. **Add to PATH** (if using --user installation):
   - **Windows**: Add `%APPDATA%\Python\Python3X\Scripts` to your PATH
   - **macOS/Linux**: Add `~/.local/bin` to your PATH

3. **Use full module path**:
   ```bash
   python -m uv sync
   python -m uv run uvicorn backend.main:app --reload
   ```

#### "uv sync" fails with dependency errors
**Problem**: Conflicting dependencies or network issues.

**Solutions**:
```bash
# Clear uv cache and retry
uv cache clean
uv sync

# Or force reinstall
uv sync --reinstall

# Check for connectivity issues
ping pypi.org
```

### Platform-Specific Issues

#### Windows: "Execution policy" errors
**Problem**: PowerShell execution policy prevents running scripts.

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS: "Developer Tools" required
**Problem**: Command line tools not installed.

**Solution**:
```bash
xcode-select --install
```

#### Linux: Missing system packages
**Problem**: System dependencies missing.

**Solutions**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-dev python3-pip build-essential

# CentOS/RHEL/Fedora
sudo yum install python3-devel python3-pip gcc
```

### Verification Steps

After troubleshooting, verify your setup:

1. **Check Python**:
   ```bash
   python --version  # Should show 3.9+
   # or
   python3 --version
   # or (Windows)
   py --version
   ```

2. **Check uv**:
   ```bash
   uv --version
   # or if uv command not found:
   python -m uv --version
   ```

3. **Test project setup**:
   ```bash
   # This should work without errors
   uv sync
   ```

If you continue having issues, please check the project's issue tracker or create a new issue with:
- Your operating system and version
- Python version (`python --version`)
- Complete error messages
- Steps you've already tried

## How It Works

### AI System Architecture

The recommendation engine uses a **hybrid approach** combining two AI techniques:

1. **Fuzzy Logic System**: 
   - Handles imprecise user preferences (budget, spiciness tolerance)
   - Uses triangular membership functions for natural language concepts
   - Provides base compatibility scores

2. **Expert System Rules**:
   - Applies domain-specific knowledge bonuses
   - Cuisine matching (+1 point)
   - Dietary preferences (Halal: +2, Vegetarian: +2)
   - Meal type matching (+5 points)

### Scoring Algorithm
```
Final Score = Fuzzy Logic Score + Expert System Bonuses
```

Example: A Malay dish that's Halal = Base Score + 1 (cuisine) + 2 (halal) = +3 bonus

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
sg-makan-recommender/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Data models
│   ├── database.py      # Database setup and seeding
│   ├── ai_system.py     # Fuzzy logic and expert system
│   └── fuzzy_config.json # Fuzzy logic configuration
├── frontend/
│   └── index.html       # Web interface
├── tests/
│   ├── conftest.py      # Test configuration
│   ├── test_api.py      # API endpoint tests
│   └── test_ai_system.py # AI system tests
├── pyproject.toml       # Project dependencies and configuration
├── uv.lock              # Dependency lock file
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