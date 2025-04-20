import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

class FileStatus(enum.Enum):
    inqueue = "inqueue"
    progress = "progress"
    completed = "completed"
    archived = "archived"

class UserRoles(enum.Enum):
    csm = "csm"
    manager="manager"
    admin="admin"
    dev="dev"

db = SQLAlchemy()



class Client(db.Model):
    clientid = db.Column(db.String(128),primary_key=True)
    clientname = db.Column(db.String(264), nullable=False)

class Project(db.Model):
    projectid = db.Column(db.String(128),primary_key=True)
    projectname = db.Column(db.String(264), nullable=False)
    clientid = db.Column(db.String(128), db.ForeignKey(Client.clientid),nullable=False)

class User(db.Model):
    userid = db.Column(db.String(128), primary_key=True)
    username=db.Column(db.String(128), nullable=False)
    role = db.Column(Enum(UserRoles), nullable=False)
    projectid = db.Column(db.String(128), db.ForeignKey(Client.clientid))

class LoginAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(128), db.ForeignKey(User.userid),nullable=False)
    password = db.Column(db.String(64), nullable=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(264), nullable=False)
    status = db.Column(Enum(FileStatus), nullable=False, )
    projectid = db.Column(db.String(128),db.ForeignKey(Project.projectid))
    poc = db.Column(db.String(128), db.ForeignKey(User.userid))