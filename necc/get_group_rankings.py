from database.models import Team, Match, Map
from peewee import fn, JOIN

def get_group_rankings(group):  
    teams = get_teams_from_group(group)
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
        teams_dict.append(team)
        get_rounds_won(team)
    

    teams_sorted = sorted(
        teams_dict, 
        key=lambda team: (
            (team["record"]["matches"]["won"]),
            (team["record"]["maps"]["won"] - team["record"]["maps"]["lost"]),
            (team["record"]["rounds"]["won"] - team["record"]["rounds"]["lost"])     
        ), 
        reverse=True)
    return teams_sorted



def get_teams_from_group(group):
    return (Team
            .select(Team)
            .where(Team.group == group)
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

def get_number_of_groups():
    return (Team
            .select(fn.MAX(Team.group))
            ).scalar()