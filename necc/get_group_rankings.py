from database.models import Team, Match
from peewee import fn, JOIN

def get_group_rankings(group):
    match_winner: Match = Match.alias()
    match_loser: Match = Match.alias()

    teams_won = (Team
                    .select(Team, fn.COUNT(match_winner.match_id).alias("matches_won_count"))
                    .join(match_winner, JOIN.LEFT_OUTER, on=(Team.team_id == match_winner.winner))  # Join for won matches
                    .where(Team.group == group)
                    .where(Team.team_id != "bye")
                    .group_by(Team)
                )

    teams_lost = (Team
                    .select(Team, fn.COUNT(match_loser.match_id).alias("matches_lost_count"))
                    .join(match_loser, JOIN.LEFT_OUTER, on=(
                        (
                            (match_loser.team1 == Team.team_id) | 
                            (match_loser.team2 == Team.team_id)
                        ) & 
                        (Team.team_id != match_loser.winner)
                        )  
                    )  # Join for lost matches
                    .where(Team.group == group)
                    .where(Team.team_id != "bye")
                    .group_by(Team)
                )

    teams_won = sorted(teams_won, key=lambda team: len(team.matches_won), reverse=True)
    teams_lost = sorted(teams_lost, key=lambda team: len(team.matches_won), reverse=True)

    return teams_won, teams_lost