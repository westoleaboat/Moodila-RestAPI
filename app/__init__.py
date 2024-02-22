'''app/__init__.py: Application package constructor.
    Moods and User Auth in their respective folders '''

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_smorest import Api
# config
from config import config
# JTW user auth
from flask_jwt_extended import JWTManager
# JWT logout BLOCKLIST
from blocklist import BLOCKLIST
# MongoDB
from pymongo import MongoClient
# MongoEngine
from flask_mongoengine import MongoEngine



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
 
    # initialize api, jwt, db
    api = Api(app)
    db = MongoEngine(app)
    jwt = JWTManager(app)

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 1:
    #         return {"is_admin": True}
    #     return {"is_admin": False}


    # LOGOUT token revoking logic
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.",
                     "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.",
                 "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        """Whenever we receive a JWT this function runs.
        If True returns Error, error msg in func 'revoked_token_callback' below  
        """
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Return message when function above returns True"""
        return (
            jsonify(
                {"description": "The token has been revoked.",
                 "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )


    ################################## 
    # commented out for MONGO DATABASE
    #
    # @app.before_first_request
    # def create_tables():
    #     with app.app_context():
    #         db.create_all()
    ##################################

    # Register Blueprints for Mood and Users in API
    from .mood import mood_blp as MoodBlueprint
    api.register_blueprint(MoodBlueprint)
    from .users import users_blp as UsersBlueprint
    api.register_blueprint(UsersBlueprint)

    
    return app
    
