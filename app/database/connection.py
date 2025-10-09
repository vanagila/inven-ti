from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/inventi_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    conn = pymysql.connect(host='localhost', user='root', password='')
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.close()
    
    db.init_app(app)

    with app.app_context():
        from app.models.Usuario import Usuario
        db.create_all()

    return db