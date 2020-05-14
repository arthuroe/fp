import uuid

from sqlalchemy import event
from .base_model import ModelMixin, db
from .articles import Article
from .fantasy_league import FantasyLeague
from .fantasyleague_team import FantasyLeagueTeam
from .fantasy_team import FantasyTeam
from .fantasy_team_players import FantasyTeamPlayers
from .fixtures import Fixture
from .game_week import GameWeek
from .pivot_tables import *
from .players import Player
from .season import Season
from .team import Team
from .user import User


tables = [
    Article, FantasyLeague, FantasyLeagueTeam, FantasyTeam, Fixture, GameWeek,
    Player, Season, Team, User
]


def unique_id_generator(mapper, connection, target):
    """A function to generate unique identifiers on insert."""
    target.uuid = str(uuid.uuid4())


for table in tables:
    event.listen(table, 'before_insert', unique_id_generator)
