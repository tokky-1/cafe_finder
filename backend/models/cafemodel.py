from sqlalchemy import  Column, Integer, String, Float
from geoalchemy2 import Geography
from database.connect_DB import  Base
# 2. Define the Cafe Model


class CafeDB(Base):
    __tablename__ = "list_of_cafes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    # '4326' is the standard WGS 84 coordinate system (used by GPS/Google Maps)
    location = Column(Geography(geometry_type='POINT', srid=4326))
