from database.models import PlayerStat, Map, Player
from playhouse.shortcuts import model_to_dict

def get_top_players_of_map(match_id: str, map_num: int):
    stats: list[PlayerStat] = (
        PlayerStat.select(
            PlayerStat,
            (Map.team1_score + Map.team2_score).alias("total_rounds")  # Calculate total rounds    
        )
        .join(Map)
        .where((Map.match_id == match_id) & (Map.map_num == map_num))
    )
    return append_hltv_ratings_and_reorder(stats)

# This looks like a long function, but it's really just combining all the stats. and theres a hellalalalalala alot of them.
def get_top_players_of_match(match_id):
    # Get all maps in the match
    maps = Map.select().where(Map.match_id == match_id)
    
    # Get all unique players who participated in the match
    players = (Player
               .select(Player)
               .join(PlayerStat)
               .join(Map)
               .where(Map.match_id == match_id)
               .distinct())
    
    aggregated_stats = []
    
    for player in players:
        # Get all stats for this player across all maps in the match
        player_map_stats = (PlayerStat
                           .select(PlayerStat, Map)
                           .join(Map)
                           .where(
                               (PlayerStat.player == player) & 
                               (Map.match_id == match_id)
                           ))
        
        if not player_map_stats:
            continue
        
        # Create a new PlayerStat object for the aggregated stats
        agg_stat = PlayerStat()
        agg_stat.player = player
        
        # Since we're returning PlayerStat objects but don't have a real map to attach them to,
        # we'll need to handle this carefully
        # Option 1: Don't set the map field (it will be None)
        # Option 2: Set map to the first map of the match (below)
        if maps:
            agg_stat.map = maps[0]
        
        # Initialize counters
        total_rounds = 0
        total_kills = 0
        total_deaths = 0
        total_damage = 0
        total_headshots = 0
        
        # Sum up all the stats
        for stat in player_map_stats:
            map_rounds = stat.map.team1_score + stat.map.team2_score
            total_rounds += map_rounds
            total_kills += stat.kills
            total_deaths += stat.deaths
            total_damage += stat.damage
            total_headshots += stat.headshots
            
            # Sum simple stats
            agg_stat.one_v_one_count = (getattr(agg_stat, 'one_v_one_count', 0) or 0) + stat.one_v_one_count
            agg_stat.one_v_one_wins = (getattr(agg_stat, 'one_v_one_wins', 0) or 0) + stat.one_v_one_wins
            agg_stat.one_v_two_count = (getattr(agg_stat, 'one_v_two_count', 0) or 0) + stat.one_v_two_count
            agg_stat.one_v_two_wins = (getattr(agg_stat, 'one_v_two_wins', 0) or 0) + stat.one_v_two_wins
            agg_stat.assists = (getattr(agg_stat, 'assists', 0) or 0) + stat.assists
            agg_stat.clutch_kills = (getattr(agg_stat, 'clutch_kills', 0) or 0) + stat.clutch_kills
            agg_stat.deaths = (getattr(agg_stat, 'deaths', 0) or 0) + stat.deaths
            agg_stat.damage = (getattr(agg_stat, 'damage', 0) or 0) + stat.damage
            agg_stat.double_kills = (getattr(agg_stat, 'double_kills', 0) or 0) + stat.double_kills
            agg_stat.enemies_flashed = (getattr(agg_stat, 'enemies_flashed', 0) or 0) + stat.enemies_flashed
            agg_stat.entry_count = (getattr(agg_stat, 'entry_count', 0) or 0) + stat.entry_count
            agg_stat.entry_wins = (getattr(agg_stat, 'entry_wins', 0) or 0) + stat.entry_wins
            agg_stat.first_kills = (getattr(agg_stat, 'first_kills', 0) or 0) + stat.first_kills
            agg_stat.flash_count = (getattr(agg_stat, 'flash_count', 0) or 0) + stat.flash_count
            agg_stat.flash_successes = (getattr(agg_stat, 'flash_successes', 0) or 0) + stat.flash_successes
            agg_stat.headshots = (getattr(agg_stat, 'headshots', 0) or 0) + stat.headshots
            agg_stat.kills = (getattr(agg_stat, 'kills', 0) or 0) + stat.kills
            agg_stat.knife_kills = (getattr(agg_stat, 'knife_kills', 0) or 0) + stat.knife_kills
            agg_stat.mvps = (getattr(agg_stat, 'mvps', 0) or 0) + stat.mvps
            agg_stat.penta_kills = (getattr(agg_stat, 'penta_kills', 0) or 0) + stat.penta_kills
            agg_stat.pistol_kills = (getattr(agg_stat, 'pistol_kills', 0) or 0) + stat.pistol_kills
            agg_stat.quadro_kills = (getattr(agg_stat, 'quadro_kills', 0) or 0) + stat.quadro_kills
            agg_stat.sniper_kills = (getattr(agg_stat, 'sniper_kills', 0) or 0) + stat.sniper_kills
            agg_stat.triple_kills = (getattr(agg_stat, 'triple_kills', 0) or 0) + stat.triple_kills
            agg_stat.utility_count = (getattr(agg_stat, 'utility_count', 0) or 0) + stat.utility_count
            agg_stat.utility_damage = (getattr(agg_stat, 'utility_damage', 0) or 0) + stat.utility_damage
            agg_stat.utility_enemies = (getattr(agg_stat, 'utility_enemies', 0) or 0) + stat.utility_enemies
            agg_stat.utility_successes = (getattr(agg_stat, 'utility_successes', 0) or 0) + stat.utility_successes
            agg_stat.zeus_kills = (getattr(agg_stat, 'zeus_kills', 0) or 0) + stat.zeus_kills
            
        # Calculate derived stats
        
        # Store total_rounds as a custom attribute
        agg_stat.total_rounds = total_rounds
        
        # Calculate ADR based on total rounds
        if total_rounds > 0:
            agg_stat.adr = round(total_damage / total_rounds, 1)
            agg_stat.kr_ratio = round(total_kills / total_rounds, 2)
        else:
            agg_stat.adr = 0
            agg_stat.kr_ratio = 0
            
        # Calculate KD ratio
        if total_deaths > 0:
            agg_stat.kd_ratio = round(total_kills / total_deaths, 2)
        else:
            agg_stat.kd_ratio = total_kills  # If no deaths, KD is just kills
            
        # Calculate headshot percentage
        if total_kills > 0:
            agg_stat.headshot_percentage = round(total_headshots / total_kills, 2)
        else:
            agg_stat.headshot_percentage = 0
            
        # Calculate one-v-one win rate
        if agg_stat.one_v_one_count > 0:
            agg_stat.match_one_v_one_win_rate = round(agg_stat.one_v_one_wins / agg_stat.one_v_one_count, 2)
        else:
            agg_stat.match_one_v_one_win_rate = 0
            
        # Calculate one-v-two win rate
        if agg_stat.one_v_two_count > 0:
            agg_stat.match_one_v_two_win_rate = round(agg_stat.one_v_two_wins / agg_stat.one_v_two_count, 2)
        else:
            agg_stat.match_one_v_two_win_rate = 0
            
        # Calculate entry success rate
        if agg_stat.entry_count > 0:
            agg_stat.match_entry_success_rate = round(agg_stat.entry_wins / agg_stat.entry_count, 2)
        else:
            agg_stat.match_entry_success_rate = 0
            
        # Calculate flash success rate
        if agg_stat.flash_count > 0:
            agg_stat.flash_success_rate = round(agg_stat.enemies_flashed / agg_stat.flash_count, 2)
        else:
            agg_stat.flash_success_rate = 0
            
        # Calculate utility success rate
        if agg_stat.utility_count > 0:
            agg_stat.utility_success_rate = round(agg_stat.utility_successes / agg_stat.utility_count, 2)
            agg_stat.utility_damage_success_rate = round(agg_stat.utility_damage / agg_stat.utility_count, 1)
        else:
            agg_stat.utility_success_rate = 0
            agg_stat.utility_damage_success_rate = 0
            
        # Calculate per-round metrics
        if total_rounds > 0:
            agg_stat.flashes_per_round = round(agg_stat.flash_count / total_rounds, 2)
            agg_stat.enemies_flashed_per_round = round(agg_stat.enemies_flashed / total_rounds, 2)
            agg_stat.utility_usage_per_round = round(agg_stat.utility_count / total_rounds, 2)
            agg_stat.utility_damage_per_round = round(agg_stat.utility_damage / total_rounds, 1)
        else:
            agg_stat.flashes_per_round = 0
            agg_stat.enemies_flashed_per_round = 0
            agg_stat.utility_usage_per_round = 0
            agg_stat.utility_damage_per_round = 0
            
        # Calculate sniper metrics
        if agg_stat.kills > 0:
            agg_stat.sniper_kill_rate = round(agg_stat.sniper_kills / agg_stat.kills, 2)
        else:
            agg_stat.sniper_kill_rate = 0
            
        if total_rounds > 0:
            agg_stat.sniper_kill_rate_per_round = round(agg_stat.sniper_kills / total_rounds, 2)
        else:
            agg_stat.sniper_kill_rate_per_round = 0
            
        # Calculate entry rate
        if total_rounds > 0:
            agg_stat.match_entry_rate = round(agg_stat.entry_count / total_rounds, 2)
        else:
            agg_stat.match_entry_rate = 0
            
        aggregated_stats.append(agg_stat)
    
    return append_hltv_ratings_and_reorder(aggregated_stats)

def append_hltv_ratings_and_reorder(playerstats: list[PlayerStat]):
    stats_dicts: list[dict] = []
    for stat in playerstats:
        rating = round(calculate_hltv_rating_brazil(stat, stat.total_rounds), 2)
        stat = model_to_dict(stat)
        stat["hltv_rating"] = rating
        stat.pop("map")
        stats_dicts.append(stat)
    
    stats_dicts.sort(key=lambda x: x.get("hltv_rating"), reverse=True)
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
