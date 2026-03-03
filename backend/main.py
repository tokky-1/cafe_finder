from fastapi import FastAPI

app = FastAPI(title= "Cafe finder",description="beginner project to help you find the cafe closet to you")

@app.get("/")
def root():
    return{"status":"ok"}

