#!/bin/sh

# flask db upgrade

# Start Gunicorn to serve the Flask application
exec gunicorn --bind 0.0.0.0:80 "app:create_app('default')"