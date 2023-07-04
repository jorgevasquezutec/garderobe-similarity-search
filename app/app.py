from fastapi import FastAPI,Request, Response
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.api import api_router
import uvicorn
from app.config.database import collection
from bson import json_util
import asyncio
from typing import Callable



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


class CustomRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = asyncio.Lock()

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            await self.lock.acquire()
            response: Response = await original_route_handler(request)
            self.lock.release()
            return response

        return custom_route_handler

#locking
#optimistic locking
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de recomendaciones de ropa"}
    # document = collection.find_one()
    # if document:
    # #get correlativo e updatear
    #     value = document.get("value")
    #     if value is None:
    #         value = 0
    #     value += 1
    #     collection.update_one(
    #         {"_id": document.get("_id")},
    #         {"$set": {"value": value}}
    #     )
    #     document = collection.find_one()
    #     json_doc = json_util.dumps(document)
    #     return json_doc
    # else:
    #     #crear documento
    #     document = {
    #         "value": 0
    #     }
    #     collection.insert_one(document)
    #     json_doc = json_util.dumps(document)


        

app.include_router(api_router, prefix="/api")
# app.router.route_class = CustomRoute


def run():
    uvicorn.run(app, 
                host=settings.api_settings.HOST, 
                port=settings.api_settings.PORT
                )