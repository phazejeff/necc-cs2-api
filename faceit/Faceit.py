import requests
from . import Match
from . import Result
class Faceit:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_root = "https://open.faceit.com/data/v4"

    def _get_header(self):
        return {
            "Authorization": "Bearer " + self.api_key,
            "Accept": "application/json"
        }

    def get_championship_matches(self, championship_id, type="past", amount=20, offset=0):
        r: dict = requests.get(
            f"{self.api_root}/championships/{championship_id}/matches?type={type}&limit={amount}&offset={offset}", 
            headers=self._get_header()
        ).json()
        items = r.get('items')
        matches: list[Match] = []
        for match in items:
            matches.append(Match(match, self))
        return matches

    def get_match_stats(self, match: Match):
        print(match.id)
        return requests.get(
            f"{self.api_root}/matches/{match.id}/stats", 
            headers=self._get_header()
        ).json()