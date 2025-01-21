from database.models import Placement, Team

placements = Placement.select().order_by(Placement.national_points.desc()).where(Placement.fall_playoff_placement != 1)

for pos, placement in enumerate(placements):
    placement: Placement
    print(f"{pos + 1}: {placement.team_id.name} ({placement.national_points})")