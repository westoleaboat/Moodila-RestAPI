from mongoengine import Document, StringField

class UserModel(Document):
    username = StringField(required=True, unique=True, max_length=80)
    email = StringField(required=True, unique=True)
    password = StringField(required=True, max_length=256)
