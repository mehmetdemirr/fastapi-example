from typing import List
from fastapi import Depends, HTTPException,status,APIRouter
from app import models
from app.utily import hash
from app.database import get_db
from app.enums import Tags
from app.schemas import InUserModel, UserModel
from sqlalchemy.orm import Session

router=APIRouter(
    tags=[Tags.user],
)

@router.get("/users",response_model=List[UserModel])
def get_users(db: Session=Depends(get_db)):
    users=db.query(models.User).all()
    user_models = [UserModel(email=user.email) for user in users]
    return user_models

@router.get("/users/{id}",response_model=UserModel)
def get_user(id:int,db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":f"{id} id'li user bulunamdı"})
    return user

@router.post("/users",response_model=UserModel)
def create_user(user:InUserModel,db:Session=Depends(get_db)):
    hashed_password=hash(user.password)
    user.password=hashed_password
    user_control= db.query(models.User).filter(models.User.email==user.email).first()
    if user_control:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="e posta zaten kayıtlı")
    new_user=models.User(email=user.email,password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{id}",response_model=UserModel)
def update_user(id : int,user:InUserModel,db:Session=Depends(get_db)):
    user_query=db.query(models.User).filter(models.User.id==id)
    user_mail_control=db.query(models.User).filter(models.User.email==user.email).first()
    if user_mail_control:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{user.email} sahip bir kullanıcı var")
    new_user=user_query.first()
    if new_user== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} sahip post bulunamadı")
    
    user_query.update(
        {"email":user.email,"password":hash(user.password)},
    synchronize_session=False)
    db.commit()
    return user_query.first()

@router.delete("/users/{id}",)
def delete_user(id : int,db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="böyle bir kullanıcı yok")
    user.delete(synchronize_session=False)
    db.commit()
    return {"message":"silindi"}
        

