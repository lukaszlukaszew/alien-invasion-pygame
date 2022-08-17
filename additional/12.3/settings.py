"""All settings of the game"""


class Settings():
    """Class dedicated to store all game configuration"""
    def __init__(self):

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_speed_factor = 1.5
