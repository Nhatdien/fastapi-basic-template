
from models import models
from db import database
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from schemas.urls import UrlResponse
from starlette.responses import RedirectResponse


router = APIRouter(tags=["Shorten Url"])


def generate_array():
    return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", 
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z","A", "B", "C", "D",
            "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def encrypt_url(id: int) -> str:
    array = generate_array()
    base = len(array)
    encrypted_url = ""
    while id > 0:
        encrypted_url = array[id % base] + encrypted_url
        id //= base
    return encrypted_url

@router.get("/shorten_url/", response_model=UrlResponse)
def login(db: Session = Depends(database.get_db), short_url: str = None):
    db_url = db.query(models.Urls).filter(models.Urls.short_url == short_url).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="Url not found")
    return RedirectResponse(url=db_url.long_url, status_code=301)

@router.post("/shorten_url/", response_model=UrlResponse)
def login(db: Session = Depends(database.get_db), long_url: str = None):
    long_url_queried = db.query(models.Urls).filter(models.Urls.long_url == long_url).first()
    if long_url_queried is not None:
        return long_url_queried

    else:
        db_url = models.Urls(long_url=long_url, short_url='')
        db.add(db_url)
        db.commit()
        long_url_queried = db.query(models.Urls).filter(models.Urls.long_url == long_url).first()
        url_with_shortened = models.Urls(long_url=long_url, short_url=encrypt_url(long_url_queried.id))
        db.add(url_with_shortened)
        db.commit() 
        db.refresh(url_with_shortened)

        return url_with_shortened

    