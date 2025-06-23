from fastapi import Depends, HTTPException, status, Response, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

from .. import models, schemas
from ..hashing import Hash

router = APIRouter( 
                    tags=['Users'] ,
                    prefix="/user"
                                    
                                    
                                    )

@router.post("/create", response_model=schemas.UserResponse,)
def create_user(request: schemas.UserModel, db : Session=Depends(get_db)):
    
    user = models.User(username=request.username, email=request.email, password=Hash.get_password_hash(request.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/", response_model = list[schemas.UserResponse])
def get_all_users(db : Session=Depends(get_db)):

    return db.query(models.User).filter().all()

@router.get("/{id}", status_code=200,response_model=schemas.UserResponse)
def get_user(id: int, db : Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
    