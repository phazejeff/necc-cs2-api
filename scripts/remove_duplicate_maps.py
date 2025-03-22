from database.models import Team, Player, TeamCaptain, Match, Map, PlayerStat, Placement
from database import database

database.connect()

matches = Match.select()
for match in matches:
    maps = Map.select().where(Map.match_id == match.match_id)
    print(len(maps))
    map_nums = []
    for map in maps:
        if map.map_num not in map_nums:
            map_nums.append(map.map_num)
        else:
            map.delete_instance()
