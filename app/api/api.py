from fastapi import APIRouter

from app.api.similarity.router import router as similarity_router
from app.api.auth.router import router as auth_router

api_router = APIRouter()
api_router.include_router(similarity_router, prefix="/similarity", tags=["similarity"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

