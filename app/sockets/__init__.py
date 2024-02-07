from flask import Blueprint

socket_blp = Blueprint('socket_blp', __name__)

from . import events