from fastapi import FastAPI
from api.routers import api_router

app = FastAPI(title="WorkoutAPI")
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level="info", reload=True)
