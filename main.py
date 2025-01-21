import os
import requests
import json
import pprint
from faceit import Faceit
from database.models import Placement

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

FACEIT_KEY = os.getenv("FACEIT_KEY")
TOURNAMENT_ID = os.getenv("FACEIT_TOURNAMENT_ID")

faceit = Faceit(FACEIT_KEY)

Placement.update_all_national_points()