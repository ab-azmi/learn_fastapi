from fastapi import FastAPI
from app import models
from app.routers import user, post, auth, vote
import uvicorn
from app.config import settings
from app.database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

if '__name__' == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
