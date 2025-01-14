import os
import requests
import json
from faceit import Faceit

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

FACEIT_KEY = os.getenv("FACEIT_KEY")
TOURNAMENT_ID = os.getenv("FACEIT_TOURNAMENT_ID")

faceit = Faceit(FACEIT_KEY)
matches = faceit.get_championship_matches(TOURNAMENT_ID)
