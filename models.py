from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()


class User(db.Model):
    """docstring for User"""
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(95))
    nombre = db.Column(db.String(40))
    cedula = db.Column(db.String(10))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    representante = db.relationship('Representante', backref="Users",
                                    lazy=True, uselist=False)

    def __init__(self, nombre, cedula, username, email, password):
        self.nombre = nombre
        self.cedula = cedula
        self.username = username
        self.email = email
        self.password = password

    def comparar(self, password):
        if self.password == password:
            return True
        return False


class Representante(db.Model):
    __tablename__ = 'Representantes'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey(
        'Users.id'), nullable=False, unique=True)

    preinscripciones = db.relationship(
        'Preinscripcion', backref='Representantes', lazy=True)


class Preinscripcion(db.Model):
    __tablename__ = "Preinscripciones"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(10))
    apellido = db.Column(db.String(15))
    edad = db.Column(db.Integer)
    escuela = db.Column(db.String(50))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)

    id_Representante = db.Column(db.Integer, db.ForeignKey(
        'Representantes.id'), nullable=False)
