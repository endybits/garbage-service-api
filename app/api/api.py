from fastapi import APIRouter

from app.api.endpoints import container, routes

api_router = APIRouter()
api_router.include_router(container.router, prefix='/containers', tags=['Container'])
api_router.include_router(routes.router, prefix='/routes', tags=['Routes'])