from app.database.connection import db


class RegistroSuporte(db.Model):
    __tablename__ = 'registros_suporte'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.Text, nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)

    def __repr__(self):
        return f'<RegistroSuporte {self.id}>'
