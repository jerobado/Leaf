"""
Leaf - simple text-based farming game for the bored developer.
"""

from src.mechanics import GameMechanics

if __name__ == "__main__":
    lets_play = GameMechanics()
    lets_play.start_game()
