# About
An AI-driven Resoursce and Profile Management Application. The aim of this application is to streamline the candidate reviewing process. A place where the recruiters can login and review a candidates profile instead of mannually sifting through the CV/resume files.  

## Project Structure  

A guide for understanding the project structure.

```python
|
|--- frontend # This is where the code for the frontend lives
|--- profile_app # This is where the code for the backend lives 
  |--- models # database models that works as request and response types as well
  |--- routers # API endpoints 
  |--- database # database repository classes
  |--- config.py # configurations for setup
  |--- app.py # starting point of the application
```

# Installation Guide

### Prerequisites

- Install Ollama and pull the `llama3.2:3b` model locally:

```bash
ollama pull llama3.2:3b
```

- Git (to clone repositories)
- Python 3.10 or newer (backend)
- Node.js and npm (frontend)
- An IDE or code editor (e.g. Visual Studio Code)
- Access credentials for external services (e.g. MongoDB connection URI)

### Setting up the Backend (Python)

1. Clone the repository:

```bash
git clone https://github.com/Bhavyakajani/AI-Profile-Application.git
cd profile-llama
```

2. Create and activate a virtual environment:

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Create a `.env` file in the project root and add the following variables (example):

```env
# Select active environment
ENV_STATE="dev"  # dev | test | prod

# Development environment
DEV_SECRET_KEY="dev-secret-key"
DEV_MONGODB_URI="YOUR_MONGO_URI"
DEV_DB_NAME="ProfileDB_DEV"
DEV_MONGO_HOST="YOUR_MONGODB_HOST"
DEV_MONGO_PORT="YOUR_MONGODB_PORT"

# Production environment
PROD_SECRET_KEY="prod-secret-key"
PROD_MONGODB_URI="YOUR_PROD_MONGO_URI"
PROD_DB_NAME="ProfileDB_PROD"
```

4. Install Python requirements:

```bash
pip install -r requirements-dev.txt
```

5. Install Tesseract OCR on your system and ensure the `tesseract` binary is available in your PATH.

6. Ensure the Ollama service is running before starting the backend:

```bash
ollama run llama3.2:3b
```

7. Run the backend server (development):

```bash
uvicorn profile_app.app:app --reload
```

The backend will be available at: http://127.0.0.1:8000
SwaggerUI: http://127.0.0.1:8000/docs

### Setting up the Frontend (React)

1. Open a new terminal and navigate to the frontend folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend will run at: http://localhost:5173

---
