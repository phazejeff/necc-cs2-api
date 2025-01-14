from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Faceit import Faceit
from .Team import Team
from .Result import Result

class Match:
    def __init__(self, match: dict, faceit: Faceit):
        self.id = match['match_id']
        teams: dict = match.get('teams')
        self.team1 = Team(teams.get('faction1'))
        self.team2 = Team(teams.get('faction2'))
        if self.team2.type == "bye" or self.team1.type == "bye":
            self.type = "bye"
            return
        else:
            self.type = "game"

        self.scheduled = match.get('scheduled_at')
        self.start = match.get('started_at')
        self.finish = match.get('finished_at')
        self.best_of = match.get('best_of')
        self.group = match.get('group')
        self.round = match.get('round')
        self.status = match.get('status')
        self.result = Result(match.get('results'), faceit.get_match_stats(self), self)
