""" 
# app/users/__init__.py
A Blueprint that registers USER info in API documentation 
"""

from flask import request, current_app, jsonify, render_template, flash, url_for, redirect, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from blocklist import BLOCKLIST
from datetime import timedelta
from schemas import UserSchema, UserRegisterSchema, fields
from flask_smorest import Api
from typing import Dict, Any
from .forms import RegistrationForm

# A Blueprint in Flask-smorest is used to divide an API into multiple segments.
users_blp = Blueprint("users", __name__, description="Operations on users")  

@users_blp.route("/register")
class UserRegister(MethodView):
    @users_blp.arguments(UserRegisterSchema)
    def post(self, new_user_data):
        """
        User Registration Endpoint.

        Registers a new user by hashing the provided password 
        and storing user data in the database.
        """
        try:
            new_user_data = request.get_json()
            # Access database and collection from current app context
            db_users = current_app.config['MONGO_DB_USERS']
            # Check if the username is empty or consists only of whitespace
            if not new_user_data["email"].strip():
                return jsonify({
                    "error":
                    "email cannot be an empty string or consist only of whitespace."
                }), 400

            # Check if the username already exists in the database
            existing_user = db_users.find_one(
                {"email": new_user_data["email"]})
            if existing_user:
                return jsonify(
                    {"error":
                     "A user with that email already exists."}), 409

            # Hash the password using pbkdf2_sha256
            hashed_password = pbkdf2_sha256.hash(new_user_data["password"])

            # Create new_user_data
            new_user = {
                'email': new_user_data['email'],
                'password': hashed_password,
            }
            # Insert the new user document into the users collection
            db_users.insert_one(new_user)

            return {"message": "User created successfully."}

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@users_blp.route("/login")
class UserLogin(MethodView):
    # @jwt_required()
    @users_blp.arguments(UserSchema)
    def post(self, user_data):
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
            user_data=request.get_json()
            # Check if required fields are present in the JSON payload
            if "email" not in user_data or "password" not in user_data:
                return jsonify(
                    {"error":
                     "Email and password are required fields."}), 400
            # Check if the username exists in the database
            user = db_users.find_one({"email": user_data["email"]})

            if user and pbkdf2_sha256.verify(user_data["password"],
                                             user["password"]):

                # User authenticated, create access token
                access_token = create_access_token(identity=str(user["_id"]), fresh=True)
                # create refresh token
                refresh_token = create_refresh_token(identity=str(user["_id"]))

                # TODO:
                # generate JWT tokens with additional claims (including 'team') as below:
                #
                # access_token = create_access_token(
                #     identity=str(user["_id"]),
                #     fresh=True, 
                #     additional_claims={'team': user['team']})
                #
                # or use JWT claims in app/__init__.py line 58
                # with @jwt.additional_claims_loader.

                return {"access_token": access_token, "refresh_token": refresh_token}

            abort(401, message="Invalid credentials.")

        except Exception as e:
            return jsonify({"error": str(e)}), 500


@users_blp.route("/logout")
class UserLogout(MethodView):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"] # Unique Identifier
        BLOCKLIST.add(jti) # Add jti to blocklist = revoked
        return {"message": "Successfully logged out"}, 200


@users_blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True) # not an access token
    def post(self):
        current_user = get_jwt_identity() # none if no user
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200