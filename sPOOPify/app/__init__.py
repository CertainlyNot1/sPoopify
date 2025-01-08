from flask import Flask
from .config import Config
from .db import db
from .routes import auth_bp, main_bp, acc_bp
from flask_migrate import Migrate
def make_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app,db)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(acc_bp)
    return app