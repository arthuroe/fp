import os

from flask import Flask
from flask_cors import CORS

from config import app_configuration

app = Flask(__name__)

environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])

from api.models import db
from api.auth import auth_blueprint
from api.articles import articles_blueprint
from api.fantasy_leagues import fantasy_league_blueprint
from api.fantasy_teams import fantasy_team_blueprint
from api.fixtures import fixtures_blueprint
from api.game_week import game_week_blueprint
from api.players import players_blueprint
from api.seasons import seasons_blueprint
from api.teams import teams_blueprint
from api.users import user_blueprint
from api.gameweek_stats import gameweek_stats_blueprint

db.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(teams_blueprint)
app.register_blueprint(seasons_blueprint)
app.register_blueprint(players_blueprint)
app.register_blueprint(fantasy_team_blueprint)
app.register_blueprint(fantasy_league_blueprint)
app.register_blueprint(articles_blueprint)
app.register_blueprint(fixtures_blueprint)
app.register_blueprint(game_week_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(gameweek_stats_blueprint)


# add support for CORS for all end points
CORS(app)


@app.route('/')
def index():
    return "Welcome to the Fantasy Rugby Api"
