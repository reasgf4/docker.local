from flask import Blueprint

bp = Blueprint('docker', __name__, url_prefix='/docker')

from app.docker_api import routes 