# 🛒 E-commerce Python avec FastAPI

Un site e-commerce moderne développé avec Python, FastAPI et SQLAlchemy, prêt pour le déploiement sur diverses plateformes cloud.

## ✨ Fonctionnalités

- **Backend moderne** : FastAPI avec documentation automatique
- **Base de données** : SQLAlchemy avec support SQLite/PostgreSQL
- **Authentification** : JWT avec hashage sécurisé des mots de passe
- **Interface web** : Design responsive avec Bootstrap 5
- **API REST** : Endpoints complets pour produits, panier, commandes
- **Déploiement** : Configuration Docker et support cloud

## 🚀 Démarrage rapide

### Prérequis

- Python 3.11+
- pip (gestionnaire de paquets Python)

### Installation locale

1. **Cloner le projet**

```bash
git clone <votre-repo>
cd "Projet e-commerce python"
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Initialiser la base de données**

```bash
python seed_data.py
```

4. **Lancer le serveur**

```bash
python main.py
```

5. **Accéder à l'application**

- Site web : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- Compte de test : admin@ecommerce.com / admin123

## 🐳 Déploiement avec Docker

### Développement local avec Docker

```bash
# Lancer avec Docker Compose
docker-compose up --build

# Accéder à l'application
# Site web : http://localhost
# Base de données : localhost:5432
```

### Production avec Docker

```bash
# Construire l'image
docker build -t ecommerce-python .

# Lancer le conteneur
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:pass@host:5432/db ecommerce-python
```

## ☁️ Déploiement sur le cloud

### Option 1 : Heroku (Gratuit)

1. **Installer Heroku CLI**

```bash
# macOS
brew install heroku/brew/heroku

# Ou télécharger depuis https://devcenter.heroku.com/articles/heroku-cli
```

2. **Se connecter à Heroku**

```bash
heroku login
```

3. **Créer l'application**

```bash
heroku create votre-ecommerce-app
```

4. **Configurer la base de données**

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Déployer**

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

6. **Initialiser la base de données**

```bash
heroku run python seed_data.py
```

### Option 2 : Railway (Recommandé)

1. **Aller sur [Railway.app](https://railway.app)**
2. **Connecter votre GitHub**
3. **Sélectionner ce repository**
4. **Railway détectera automatiquement Python et installera les dépendances**
5. **Ajouter une base de données PostgreSQL**
6. **Déployer !**

### Option 3 : Render

1. **Aller sur [Render.com](https://render.com)**
2. **Créer un nouveau "Web Service"**
3. **Connecter votre GitHub**
4. **Configuration :**
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Ajouter une base de données PostgreSQL**
6. **Déployer !**

### Option 4 : DigitalOcean App Platform

1. **Aller sur [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)**
2. **Créer une nouvelle app**
3. **Connecter votre GitHub**
4. **Configuration automatique détectée**
5. **Ajouter une base de données PostgreSQL**
6. **Déployer !**

## 🔧 Configuration

### Variables d'environnement

Copiez `env.example` vers `.env` et modifiez les valeurs :

```bash
cp env.example .env
```

Variables importantes :

- `DATABASE_URL` : URL de connexion à la base de données
- `SECRET_KEY` : Clé secrète pour JWT (changez en production !)
- `DEBUG` : Mode debug (False en production)

### Base de données

**SQLite (développement) :**

```env
DATABASE_URL=sqlite:///./ecommerce.db
```

**PostgreSQL (production) :**

```env
DATABASE_URL=postgresql://username:password@host:5432/database
```

## 📚 API Documentation

L'API est automatiquement documentée avec Swagger UI :

- **Développement** : http://localhost:8000/docs
- **Production** : https://votre-domaine.com/docs

### Endpoints principaux

- `GET /api/products` - Liste des produits
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/cart` - Panier utilisateur
- `POST /api/cart/add` - Ajouter au panier
- `POST /api/orders` - Créer une commande

## 🏗️ Architecture

```
ecommerce-python/
├── main.py              # Point d'entrée FastAPI
├── database.py          # Configuration base de données
├── models.py            # Modèles SQLAlchemy
├── schemas.py           # Schémas Pydantic
├── crud.py              # Opérations base de données
├── auth.py              # Authentification JWT
├── requirements.txt     # Dépendances Python
├── Dockerfile           # Image Docker
├── docker-compose.yml   # Orchestration Docker
├── nginx.conf           # Configuration Nginx
├── Procfile             # Configuration Heroku
├── seed_data.py         # Données de test
├── templates/           # Templates HTML
│   └── index.html
└── static/              # Fichiers statiques
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 🛠️ Développement

### Ajouter de nouvelles fonctionnalités

1. **Modèles** : Ajoutez dans `models.py`
2. **Schémas** : Ajoutez dans `schemas.py`
3. **CRUD** : Ajoutez dans `crud.py`
4. **API** : Ajoutez dans `main.py`
5. **Frontend** : Modifiez `templates/` et `static/`

### Tests

```bash
# Installer pytest
pip install pytest

# Lancer les tests
pytest
```

### Linting

```bash
# Installer les outils de linting
pip install black flake8

# Formater le code
black .

# Vérifier le style
flake8 .
```

## 🔒 Sécurité

- ✅ Mots de passe hashés avec bcrypt
- ✅ JWT pour l'authentification
- ✅ Validation des données avec Pydantic
- ✅ Protection CSRF (à ajouter)
- ✅ Rate limiting (à ajouter)
- ✅ HTTPS en production (automatique avec les plateformes cloud)

## 📈 Monitoring et logs

### Logs en production

La plupart des plateformes cloud fournissent des logs automatiques :

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Render
# Logs disponibles dans le dashboard
```

### Métriques

- **Performance** : FastAPI avec Uvicorn (très performant)
- **Base de données** : Requêtes optimisées avec SQLAlchemy
- **Monitoring** : Intégration possible avec Sentry, DataDog, etc.

## 🚀 Optimisations pour la production

1. **Base de données** : Utilisez PostgreSQL en production
2. **Cache** : Ajoutez Redis pour le cache
3. **CDN** : Utilisez CloudFlare pour les assets statiques
4. **Monitoring** : Ajoutez des métriques et alertes
5. **Backup** : Configurez des sauvegardes automatiques

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Documentation FastAPI** : https://fastapi.tiangolo.com/
- **Documentation SQLAlchemy** : https://docs.sqlalchemy.org/
- **Documentation Bootstrap** : https://getbootstrap.com/

## 🎯 Prochaines étapes

- [ ] Système de paiement (Stripe, PayPal)
- [ ] Gestion des images de produits
- [ ] Système de reviews/avis
- [ ] Notifications email
- [ ] Dashboard administrateur
- [ ] API mobile
- [ ] Tests automatisés
- [ ] CI/CD pipeline

---

**Développé avec ❤️ en Python** | **Prêt pour le cloud** ☁️
