from faceit import Faceit
from database.models import Team, Player, TeamCaptain, Match, Map, PlayerStat, Placement
from database import database
import os
import json
from peewee import DoesNotExist

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

FACEIT_KEY = os.getenv("FACEIT_KEY")
FALL_TOURNAMENT_D1 = "0be8fc40-276c-4d28-95bd-a1a7d69eb04a"
FALL_TOURNAMENT_D2 = "bf98adaa-f804-4f9d-b8fa-bd79fe173341"
SPRING_TOURNAMENT_D1 = "62554deb-7401-4e35-ae05-8ee04e1bf9e2"
SPRING_TOURNAMENT_D2 = "445efca4-3b34-49e2-b0eb-226656b5a885"
SPRING_TOURNAMENT_D3 = "a9337734-05a6-45a1-a045-3174fb87857c"

class Tournament:
    def __init__(self, tournament_id: str, group_amount: int, semester: str, division_num: int):
        self.id = tournament_id
        self.group_amount = group_amount
        self.semester = semester.lower()
        self.division_num = division_num

    def __repr__(self):
        return f"Division: {self.division_num}, Semester: {self.semester}"

tournaments = [
    Tournament(FALL_TOURNAMENT_D1, 2, "fall", 1),
    Tournament(FALL_TOURNAMENT_D2, 10, "fall", 2),
    Tournament(SPRING_TOURNAMENT_D1, 4, "spring", 1),
    Tournament(SPRING_TOURNAMENT_D2, 4, "spring", 2),
    Tournament(SPRING_TOURNAMENT_D3, 4, "spring", 3)
]

faceit = Faceit(FACEIT_KEY)

database.connect()

placements_db_fall: list[Placement] = []
placements_db_spring: list[Placement] = []
for tournament in tournaments:
    print(f"Running for {tournament}")
    for i in range(1, tournament.group_amount + 1):
        positions = faceit.get_rankings(tournament.id, i)
        for num, pos in enumerate(positions):
            if tournament.semester == "fall":
                placement_db = Placement(
                    team_id = pos.get("player").get("user_id"),
                    fall_division = tournament.division_num
                )
                placements_db_fall.append(placement_db)
            elif tournament.semester == "spring":
                placement_db = Placement(
                    team_id = pos.get("player").get("user_id"),
                    spring_division = tournament.division_num
                )
                placements_db_spring.append(placement_db)
            else:
                print("something broke.")

    with database.atomic():
        if tournament.semester == "fall":
            Placement.bulk_update(placements_db_fall, batch_size=50, fields=["fall_division"])
        elif tournament.semester == "spring":
            Placement.bulk_update(placements_db_spring, batch_size=50, fields=["spring_division"])