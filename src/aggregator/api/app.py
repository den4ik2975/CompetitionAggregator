import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.aggregator.api.router import all_routers

app = FastAPI()

origins = [
    "https://ai.radolyn.com",
    "http://localhost:8000",
]

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="app:app", reload=True)
