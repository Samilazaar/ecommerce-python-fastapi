from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from database import get_db, engine
import models
import schemas
import crud
from auth import get_current_user, create_access_token, verify_password, get_password_hash
from datetime import datetime, timedelta
import uvicorn

# Créer les tables de base de données
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Base de données initialisée avec succès")
except Exception as e:
    print(f"⚠️ Erreur lors de l'initialisation de la base de données: {e}")
    print("Le site fonctionnera en mode dégradé (sans persistance des données)")

app = FastAPI(title="E-commerce Python", version="1.0.0")

# Configuration des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuration de sécurité
security = HTTPBearer()

# Page d'accueil
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Page de statut pour debug
@app.get("/status")
async def status():
    return {
        "status": "ok",
        "database": "connected" if DATABASE_URL else "not configured",
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# API Routes
@app.get("/api/products")
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer tous les produits"""
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/api/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Récupérer un produit par ID"""
    product = crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

@app.post("/api/products")
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Créer un nouveau produit (nécessite authentification)"""
    return crud.create_product(db=db, product=product)

@app.post("/api/auth/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Inscription d'un nouvel utilisateur"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    db_user = crud.create_user(db, schemas.UserCreate(**user_data))
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Connexion utilisateur"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/cart")
async def get_cart(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Récupérer le panier de l'utilisateur"""
    return crud.get_user_cart(db, current_user.id)

@app.post("/api/cart/add")
async def add_to_cart(
    product_id: int, 
    quantity: int = 1,
    current_user: schemas.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Ajouter un produit au panier"""
    return crud.add_to_cart(db, current_user.id, product_id, quantity)

@app.delete("/api/cart/remove/{item_id}")
async def remove_from_cart(
    item_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprimer un article du panier"""
    return crud.remove_from_cart(db, item_id, current_user.id)

@app.post("/api/orders")
async def create_order(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Créer une commande à partir du panier"""
    return crud.create_order_from_cart(db, current_user.id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
