import os
import requests
import json
import pprint
from faceit import Faceit, RankedTeam

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

FACEIT_KEY = os.getenv("FACEIT_KEY")
TOURNAMENT_ID = os.getenv("FACEIT_TOURNAMENT_ID")

faceit = Faceit(FACEIT_KEY)

# groups = faceit.get_all_groups(TOURNAMENT_ID)
# rankings: dict[int, list[RankedTeam]] = {}
# for group in groups:
#     rankings[group] = []
#     for team in faceit.get_rankings(TOURNAMENT_ID, group):
#         player: dict = team.get("player") # faceit API calls the team a player in this context for some fucking reason
#         teamname = player.get("nickname")
#         wins = team.get("won")
#         id = player.get("user_id")
#         ranked_team = RankedTeam(id, teamname, wins, group, faceit, TOURNAMENT_ID, old_tiebreaker=True)
#         rankings[group].append(ranked_team)

# print(rankings)
# for group in rankings:
#     rankings[group].sort()
# pprint.pprint(rankings)

r = faceit.get_match("1-27baf334-6f27-473e-9c3c-013b224ac88a")
pprint.pprint(r)
# stats = faceit.get_match_stats(matches[15])
# a = pprint.pformat(stats)
# f = open("test.txt", "w+")
# f.write(a)
# f.close()
# print(matches)
# for match_id in matches:
#     match = faceit.get_match(match_id)
#     print(match.group)
#     print(match.team1.name)