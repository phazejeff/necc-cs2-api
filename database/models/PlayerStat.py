from database import BaseModel
from database.models import Map, Player
from peewee import *

class PlayerStat(BaseModel):
    map = ForeignKeyField(Map, backref='player_stats')
    player = ForeignKeyField(Player, backref='stats')

    one_v_one_count = SmallIntegerField()
    one_v_one_wins = SmallIntegerField()
    one_v_two_count = SmallIntegerField()
    one_v_two_wins = SmallIntegerField()
    adr = FloatField()  # Average Damage per Round
    assists = SmallIntegerField()
    clutch_kills = SmallIntegerField()
    damage = IntegerField()
    deaths = SmallIntegerField()
    double_kills = SmallIntegerField()
    enemies_flashed = SmallIntegerField()
    enemies_flashed_per_round = FloatField()
    entry_count = SmallIntegerField()
    entry_wins = SmallIntegerField()
    first_kills = SmallIntegerField()
    flash_count = SmallIntegerField()
    flash_success_rate = FloatField()
    flash_successes = SmallIntegerField()
    flashes_per_round = FloatField()
    headshots = SmallIntegerField()
    headshot_percentage = SmallIntegerField()
    kd_ratio = FloatField()
    kr_ratio = FloatField()  # Kills per Round Ratio
    kills = SmallIntegerField()
    knife_kills = SmallIntegerField()
    mvps = SmallIntegerField()
    match_one_v_one_win_rate = FloatField()
    match_one_v_two_win_rate = FloatField()
    match_entry_rate = FloatField()
    match_entry_success_rate = FloatField()
    penta_kills = SmallIntegerField()
    pistol_kills = SmallIntegerField()
    quadro_kills = SmallIntegerField()
    sniper_kill_rate = FloatField()
    sniper_kill_rate_per_round = FloatField()
    sniper_kills = SmallIntegerField()
    triple_kills = SmallIntegerField()
    utility_count = SmallIntegerField()
    utility_damage = IntegerField()
    utility_damage_success_rate = FloatField()
    utility_damage_per_round = FloatField()
    utility_enemies = SmallIntegerField()
    utility_success_rate = FloatField()
    utility_successes = SmallIntegerField()
    utility_usage_per_round = FloatField()
    zeus_kills = SmallIntegerField()

    @staticmethod
    def initialize(player: dict, map: Map):
        playerstats: dict = player.get("player_stats")
        return PlayerStat(
            map=map,
            player=player.get("player_id"),
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