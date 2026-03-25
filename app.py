from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, User

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.post("/create-user")
def create_user(name: str, email: str, age: int, sex: str):
    db = SessionLocal()

    new_user = User(
        name=name,
        email=email,
        age=age,
        sex=sex
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }