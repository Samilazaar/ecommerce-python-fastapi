from sqlalchemy.orm import Session
from sqlalchemy import and_
import models
import schemas
from typing import List, Optional

# CRUD pour les utilisateurs
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# CRUD pour les produits
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).filter(models.Product.is_active == True).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_stock(db: Session, product_id: int, quantity: int):
    product = get_product(db, product_id)
    if product:
        product.stock_quantity -= quantity
        db.commit()
        db.refresh(product)
    return product

# CRUD pour le panier
def get_user_cart(db: Session, user_id: int):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1):
    # Vérifier si l'article existe déjà dans le panier
    existing_item = db.query(models.CartItem).filter(
        and_(models.CartItem.user_id == user_id, models.CartItem.product_id == product_id)
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Créer un nouvel article dans le panier
        cart_item = models.CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

def remove_from_cart(db: Session, item_id: int, user_id: int):
    cart_item = db.query(models.CartItem).filter(
        and_(models.CartItem.id == item_id, models.CartItem.user_id == user_id)
    ).first()
    
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return {"message": "Article supprimé du panier"}
    return {"message": "Article non trouvé"}

def clear_cart(db: Session, user_id: int):
    db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()
    return {"message": "Panier vidé"}

# CRUD pour les commandes
def create_order_from_cart(db: Session, user_id: int):
    # Récupérer les articles du panier
    cart_items = get_user_cart(db, user_id)
    
    if not cart_items:
        return {"message": "Panier vide"}
    
    # Calculer le total
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    # Créer la commande
    order = models.Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Créer les articles de commande et mettre à jour le stock
    for cart_item in cart_items:
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.add(order_item)
        
        # Mettre à jour le stock
        update_product_stock(db, cart_item.product_id, cart_item.quantity)
    
    # Vider le panier
    clear_cart(db, user_id)
    
    db.commit()
    return order

def get_user_orders(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()
