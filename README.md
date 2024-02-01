# flask-boilerplate
Quick-start deployment of your Flask site on render.com Make a REST API or a static site.

## test locally:

create virtual environment (.venv) 
```
python3 -m venv .venv
```

activate virtual env
```
source .venv/bin/activate
```

install packages with pip
```
pip install -r requirements.txt
```

run application
```
# export FLASK_APP=app.py (if needed)
flask run
```
you should see the following:
```
* Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 999-***-***
```
## API endpoints
with app running, go to http://127.0.0.1:5000/swagger-ui

![Moodila-REST-API](https://github.com/westoleaboat/Moodila-RestAPI/assets/68698872/764e2a46-7c07-420f-ace2-0d3e14c884b4)
