from database.models import PlayerStat, Map
from playhouse.shortcuts import model_to_dict

def get_top_players_of_match(match_id: str, map_num: int):
    stats: list[PlayerStat] = (
        PlayerStat.select(PlayerStat)
        .join(Map)
        .where((Map.match_id == match_id) & (Map.map_num == map_num))
    )

    stats_dicts = []
    for stat in stats:
        map: Map = stat.map
        rating = calculate_hltv_rating_brazil(stat, map.team1_score + map.team2_score)
        stat = model_to_dict(stat)
        stat["hltv_rating"] = rating
        # stat.pop("map")
        stats_dicts.append(stat)
    return stats_dicts

# https://dave.コム/posts/reverse-engineering-hltv-rating/
def calculate_hltv_rating_dave(playerstat: PlayerStat, total_rounds: int):
    return (
        (0.3591 * (playerstat.kills / total_rounds)) +
        (-0.5329 * (playerstat.deaths / total_rounds)) +
        (0.2372 * ((2.13 * (playerstat.kills / total_rounds)) + (0.42 * (playerstat.assists / total_rounds)) - 0.41)) +
        (0.0032 * playerstat.adr) +
        0.1587
    )

# https://www.hltv.org/forums/threads/2433094/rating-20
def calculate_hltv_rating_brazil(playerstat: PlayerStat, total_rounds: int):
    kpr = playerstat.kills / total_rounds
    dpr = playerstat.deaths / total_rounds
    return (
        (0.405022 * kpr) +
        (-0.657678 * dpr) +
        (
            (
                ((kpr - 0.1585) / 0.4938) +
                ((1 - dpr) / 0.3041) +
                ((playerstat.adr - 24.32) / 48.74)
            ) / 5
        ) +
        (0.00410341 * playerstat.adr) +
        0.343334
    )
