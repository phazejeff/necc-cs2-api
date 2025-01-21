import os
import requests
import json
import pprint
from faceit import Faceit
from necc import update_national_points

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

FACEIT_KEY = os.getenv("FACEIT_KEY")
TOURNAMENT_ID = os.getenv("FACEIT_TOURNAMENT_ID")

faceit = Faceit(FACEIT_KEY)

update_national_points("7fd341a2-d958-4381-9596-22e0b623658b")