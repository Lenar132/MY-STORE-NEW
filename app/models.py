from app import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='client')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    movements = db.relationship('Movement', backref='user', lazy=True)
    
    def can_add_product(self):
        return self.role in ['admin', 'storekeeper']
    
    def can_sell(self):
        return self.role in ['admin', 'manager', 'storekeeper']
    
    def can_view_reports(self):
        return self.role in ['admin', 'director', 'accountant', 'viewer']
    
    def can_manage_users(self):
        return self.role == 'admin'
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    article = db.Column(db.String(50), unique=True)
    quantity = db.Column(db.Float, default=0)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    unit = db.Column(db.String(10), default='шт')
    manufacturer = db.Column(db.String(100))
    min_stock = db.Column(db.Float, default=5)
    location = db.Column(db.String(50))
    
    movements = db.relationship('Movement', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10))
    quantity = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Movement {self.type} {self.quantity}>'


class Order(db.Model):
    """Модель заказа (предзаказа) от клиента"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String(200))
    
    user = db.relationship('User', backref='orders', lazy=True)
    product = db.relationship('Product', backref='orders', lazy=True)
      
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'

class Notification(db.Model):
    """Модель уведомлений для пользователей"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    link = db.Column(db.String(200), nullable=True)
    
    user = db.relationship('User', backref='notifications', lazy=True)
    
    def __repr__(self):
        return f'<Notification {self.title}>'