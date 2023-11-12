from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Secret Key
#Algorithm
#Access Token Expiration

SECRET_KEY = "6fe150f181e108c6ab13b7aea7549657afa0baf2e9572c7cb02c3fd2fdcf9046"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credeintals_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credeintals_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credeintals_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user