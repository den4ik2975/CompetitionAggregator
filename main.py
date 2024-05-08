import uvicorn

from src.setup import get_fastapi_app

if __name__ == "__main__":
    app_fastapi = get_fastapi_app()
    uvicorn.run(app_fastapi)
