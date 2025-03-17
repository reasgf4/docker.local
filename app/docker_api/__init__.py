from flask import Blueprint

# Use a more unique name for the blueprint to avoid conflicts
bp = Blueprint('docker_api', __name__, url_prefix='/docker')

from app.docker_api import routes 