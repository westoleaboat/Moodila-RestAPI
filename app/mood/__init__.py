""" 
# app/mood/__init__.py
A Blueprint that registers Moods in API documentation 
"""

from flask import request, current_app, render_template, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson import ObjectId
import json
from tabulate import tabulate
from schemas import MoodSchema
from datetime import datetime
# from flask_socketio import send, emit
# from app import socketio

#JWT
from flask_jwt_extended import jwt_required

# Create a Blueprint instance for API
mood_blp = Blueprint("moods", __name__, description="Operations on moods")

# Define the route
@mood_blp.route('/mood')
class MoodList(MethodView):
    @jwt_required()
    def get(self):
        """
        Retrieve and display moods based on their creation date.

        Accesses the MongoDB client and database from the current app context,
        retrieves all mood documents from the 'Moodila' database, the 
        retrieved moods are returned.

        Returns:
            List of moods.
        """
        try:
            # Access database and collection from the current app context
            db_moods = current_app.config['MONGO_DB_MOODS']
            # Fetch all mood documents from the collection
            moods_collection = db_moods.find({})
            # Convert the cursor to a list of dictionaries
            data = list(moods_collection)

            # Iterate over each mood in the data
            for i, item in enumerate(data, start=1):
                # Remove the '_id' field from each dictionary
                item.pop("_id")
                # Add an 'index' field with the current index
                item["index"] = i
            
            return data


        except Exception as e:
            # Handle exceptions and return an appropriate JSON response
            response_data = {"error": str(e)}
            return jsonify(response_data), 500

    @jwt_required()
    @mood_blp.arguments(MoodSchema)#, required=True)
    @mood_blp.response(201, MoodSchema)
    def post(self, mood_data):
        """
        Add a new Mood to the Database.

        Accesses MongoDB client and database from the current app context,
        retrieves data from the POST request JSON payload, and adds a new
        mood to the 'moods' collection in the 'Moodila' database.

        Returns:
            Flask response: JSON response indicating success or failure.
        """
        try:
            mood_data=request.get_json()
            # Access database and collection from current app context
            db_moods = current_app.config['MONGO_DB_MOODS']
            # Set 'created_at' to the current time
            mood_data['created_at'] = datetime.utcnow()

            # Create a new mood dictionary from JSON payload
            new_mood = {
                'title': mood_data["title"],
                'quote': mood_data["quote"],
                'author': mood_data["author"],
                'created_at': mood_data['created_at']
            }
            # Insert the new mood into the MongoDB collection
            db_moods.insert_one(new_mood)
            # new_mood.pop("_id")  # avoid ObjectId bug
            
            return jsonify({"message": "Mood added successfully"}), 201

        except Exception as e:
            # Handle exceptions and return an appropriate JSON response
            abort(500, error=str(e))

# return spicific mood
@mood_blp.route('/mood/<string:mood_id>')
class Mood(MethodView):
    '''
    The endpoint now expects an ObjectId for the mood_id parameter, assuming that the _id in MongoDB is of type ObjectId.


    The get method retrieves the mood with the specified mood_id from the MongoDB collection and returns it as JSON. If the mood is not found, it returns a 404 Not Found response.
    The delete method deletes the mood with the specified mood_id from the MongoDB collection. It returns a success message if the mood is deleted successfully and a 404 Not Found response if the mood is not found.
    '''
    @jwt_required()
    @mood_blp.response(200, MoodSchema)
    def get(self, mood_id):
        """
        Retrieve a mood by its index.

        This endpoint retrieves a mood from the MongoDB collection based on the provided index.
        If the specified index is within the valid range, the corresponding mood is returned as JSON.
        The '_id' field is removed from the response for cleaner representation.
        If the specified index is out of range, a 'Not found' response with a 404 status is returned.

        Args:
            mood_id (str): The index of the mood to retrieve.

        Returns:
            Flask response: JSON representation of the mood or a 'Not found' response.
        """
        try:
            # Access database and collection from the current app context
            db_moods = current_app.config['MONGO_DB_MOODS']
            # Fetch all documents in the users collection
            moods_collection = db_moods.find({})  # cursor
            data = list(moods_collection)

            # TODO: improve obtaining mood_id with ObjectId properly not as below

            # fix python index start at 0,
            # if you request mood_id=2 
            # you would get python_id=3 because [0, 1, 2]
            selected_index = int(mood_id) - 1

            # Make sure requested index is between zero and database length
            if 0 <= selected_index < len(data):
                mood = data[selected_index]
                mood.pop('_id')  # Remove the _id field from the response because mongoDB ObjectId sucks for retrieving
                return jsonify(mood)
            else:
                # If index not in database (negative values or higher than database lenght)
                response_data = {
                    "error": f"Mood with id={selected_index +1} not found"
                }
                return jsonify(response_data), 404

        except Exception as e:
            response_data = {
                "error": str(e)
            }
            return jsonify(response_data), 500
