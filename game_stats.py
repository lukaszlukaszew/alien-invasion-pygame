"""Module to track game variables"""


class GameStats:
    """Class containing game variables"""

    def __init__(self, settings):
        self.settings = settings

        self.reset_stats()

        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """Initialize base values of stats"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 18
