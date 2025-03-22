from database.models import Map
import uuid

match_id = "1-938cb871-fc55-46c5-800a-cca669e9f36f"
csusm_blue = "7fd341a2-d958-4381-9596-22e0b623658b"
ucsc_onyx = "0e028284-054c-4d03-b11c-c2a15915cc93"

map1 = Map.create(
    map_id = uuid.uuid5(uuid.NAMESPACE_DNS, f"{match_id}-1"),
    match_id = match_id,
    map_num = 1,
    map = "de_inferno",
    winner = ucsc_onyx,
    team1 = ucsc_onyx,
    team2 = csusm_blue,
    team1_score = 13,
    team2_score = 4,
    team1_first_half_score = 10,
    team2_first_half_score = 2,
    team1_second_half_score = 3,
    team2_second_half_score = 2,
    team1_overtime_score = 0,
    team2_overtime_score = 0
)

map2 = Map.create(
    map_id = uuid.uuid5(uuid.NAMESPACE_DNS, f"{match_id}-2"),
    match_id = match_id,
    map_num = 2,
    map = "de_anubis",
    winner = csusm_blue,
    team1 = ucsc_onyx,
    team2 = csusm_blue,
    team1_score = 3,
    team2_score = 13,
    team1_first_half_score = 3,
    team2_first_half_score = 9,
    team1_second_half_score = 0,
    team2_second_half_score = 4,
    team1_overtime_score = 0,
    team2_overtime_score = 0
)

map3 = Map.create(
    map_id = uuid.uuid5(uuid.NAMESPACE_DNS, f"{match_id}-3"),
    match_id = match_id,
    map_num = 3,
    map = "de_ancient",
    winner = ucsc_onyx,
    team1 = ucsc_onyx,
    team2 = csusm_blue,
    team1_score = 13,
    team2_score = 11,
    team1_first_half_score = 7,
    team2_first_half_score = 5,
    team1_second_half_score = 6,
    team2_second_half_score = 6,
    team1_overtime_score = 0,
    team2_overtime_score = 0
)

Map.insert_many([map1, map2, map3])