from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers.login import router as loginRouter
from .routers.blog import router as blogRouter
from .routers.user import router as userRouter

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(loginRouter)
app.include_router(blogRouter)
app.include_router(userRouter)


@app.get("/")
def read_root():
    return {"Hello": "World"}


