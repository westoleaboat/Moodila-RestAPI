#!/usr/bin/env python2.7
''' pyinstance.py: Module script where the application instance is defined'''

import os
from app import create_app, socketio

'''
The script begins by creating an application. The configuration is taken from the
environment variable FLASK_CONFIG if it's defined, or else the default configuration is
used. Flask-Migrate and the custom context for the Python shell are then initialized.
'''

app = create_app(os.getenv('FLASK_CONFIG') or 'default')



if __name__ == "__main__":
    # Run the Flask app using the Flask CLI command
    socketio.run(app, debug=True,logger=True, engineio_logger=True)