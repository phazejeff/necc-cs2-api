from .Player import Player
class Team:
    def __init__(self, team: dict):
        self.type = team.get('type')
        if self.type == "bye":
            return
        
        self.name = team.get('name')
        self.avatar = team.get('avatar')
        self.roster = []
        for player in team.get('roster'):
            self.roster.append(Player(player))

