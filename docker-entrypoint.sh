#!/bin/sh

# flask db upgrade

# Start Gunicorn to serve the Flask application
exec --log-level debug gunicorn --bind 0.0.0.0:80 "pyinstance:create_app('default')"