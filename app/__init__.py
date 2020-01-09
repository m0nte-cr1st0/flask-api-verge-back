import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from config import Config


db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.debug = True
CORS(app)

app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)

ma = Marshmallow(app)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/apps')


from app import models
