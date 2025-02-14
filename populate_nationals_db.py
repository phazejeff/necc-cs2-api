'''
Used to populate the placements database one-time. Only run per division.
'''
from faceit import Faceit
from database.models import Team, Player, TeamCaptain, Match, Map, PlayerStat, Placement
from database import database
import os
import json
from peewee import DoesNotExist

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

FACEIT_KEY = os.getenv("FACEIT_KEY")
TOURNAMENT_IDS = json.loads(os.getenv("FACEIT_TOURNAMENT_IDS"))
PLAYOFF_IDS = json.loads(os.getenv("FACEIT_PLAYOFFS_IDS"))
THIRD_PLACE_IDS = json.loads(os.getenv("FACEIT_THIRD_PLACE_IDS"))
GROUP_AMOUNT = int(os.getenv("FACEIT_GROUP_AMOUNT"))
faceit = Faceit(FACEIT_KEY)

database.connect()
database.create_tables([Team, Player, TeamCaptain, Match, Map, PlayerStat, Placement])

placements_db: list[Placement] = []
tournament_id = TOURNAMENT_IDS[0]
for i in range(1, GROUP_AMOUNT + 1):
    positions = faceit.get_rankings(tournament_id, i)
    for num, pos in enumerate(positions):
        placement_db = Placement(
            team_id = pos.get("player").get("user_id"),
            fall_season_placement = num + 1
        )
        placements_db.append(placement_db)

with database.atomic():
    Placement.bulk_create(placements_db, batch_size=50)

for playoff_id in PLAYOFF_IDS:
    playoff = faceit.get_playoff_rankings(playoff_id).get("items")
    for item in playoff:
        for team in item.get("placements"):
            placement_db: Placement = Placement.get(Placement.team_id == team.get("id"))
            placement_db.fall_playoff_placement = item.get("bounds").get("left")
            placement_db.save()

Placement.update_all_national_points()