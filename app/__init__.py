from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'routes.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа'
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    with app.app_context():
        db.create_all()
        from app.models import User
        if not User.query.first():
            admin = User(
                username='admin',
                email='admin@shop.ru',
                password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('✅ Админ создан: admin@shop.ru / admin123')
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))