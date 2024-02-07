#!/bin/sh

# flask db upgrade

# Start Gunicorn to serve the Flask application
exec gunicorn --log-level debug --bind 0.0.0.0:80 "pyinstance:create_app('default')"