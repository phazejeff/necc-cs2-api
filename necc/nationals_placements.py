from database.models import Team, Placement
from playhouse.shortcuts import model_to_dict

def get_national_placements(division: int, ignoredQualified: bool):
    placements: list[Placement] = (Placement
        .select(Placement, Team)
        .join(Team, on=(Placement.team_id == Team.team_id), attr='team')
        .where(Team.division == division)
        .order_by(Placement.national_points.desc())
        )

    if ignoredQualified:
        placements = placements.where(Placement.fall_playoff_placement != 1)
        placements = placements.where(Placement.spring_playoff_placement != 1)

    placements_list: list[dict] = []
    for placement in placements:
        placement_dict = model_to_dict(placement)
        placement_dict['team'] = model_to_dict(placement.team)
        placements_list.append(placement_dict)
    
    return placements_list