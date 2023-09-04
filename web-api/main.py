from fastapi import FastAPI

from logger import logging
from api import api_route

app = FastAPI()

app.mount('/api/v1/', app=api_route, name='api')

@app.get("/")
async def root():
    return {"message": "Please use /api/v1/docs for more information"}
