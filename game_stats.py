"""Module contains class to monitor game variables"""


class GameStats:
    """Class containing game variables"""

    def __init__(self, ai_setttings):
        self.ships_left = None
        self.ai_settings = ai_setttings
        self.reset_stats()

        self.game_active = True

    def reset_stats(self):
        """Initialize base values of stats"""
        self.ships_left = self.ai_settings.ship_limit
