from fastapi import FastAPI
from api import common_router

app = FastAPI()
app.include_router(common_router)