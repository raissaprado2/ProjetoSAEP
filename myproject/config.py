import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:minhasenha%40123@localhost/mydatabase'