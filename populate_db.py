'''
Script to populate a database with Fall 2024 data.
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
TOURNAMENT_ID = os.getenv("FACEIT_TOURNAMENT_ID")
PLAYOFF_IDS = json.loads(os.getenv("FACEIT_PLAYOFFS_IDS"))
THIRD_PLACE_IDS = json.loads(os.getenv("FACEIT_THIRD_PLACE_IDS"))
GROUP_AMOUNT = int(os.getenv("FACEIT_GROUP_AMOUNT"))
faceit = Faceit(FACEIT_KEY)

database.connect()
database.create_tables([Team, Player, TeamCaptain, Match, Map, PlayerStat, Placement])

players_db: list[Player] = []
matches_db: list[Match] = []
teams_db: list[Team] = []
maps_db: list[Map] = []
teamcaptain_db: list[TeamCaptain] = []
playerstats_db: list[PlayerStat] = []
offset = 0
matches: list[dict] = faceit.get_championship_matches(TOURNAMENT_ID, "past", 100, offset)
while len(matches) != 0:
    print(f"Running offset {offset}")
    for match in matches:
        try: 
            Match.get_by_id(match.get("match_id"))
        except DoesNotExist:
            continue

        team1: dict = match.get("teams").get("faction1")
        team1_db = Team.initialize(match, team1)
        team2: dict = match.get("teams").get("faction2")
        team2_db = Team.initialize(match, team2)

        if team1_db not in teams_db:
            teams_db.append(team1_db)
        if team2_db not in teams_db:
            teams_db.append(team2_db)

        match_db = Match.initialize(match, team1, team2)

        if match_db not in matches_db:
            matches_db.append(match_db)

        if team1_db.name == 'bye' or team2_db.name == 'bye':
            continue

        for player in team1.get("roster"):
            player: dict
            player_db = Player.initialize(player, team1)
            if player_db not in players_db:
                players_db.append(player_db)

        for player in team2.get("roster"):
            player: dict
            player_db = Player.initialize(player, team2)
            if player_db not in players_db:
                players_db.append(player_db)
        
        match_stats: dict = faceit.get_match_stats(match.get("match_id"))
        rounds = match_stats.get("rounds")
        if rounds == None:
            continue

        for map in match_stats.get("rounds"):
            map: dict
            map_db = Map.initialize(map, match)

            if map_db not in maps_db:
                maps_db.append(map_db)

            teams: list[dict] = map.get("teams")
            for team in teams:
                players: list[dict] = team.get("players")
                for player in players:
                    playerstat_db = PlayerStat.initialize(player, map_db)
                    
                    if playerstat_db not in playerstats_db:
                        playerstats_db.append(playerstat_db)

    offset += 100
    matches: list[dict] = faceit.get_championship_matches(TOURNAMENT_ID, "past", 100, offset)

with database.atomic():
    Team.bulk_create(teams_db, batch_size=50)
    Player.bulk_create(players_db, batch_size=50)
    Match.bulk_create(matches_db, batch_size=50)
    Map.bulk_create(maps_db, batch_size=50)
    PlayerStat.bulk_create(playerstats_db, batch_size=50)


# placements_db: list[Placement] = []
# for i in range(1, GROUP_AMOUNT + 1):
#     positions = faceit.get_rankings(TOURNAMENT_ID, i)
#     for num, pos in enumerate(positions):
#         placement_db = Placement(
#             team = pos.get("player").get("user_id"),
#             fall_season_placement = num + 1
#         )
#         placements_db.append(placement_db)

# with database.atomic():
#     Placement.bulk_create(placements_db, batch_size=50)

# for playoff_id in PLAYOFF_IDS:
#     playoff = faceit.get_playoff_rankings(playoff_id).get("items")
#     for item in playoff:
#         for team in item.get("placements"):
#             placement_db: Placement = Placement.get(Placement.team == team.get("id"))
#             placement_db.fall_playoff_placement = item.get("bounds").get("left")
#             placement_db.save()


# for third_place_id in THIRD_PLACE_IDS:
#     playoff = faceit.get_playoff_rankings(third_place_id).get("items")
#     for item in playoff:
#         for team in item.get("placements"):
#             placement_db: Placement = Placement.get(Placement.team == team.get("id"))
#             placement_db.fall_playoff_placement = item.get("bounds").get("left") + 2
#             placement_db.save()

# Placement.update_all_national_points()

print("Done.")