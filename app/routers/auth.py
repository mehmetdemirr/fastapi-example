from fastapi import APIRouter,Depends,HTTPException,status
from app.enums import Tags
from app.schemas import InUserModel,UserModel
from app.models import User
from app.utily import verifiy
from app.database import get_db
from sqlalchemy.orm import Session
from app.oauth2 import create_access_token,get_current_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router =APIRouter(
    tags=[Tags.auth]
)

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user_control=db.query(User).filter(User.email== user_credentials.username).first()
    if not user_control:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="şifre veya email hatalı")
    # if not verifiy(user.password,User.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="şifre veya email hatalı")
    token=create_access_token(data={"user_id":user_credentials.username})
    user =get_current_user(token=token,db=db)
    
    return token

