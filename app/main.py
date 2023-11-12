from fastapi import FastAPI
from app.routers import user, post, auth
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

if '__name__' == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
