# WorkoutAPI
This project is a FastAPI application for managing crossfit students, training categories and training centers. It provides endpoints for creating, retrieving, updating, and deleting athletes, categories, and training centers. Besides FastAPI, it was built using SQLAlchemy, Pydantic, Docker, Alembic and PostgreSQL.

## Requirements
- Python 3.12
- Docker

## Installation
1. Clone this repository:
```bash
git clone https://github.com/JoaoBarroso4/WorkoutAPI.git
```
2. Navigate to the project's root directory.
3. Install the required dependencies
```bash
pip install -r requirements.txt
```
4. Run docker-compose to start the Postgres container
```bash
docker-compose up -d
```
6. Run the application.

The server will start running at `http://localhost:3000`. Docs at `http://localhost:3000/docs`.

## Endpoints
### Athletes
- GET /atletas: List all athletes.
- POST /atletas: Register a new athlete.
- GET /atletas/{id}: Retrieve an athlete by ID.
- PATCH /atletas/{id}: Update an athlete's registration by ID.
- DELETE /atletas/{id}: Delete an athlete by ID.

### Categories
- GET /categorias: List all categories.
- POST /categorias: Register a new category.
- GET /categorias/{id}: Retrieve a category by ID.

### Training Centers
- GET /centros_treinamento: List all training centers.
- POST /centros_treinamento: Register a new training center.
- GET /centros_treinamento/{id}: Retrieve a training center by ID.
