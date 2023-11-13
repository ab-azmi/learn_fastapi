from app import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import engine, get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#Get all posts
# @router.get('/', response_model=List[schemas.ResponsePost])
@router.get('/', response_model=List[schemas.PostVote])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #only my posts
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    result = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return result

#Get a post
@router.get('/{id}',  response_model=schemas.PostVote)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found')

# #Create a new post
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponsePost)
async def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#Update a todo
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ResponsePost)
async def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_update = db.query(models.Post).filter(models.Post.id == id)

    if not post_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found')
    
    if post_update.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the owner of this post')

    post_update.update(post.model_dump())
    db.commit()
    db.refresh(post_update.first())

    return post_update.first()

#Delete a todo
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Data not found')
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not the owner of this post')
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
