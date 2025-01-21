from database import BaseModel
from database.models import Team
from peewee import *

class Placement(BaseModel):
    team_id = ForeignKeyField(Team)
    fall_season_placement = SmallIntegerField(null=True)
    fall_playoff_placement = SmallIntegerField(null=True)
    spring_season_placement = SmallIntegerField(null=True)
    fall_playoff_placement = SmallIntegerField(null=True)
    national_points = SmallIntegerField(null=True)