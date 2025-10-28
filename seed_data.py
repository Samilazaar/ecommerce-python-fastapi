#!/usr/bin/env python3
"""
Script pour ajouter des données de test à la base de données
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

def create_sample_products():
    """Créer des produits d'exemple"""
    db = SessionLocal()
    
    # Vérifier si des produits existent déjà
    if db.query(models.Product).first():
        print("Des produits existent déjà dans la base de données.")
        db.close()
        return
    
    sample_products = [
        {
            "name": "Laptop Gaming Pro",
            "description": "Ordinateur portable haute performance pour le gaming",
            "price": 1299.99,
            "stock_quantity": 10,
            "category": "Informatique",
            "image_url": "/static/images/laptop.jpg"
        },
        {
            "name": "Smartphone Android",
            "description": "Smartphone dernière génération avec caméra 108MP",
            "price": 699.99,
            "stock_quantity": 25,
            "category": "Téléphonie",
            "image_url": "/static/images/smartphone.jpg"
        },
        {
            "name": "Casque Bluetooth",
            "description": "Casque sans fil avec réduction de bruit active",
            "price": 199.99,
            "stock_quantity": 50,
            "category": "Audio",
            "image_url": "/static/images/headphones.jpg"
        },
        {
            "name": "Montre Connectée",
            "description": "Montre intelligente avec suivi de santé",
            "price": 299.99,
            "stock_quantity": 30,
            "category": "Wearables",
            "image_url": "/static/images/smartwatch.jpg"
        },
        {
            "name": "Tablette Graphique",
            "description": "Tablette pour dessin numérique et design",
            "price": 449.99,
            "stock_quantity": 15,
            "category": "Informatique",
            "image_url": "/static/images/tablet.jpg"
        },
        {
            "name": "Enceinte Bluetooth",
            "description": "Enceinte portable avec son stéréo",
            "price": 89.99,
            "stock_quantity": 40,
            "category": "Audio",
            "image_url": "/static/images/speaker.jpg"
        }
    ]
    
    for product_data in sample_products:
        product = models.Product(**product_data)
        db.add(product)
    
    db.commit()
    print(f"✅ {len(sample_products)} produits ajoutés à la base de données")
    db.close()

def create_sample_user():
    """Créer un utilisateur de test"""
    from auth import get_password_hash
    
    db = SessionLocal()
    
    # Vérifier si un utilisateur existe déjà
    if db.query(models.User).first():
        print("Des utilisateurs existent déjà dans la base de données.")
        db.close()
        return
    
    user_data = {
        "email": "admin@ecommerce.com",
        "password": get_password_hash("admin123"),
        "first_name": "Admin",
        "last_name": "E-commerce"
    }
    
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    print("✅ Utilisateur admin créé (email: admin@ecommerce.com, mot de passe: admin123)")
    db.close()

if __name__ == "__main__":
    print("🌱 Ajout de données de test...")
    
    # Créer les tables
    models.Base.metadata.create_all(bind=engine)
    print("✅ Tables de base de données créées")
    
    # Ajouter les données de test
    create_sample_products()
    create_sample_user()
    
    print("🎉 Données de test ajoutées avec succès !")
    print("\n📝 Informations de connexion:")
    print("   Email: admin@ecommerce.com")
    print("   Mot de passe: admin123")
