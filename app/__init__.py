import os
from flask import Flask, current_app, jsonify, request
from flask_migrate import Migrate

from app.utils import generate_response
from .config import Config
from flask_cors import CORS

migrate = Migrate()


def page_not_found(e):
    current_app.logger.error(f"Page not found: {request.path} - {e}")
    return jsonify(generate_response(success=False, message=f"{e}")), 404


def internal_server_error(e):
    current_app.logger.error(f"Server Error: {e}", exc_info=True)
    return (
        jsonify(generate_response(success=False, message="Internal Server Error")),
        500,
    )


def create_app(config_overrides=None):
    app = Flask(__name__)

    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])

    CORS(app)

    from app.models import db

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    from app.routes.auth import auth_bp
    from app.routes.profiles import profiles_bp

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(profiles_bp, url_prefix="/api")

    return app
