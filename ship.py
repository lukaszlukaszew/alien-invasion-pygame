"""Module containing ship features"""

from pygame.sprite import Sprite

from animations import Animation


class Ship(Sprite, Animation):
    """Class representing player's ship and its functionalities"""

    animations = {}

    def __init__(self, settings, screen, x=None):
        """Create ship object at the center & bottom of the screen"""
        super().__init__()

        self.screen = screen
        self.settings = settings

        for animation, frames in {"main": 4, "move_left": 4, "move_right": 4}.items():
            self.load_images(self.__str__(), animation, frames, Ship.animations)

        self.current_frame = 0
        self.image = Ship.animations["main"][self.current_frame]

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

        self.screen_x = x

    def __str__(self):
        return "ship"

    def blitme(self):
        """Show ship on the screen in its current position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update position of the ship"""

        self.current_frame += 1

        if self.current_frame >= len(Ship.animations["main"]) * 10:
            self.current_frame = 0

        if not (self.moving_right or self.moving_left):
            self.image = Ship.animations["main"][self.current_frame // 10]
        else:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.settings.ship_speed_factor
                self.image = Ship.animations["move_right"][self.current_frame // 10]
                self.screen_x -= self.settings.ship_speed_factor // 2

            if self.moving_left and self.rect.left > 0:
                self.center -= self.settings.ship_speed_factor
                self.image = Ship.animations["move_left"][self.current_frame // 10]
                self.screen_x += self.settings.ship_speed_factor // 2

        self.rect.centerx = self.center

        return self.screen_x

    def center_ship(self):
        """Move ship to the center of the screen"""
        self.center = self.screen_rect.centerx
