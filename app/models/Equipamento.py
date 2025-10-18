from app.database.connection import db
from datetime import datetime, timezone
from app.models.enums import StatusEquipamento

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patrimonio = db.Column(db.String(255), unique=True, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(255), unique=True, nullable=False)
    data_aquisicao = db.Column(db.Date, nullable=False)
    localizacao = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default=StatusEquipamento.EM_USO)
    observacoes = db.Column(db.Text, nullable=True)
    data_cadastro = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    data_ultima_alteracao = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    id_usuario_cadastro = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    id_usuario_ultima_alteracao = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    registros_suporte = db.relationship('RegistroSuporte', backref='equipamento', lazy=True, cascade='all, delete-orphan')
    usuario_cadastro = db.relationship('Usuario', foreign_keys=[id_usuario_cadastro], back_populates='equipamentos_cadastrados')
    usuario_ultima_alteracao = db.relationship('Usuario', foreign_keys=[id_usuario_ultima_alteracao], back_populates='equipamentos_alterados')

    def __init__(self, patrimonio, tipo, marca, modelo, numero_serie, data_aquisicao, localizacao, id_usuario_cadastro, status=StatusEquipamento.EM_USO, observacoes=None):
        self.patrimonio = patrimonio
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.numero_serie = numero_serie
        self.data_aquisicao = data_aquisicao
        self.localizacao = localizacao
        self.status = status
        self.observacoes = observacoes
        self.id_usuario_cadastro = id_usuario_cadastro
        self.data_cadastro = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            'id': self.id,
            'patrimonio': self.patrimonio,
            'tipo': self.tipo,
            'marca': self.marca,
            'modelo': self.modelo,
            'numero_serie': self.numero_serie,
            'data_aquisicao': self.data_aquisicao.isoformat() if self.data_aquisicao else None,
            'localizacao': self.localizacao,
            'status': self.status,
            'observacoes': self.observacoes,
            'id_usuario_cadastro': self.id_usuario_cadastro,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'id_usuario_ultima_alteracao': self.id_usuario_ultima_alteracao,
            'data_ultima_alteracao': self.data_ultima_alteracao.isoformat() if self.data_ultima_alteracao else None
        }
    
    def atualizar_alteracao(self, id_usuario):
        self.id_usuario_ultima_alteracao = id_usuario
        self.data_ultima_alteracao = datetime.now(timezone.utc)
    
    def __repr__(self):
        return f'<Equipamento {self.id}>'
