from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.api import api_router
import uvicorn


app = FastAPI(
    title=settings.api_settings.TITLE,
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


def run():
    uvicorn.run(app, 
                host=settings.api_settings.HOST, 
                port=settings.api_settings.PORT
                )