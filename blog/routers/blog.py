from fastapi import Depends, HTTPException, status, Response, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2

router = APIRouter(
    tags=['Blogs'],
    prefix="/blogs"
)

# Create blog
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlogResponse)
def create_blog(
    request: schemas.BlogModel,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=current_user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Update blog
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int,
    request: schemas.BlogModel,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user_id == current_user.id)
    blog = blog_query.first()
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found or not authorized")

    blog_query.update(request.dict()) # type: ignore
    db.commit()
    return {"message": "Blog updated successfully"}

# Get all blogs
@router.get("/", response_model=list[schemas.BlogResponse])
def get_all_blogs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    blogs = db.query(models.Blog).all()
    return blogs

# Get single blog
@router.get("/{id}", status_code=200, response_model=schemas.BlogResponse)
def get_blog(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id no. {id} does not exist")
    return blog

# Delete blog
@router.delete("/{id}")
def delete_blog(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.user_id == current_user.id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found or not authorized")

    db.delete(blog)
    db.commit()
    return {"message": f"Blog with id {id} deleted successfully"}
