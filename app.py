from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, User
import logging
import os

# Ensure logs directory exists
log_dir = "/home/ubuntu/API/logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=f"{log_dir}/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.post("/create-user")
def create_user(name: str, email: str, age: int, sex: str):
    db = SessionLocal()

    logger.info(f"Creating user: {name}, {email}, {age}, {sex}")

    new_user = User(
        name=name,
        email=email,
        age=age,
        sex=sex
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"User created successfully with ID: {new_user.id}")

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }