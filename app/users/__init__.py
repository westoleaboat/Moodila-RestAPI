""" 
# app/users/__init__.py
A Blueprint that registers info in API documentation 
"""

from flask import request, current_app, jsonify, render_template, flash, url_for, redirect, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
from schemas import UserSchema, UserRegisterSchema, fields
from flask_smorest import Api
from typing import Dict, Any

from .forms import RegistrationForm


# A Blueprint in Flask-smorest is used to divide an API into multiple segments.
users_blp = Blueprint("users", __name__, description="Operations on users")  #, url_prefix="/users")



@users_blp.route("/register")
class UserRegister(MethodView):
    @users_blp.arguments(UserRegisterSchema)
    def post(self, new_user_data):
        """
        User Registration Endpoint.

        Registers a new user by hashing the provided password and storing user data in the database.
        """
        try:
            new_user_data = request.get_json()
            # print(new_user_data)

            # Access database and collection from current app context
            db_users = current_app.config['MONGO_DB_USERS']

            # Check if the username is empty or consists only of whitespace
            if not new_user_data["username"].strip():
                return jsonify({
                    "error":
                    "Username cannot be an empty string or consist only of whitespace."
                }), 400

            # Check if the username already exists in the database
            existing_user = db_users.find_one(
                {"username": new_user_data["username"]})
            if existing_user:
                return jsonify(
                    {"error":
                     "A user with that username already exists."}), 409

            # Hash the password using pbkdf2_sha256
            hashed_password = pbkdf2_sha256.hash(new_user_data["password"])

            # Create new_user_data
            new_user = {
                'username': new_user_data["username"],
                'email': new_user_data['email'],
                'password': hashed_password,
                'team': new_user_data["team"]
            }

            # Insert the new user document into the users collection
            db_users.insert_one(new_user)

            additional_claim = {'team': new_user['team']}
            register_token_expires_in = timedelta(minutes=30)

            access_token = create_access_token(
                identity=str(new_user["_id"]),
                fresh=True,
                additional_claims={'team': new_user['team']},
                expires_delta=register_token_expires_in)
            refresh_token = create_refresh_token(str(new_user["_id"]))

            # Construct the response
            response_data = {
                "message": "User created successfully.",
                "user_data": {
                    "username": new_user["username"],
                    "email": new_user["email"],
                    "team": new_user["team"]
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": register_token_expires_in.total_seconds(),
            }

            # return jsonify(response_data), 201
            # return render_template('users/login.html')#, form=form)
            # return redirect(url_for(users.login))
            response = make_response(jsonify(response_data), 201)
            # Set the access token as a cookie
            response.set_cookie('access_token', access_token, httponly=False)
            print(access_token)
            return response

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    
    def get(self):
        # form = RegistrationForm()
        return render_template('users/register.html')#, form=form)


@users_blp.route("/login")
class UserLogin(MethodView):
    # @jwt_required()
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
            # user_data = request.json
            user_data=request.get_json()

            # Check if required fields are present in the JSON payload
            if "username" not in user_data or "password" not in user_data:
                return jsonify(
                    {"error":
                     "Username and password are required fields."}), 400

            # Check if the username exists in the database
            user = db_users.find_one({"username": user_data["username"]})

            if user and pbkdf2_sha256.verify(user_data["password"],
                                             user["password"]):

                # User authenticated, generate NEW JWT tokens with additional claims (including 'team')
                # access_token = create_access_token(
                #     identity=str(user["_id"]),
                #     fresh=True)  #, additional_claims={'team': user['team']})


                response_data = {
                    # "access_token": access_token,
                    # "refresh_token": refresh_token,
                    "you work for": user['team'],
                    "message": "correct"
                }

                response = make_response(jsonify(response_data), 201)

                # response.set_cookie('access_token', access_token, httponly=True)
                
                # print(response_data)
                # return jsonify(response_data), 200
                return response

            return jsonify({"error": "Invalid credentials."}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get(self):
        return render_template('users/login.html')


@users_blp.route('/profile')
class UserProfile(MethodView):
    # @jwt_required()
    def get(self):
        # current_user = get_jwt_identity()
        return jsonify({"message": "User profile accessed successfully."}), 200#, "user": current_user}), 200
        # return render_template('users/profile.html')
