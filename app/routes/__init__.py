

from flask import jsonify
from app.app import app
from app.utils import generate_response

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(generate_response(success=False, message='Route not found!')), 404