from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import schemas, models, database, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

    query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already voted on this post")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote created"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        
        query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted"}