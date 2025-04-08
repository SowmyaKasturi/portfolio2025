from flask import Flask, request, jsonify
from shortner import short_url, get_url
from models import db, URLMap
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorty.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/shorturl", methods=["POST"])
def shorturl():
    return jsonify({"url":short_url(request.get_json().get("url"))})

@app.route("/geturl/<slug>")
def geturl(slug):
    return get_url(slug)

if __name__ == '__main__':
    app.run(port=5001, debug=True)