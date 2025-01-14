class Game:
    # in the annoying format "score1 / score2"
    def __init__(self, score: str):
        score = score.split("/")
        self.score1 = int(score[0])
        self.score2 = int(score[1])