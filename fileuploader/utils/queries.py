from models import Project, Client,User
from flask import abort

def get_project_data_or_abort(projectid):
    project_data = Project.query.filter_by(projectid=projectid).first()
    if not project_data:
        abort(400, "Project not found")
    return project_data

def get_client_data_or_abort(clientid):
    client_data = Client.query.filter_by(clientid=clientid).first()
    if not client_data:
        abort(400, "Client already exists")
    return client_data

def get_user_data_or_abort(userid):
    userids = User.query.filter_by(userid=userid).first()
    if not userids:
        abort(400, "User does not exist")
    return userids