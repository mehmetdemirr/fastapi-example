from fastapi import FastAPI
from . import models
from .database import engine
from app.routers import post,user,auth
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username:str="postgres"
    database_password:str="12345678"
    secret_key:str="secret_key"

models.Base.metadata.create_all(bind=engine)

app =FastAPI()

app.include_router(post.router,prefix="/api")
app.include_router(user.router,prefix="/api")
app.include_router(auth.router,prefix="/api")
