from fastapi import FastAPI, HTTPException,Depends
from models.cafe import Cafe ,SpecificCafe
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.connect_DB import get_db
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

@app.get("/NEAR-ME",response_model=list[SpecificCafe])
def cafe_near_me(long:float,lat:float,radius:int = 2000,db:Session= Depends(get_db)):
    #This creates the 'reference pin' inside the query
    user_location = func.ST_SetSRID(func.ST_MakePoint(long, lat), 4326)

    # 1. Start the query on the Cafe model
    query = db.query(CafeDB)

    # 2. Apply the Spatial Filter
    query = query.filter(func.ST_DWithin(
                            CafeDB.location, 
                            user_location, 
                            radius))

    # 3. Sort by Distance (Closest first)
    query = query.order_by(func.ST_Distance(
                            CafeDB.location, 
                            user_location))

    # 4. Execute the query
    cafes = query.all()

    return cafes