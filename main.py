import uvicorn

from src.setup import setup_fastapi, setup_logging

if __name__ == "__main__":
    app_fastapi = setup_fastapi()


    @app_fastapi.on_event("startup")
    async def startup_event():
        setup_logging()


    uvicorn.run(app_fastapi)
