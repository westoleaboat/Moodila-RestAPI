#!/usr/bin/env python2.7
'''This module script is where the application instance is defined'''

import os
from app import create_app, socketio#, db
# from flask_socketio import SocketIO, emit
# from app.sockets import socketio

# from app.models import User, Role, Permission
# import click
# from flask_migrate import Migrate

'''
The script begins by creating an application. The configuration is taken from the
environment variable FLASK_CONFIG if it's defined, or else the default configuration is
used. Flask-Migrate and the custom context for the Python shell are then initialized.
'''
# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# config_name = create_app(os.getenv('FLASK_CONFIG') or 'default')
# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000",async_mode='threading')
# secret_key = os.getenv('SECRET_KEY')
# app.secret_key = secret_key


if __name__ == "__main__":
    # Run the Flask app using the Flask CLI command
    socketio.run(app, debug=True,logger=True, engineio_logger=True)
    # app.run(app, debug=True)