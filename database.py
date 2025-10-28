from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Pour Vercel, utiliser PostgreSQL obligatoirement
if os.getenv("VERCEL"):
    if not DATABASE_URL or DATABASE_URL.startswith("sqlite"):
        # Utiliser une base de données temporaire en mémoire pour éviter l'erreur
        DATABASE_URL = "sqlite:///:memory:"
        print("⚠️ ATTENTION: Utilisation d'une base de données temporaire. Configurez DATABASE_URL avec PostgreSQL pour la production.")

# Pour SQLite (développement)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # Pour PostgreSQL (production)
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dépendance pour obtenir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
