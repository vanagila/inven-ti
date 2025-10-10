from app import create_app
from app.database.connection import init_app, db
from flask_migrate import Migrate

# Create app using factory if available, otherwise fall back to importing app.app
try:
    app = create_app()
except Exception:
    # fallback: try to import app object from app.py
    from app import app as app

init_app(app)
Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
