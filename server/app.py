from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            messages_dict = message.to_dict()
            messages.append(messages_dict)

        response = make_response(
            messages,
            200
        )
        return response

    elif request.method == 'POST':
        new_message = Message(
            body=request.json.get("body"),
            username=request.json.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        messages_dict = new_message.to_dict()

        response = make_response(
            messages_dict,
            201
        )

        return response

@app.route('/messages/<int:id>', methods=['GET','PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if message is None:
        response_body = {
            "message": "This record does not exist in our database. Please try again"
        }
        response = make_response(jsonify(response_body), 404)
        return response

    if request.method == 'GET':
        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200
        )
        return response

    elif request.method == 'PATCH':
        data = request.get_json()  # Parses JSON input
        for attr, value in data.items():
            setattr(message, attr, value)  # Updates message attributes

        db.session.commit()  # Commits changes to the database

        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200
        )
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response
        
if __name__ == '__main__':
    app.run(port=5555)


#Routes
#Build out the following routes to handle the necessary CRUD actions:

#GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
#POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
#PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
#DELETE /messages/<int:id>: deletes the message from the database.