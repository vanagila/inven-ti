from app.database.connection import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(250), nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    is_admin =  db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    ativo = db.Column(db.Boolean, default=True)

    registros_suporte = db.relationship('RegistroSuporte', backref='usuario', lazy=True)
    equipamentos_cadastrados = db.relationship('Equipamento', foreign_keys='Equipamento.id_usuario_cadastro', back_populates='usuario_cadastro', lazy=True)
    equipamentos_alterados = db.relationship('Equipamento', foreign_keys='Equipamento.id_usuario_ultima_alteracao', back_populates='usuario_ultima_alteracao', lazy=True)

    def __init__(self, nome, email, senha, departamento, cargo, is_admin=False):
        self.nome = nome
        self.email = email
        self.set_senha(senha)
        self.departamento = departamento
        self.cargo = cargo
        self.is_admin = is_admin

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'departamento': self.departamento,
            'cargo': self.cargo,
            'is_admin': self.is_admin,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'ativo': self.ativo,
            'total_equipamentos_cadastrados': len(self.equipamentos_cadastrados),
            'total_registros_suporte': len(self.registros_suporte)
        }
    
    def __repr__(self):
        return f'<Usuario {self.email}>'