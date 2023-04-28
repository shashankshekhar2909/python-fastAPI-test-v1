from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import ValidationError
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine, User

app = FastAPI()

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True 

class UserUpdate(BaseModel):
    name: str
    email: str
    password: str

class UserDelete(BaseModel):
    id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        user = User(id=1, name="John Doe", email="jdoe@example.com", password="password")
        user_read = UserRead.from_orm(user)
    except ValidationError as e:
        print(f"Validation error: {e}")
        for error in e.errors():
            print(error["loc"], error["msg"])
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=UserDelete)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id)
