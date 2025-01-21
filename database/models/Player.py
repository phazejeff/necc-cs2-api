from database import BaseModel
from database.models import Team
from peewee import *

class Player(BaseModel):
    player_id = TextField(primary_key=True)
    team = ForeignKeyField(Team, backref='players')
    nickname = TextField()
    avatar = TextField()
    level = SmallIntegerField()

    @staticmethod
    def initialize(player: dict, team: dict):
        return Player(
            player_id = player.get("player_id"),
            team = team.get("faction_id"),
            nickname = player.get("nickname"),
            avatar = player.get("avatar"),
            level = player.get("game_skill_level")
        )