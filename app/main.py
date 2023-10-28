from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
import models
import schemas
from database import engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

#Get all posts
@app.get('/posts', response_model=List[schemas.ResponsePost])
async def get_porsts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#Get a post
@app.get('/posts/{id}',  response_model=schemas.ResponsePost)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found')

# #Create a new post
@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
async def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#Update a todo
@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResponsePost)
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    post_update = db.query(models.Post).filter(models.Post.id == id)

    if not post_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found')
    
    post_update.update(post.model_dump())
    db.commit()
    db.refresh(post_update.first())

    return post_update.first()

#Delete a todo
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found')
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    #get data from user schema, dump it to model, then pass it to db
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
