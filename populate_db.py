'''
Script to populate a database with Fall 2024 data.
'''

from faceit import Faceit
from database.models import Team, Player, TeamCaptain, Match, Map, PlayerStat, Placement
from database import database
import os
from datetime import datetime
import uuid
from pprint import pprint
import json

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
        print(match.get("teams").get("faction1").get("name"))
        print(match.get("teams").get("faction2").get("name"))
        if match.get("status") == "CANCELLED":
            continue

        match_stats: dict = faceit.get_match_stats(match.get("match_id"))

        team1: dict = match.get("teams").get("faction1")
        team1_db = Team(
            team_id = team1.get("faction_id"),
            group = match.get("group"),
            name = team1.get("name"),
            avatar = match.get("avatar")
        )
        team2: dict = match.get("teams").get("faction2")
        team2_db = Team(
            team_id = team2.get("faction_id"),
            group = match.get("group"),
            name = team2.get("name"),
            avatar = match.get("avatar")
        )

        if team1_db not in teams_db:
            teams_db.append(team1_db)
        if team2_db not in teams_db:
            teams_db.append(team2_db)

        for player in team1.get("roster"):
            player: dict
            player_db = Player(
                player_id = player.get("player_id"),
                team = team1.get("faction_id"),
                nickname = player.get("nickname"),
                avatar = player.get("avatar"),
                level = player.get("game_skill_level")
            )
            if player_db not in players_db:
                players_db.append(player_db)

        for player in team2.get("roster"):
            player: dict
            player_db = Player(
                player_id = player.get("player_id"),
                team = team2.get("faction_id"),
                nickname = player.get("nickname"),
                avatar = player.get("avatar"),
                level = player.get("game_skill_level")
            )
            if player_db not in players_db:
                players_db.append(player_db)

        winner_faction_num = match.get("results").get("winner")
        match_db = Match(
            match_id = match.get("match_id"),
            url = match.get("faceit_url"),
            week = match.get("round"),
            finished_at = datetime.fromtimestamp(match.get("finished_at")),
            team1 = team1.get("faction_id"),
            team2 = team2.get("faction_id"),
            winner = match.get("teams").get(winner_faction_num).get("faction_id")
        )

        if match_db not in matches_db:
            matches_db.append(match_db)
        
        rounds = match_stats.get("rounds")
        if rounds == None:
            continue

        for map in match_stats.get("rounds"):
            map: dict
            map_stats: dict = map.get("round_stats")
            teams: list[dict] = map.get("teams")
            team1_stats: dict = teams[0].get("team_stats")
            team2_stats: dict = teams[1].get("team_stats")
            map_db = Map(
                map_id = uuid.uuid4(),
                match_id = match.get("match_id"),
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

            if map_db not in maps_db:
                maps_db.append(map_db)

            for team in teams:
                players: list[dict] = team.get("players")
                for player in players:
                    playerstats: dict = player.get("player_stats")
                    playerstat_db = PlayerStat(
                        map_id=map_db,
                        player_id=player.get("player_id"),
                        one_v_one_count=int(playerstats.get("1v1Count", 0)),
                        one_v_one_wins=int(playerstats.get("1v1Wins", 0)),
                        one_v_two_count=int(playerstats.get("1v2Count", 0)),
                        one_v_two_wins=int(playerstats.get("1v2Wins", 0)),
                        adr=float(playerstats.get("ADR", 0)),
                        assists=int(playerstats.get("Assists", 0)),
                        clutch_kills=int(playerstats.get("Clutch Kills", 0)),
                        damage=int(playerstats.get("Damage", 0)),
                        deaths=int(playerstats.get("Deaths", 0)),
                        double_kills=int(playerstats.get("Double Kills", 0)),
                        enemies_flashed=int(playerstats.get("Enemies Flashed", 0)),
                        enemies_flashed_per_round=float(playerstats.get("Enemies Flashed per Round in a Match", 0.0)),
                        entry_count=int(playerstats.get("Entry Count", 0)),
                        entry_wins=int(playerstats.get("Entry Wins", 0)),
                        first_kills=int(playerstats.get("First Kills", 0)),
                        flash_count=int(playerstats.get("Flash Count", 0)),
                        flash_success_rate=float(playerstats.get("Flash Success Rate per Match", 0.0)),
                        flash_successes=int(playerstats.get("Flash Successes", 0)),
                        flashes_per_round=float(playerstats.get("Flashes per Round in a Match", 0.0)),
                        headshots=int(playerstats.get("Headshots", 0)),
                        headshot_percentage=int(playerstats.get("Headshots %", 0)),
                        kd_ratio=float(playerstats.get("K/D Ratio", 0.0)),
                        kr_ratio=float(playerstats.get("K/R Ratio", 0.0)),
                        kills=int(playerstats.get("Kills", 0)),
                        knife_kills=int(playerstats.get("Knife Kills", 0)),
                        mvps=int(playerstats.get("MVPs", 0)),
                        match_one_v_one_win_rate=float(playerstats.get("Match 1v1 Win Rate", 0.0)),
                        match_one_v_two_win_rate=float(playerstats.get("Match 1v2 Win Rate", 0.0)),
                        match_entry_rate=float(playerstats.get("Match Entry Rate", 0.0)),
                        match_entry_success_rate=float(playerstats.get("Match Entry Success Rate", 0.0)),
                        penta_kills=int(playerstats.get("Penta Kills", 0)),
                        pistol_kills=int(playerstats.get("Pistol Kills", 0)),
                        quadro_kills=int(playerstats.get("Quadro Kills", 0)),
                        sniper_kill_rate=float(playerstats.get("Sniper Kill Rate per Match", 0.0)),
                        sniper_kill_rate_per_round=float(playerstats.get("Sniper Kill Rate per Round", 0.0)),
                        sniper_kills=int(playerstats.get("Sniper Kills", 0)),
                        triple_kills=int(playerstats.get("Triple Kills", 0)),
                        utility_count=int(playerstats.get("Utility Count", 0)),
                        utility_damage=int(playerstats.get("Utility Damage", 0)),
                        utility_damage_success_rate=float(playerstats.get("Utility Damage Success Rate per Match", 0.0)),
                        utility_damage_per_round=float(playerstats.get("Utility Damage per Round in a Match", 0.0)),
                        utility_enemies=int(playerstats.get("Utility Enemies", 0)),
                        utility_success_rate=float(playerstats.get("Utility Success Rate per Match", 0.0)),
                        utility_successes=int(playerstats.get("Utility Successes", 0)),
                        utility_usage_per_round=float(playerstats.get("Utility Usage per Round", 0.0)),
                        zeus_kills=int(playerstats.get("Zeus Kills", 0)),
                    )
                    
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


placements_db: list[Placement] = []
for i in range(1, GROUP_AMOUNT + 1):
    positions = faceit.get_rankings(TOURNAMENT_ID, i)
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


for third_place_id in THIRD_PLACE_IDS:
    playoff = faceit.get_playoff_rankings(third_place_id).get("items")
    for item in playoff:
        for team in item.get("placements"):
            placement_db: Placement = Placement.get(Placement.team_id == team.get("id"))
            placement_db.fall_playoff_placement = item.get("bounds").get("left") + 2
            placement_db.save()