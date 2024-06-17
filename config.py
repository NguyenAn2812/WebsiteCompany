import os

class Config:
    SECRET_KEY = 'Your_secret_key_here' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
