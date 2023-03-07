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
        self.ship_speed_factor = None

        # bullet settings
        self.bullet_width = 3
        self.alien_bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 0)
        self.bullets_allowed = 3

        self.beam_color_1 = (127, 255, 127)
        self.beam_color_2 = (15, 255, 80)

        self.bullet_speed_factor = None
        self.alien_bullet_speed_factor = None

        # alien settings
        self.fleet_drop_speed = 10
        self.alien_shooting_range = 999

        self.alien_boss_single_move_range = 30
        self.alien_boss_points = 2000000
        self.starting_alien_boss_life = 50

        self.current_alien = None
        self.fleet_direction = None

        self.alien_vertical_speed_factor = None
        self.alien_horizontal_speed_factor = None

        self.alien_points = None
        self.alien_boss_life = None

        # level settings
        self.alien_changes = (6, 11, 16, 21)
        self.alien_types = (
            "AlienUFO",
            "AlienTentacle",
            "AlienTeleport",
            "AlienShoot",
            "AlienBoss",
        )

        # game settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.bonus_probability_scale = 1.01

        # bonus settings
        self.bonus_drop_speed = 3
        self.bonus_active_time = 600
        self.bonus_drop_rate = None
        self.aliens_frozen = None
        self.aliens_slowed_down = None
        self.more_bullets = None

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Add values to the game dynamic data"""
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
        self.current_alien = 0

        # bonus settings
        self.bonus_drop_rate = 9999

    def increase_speed(self):
        """Change speed factors due to higher level"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_bullet_speed_factor *= self.speedup_scale
        self.alien_horizontal_speed_factor *= self.speedup_scale
        self.alien_points *= self.score_scale
        self.bonus_drop_rate /= self.bonus_probability_scale
