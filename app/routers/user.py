from app import models, schemas, utils
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db, engine

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

#Register a user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    #hashing password
    user.password = utils.hash(user.password)

    #get data from user schema, dump it to model, then pass it to db
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#Get user by id
@router.get('/{id}', response_model=schemas.ResponseUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User doesnt exist")
    return user