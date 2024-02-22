from mongoengine import Document, StringField, ListField

class UserModel(Document):
    """ Define the User for MongoDB. 
    In MongoDB with "mongoengine", the "id" field is automatically 
    created for each document as the primary key (the "_id" field). 
    """

    username = StringField(required=False, unique=True, max_length=80)
    email = StringField(required=True, unique=True)
    password = StringField(required=True, max_length=256)
    team = ListField(StringField(), default=[])

    def add_team(self, team_name):
        if team_name not in self.teams:
            self.teams.append(team_name)
            self.save()

    def remove_team(self, team_name):
        if team_name in self.teams:
            self.teams.remove(team_name)
            self.save()
