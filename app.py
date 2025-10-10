from flask import Flask, render_template, request, redirect, url_for
from app.controllers.AuthController import auth_bp
from app.database.connection import init_app
from flask_migrate import Migrate

app = Flask(__name__, template_folder='app/views', static_folder='app/static')
app.secret_key = 'inven_ti_key'

db = init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)

def ensure_admin():
    from app.models.Usuario import Usuario
    from app.database.connection import db as _db

    with app.app_context():
        admin = Usuario.query.filter_by(email='admin@empresa.com').first()
        if not admin:
            admin = Usuario(
                nome='Administrador',
                email='admin@empresa.com',
                senha='admin123',
                departamento='TI',
                cargo='Administrador',
                is_admin=True
            )
            _db.session.add(admin)
            _db.session.commit()
            print('Usuário admin criado: admin@empresa.com / admin123')

if __name__ == '__main__':
    ensure_admin()
    app.run(debug=True)