from flask import Flask, request, abort, jsonify
from models import db, LoginAuth, Client, User, File, FileStatus, UserRoles, Project
from hashlib import sha256
from utils.auth import *
from utils.queries import *
import shutil,os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fileuploader.db'
app.config["FILE_UPLOAD"] = "/home/asus/portfolio2025/fileuploader/files/"
app.config["FILE_DOWNLOAD"] = "/home/asus/portfolio2025/fileuploader/files/DOWNLOAD"
db.init_app(app)
# next steps
# Sure, here are the **5 points only**:

# 1. Use a **salt** with password hashing to prevent rainbow table attacks.  
# 2. Use `secure_filename()` to sanitize uploaded file names.  
# 3. Validate **file type and size** before accepting uploads.  
# 4. Store uploaded files with **unique names** (e.g., UUIDs).  
# 5. Wrap all file operations in **try-except blocks** to handle errors safely.
with app.app_context():
    db.create_all()  # Only create tables if they don't exist
    
    # Only add initial data if it doesn't exist
    if not LoginAuth.query.first():
        new_data = LoginAuth(uname="XYZ_U_1", password=sha256("pass".encode()).hexdigest()[:8])
        db.session.add(new_data)
        db.session.commit()

    # Check if client data exists before adding
    if not Client.query.filter_by(clientid="XYZ_C_1").first():
        client_data = Client(
            clientid="XYZ_C_1",
            clientname="GBS",
        )
        db.session.add(client_data)

    if not Client.query.filter_by(clientid="XYZ_C_2").first():
        client_data1 = Client(
            clientid="XYZ_C_2",
            clientname="GBS",
        )
        db.session.add(client_data1)
    
    if not Project.query.filter_by(projectid="XYZ_P_1").first():
        project_data = Project(
            projectid="XYZ_P_1",
            clientid="XYZ_C_1",
            projectname="Accounting",
        )
        db.session.add(project_data)

    if not Project.query.filter_by(projectid="XYZ_P_2").first():
        project_data1 = Project(
            clientid="XYZ_C_2",
            projectid="XYZ_P_2",
            projectname="Costing",
        )
        db.session.add(project_data1)


    if not User.query.filter_by(userid="XYZ_U_1").first():
        user_data = User(
            userid="XYZ_U_1",
            username="sowmya",
            role="admin",
            projectid="XYZ_P_1"
        )
        db.session.add(user_data)

    db.session.commit()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    userid = data.get("userid")
    password = data.get("password")
    password = sha256(password.encode()).hexdigest()
    get_records = LoginAuth.query.filter_by(userid=userid).first()
    user_data = User.query.filter_by(userid=userid).first()
    if get_records and get_records.password != password:
        abort(400, "Unauthorized contact admin for login")
    if not get_records and user_data:
        db.session.add(LoginAuth(uname=userid, password=password))
        db.session.commit()
    elif not get_records or not user_data:
        abort(400, "Unauthorized contact admin for login")
    return get_token(userid, user_data.role.value)

@app.route("/adduser", methods=["POST"])
@require_roles(UserRoles.admin.value)
def add_user():
    user_data = request.get_json()
    userid=user_data["userid"]
    username=user_data["username"]
    role=user_data["role"]
    project_data=get_project_data_or_abort(user_data["projectid"])
    db.session.add(User(userid=userid, username=username,role=role, projectid=project_data.projectid ))
    db.session.commit()
    return "User added successfully"

@app.route("/addclient", methods=["POST"])
@require_roles(UserRoles.admin.value)
def add_client():
    client_project_data = request.get_json()
    clientid=client_project_data["clientid"]
    clientname=client_project_data["clientname"]
    clientdata=Client.query.filter_by(clientid=clientid).first()
    if clientdata:
        abort(400, "Client already exists")
    db.session.add(Client(clientid=clientid, clientname=clientname))
    db.session.commit()
    return "Client added successfully"

