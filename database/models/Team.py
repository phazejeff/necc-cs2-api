from database import BaseModel
from peewee import *

class Team(BaseModel):
    team_id = TextField(primary_key=True)
    group = SmallIntegerField()
    name = TextField()
    avatar = TextField(null=True)

    @staticmethod
    def initialize(match: dict, team: dict):
        return Team(
            team_id = team.get("faction_id"),
            group = match.get("group"),
            name = team.get("name"),
            avatar = match.get("avatar")
        )