from gamebase.client.Player import Player, play
from game.omok.CustomOMOKLogic import CustomOMOKLogic

def run():
    game_logic = CustomOMOKLogic()
    play(game_logic)

if __name__ == "__main__":
    run()



