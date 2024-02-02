# import uuid
from flask import request, current_app, render_template, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson import ObjectId
import json
from tabulate import tabulate


# Create a Blueprint instance
blp = Blueprint("moods", __name__, description="Operations on moods")

# Define the route
@blp.route('/')
class MoodList(MethodView):
    # @blp.response(200)#, description='User created successfully.',schema=UserSchema)
    def get(self):
        """
        List all Moods in Database

        Accesses MongoDB client and database from the current app context,
        retrieves all documents from the 'users' collection in the 'Moodila'
        database, converts the cursor to a list of dictionaries, and prints
        the retrieved data. Finally, renders the 'index.html' template with
        the retrieved data.

        Returns:
            Flask response: Rendered HTML template.
        """
        try:
            # Access database and collection from current app context
            db_moods = current_app.config['MONGO_DB_MOODS']

            # Fetch all documents in the users collection
            moods_collection = db_moods.find({}) # cursor
            # print(users_collection) # debuggin purposes

            # Convert the cursor to a list of dictionaries
            data = list(moods_collection)

            # Remove the '_id' field from each dictionary in 'data'
            for i, item in enumerate(data, start=1):
                item.pop("_id")
                item["index"] = i  # Add an 'index' field with the current index

            return jsonify(data)

        except Exception as e:
                # Handle exceptions and return an appropriate JSON response
                response_data = {
                    "error": str(e)
                }
                return jsonify(response_data), 500

        # return jsonify(data)

        # # # Print data as a table with loop index
        # table_data = [(i + 1, mood) for i, mood in enumerate(data)]
        # table_headers = ["Index", "Data"]
        # table_format = "grid"  # You can change it to "grid", "pipe", "html", etc.

        # print(tabulate(table_data, headers=table_headers, tablefmt=table_format))
        

        # Render the template with the retrieved data
        # return render_template('index.html', moods=data)#

@blp.route('/mood/<string:mood_id>')
# @blp.route('/mood/<i:mood_id>')
class Mood(MethodView):
    '''
    The endpoint now expects an ObjectId for the mood_id parameter, assuming that the _id in MongoDB is of type ObjectId.


    The get method retrieves the mood with the specified mood_id from the MongoDB collection and returns it as JSON. If the mood is not found, it returns a 404 Not Found response.
    The delete method deletes the mood with the specified mood_id from the MongoDB collection. It returns a success message if the mood is deleted successfully and a 404 Not Found response if the mood is not found.
    '''
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

    # def delete(self, mood_id):
    #     try:
    #         # Access database and collection from the current app context
    #         db_moods = current_app.config['MONGO_DB_MOODS']

    #         # Delete the document with the specified mood_id
    #         result = db_moods.delete_one({"_id": mood_id})

    #         # Check if the document was deleted successfully
    #         if result.deleted_count > 0:
    #             response_data = {
    #                 "message": f"Mood with ID {mood_id} deleted successfully."
    #             }
    #             return jsonify(response_data)
    #         else:
    #             # Return a 404 Not Found response if mood_id is not found
    #             response_data = {
    #                 "error": "Mood not found."
    #             }
    #             return jsonify(response_data), 404

    #     except Exception as e:
    #         response_data = {
    #             "error": str(e)
    #         }
    #         return jsonify(response_data), 500