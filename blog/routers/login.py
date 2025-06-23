from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, database, hashing, token

router = APIRouter(prefix="/Login", tags=["Login"])

@router.post("/",response_model=schemas.Token)
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if not user or not hashing.Hash.verify(request.password, user.password):  # type: ignore
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    access_token = token.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
