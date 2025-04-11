
from flask import Flask, request, jsonify, redirect,abort
from shortner import short_url, get_url
from models import db, URLMap
from auth import basic_auth, check_api_key,generate_token,require_jwt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorty.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/shorturl", methods=["POST"])
@require_jwt
def shorturl():
    return jsonify({"url":short_url(request.get_json().get("url"))})

@app.route("/geturl/<slug>")
def geturl(slug):
    return jsonify({"url":get_url(slug)})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")
    if name == "admin" and password == "pass":
        return jsonify({"token": generate_token(name)})
    abort(401, description="Unauthorized")
    

# @app.route("/getcacheinfo")
# def get_cache_info():
#     cach_in = short_url.cache_info()
#     return jsonify({"hits": cach_in.hits, "misses": cach_in.misses})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)