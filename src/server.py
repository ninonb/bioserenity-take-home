from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
import os
from dotenv import load_dotenv

from models import Event, Token
from auth import authenticate_user, create_access_token

load_dotenv("../.env")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

client = MongoClient(MONGO_URI)
db = client["event_manager"]
events_collection = db["events"]
users_collection = db["users"]


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/add_event")
async def add_event(event: Event, token: str = Depends(oauth2_scheme)):
    events_collection.insert_one(event.dict())
    return {"message": "Event added successfully"}


@app.get("/list_events")
async def list_events(token: str = Depends(oauth2_scheme)):
    events = list(events_collection.find({}, {"_id": 0}))
    return events


@app.post("/remove_events")
async def remove_events(event: Event, token: str = Depends(oauth2_scheme)):
    result = events_collection.delete_many(event.dict())
    return {"deleted_count": result.deleted_count}
