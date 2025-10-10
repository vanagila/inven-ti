from app.database.connection import db

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=True)
    id_usuario_cadastro = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    id_usuario_ultima_alteracao = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    def __repr__(self):
        return f'<Equipamento {self.id}>'
