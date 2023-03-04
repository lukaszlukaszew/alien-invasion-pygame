"""Module containing all the ship features"""

from pygame.sprite import Sprite

from animations import Animation


class Ship(Animation, Sprite):
    """Class representing player's ship and its movement functionalities"""

    animations = {"main": 4, "move_left": 4, "move_right": 4}
    animation_images = {}
    multiplier = 10
    starting_frame = 0

    def __init__(self, game):
        super().__init__("main")
        self.game = game
        self.screen = game.screen
        self.animation = "main"
        self.moving_right = False
        self.moving_left = False

        self.rect.centerx = self.game.settings.screen_width // 2
        self.rect.bottom = self.game.settings.screen_height

        self.centerx = float(self.rect.centerx)

    def update(self):
        """Prepare next frame of the animation for Ship object and adjust its position"""
        if self.moving_right == self.moving_left:
            self.animation = "main"
        elif self.moving_right:
            self.animation = "move_right"
            self.centerx = min(
                self.centerx + self.game.settings.ship_speed_factor,
                self.game.settings.screen_width - self.rect.width // 2,
            )
            self.game.background_rect.centerx -= (
                self.game.settings.ship_speed_factor // 2
            )
        elif self.moving_left:
            self.animation = "move_left"
            self.centerx = max(
                self.rect.width // 2,
                self.centerx - self.game.settings.ship_speed_factor,
            )
            self.game.background_rect.centerx += (
                self.game.settings.ship_speed_factor // 2
            )

        self.next_frame()
        self.rect.centerx = self.centerx

    def center_ship(self):
        """Transfer ship to the center of the screen"""
        self.centerx = self.game.settings.screen_width // 2
