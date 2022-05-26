from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from company.models import db
from config import DB_URL


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]  = True

db.init_app(app)
db.app = app
db.create_all()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)