@app.route("/addproject", methods=["POST"])
@require_roles(UserRoles.admin.value)
def add_project():
    client_project_data = request.get_json()
    clientid=client_project_data["clientid"]
    projectid=client_project_data["projectid"]
    projectname=client_project_data["projectname"]
    clientdata=get_client_data_or_abort()
    project_id=Project.query.filter_by(projectid =projectid).first()
    if project_id:
        abort(400, "Client and Project already exists")
    db.session.add(Project(projectid=projectid, projectname=projectname, clientid=client_data.clientid))
    db.session.commit()
    return "Project added successfully"

@app.route("/upload", methods=["POST"])
@require_roles([UserRoles.admin.value, UserRoles.csm.value, UserRoles.manager.value])
def upload():
    file = request.files.get("file")
    data = request
    if not file or not file.filename:
        abort(400, "No file")
    status = data.form.get("status")
    project_id = data.form.get("projectid")
    poc=data.form.get("poc")
    if status not in [_.value  for _ in FileStatus]:
        abort(400, "Not a valid status")
    project_ids = get_project_data_or_abort(project_id)
    userids = get_user_data_or_abort(poc)
    file_info = File(filename =file.filename,
    status = status,
    projectid = project_ids.projectid,
    poc=userids.userid)
    file.save(app.config["FILE_UPLOAD"]+file.filename)
    db.session.add(file_info)
    db.session.commit()
    print(File.query.all())
    return "File addded"
    
@app.route("/delete", methods=["POST"])
@require_roles([UserRoles.admin.value, UserRoles.csm.value, UserRoles.manager.value])
def delete():
    data=request.get_json()
    project_id = data.get("projectid")
    userid=data.get("userid")
    project_ids = get_project_data_or_abort(project_id)
    userids = get_user_data_or_abort(userid)
    if userids.projectid != project_ids.projectid:
        abort(400, "User cannot delete as they are not assigned to the project")
    file_info = File.query.filter_by(projectid=project_ids.projectid).first()
    if not file_info:
        abort(400, "No files to delete")
    if file_info.poc == userid and file_info.status != "Deleted":
            file_info.status = "Deleted"
            if userids.role.value != "admin":
                db.session.add(file_info)
                db.session.commit()
            else:
                db.session.delete(file_info)
                db.session.commit()
                os.remove(app.config["FILE_UPLOAD"]+file_info.filename)
    return "File deleted"


@app.route("/download", methods=["POST"])
@require_roles([UserRoles.admin.value, UserRoles.csm.value, UserRoles.manager.value, UserRoles.dev.value])
def download():
    data=request.get_json()
    project_id = data.get("projectid")
    userid=data.get("userid")
    project_ids = get_project_data_or_abort(project_id)
    userids = get_user_data_or_abort(userid)
    file_info = File.query.all()
    for i in file_info:
        if i.projectid == project_ids.projectid and i.poc == userids.userid and i.status != "Deleted":
            shutil.copy(app.config["FILE_UPLOAD"]+"/"+i.filename,app.config["FILE_DOWNLOAD"]+"/")
    return "File downloaded"

@app.route("/files")
@require_roles([UserRoles.admin.value, UserRoles.csm.value, UserRoles.manager.value, UserRoles.dev.value])
def get_files():
    file_info = File.query.all()
    res = []
    for i in file_info:
        res.append({"project": i.projectid, "poc": i.poc, "file": i.filename, "status": i.status.value})
    return jsonify(res)


@app.route("/users")
@require_roles([UserRoles.admin.value, UserRoles.manager.value])
def get_users():
    user_data = User.query.all()
    res = []
    for i in user_data:
        res.append({"project": i.projectid, "poc": i.userid, "role": i.role.value})
    print(res)
    return jsonify(res)

@app.route("/projects")
@require_roles([UserRoles.admin.value, UserRoles.manager.value])
def get_projects():
    user_data = Project.query.all()
    res = []
    for i in user_data:
        res.append({"project": i.projectname})
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True)