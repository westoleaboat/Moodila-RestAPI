from flask import Flask
from dotenv import load_dotenv
from flask_smorest import Api
from resources.mood import blp as MoodBlueprint
from resources.users import blp as UsersBlueprint, UserRegister
# JTW user auth
from flask_jwt_extended import JWTManager
# MongoDB
from pymongo import MongoClient
# SocketIO
from flask_socketio import SocketIO, emit


def create_app():
    app = Flask(__name__)

    load_dotenv()
    app.config['SECRET_KEY'] = 'super-hard to guess string'
    app.config['JWT_SECRET_KEY'] = 'KHANDUSHA'
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app.config["API_TITLE"] = "Moodila REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000",async_mode='eventlet')
    socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:5000",async_mode='threading')


    # MongoDB configuration
    # app.config['MONGO_URI']= 'mongodb+srv://Tomaschac@fedos27.hrtdm4r.mongodb.net/' 
    mongo_client = MongoClient('mongodb+srv://Tomaschac:cat@fedos27.hrtdm4r.mongodb.net/', username='Tomaschac', password='cat')
    
    # Access Moodila database
    app.config['MONGO_CLIENT'] = mongo_client.Moodila
    
    # Access the 'users' collection in the 'Moodila' database
    app.config['MONGO_DB_USERS'] = mongo_client.Moodila.users
    # Access the 'moods' collection in the 'Moodila' database
    app.config['MONGO_DB_MOODS'] = mongo_client.Moodila.moods

    api = Api(app)
    jwt = JWTManager(app)

    # @app.before_first_request
    # def create_tables():
    #     with app.app_context():
    #         db.create_all()

    # Register Blueprints
    api.register_blueprint(MoodBlueprint)
    api.register_blueprint(UsersBlueprint)

 

    return app#, socketio

    
# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)