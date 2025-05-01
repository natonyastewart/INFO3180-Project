import os
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .routes.auth import auth_bp

app.register_blueprint(auth_bp, url_prefix='/api')

from .models import User, Profile, Favourite

if __name__ == '__main__':
    app.run(debug=True)