#!/usr/bin/env python3
"""
Script de démarrage pour l'e-commerce Python
"""

import subprocess
import sys
import os

def install_requirements():
    """Installer les dépendances"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation des dépendances: {e}")
        return False

def seed_database():
    """Initialiser la base de données avec des données de test"""
    print("🌱 Initialisation de la base de données...")
    try:
        subprocess.check_call([sys.executable, "seed_data.py"])
        print("✅ Base de données initialisée")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        return False

def start_server():
    """Démarrer le serveur"""
    print("🚀 Démarrage du serveur...")
    print("📍 Site web: http://localhost:8000")
    print("📚 Documentation API: http://localhost:8000/docs")
    print("👤 Compte de test: admin@ecommerce.com / admin123")
    print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur")
    
    try:
        subprocess.check_call([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")

def main():
    """Fonction principale"""
    print("🛒 E-commerce Python - Script de démarrage")
    print("=" * 50)
    
    # Vérifier si on est dans le bon répertoire
    if not os.path.exists("main.py"):
        print("❌ Erreur: main.py non trouvé. Assurez-vous d'être dans le bon répertoire.")
        sys.exit(1)
    
    # Installer les dépendances
    if not install_requirements():
        sys.exit(1)
    
    # Initialiser la base de données
    if not seed_database():
        print("⚠️  Avertissement: Impossible d'initialiser la base de données")
        print("   Vous pouvez continuer, mais il n'y aura pas de données de test")
    
    # Démarrer le serveur
    start_server()

if __name__ == "__main__":
    main()
