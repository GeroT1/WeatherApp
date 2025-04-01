from flask import Flask
from .config import Config
from .app import bp

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    app.register_blueprint(bp)
    
    return app