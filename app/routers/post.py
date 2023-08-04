from typing import List
from fastapi import Depends, HTTPException,status,APIRouter
from app import models
from app.database import SessionLocal, get_db
from app.enums import Tags
from app.oauth2 import get_current_user
from app.schemas import PostModel
from sqlalchemy.orm import Session

router = APIRouter(
    tags=[Tags.post]
)
@router.get("/posts",response_model=List[PostModel])
def get_posts(db: Session=Depends(get_db),get_current_user:str=Depends(get_current_user),
    skip:int=0,limit:int=10,search:str=""):
    # cursor.execute("Select * from posts")
    # posts=cursor.fetchall()
    posts=db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit=limit).offset(skip).all()
    return posts

@router.get("/posts/{id}")
def get_post(id:int,db:Session=Depends(get_db)):
    try:
        # sql="""Select * From posts Where id = %s """
        # cursor.execute(sql,(str(id),))
        # post=cursor.fetchone()
        post= db.query(models.Post).filter(models.Post.id==id).first()
        if not post:
            return {"message":f"{id} id'li post bulunamdı"}
    except:
        return {"message":"hata"}
    return post

@router.post("/posts",)
def create_post(post:PostModel,db:Session=Depends(get_db),get_current_user:str=Depends(get_current_user)):
    # sql="""Insert Into posts (title,content) Values (%s,%s) RETURNING *"""
    # cursor.execute(sql,(post.title,post.content))
    #post=cursor.fetchone()
    # connect.commit()
    new_post=models.Post(title=post.title,content=post.content,published=post.published,owner_id=get_current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/posts/{id}")
def update_post(id : int,post:PostModel,db:Session=Depends(get_db),get_current_user:str=Depends(get_current_user)):
    # sql="""Update posts set title=%s,content=%s,published=%s Where id = %s Returning *"""
    # cursor.execute(sql,(post.title,post.content,post.published,id))
    # new_post=cursor.fetchone()
    # connect.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    new_post=post_query.first()
    if new_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} sahip post bulunamadı")
    post_query.update(
        {"title":post.title,"content":post.content,"published":post.published},
    synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/posts/{id}",)
def delete_post(id : int,db:SessionLocal=Depends(get_db),get_current_user:str=Depends(get_current_user)):
    post= db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="böyle bir post yok")
    post.delete(synchronize_session=False)
    db.commit()
    return {"message":"silindi"}