# import uuid
from flask import request, current_app, render_template, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bson import ObjectId
import json
from tabulate import tabulate
from schemas import MoodSchema
from datetime import datetime
from flask_socketio import send, emit
from app import socketio

# Create a Blueprint instance
mood_blp = Blueprint("moods", __name__, description="Operations on moods")


# handle ID 
# @socketio.on('selected_id')
# def handle_console_log_id(message):
#     global selected_id
#     if 'value' in data:
#         # selected_id = message['value']
#         selected_id = data.get('value')
#         print(f'this is your item id: \n{selected_id}\n')
#     if 'indexnum' in data:
#         tab_index = message['indexnum']
#         print(f'this is your item INDEX: \n{tab_index}\n')

#     else:
#         print('invalid message format')
#     return selected_id


# selected_id = None
                    
                    
# selected_id = None


# Define the route
@mood_blp.route('/')
class MoodList(MethodView):
    def get(self):
        """
        Retrieve and display moods based on their creation date.

        Accesses the MongoDB client and database from the current app context,
        retrieves all mood documents from the 'Moodila' database, and categorizes
        them based on their creation date. Moods created today, within the last
        week, and older moods are separated into different lists. Each mood's
        '_id' field is removed, and an 'index' field is added with the current
        index. The 'created_at' date is formatted for display. Finally, the 
        retrieved moods are passed to the 'index.html' template for rendering.

        Returns:
            Flask response: Rendered HTML template.
        """
        # global selected_id
        # selected_id = None

        try:
            # selected_id = None

            # Access database and collection from the current app context
            db_moods = current_app.config['MONGO_DB_MOODS']

            # Fetch all mood documents from the collection
            moods_collection = db_moods.find({})

            # Convert the cursor to a list of dictionaries
            data = list(moods_collection)

            # Separate moods based on 'created_at' date
            today_moods = []
            this_week_moods = []
            older_moods = []

            # Define today's date without time
            today = datetime.utcnow().date()

            # Format today's date as 'day month year'
            today_date = today.strftime('%d %b %Y')

            # Parse today_date string to datetime.date object
            today_date_obj = datetime.strptime(today_date, '%d %b %Y').date()

            # Iterate over each mood in the data
            for i, item in enumerate(data, start=1):
                # Remove the '_id' field from each dictionary
                item.pop("_id")
                # Add an 'index' field with the current index
                item["index"] = i
                # Format the 'created_at' date for display
                item["formatted_created_at"] = datetime.strftime(item["created_at"], '%d %b')

                # Check if the mood was created today
                if item['created_at'].date() == today:
                    today_moods.append(item)
                # Check if the mood was created within the last 7 days
                elif (today_date_obj - item['created_at'].date()).days <= 7:
                    this_week_moods.append(item)
                # Otherwise, the mood is older
                else:
                    older_moods.append(item)

            
            

            selected_id = data[0]
            # Handle the 'selected_id' event from the client
            @socketio.on('selected_id')
            def handle_selected_id(message):
                global selected_id
                
                if 'value' in message and 'indexnum' in message:
                    # selected_id = message['value']
                    new_selected_id = message['value']
                    if new_selected_id is not None:
                        selected_id = new_selected_id
                    tab_index = message['indexnum']
                    print(f'This is your item id: {selected_id}')
                    print(f'This is your item index: {tab_index}')
                    print(selected_id)

                    return selected_id


                else:
                    print('Invalid message format')
                    return None
            
            



            # Render the 'index.html' template with the categorized moods
            # return render_template('index.html',
            #                        moods=data,
            #                        today_date=today_date,
            #                        today_moods=reversed(today_moods),
            #                        this_week_moods=reversed(this_week_moods),
            #                        older_moods=reversed(older_moods),
            #                        selected_id=selected_id)
            return jsonify(data)

        except Exception as e:
            # Handle exceptions and return an appropriate JSON response
            response_data = {"error": str(e)}
            return jsonify(response_data), 500


            # Print data as a table with loop index
            # table_data = [(i + 1, mood) for i, mood in enumerate(data)]
            # table_headers = ["Index", "Data"]
            # table_format = "html"  # You can change it to "grid", "pipe", "html", etc.

            # print(tabulate(table_data, headers=table_headers, tablefmt=table_format))


# Add a mood
@mood_blp.route("/mood")
class AddMood(MethodView):
    @mood_blp.arguments(MoodSchema(exclude=['created_at']))
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
            # Access database and collection from current app context
            db_moods = current_app.config['MONGO_DB_MOODS']

            # Get mood data from JSON payload in the POST request
            # mood_data = request.json

            # Set 'created_at' to the current time
            mood_data['created_at'] = datetime.utcnow()

            # Create a new mood dictionary from JSON payload
            new_mood = {
                'title': mood_data["title"],
                'quote': mood_data["quote"],
                'author': mood_data["author"],
                # 'created_at': mood_data['created_at'].strftime('%d %b - %H:%M')
                'created_at': mood_data['created_at']
            }

            # Insert the new mood into the MongoDB collection
            db_moods.insert_one(new_mood)
            new_mood.pop("_id") # avoid ObjectId bug

            # Format 'created_at' to display only the day and time
            # new_mood['formatted_created_at'] = new_mood['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            # Return a success message
            response_data = {
                "message": "Mood added successfully.",
                "mood_data": new_mood
            }
            return jsonify(response_data), 201

        except Exception as e:
            # Handle exceptions and return an appropriate JSON response
            response_data = {
                "error": str(e)
            }
            return jsonify(response_data), 500

@mood_blp.route('/mood/<string:mood_id>')
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