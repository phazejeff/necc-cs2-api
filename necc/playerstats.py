from database.models import PlayerStat, Player, Team, Map
from peewee import fn

def convert_to_dict(sql):
    stats = sql.dicts() 
    return list(stats)

def filter_by_division(sql, division):
    return sql.where(Team.division == division)

def filter_by_group(sql, group):
    return sql.where(Team.group == group)

# https://dave.コム/posts/reverse-engineering-hltv-rating/
def calculate_hltv_rating_dave(playerstat_dict: dict):
    if playerstat_dict.get("total_rounds") == 0 or playerstat_dict.get("total_rounds") == None:
        return 0
    return (
        (0.3591 * (playerstat_dict.get("total_kills") / playerstat_dict.get("total_rounds"))) +
        (-0.5329 * (playerstat_dict.get("total_deaths") / playerstat_dict.get("total_rounds"))) +
        (0.2372 * ((2.13 * (playerstat_dict.get("total_kills") / playerstat_dict.get("total_rounds"))) + (0.42 * (playerstat_dict.get("total_assists") / playerstat_dict.get("total_rounds"))) - 0.41)) +
        (0.0032 * playerstat_dict.get("avg_adr")) +
        0.1587
    )

# https://www.hltv.org/forums/threads/2433094/rating-20
def calculate_hltv_rating_brazil(playerstat_dict: dict):
    if playerstat_dict.get("total_rounds") == 0 or playerstat_dict.get("total_rounds") == None:
        return 0
    total_rounds = playerstat_dict.get("total_rounds")
    kpr = playerstat_dict.get("total_kills") / total_rounds
    dpr = playerstat_dict.get("total_deaths") / total_rounds
    return (
        (0.405022 * kpr) +
        (-0.657678 * dpr) +
        (
            (
                ((kpr - 0.1585) / 0.4938) +
                ((1 - dpr) / 0.3041) +
                ((playerstat_dict.get("avg_adr") - 24.32) / 48.74)
            ) / 5
        ) +
        (0.00410341 * playerstat_dict.get("avg_adr")) +
        0.343334
    )


def append_hltv_rating(dicts: list[dict]):
    for row in dicts:
        row["rating"] = calculate_hltv_rating_brazil(row)
    dicts.sort(key=lambda x: x.get("rating"), reverse=True)
    return dicts

def get_all_total_playerstats():
    return (PlayerStat
            .select(
               Player.player_id,
               Player.nickname,
               Player.avatar,
               Team.team_id.alias('team_id'),
               Team.name.alias('team_name'),
               Team.division,
               Team.group,
               fn.SUM(Map.team1_score + Map.team2_score).alias('total_rounds'),
               fn.SUM(PlayerStat.one_v_one_count).alias('total_one_v_one_count'),
               fn.SUM(PlayerStat.one_v_one_wins).alias('total_one_v_one_wins'),
               fn.SUM(PlayerStat.one_v_two_count).alias('total_one_v_two_count'),
               fn.SUM(PlayerStat.one_v_two_wins).alias('total_one_v_two_wins'),
               fn.AVG(PlayerStat.adr).alias('avg_adr'),  # Average makes more sense here
               fn.SUM(PlayerStat.assists).alias('total_assists'),
               fn.SUM(PlayerStat.clutch_kills).alias('total_clutch_kills'),
               fn.SUM(PlayerStat.damage).alias('total_damage'),
               fn.SUM(PlayerStat.deaths).alias('total_deaths'),
               fn.SUM(PlayerStat.double_kills).alias('total_double_kills'),
               fn.SUM(PlayerStat.enemies_flashed).alias('total_enemies_flashed'),
               fn.AVG(PlayerStat.enemies_flashed_per_round).alias('avg_enemies_flashed_per_round'),
               fn.SUM(PlayerStat.entry_count).alias('total_entry_count'),
               fn.SUM(PlayerStat.entry_wins).alias('total_entry_wins'),
               fn.SUM(PlayerStat.first_kills).alias('total_first_kills'),
               fn.SUM(PlayerStat.flash_count).alias('total_flash_count'),
               fn.AVG(PlayerStat.flash_success_rate).alias('avg_flash_success_rate'),
               fn.SUM(PlayerStat.flash_successes).alias('total_flash_successes'),
               fn.AVG(PlayerStat.flashes_per_round).alias('avg_flashes_per_round'),
               fn.SUM(PlayerStat.headshots).alias('total_headshots'),
               fn.AVG(PlayerStat.headshot_percentage).alias('avg_headshot_percentage'),
               # For ratios, it's better to calculate them after summing the components
               fn.SUM(PlayerStat.kills).alias('total_kills'),
               fn.SUM(PlayerStat.knife_kills).alias('total_knife_kills'),
               fn.SUM(PlayerStat.mvps).alias('total_mvps'),
               fn.AVG(PlayerStat.match_one_v_one_win_rate).alias('avg_match_one_v_one_win_rate'),
               fn.AVG(PlayerStat.match_one_v_two_win_rate).alias('avg_match_one_v_two_win_rate'),
               fn.AVG(PlayerStat.match_entry_rate).alias('avg_match_entry_rate'),
               fn.AVG(PlayerStat.match_entry_success_rate).alias('avg_match_entry_success_rate'),
               fn.SUM(PlayerStat.penta_kills).alias('total_penta_kills'),
               fn.SUM(PlayerStat.pistol_kills).alias('total_pistol_kills'),
               fn.SUM(PlayerStat.quadro_kills).alias('total_quadro_kills'),
               fn.AVG(PlayerStat.sniper_kill_rate).alias('avg_sniper_kill_rate'),
               fn.AVG(PlayerStat.sniper_kill_rate_per_round).alias('avg_sniper_kill_rate_per_round'),
               fn.SUM(PlayerStat.sniper_kills).alias('total_sniper_kills'),
               fn.SUM(PlayerStat.triple_kills).alias('total_triple_kills'),
               fn.SUM(PlayerStat.utility_count).alias('total_utility_count'),
               fn.SUM(PlayerStat.utility_damage).alias('total_utility_damage'),
               fn.AVG(PlayerStat.utility_damage_success_rate).alias('avg_utility_damage_success_rate'),
               fn.AVG(PlayerStat.utility_damage_per_round).alias('avg_utility_damage_per_round'),
               fn.SUM(PlayerStat.utility_enemies).alias('total_utility_enemies'),
               fn.AVG(PlayerStat.utility_success_rate).alias('avg_utility_success_rate'),
               fn.SUM(PlayerStat.utility_successes).alias('total_utility_successes'),
               fn.AVG(PlayerStat.utility_usage_per_round).alias('avg_utility_usage_per_round'),
               fn.SUM(PlayerStat.zeus_kills).alias('total_zeus_kills')
            )
            .join(Player)
            .join(Team)
            .switch(PlayerStat)
            .join(Map)
            .group_by(PlayerStat.player)
            )