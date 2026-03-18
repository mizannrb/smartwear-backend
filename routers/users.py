from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserResponse
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import os

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Token থেকে current user বের করো
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User পাওয়া যায়নি")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token অবৈধ")

# আমার profile দেখো
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# আমার profile আপডেট করো
@router.put("/me", response_model=UserResponse)
def update_me(data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if "name" in data:
        current_user.name = data["name"]
    if "phone" in data:
        current_user.phone = data["phone"]
    if "address" in data:
        current_user.address = data["address"]
    db.commit()
    db.refresh(current_user)
    return current_user

# পাসওয়ার্ড পরিবর্তন করো
@router.put("/me/password")
def change_password(data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not pwd_context.verify(data.get("old_password"), current_user.password):
        raise HTTPException(status_code=400, detail="পুরনো পাসওয়ার্ড সঠিক নয়")
    current_user.password = pwd_context.hash(data.get("new_password"))
    db.commit()
    return {"message": "পাসওয়ার্ড পরিবর্তন হয়েছে"}

# সব users দেখো (admin)
@router.get("/", response_model=list[UserResponse])
def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access প্রয়োজন")
    return db.query(User).all()

# একটা user দেখো
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User পাওয়া যায়নি")
    return user

# user আপডেট (admin)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access প্রয়োজন")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User পাওয়া যায়নি")
    for key, value in data.items():
        if hasattr(user, key) and key != "password":
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# user মুছো (admin)
@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access প্রয়োজন")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User পাওয়া যায়নি")
    db.delete(user)
    db.commit()
    return {"message": "User মুছে ফেলা হয়েছে"}