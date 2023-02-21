"""Module to track game variables"""

from collections import defaultdict


class GameStats:
    """Class containing game variables"""

    def __init__(self, settings):
        self.settings = settings

        self.reset_stats()

        self.game_active = False
        self.game_played = False
        self.game_not_paused = True

        self.high_score = 0

    def reset_stats(self):
        """Initialize base values of stats"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1  # CHANGED
        self.game_won = False

        self.bullets_fired = 0
        self.hits = defaultdict(int)
        self.bonuses_used = 0
