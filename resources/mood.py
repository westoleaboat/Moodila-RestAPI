# import uuid
from flask import request, current_app, render_template, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

# Create a Blueprint instance
blp = Blueprint("moods", __name__, description="Operations on moods")

# Define the route
@blp.route('/')
class MoodList(MethodView):
    # @blp.response(200)#, description='User created successfully.',schema=UserSchema)
    def get(self):
        """
        Handle GET requests to the / endpoint.

        Accesses MongoDB client and database from the current app context,
        retrieves all documents from the 'users' collection in the 'Moodila'
        database, converts the cursor to a list of dictionaries, and prints
        the retrieved data. Finally, renders the 'index.html' template with
        the retrieved data.

        Returns:
            Flask response: Rendered HTML template.
        """
        # Access database and collection from current app context
        db_moods = current_app.config['MONGO_DB_MOODS']

        # Fetch all documents in the users collection
        moods_collection = db_moods.find({}) # cursor
        # print(users_collection) # debuggin purposes

        # Convert the cursor to a list of dictionaries
        data = list(moods_collection)

        print(data)

        # Render the template with the retrieved data
        return render_template('index.html', moods=data)#
