from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# সব category দেখো
@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

# নতুন category তৈরি করো
@router.post("/", response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    # slug already আছে কিনা চেক করো
    existing = db.query(models.Category).filter(models.Category.slug == category.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="এই slug আগে থেকেই আছে")
    
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# একটি category দেখো
@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category পাওয়া যায়নি")
    return category

# category আপডেট করো
@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category পাওয়া যায়নি")
    
    db_category.name = category.name
    db_category.slug = category.slug
    db.commit()
    db.refresh(db_category)
    return db_category

# category মুছে ফেলো
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category পাওয়া যায়নি")
    
    db.delete(db_category)
    db.commit()
    return {"message": "Category মুছে ফেলা হয়েছে"}
