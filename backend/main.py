from fastapi import FastAPI, HTTPException,Depends
from models.cafe import Cafe ,SpecificCafe
from sqlalchemy.orm import Session
from database.connect_DB import get_db,engine
from models.cafemodel import CafeDB
app = FastAPI(title= "Cafe finder",description="beginner project to help you find the cafe closet to you")

@app.get("/")
def root():
    return{"status":"ok"}

@app.get("/GET-ALL-CAFES",response_model=list[SpecificCafe])
def get_all(db:Session= Depends(get_db)):
    cafes = db.query(CafeDB).all()
    return cafes


@app.get("/RETURN-CAFEBYID",response_model=Cafe)
def return_cafebyid(id:int,db:Session= Depends(get_db)):
    cafe = db.query(CafeDB).filter(CafeDB.id == id).first()
    if not cafe:
        raise HTTPException(status_code=404,detail="Cafe Not in Dataset") 
    return cafe