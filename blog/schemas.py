from pydantic import BaseModel


class BlogModel(BaseModel):
    title: str
    body: str
    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str
    email: str
    password: str  # required for registration

class UserResponse(BaseModel):
    email: str
    username: str
    blogs: list[BlogModel]
    class Config:
        from_attributes = True        


class UserBlog(BaseModel):
    email: str
    username: str
    class Config:
        from_attributes = True        

        
class BlogResponse(BlogModel):
    title: str
    body: str
    creator: UserBlog
    class Config:
        from_attributes = True        

class LoginModel(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
