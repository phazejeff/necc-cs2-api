from database.models import Placement
from necc import nationals_table

def update_national_points(team_id: str):
    placement_db: Placement = Placement.get(Placement.team_id == team_id)
    placement_db.national_points = (
        nationals_table["season"][placement_db.fall_season_placement] +
        nationals_table["season"][placement_db.spring_season_placement] +
        nationals_table["playoffs"][placement_db.fall_playoff_placement] +
        nationals_table["playoffs"][placement_db.spring_playoff_placement]
    )
    placement_db.save()