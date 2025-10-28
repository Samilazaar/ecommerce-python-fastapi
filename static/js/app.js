// Application JavaScript pour l'e-commerce
class ECommerceApp {
    constructor() {
        this.apiBase = '/api';
        this.token = localStorage.getItem('token');
        this.cart = [];
        this.products = [];
        
        this.init();
    }

    init() {
        this.loadProducts();
        this.setupEventListeners();
        this.updateCartUI();
    }

    setupEventListeners() {
        // Formulaire de connexion
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        // Formulaire d'inscription
        document.getElementById('registerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });
    }

    // Gestion de l'authentification
    async login() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch(`${this.apiBase}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.access_token;
                localStorage.setItem('token', this.token);
                
                this.showAlert('Connexion réussie !', 'success');
                this.hideModal('loginModal');
                this.updateAuthUI();
            } else {
                const error = await response.json();
                this.showAlert(error.detail || 'Erreur de connexion', 'danger');
            }
        } catch (error) {
            this.showAlert('Erreur de connexion', 'danger');
        }
    }

    async register() {
        const firstName = document.getElementById('registerFirstName').value;
        const lastName = document.getElementById('registerLastName').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        try {
            const response = await fetch(`${this.apiBase}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    first_name: firstName, 
                    last_name: lastName, 
                    email, 
                    password 
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.token = data.access_token;
                localStorage.setItem('token', this.token);
                
                this.showAlert('Inscription réussie !', 'success');
                this.hideModal('registerModal');
                this.updateAuthUI();
            } else {
                const error = await response.json();
                this.showAlert(error.detail || 'Erreur d\'inscription', 'danger');
            }
        } catch (error) {
            this.showAlert('Erreur d\'inscription', 'danger');
        }
    }

    logout() {
        this.token = null;
        localStorage.removeItem('token');
        this.updateAuthUI();
        this.showAlert('Déconnexion réussie', 'info');
    }

    updateAuthUI() {
        const loginBtn = document.querySelector('button[onclick="showLoginModal()"]');
        const registerBtn = document.querySelector('button[onclick="showRegisterModal()"]');
        
        if (this.token) {
            loginBtn.innerHTML = '<i class="fas fa-user me-1"></i> Mon compte';
            loginBtn.onclick = () => this.logout();
            registerBtn.style.display = 'none';
        } else {
            loginBtn.innerHTML = '<i class="fas fa-sign-in-alt me-1"></i> Connexion';
            loginBtn.onclick = showLoginModal;
            registerBtn.style.display = 'inline-block';
        }
    }

    // Gestion des produits
    async loadProducts() {
        try {
            const response = await fetch(`${this.apiBase}/products`);
            this.products = await response.json();
            this.renderProducts();
        } catch (error) {
            console.error('Erreur lors du chargement des produits:', error);
        }
    }

    renderProducts() {
        const container = document.getElementById('products-container');
        container.innerHTML = '';

        this.products.forEach(product => {
            const productCard = this.createProductCard(product);
            container.appendChild(productCard);
        });
    }

    createProductCard(product) {
        const col = document.createElement('div');
        col.className = 'col-lg-4 col-md-6 mb-4';

        col.innerHTML = `
            <div class="card product-card h-100">
                <div class="product-image">
                    <i class="fas fa-box"></i>
                </div>
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text text-muted">${product.description || 'Aucune description'}</p>
                    <div class="mt-auto">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <span class="product-price">${product.price}€</span>
                            <small class="text-muted">Stock: ${product.stock_quantity}</small>
                        </div>
                        <button class="btn btn-primary w-100" onclick="app.addToCart(${product.id})">
                            <i class="fas fa-cart-plus me-2"></i>
                            Ajouter au panier
                        </button>
                    </div>
                </div>
            </div>
        `;

        return col;
    }

    // Gestion du panier
    async addToCart(productId) {
        if (!this.token) {
            this.showAlert('Veuillez vous connecter pour ajouter des articles au panier', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/cart/add`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ product_id: productId, quantity: 1 })
            });

            if (response.ok) {
                this.showAlert('Produit ajouté au panier !', 'success');
                this.loadCart();
            } else {
                this.showAlert('Erreur lors de l\'ajout au panier', 'danger');
            }
        } catch (error) {
            this.showAlert('Erreur lors de l\'ajout au panier', 'danger');
        }
    }

    async loadCart() {
        if (!this.token) return;

        try {
            const response = await fetch(`${this.apiBase}/cart`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.cart = await response.json();
                this.updateCartUI();
            }
        } catch (error) {
            console.error('Erreur lors du chargement du panier:', error);
        }
    }

    updateCartUI() {
        const cartCount = document.getElementById('cart-count');
        const totalItems = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
    }

    async showCart() {
        if (!this.token) {
            this.showAlert('Veuillez vous connecter pour voir votre panier', 'warning');
            return;
        }

        await this.loadCart();
        this.renderCart();
        this.showModal('cartModal');
    }

    renderCart() {
        const container = document.getElementById('cart-items');
        
        if (this.cart.length === 0) {
            container.innerHTML = '<p class="text-center text-muted">Votre panier est vide</p>';
            return;
        }

        container.innerHTML = '';
        let total = 0;

        this.cart.forEach(item => {
            const itemTotal = item.product.price * item.quantity;
            total += itemTotal;

            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item d-flex align-items-center';
            cartItem.innerHTML = `
                <div class="cart-item-image me-3">
                    <i class="fas fa-box"></i>
                </div>
                <div class="flex-grow-1">
                    <h6 class="mb-1">${item.product.name}</h6>
                    <small class="text-muted">${item.product.price}€ × ${item.quantity}</small>
                </div>
                <div class="quantity-controls me-3">
                    <button class="quantity-btn" onclick="app.updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                    <span class="mx-2">${item.quantity}</span>
                    <button class="quantity-btn" onclick="app.updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </div>
                <div class="text-end">
                    <strong>${itemTotal.toFixed(2)}€</strong>
                    <br>
                    <button class="btn btn-sm btn-outline-danger" onclick="app.removeFromCart(${item.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            container.appendChild(cartItem);
        });

        // Ajouter le total
        const totalRow = document.createElement('div');
        totalRow.className = 'cart-item border-top pt-3';
        totalRow.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Total</h5>
                <h5 class="mb-0 text-success">${total.toFixed(2)}€</h5>
            </div>
        `;
        container.appendChild(totalRow);
    }

    async updateQuantity(itemId, newQuantity) {
        if (newQuantity <= 0) {
            await this.removeFromCart(itemId);
            return;
        }

        // Ici vous pourriez implémenter une API pour mettre à jour la quantité
        // Pour l'instant, on recharge le panier
        await this.loadCart();
        this.renderCart();
    }

    async removeFromCart(itemId) {
        try {
            const response = await fetch(`${this.apiBase}/cart/remove/${itemId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.showAlert('Article supprimé du panier', 'info');
                await this.loadCart();
                this.renderCart();
            }
        } catch (error) {
            this.showAlert('Erreur lors de la suppression', 'danger');
        }
    }

    async checkout() {
        if (!this.token) {
            this.showAlert('Veuillez vous connecter pour passer commande', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/orders`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.showAlert('Commande passée avec succès !', 'success');
                this.hideModal('cartModal');
                await this.loadCart();
            } else {
                this.showAlert('Erreur lors de la commande', 'danger');
            }
        } catch (error) {
            this.showAlert('Erreur lors de la commande', 'danger');
        }
    }

    // Utilitaires
    showModal(modalId) {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    hideModal(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) modal.hide();
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Supprimer automatiquement après 5 secondes
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    }
}

// Fonctions globales pour les boutons
function showLoginModal() {
    app.showModal('loginModal');
}

function showRegisterModal() {
    app.showModal('registerModal');
}

function showCart() {
    app.showCart();
}

// Initialiser l'application
const app = new ECommerceApp();
