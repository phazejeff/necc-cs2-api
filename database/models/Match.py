from database import BaseModel
from database.models import Team
from datetime import datetime
from peewee import *

class Match(BaseModel):
    match_id = TextField(primary_key=True)
    team1 = ForeignKeyField(Team, backref='matches_as_team1')
    team2 = ForeignKeyField(Team, backref='matches_as_team2')
    winner = ForeignKeyField(Team, backref='matches_won')
    url = TextField()
    finished_at = DateTimeField()
    week = SmallIntegerField()

    @staticmethod
    def initialize(match: dict, team1: dict, team2: dict):
        winner_faction_num = match.get("results").get("winner")
        return Match(
            match_id = match.get("match_id"),
            url = match.get("faceit_url"),
            week = match.get("round"),
            finished_at = datetime.fromtimestamp(match.get("finished_at")),
            team1 = team1.get("faction_id"),
            team2 = team2.get("faction_id"),
            winner = match.get("teams").get(winner_faction_num).get("faction_id")
        )