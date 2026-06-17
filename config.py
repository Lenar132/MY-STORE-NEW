import os

class Config:
    SECRET_KEY = 'your-secret-key-change-this'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///warehouse.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False