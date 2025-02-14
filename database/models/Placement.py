from database import BaseModel
from database.models import Team
from necc import nationals_table, reduction_table
from peewee import *

class Placement(BaseModel):
    team_id = TextField(primary_key=True)
    fall_season_placement = SmallIntegerField(default=0)
    fall_playoff_placement = SmallIntegerField(default=0)
    spring_season_placement = SmallIntegerField(default=0)
    spring_playoff_placement = SmallIntegerField(default=0)
    national_points = SmallIntegerField(default=0)
    fall_division = SmallIntegerField(default=0)
    spring_division = SmallIntegerField(default=0)

    @staticmethod
    def update_all_national_points():
        placements: list[Placement] = Placement.select()
        for placement in placements:
            placement.national_points = (
                nationals_table["season"][placement.fall_season_placement] +
                nationals_table["season"][placement.spring_season_placement] +
                nationals_table["playoffs"][placement.fall_playoff_placement] +
                nationals_table["playoffs"][placement.spring_playoff_placement]
            )

            division_loss = max(placement.spring_division - placement.fall_division, 0)
            placement.national_points -= (placement.national_points * reduction_table[division_loss])
            placement.national_points = round(placement.national_points)
            if division_loss >= 3:
                placement.national_points = 0
        Placement.bulk_update(placements, fields=[Placement.national_points])