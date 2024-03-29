
# Live @ https://moodila.onrender.com/swagger-ui

Our Flask REST API, designed with a Factory pattern, ensures robustness and scalability. Deployed using Docker containers, it offers enhanced reliability and portability across various environments. The API utilizes PostgreSQL as its primary data storage solution, offering a reliable and efficient database backend. Alternatively, it seamlessly integrates with MongoDB clusters for those preferring a NoSQL database approach. User authentication is implemented using JSON Web Tokens (JWT), ensuring secure access control and authentication mechanisms.

## TODO

### Improve
- [ ] Token revoke BLOCKLIST in DB not python set()

### Completed
- [x] Use environment variables for API, db credentials
- [x] Login/Logout users
- [x] Fresh and Refresh tokens

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
(needed) Provide .env file with following variables:
these need to be loaded in deployment site config
```
SECRET_KEY=<SOME_SUPER_HARD_STRING>
# M_USERNAME=
# M_PASSWORD=
# CLUSTER=
JWT_SECRET_KEY=<SOME_SUPER_HARD_STRING>
# cluster connection string format: see https://www.mongodb.com/docs/manual/reference/connection-string/
# 'mongodb+srv://<<USERNAME>>:<<PASSWORD>>@<<CLUSTER>>.mongodb.net/'
MONGO_URI=<YOUR_MONGODB_CLUSTER>
```

run application
```
# export FLASK_APP=pyinstance.py (if needed)
flask run
```
or with Gunicorn:
```
gunicorn --bind 127.0.0.1:5000 "pyinstance:create_app('default')"
# improved
gunicorn -w 1 --threads 100 --log-level debug --bind 127.0.0.1:5000 "pyinstance:create_app('default')"
```
you should see the following:
```
[2024-02-07 10:52:53 +0200] [236939] [INFO] Starting gunicorn 20.1.0
[2024-02-07 10:52:53 +0200] [236939] [INFO] Listening at: http://127.0.0.1:5000 (236939)
[2024-02-07 10:52:53 +0200] [236939] [INFO] Using worker: sync
[2024-02-07 10:52:53 +0200] [236940] [INFO] Booting worker with pid: 236940
```
To run with **Docker**:
first create docker image:
```
# with dockerd (daemon) running
docker build -t <YOUR-IMAGE-NAME> .
# the a dot (.) at the end of previous command is no mistake
```

then run the docker container locally:
```
docker run -p 5000:5000 -w /app -v "$(pwd):/app" <YOUR-IMAGE-NAME> sh -c "flask run --host 0.0.0.0"
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
