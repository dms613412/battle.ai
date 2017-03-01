

"""
game_id : Server gives identifier per game which is address form
winners : list of players who win the game
losers : list of players who lose the game
drawers : list of players who draw the game
"""

class GameLog(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.winners = []
        self.losers = []
        self.drawers= []
    pass
