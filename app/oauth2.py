from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from app.schemas import Token
from app.database import get_db
from app.models import User
from sqlalchemy.orm import Session

oauth2_schema=OAuth2PasswordBearer(tokenUrl='/login')
SECRET_KEY="secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credantials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        mail :str =payload.get("user_id")
        if mail is None:
            raise credantials_exception
        token_data=Token(mail=mail)
        return token_data
    except JWTError:
        raise credantials_exception
    
def get_current_user(token:str=Depends(oauth2_schema),db:Session=Depends(get_db)):
    credantials_exception= HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="kimlik doğrulanmadı",
            headers={"WWW-Authenticate": "Bearer"},
    )
    token_mail=verify_access_token(token=token,credantials_exception=credantials_exception).mail
    user= db.query(User).filter(User.email == token_mail).first()
    return user
