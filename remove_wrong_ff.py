
from database.models import Match, Team
from necc.get_group_rankings import get_team_past_matches

def remove_wrong_ff():
    teams: list[Team] = Team.select()
    duplicates = []
    for team in teams:
        grouped = {}
        matches = get_team_past_matches(team.team_id)
        for match in matches:
            key = (match["team1"]["team_id"], match["team2"]["team_id"])
            key2 = (match["team2"]["team_id"], match["team1"]["team_id"])
            if grouped.get(key):
                duplicates.append((match, grouped.get(key)))
            elif grouped.get(key2):
                duplicates.append((match, grouped.get(key2)))
            else:
                grouped[key] = match

    match_ids_to_remove = set()
    for d in duplicates:
        if len(d[0]["maps"]) == len(d[1]["maps"]):
            if d[0]["week"] > d[1]["week"]:
                match_ids_to_remove.add(d[1]["match_id"])
            else:
                match_ids_to_remove.add(d[0]["match_id"])
        else:
            if len(d[0]["maps"]) > len(d[1]["maps"]):
                match_ids_to_remove.add(d[1]["match_id"])
            else:
                match_ids_to_remove.add(d[0]["match_id"])
    for match_id in match_ids_to_remove:
        Match.delete_by_id(match_id)