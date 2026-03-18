from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ===== CATEGORY SCHEMAS =====
class CategoryCreate(BaseModel):
    name: str
    slug: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True


# ===== PRODUCT SCHEMAS =====
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    image_url: Optional[str] = None
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    image_url: Optional[str]
    is_active: bool
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ===== USER SCHEMAS =====
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ===== AUTH SCHEMAS =====
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ===== ORDER SCHEMAS =====
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    address: str
    items: list[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    address: str
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True