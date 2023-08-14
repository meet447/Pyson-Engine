from Game.main import VisualNovelGame
import os

# Create directory for save files
if not os.path.exists("saves"):
    os.makedirs("saves")

if __name__ == "__main__":
    game = VisualNovelGame()
    game.run()  