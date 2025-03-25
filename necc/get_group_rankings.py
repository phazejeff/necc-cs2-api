from database.models import Team, Match, Map
from peewee import fn, JOIN

def get_group_rankings(division: int, group: int):  
    teams = get_teams_from_group(division, group)
    teams_dict = []
    for team in teams:
        team["record"] = {
            "matches" : {
                "won" : get_matches_won(team),
                "lost" : get_matches_lost(team)
            },
            "maps" : {
                "won" : get_maps_won(team),
                "lost" : get_maps_lost(team)
            },
            "rounds" : {
                "won" : get_rounds_won(team),
                "lost" : get_rounds_lost(team)
            }
        }

        # ff wins count as 2-0 with both being 13-0 wins
        ff_wins, ff_losses = get_forfeit_wins_and_loss_count(team)
        team["record"]["maps"]["won"] += ff_wins * 2
        team["record"]["maps"]["lost"] += ff_losses * 2
        team["record"]["rounds"]["won"] += ff_wins * 2 * 13
        team["record"]["rounds"]["lost"] += ff_losses * 2 * 13
        teams_dict.append(team)
    

    teams_sorted = sorted(
        teams_dict, 
        key=lambda team: (
            (team["record"]["matches"]["won"]),
            (team["record"]["maps"]["won"] - team["record"]["maps"]["lost"]),
            (team["record"]["rounds"]["won"] - team["record"]["rounds"]["lost"])     
        ), 
        reverse=True)
    return teams_sorted

# Assume if a match has no map data it must have been a ff
def get_forfeit_wins_and_loss_count(team):
    ff_wins = 0
    ff_losses = 0

    matches: list[Match] = (Match
            .select(Match)
            .where((Match.team1 == team["team_id"]) | (Match.team2 == team["team_id"]))
            )
    for match in matches:
        map_count = (Map
                .select(Map)
                .where(Map.match_id == match.match_id)
                ).count()
        if map_count == 0:
            if match.winner.team_id == team["team_id"]:
                ff_wins += 1
            else:
                ff_losses += 1
        
    return ff_wins, ff_losses

def get_team_past_matches(team_id: str):
    matches = list((Match
    .select(Match)
    .where((Match.team1 == team_id) | (Match.team2 == team_id))
    ).dicts())

    for match in matches:
        match["team1"] = Team.get_by_id(match["team1"]).__data__
        match["team2"] = Team.get_by_id(match["team2"]).__data__

        maps = list((Map
        .select(Map)
        .where((match["match_id"] == Map.match_id))
        ).dicts())
        match["maps"] = maps
    
    return matches


def get_teams_from_group(division: int, group: int):
    return (Team
            .select(Team)
            .where(Team.group == group)
            .where(Team.division == division)
            ).dicts()

def get_matches_won(team):
    return (Match
            .select(Match)
            .where(Match.winner == team['team_id'])
            ).count()

def get_matches_lost(team):
    return (Match
            .select(Match)
            .where(
                (Match.winner != team['team_id']) &
                ((Match.team1 == team['team_id']) | (Match.team2 == team['team_id']))
            )
            ).count()

def get_maps_won(team):
    return(Map
           .select(Map)
           .where(Map.winner == team['team_id'])
           ).count()

def get_maps_lost(team):
    return (Map
            .select(Map)
            .join(Match)
            .where(
                (Map.winner != team['team_id']) &
                ((Match.team1 == team['team_id']) | (Match.team2 == team['team_id']))
            )
            ).count()

def get_rounds_won(team):
    team1_score = (Map
                   .select(fn.COALESCE(fn.SUM(Map.team1_score), 0))
                   .join(Match)
                   .where(Match.team1 == team['team_id'])
                   ).scalar()
    
    team2_score = (Map
                   .select(fn.COALESCE(fn.SUM(Map.team2_score), 0))
                   .join(Match)
                   .where(Match.team2 == team['team_id'])
                   ).scalar()
    return team1_score + team2_score

def get_rounds_lost(team):
    team1_score = (Map
                   .select(fn.COALESCE(fn.SUM(Map.team1_score), 0))
                   .join(Match)
                   .where(Match.team2 == team['team_id'])
                   ).scalar()
    
    team2_score = (Map
                   .select(fn.COALESCE(fn.SUM(Map.team2_score), 0))
                   .join(Match)
                   .where(Match.team1 == team['team_id'])
                   ).scalar()
    return team1_score + team2_score

def get_number_of_groups(division: int):
    return (Team
            .select(fn.MAX(Team.group))
            .where(Team.division == division)
            ).scalar()

def get_number_of_divisions():
    return (Team
            .select(fn.MAX(Team.division))
            ).scalar()