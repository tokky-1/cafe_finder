import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker,  declarative_base
from geoalchemy2 import Geography
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from dotenv import load_dotenv
import os

# 1. Database Connection
load_dotenv(override=True)
DB_URL = os.getenv("DATABASE_URL")
if DB_URL is None:
    raise ImportError("DB_URL not found. Please check your .env file.")
engine = create_engine(DB_URL,echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 2. Define the Cafe Model
class Cafe(Base):
    __tablename__ = "list_of_cafes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    # '4326' is the standard WGS 84 coordinate system (used by GPS/Google Maps)
    location = Column(Geography(geometry_type='POINT', srid=4326))

# Create the table in Postgres
Base.metadata.create_all(engine)

def seed_cafes(csv_file_path):
    df = pd.read_csv(csv_file_path)
    db = SessionLocal()
    
    try:
        for index, row in df.iterrows():
            # Create a Point object (longitude comes first in GeoJSON/PostGIS standards!)
            point = Point(row['lng'], row['lat'])
            
            new_cafe = Cafe(
                name=row['name'],
                address=row['address'],
                # Convert the Shapely point to a format PostGIS understands
                location=from_shape(point, srid=4326),
                phone=row['phone'],
            )
            db.add(new_cafe)
        
        db.commit()
        print(f"Successfully imported {len(df)} cafes!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_cafes("backend/original/abuja_cafes.csv")