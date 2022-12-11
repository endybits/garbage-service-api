# Python
import json
from typing import List

# External Resources
from fastapi import FastAPI
from fastapi import Body, Path
from fastapi import status

# Local modules
from app.api.api import api_router

app = FastAPI()

app.include_router(api_router)

@app.get(path='/', status_code=status.HTTP_200_OK)
async def home():
    return {'message': 'Hi, this is the incredible service project\'s home page'}