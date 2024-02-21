'''app/__init__.py: Application package constructor'''

from flask import Flask
from dotenv import load_dotenv
from flask_smorest import Api
# config
from config import config
# JTW user auth
from flask_jwt_extended import JWTManager
# MongoDB
from pymongo import MongoClient
# MongoEngine
from flask_mongoengine import MongoEngine
# SocketIO
from flask_socketio import SocketIO

# socket connection
socketio = SocketIO(cors_allowed_origins="*",async_mode='threading')


def create_app(config_name):
    """Factory Pattern configuration return app for ./pyinstance.py"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    load_dotenv()
    
    # MongoDB configuration
    mongo_client = MongoClient('mongodb+srv://Tomaschac:cat@fedos27.hrtdm4r.mongodb.net/', username='Tomaschac', password='cat')

    # Access Moodila database
    moodila_db = mongo_client['Moodila']
    # Access the 'users' collection in the 'Moodila' database
    users_collection = moodila_db['users']
    # Access the 'moods' collection in the 'Moodila' database
    moods_collection = moodila_db['moods']

    # Store MongoDB objects in Flask app.config
    app.config['MONGO_CLIENT'] = mongo_client
    app.config['MONGO_DB_USERS'] = users_collection
    app.config['MONGO_DB_MOODS'] = moods_collection

    app.config['SECRET_KEY'] = 'super-hard to guess string'
    app.config['JWT_SECRET_KEY'] = 'KHANDUSHA'
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # Swagger-UI
    app.config["API_TITLE"] = "Moodila REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
 
    # initialize api, jwt, db, socketio
    api = Api(app)
    jwt = JWTManager(app)
    db = MongoEngine(app)

    socketio.init_app(app)

    # commented out for MONGO DATABASE
    # @app.before_first_request
    # def create_tables():
    #     with app.app_context():
    #         db.create_all()

    # Register Blueprints for Mood and Users in API
    from .mood import mood_blp as MoodBlueprint
    api.register_blueprint(MoodBlueprint)
    from .users import users_blp as UsersBlueprint
    api.register_blueprint(UsersBlueprint)

    
    return app
    
