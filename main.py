from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import products, auth, users, categories  # ← categories যোগ করো

app = FastAPI(
    title="SmartWear API",
    description="SmartWear E-Commerce এর Backend API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers যোগ করুন
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)  # ← এই লাইনটা যোগ করো

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "স্বাগতম SmartWear API তে! 👕",
        "docs": "http://localhost:8000/docs"
    }