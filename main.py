import multiprocessing
import uvicorn

from src.setup import setup_fastapi, setup_rocketry, setup_logging
import multiprocessing

import uvicorn

from src.setup import setup_fastapi, setup_rocketry, setup_logging

if __name__ == "__main__":
    app_fastapi = setup_fastapi()  # setup

    @app_fastapi.on_event("startup")
    async def startup_event():
        setup_logging()
        rocketry_process = multiprocessing.Process(target=setup_rocketry)
        rocketry_process.start()


    uvicorn.run(app_fastapi, port=8001)
