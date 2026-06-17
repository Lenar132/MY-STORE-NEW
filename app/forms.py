from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User, Product

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован')
        
        # Проверка на реальные почтовые сервисы
        allowed_domains = ['gmail.com', 'mail.ru', 'yandex.ru', 'yahoo.com', 'outlook.com', 'bk.ru', 'list.ru', 'inbox.ru']
        email_domain = email.data.split('@')[-1].lower()
        
        if email_domain not in allowed_domains:
            raise ValidationError(f'Используйте email с доменом: {", ".join(allowed_domains)}')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class ProductForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    article = StringField('Артикул')
    quantity = FloatField('Количество', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    category = StringField('Категория')
    unit = SelectField('Единица измерения', choices=[
        ('шт', 'Штуки'),
        ('кг', 'Килограммы'),
        ('м', 'Метры'),
        ('м²', 'Квадратные метры'),
        ('упак', 'Упаковка'),
        ('л', 'Литры')
    ], default='шт')
    manufacturer = StringField('Производитель')
    min_stock = FloatField('Минимальный остаток', default=5)
    location = StringField('Место хранения (стеллаж/ряд)')
    submit = SubmitField('Добавить товар')
    
    def validate_article(self, article):
        if article.data:
            product = Product.query.filter_by(article=article.data).first()
            if product:
                raise ValidationError('Товар с таким артикулом уже существует')


class MovementForm(FlaskForm):
    product_id = SelectField('Товар', coerce=int, validators=[DataRequired()])
    type = SelectField('Тип операции', choices=[
        ('приход', 'Приход'), 
        ('расход', 'Расход'), 
        ('продажа', 'Продажа клиенту')
    ])
    quantity = FloatField('Количество', validators=[DataRequired()])
    comment = StringField('Комментарий')
    submit = SubmitField('Выполнить')