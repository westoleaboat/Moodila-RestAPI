from flask import request, current_app, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
# from marshmallow import fields
from schemas import UserSchema, fields
from flask_smorest import Api
from typing import Dict, Any

# Create a Blueprint instance
blp = Blueprint("users", __name__, description="Operations on users")  #, url_prefix="/users")


@blp.route("/register")
class UserRegister(MethodView):
   
    def post(self):
        """
        User Registration Endpoint.

        Registers a new user by hashing the provided password and storing user data in the database.

        """
        try:
            # Access database and collection from current app context
            db_users = current_app.config['MONGO_DB_USERS']

            # Get user_data from JSON payload
            user_data = request.json

            # Check if required fields are present in the JSON payload
            # if "username" not in user_data or "password" not in user_data:
            if "username" not in user_data or "password" not in user_data or "team" not in user_data:
                return jsonify({
                    "error":
                    "Username, password and team are required fields."
                }), 400

            # Check if the username is empty or consists only of whitespace
            if not user_data["username"].strip():
                return jsonify({
                    "error":
                    "Username cannot be an empty string or consist only of whitespace."
                }), 400

            # Check if the username already exists in the database
            existing_user = db_users.find_one(
                {"username": user_data["username"]})
            if existing_user:
                return jsonify(
                    {"error":
                     "A user with that username already exists."}), 409

            # Hash the password using pbkdf2_sha256
            hashed_password = pbkdf2_sha256.hash(user_data["password"])

            # Create new_user_data
            new_user_data = {
                'username': user_data["username"],
                'email': user_data.get(
                    "email",
                    ""),  # Optional field, use get() to avoid KeyError
                'password': hashed_password,
                'team': user_data["team"]
            }

            # Insert the new user document into the users collection
            db_users.insert_one(new_user_data)

            additional_claim = {'team': new_user_data['team']}
            register_token_expires_in = timedelta(minutes=30)

            access_token = create_access_token(
                identity=str(new_user_data["_id"]),
                fresh=True,
                additional_claims={'team': new_user_data['team']},
                expires_delta=register_token_expires_in)
            refresh_token = create_refresh_token(str(new_user_data["_id"]))

            # Construct the response
            response_data = {
                "message": "User created successfully.",
                "user_data": {
                    "username": new_user_data["username"],
                    "email": new_user_data["email"],
                    "team": new_user_data["team"]
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": register_token_expires_in.total_seconds(),
            }

            # @blp.response(jsonify(response_data))
            return jsonify(response_data), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@blp.route("/login")
class UserLogin(MethodView):

    def post(self):
        """
        User Login Endpoint

        Authenticates a user using provided credentials and generates access and refresh tokens.

        Args:
            None (Uses data from the JSON payload in the request)

        Returns:
            JSON response containing the result of the login process:
            - Success (200): Authentication successful with access and refresh tokens.
            - Client Error (400): Missing or invalid input fields in the JSON payload.
            - Unauthorized (401): Invalid credentials.
            - Server Error (500): Internal server error during login.
        """
        try:
            # Access database and collection from current app context
            db_users = current_app.config['MONGO_DB_USERS']

            # Get user_data from JSON payload
            user_data = request.json

            # Check if required fields are present in the JSON payload
            if "username" not in user_data or "password" not in user_data:
                return jsonify(
                    {"error":
                     "Username and password are required fields."}), 400

            # Check if the username exists in the database
            user = db_users.find_one({"username": user_data["username"]})

            if user and pbkdf2_sha256.verify(user_data["password"],
                                             user["password"]):
                # User authenticated, generate JWT tokens with additional claims (including 'team')
                access_token = create_access_token(
                    identity=str(user["_id"]),
                    fresh=True)  #, additional_claims={'team': user['team']})
                refresh_token = create_refresh_token(str(user["_id"]))

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "you work for": user['team']
                }, 200

            return jsonify({"error": "Invalid credentials."}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500