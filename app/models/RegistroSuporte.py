from app.database.connection import db
from datetime import datetime, timezone

class RegistroSuporte(db.Model):
    __tablename__ = 'registros_suporte'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipamento = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    data_suporte = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    tipo_suporte = db.Column(db.String(100), nullable=False)
    responsavel = db.Column(db.String(255), nullable=False)
    custo = db.Column(db.Numeric(10, 2), default=0.00)

    def __init__(self, id_equipamento, id_usuario, data_suporte, tipo_suporte, descricao, responsavel, custo=0.00):
        self.id_equipamento = id_equipamento
        self.id_usuario = id_usuario
        self.data_suporte = data_suporte
        self.tipo_suporte = tipo_suporte
        self.descricao = descricao
        self.responsavel = responsavel
        self.custo = custo

    def to_dict(self):
        return {
            'id': self.id,
            'id_equipamento': self.id_equipamento,
            'id_usuario': self.id_usuario,
            'data_suporte': self.data_suporte.isoformat() if self.data_suporte else None,
            'tipo_suporte': self.tipo_suporte,
            'descricao': self.descricao,
            'responsavel': self.responsavel,
            'custo': float(self.custo) if self.custo else 0.00
        }

    def __repr__(self):
        return f'<RegistroSuporte {self.id}>'
