"""Module to track game variables"""

from collections import defaultdict


class GameStats:
    """Class containing game variables"""

    def __init__(self, settings):
        self.settings = settings

        # ship stats
        self.ships_left = None

        # bullet stats
        self.bullets_fired = None
        self.hits = None

        # level stats
        self.level = None

        # game stats
        self.game_won = None
        self.game_active = False
        self.game_played = False
        self.game_not_paused = True

        # bonus stats
        self.bonuses_used = None

        # score stats
        self.score = None
        self.high_score = 0

        self.reset_stats()

    def reset_stats(self):
        """Initialize base values of choosen stats"""
        # ship stats
        self.ships_left = self.settings.ship_limit

        # bullet stats
        self.bullets_fired = 0
        self.hits = defaultdict(int)

        # level stats
        self.level = 1

        # game stats
        self.game_won = False

        # bonus stats
        self.bonuses_used = 0

        # score stats
        self.score = 0
