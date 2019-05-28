import os

from flask import Flask

from config import app_configuration

app = Flask(__name__)

environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])

from api.models import db
from api.auth import auth_blueprint
from api.teams import teams_blueprint
from api.seasons import seasons_blueprint

db.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(teams_blueprint)
app.register_blueprint(seasons_blueprint)


@app.route('/')
def index():
    return "Welcome to the Fantasy Rugby Api"
