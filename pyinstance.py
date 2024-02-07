#!/usr/bin/env python2.7
'''This module script is where the application instance is defined'''

import os
from app import create_app#, db
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
app, socketio = create_app(os.getenv('FLASK_CONFIG') or 'default')

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# migrate = Migrate(app, db)

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Role=Role, Permission=Permission)
# Create the Flask app instance
# app, socketio = create_app(config_name)

if __name__ == "__main__":
    # Run the Flask app using the Flask CLI command
    socketio.run(app, debug=True)