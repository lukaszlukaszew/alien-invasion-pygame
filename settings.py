"""Module for predefinied settings of the game"""


class Settings:
    """Class dedicated to store all game configuration"""

    def __init__(self):
        """Creation of game static data"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3  # CHANGED
        self.bullet_height = 15
        self.bullet_color = (255, 255, 0)
        self.bullets_allowed = 3  # CHANGED

        # boss beam colors
        self.beam_color_1 = (127, 255, 127)
        self.beam_color_2 = (15, 255, 80)

        # alien settings
        self.fleet_drop_speed = 10
        self.alien_boss_area = 30
        self.alien_bullet_width = 3
        self.alien_boss_points = 2000000
        self.starting_alien_boss_life = 50
        self.alien_shooting_range = 998

        # level settings
        self.alien_changes = (6, 11, 16, 21)
        self.alien_types = (
            "AlienUFO",
            "AlienTentacle",
            "AlienShoot",
            "AlienTeleport",
            "AlienBoss1",
        )

        # game speed change
        self.speedup_scale = 1.1

        # game score change
        self.score_scale = 1.5

        # bonus settings
        self.bonus_drop_speed = 3
        self.bonus_active_time = 600

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Creation of game dynamic data"""

        # ship settings
        self.ship_speed_factor = 2

        # bullet settings
        self.bullet_speed_factor = 3
        self.alien_bullet_speed_factor = 3

        # alien settings
        self.alien_vertical_speed_factor = 1
        self.alien_horizontal_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50
        self.alien_boss_life = self.starting_alien_boss_life
        self.current_alien = 0  # CHANGED

    def increase_speed(self):
        """Change speed factors due to higher level"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_bullet_speed_factor *= self.speedup_scale
        self.alien_horizontal_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
