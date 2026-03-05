import pandas as pd
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from connect_DB import engine,sessionlocal, Base
from models.cafemodel import CafeDB

# Create the table in Postgres
Base.metadata.create_all(engine)

def seed_cafes(csv_file_path):
    df = pd.read_csv(csv_file_path)
    db = sessionlocal()
    
    try:
        for index, row in df.iterrows():
            # Create a Point object (longitude comes first in GeoJSON/PostGIS standards!)
            point = Point(row['lng'], row['lat'])
            
            new_cafe = CafeDB(
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
    seed_cafes("backend/database/abuja_cafes.csv")