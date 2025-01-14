class Player:
    def __init__(self, player: dict):
        self.player_id = player.get('player_id')
        self.nickname = player.get('nickname')
        self.avatar = player.get('avatar')
        self.game_player_name = player.get('game_player_name')
        self.level = player.get('game_skill_level')
