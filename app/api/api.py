from fastapi import APIRouter

from app.api.endpoints import container

api_router = APIRouter()
api_router.include_router(container.router, prefix='/containers', tags=['Container'])