from database import BaseModel
from database.models import Match, Team
import uuid
from peewee import *

class Map(BaseModel):
    match_id = ForeignKeyField(Match, backref='maps')
    map_id = UUIDField(primary_key=True)
    map_num = SmallIntegerField()
    team1_score = SmallIntegerField()
    team2_score = SmallIntegerField()
    winner = ForeignKeyField(Team, backref='maps_won')
    map = TextField()
    team1_first_half_score = SmallIntegerField()
    team2_first_half_score = SmallIntegerField()
    team1_second_half_score = SmallIntegerField()
    team2_second_half_score = SmallIntegerField()
    team1_overtime_score = SmallIntegerField()
    team2_overtime_score = SmallIntegerField()

    @staticmethod
    def initialize(map: dict, match: dict):
        map_stats: dict = map.get("round_stats")
        teams: list[dict] = map.get("teams")
        team1_stats: dict = teams[0].get("team_stats")
        team2_stats: dict = teams[1].get("team_stats")
        return Map(
            map_id = uuid.uuid4(),
            match = match.get("match_id"),
            map_num = map.get("match_round"),
            map = map_stats.get("Map"),
            winner = map_stats.get("Winner"),
            team1_score = team1_stats.get("Final Score"),
            team2_score = team2_stats.get("Final Score"),
            team1_first_half_score = team1_stats.get("First Half Score"),
            team2_first_half_score = team2_stats.get("First Half Score"),
            team1_second_half_score = team1_stats.get("Second Half Score"),
            team2_second_half_score = team2_stats.get("Second Half Score"),
            team1_overtime_score = team1_stats.get("Overtime score"),
            team2_overtime_score = team2_stats.get("Overtime score"),
            team1 = teams[0].get("team_id"),
            team2 = teams[1].get("team_id")
        )