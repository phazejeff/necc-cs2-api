from __future__ import annotations
from .Game import Game
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Match import Match
    # is there a more elegant way to have type checking without actually importing to avoid circular import?

class Result:
    def __init__(self, results: dict, stats: dict, match: Match):
        self.team1 = match.team1
        self.team2 = match.team2
        if results.get('winner') == 'faction1':
            self.winner = match.team1
        else:
            self.winner = match.team2
        bo3_score: dict = results.get('score')
        self.bo3_score_1 = bo3_score.get('faction1')
        self.bo3_score_2 = bo3_score.get('faction2')

        # games that were completed outside faceit wont have stats
        if stats.get('errors'):
            return

        last_score = ""
        map_num = 1
        self.scores = []
        for round in stats.get('rounds'):
            round: dict
            if int(round.get('match_round')) > map_num:
                self.scores.append(Game(last_score))
                map_num = int(round.get('match_round'))
            round_stats: dict = round.get('round_stats')
            last_score = round_stats.get('Score')
        self.scores.append(Game(last_score))
        

