"""Module for ship features"""

import pygame
from pygame.sprite import Sprite
from animations import Animation


class Ship(Sprite, Animation):
    """Class representing ship and it's functionalities"""

    def __init__(self, ai_settings, screen):
        """Create ship object at the center & bottom of the screen"""
        Sprite.__init__(self)
        self.screen = screen
        self.ai_settings = ai_settings
        self.main = []
        self.main.append(pygame.image.load('images/ship/main/sprite_0.png'))
        self.main.append(pygame.image.load('images/ship/main/sprite_1.png'))
        self.main.append(pygame.image.load('images/ship/main/sprite_2.png'))
        self.main.append(pygame.image.load('images/ship/main/sprite_3.png'))

        self.move_right = []
        self.move_right.append(pygame.image.load('images/ship/move_right/sprite_0.png'))
        self.move_right.append(pygame.image.load('images/ship/move_right/sprite_1.png'))
        self.move_right.append(pygame.image.load('images/ship/move_right/sprite_2.png'))
        self.move_right.append(pygame.image.load('images/ship/move_right/sprite_3.png'))

        self.move_left = []
        self.move_left.append(pygame.image.load('images/ship/move_left/sprite_0.png'))
        self.move_left.append(pygame.image.load('images/ship/move_left/sprite_1.png'))
        self.move_left.append(pygame.image.load('images/ship/move_left/sprite_2.png'))
        self.move_left.append(pygame.image.load('images/ship/move_left/sprite_3.png'))

        self.current_frame = 0
        self.image = self.main[self.current_frame]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Show ship in its current position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update position of the ship"""

        self.current_frame += 1
        if self.current_frame >= len(self.main) * 10:
            self.current_frame = 0
        if not self.moving_right:
            self.image = self.main[self.current_frame // 10]

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
            self.image = self.move_right[self.current_frame // 10]
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            self.image = self.move_left[self.current_frame // 10]

        self.rect.centerx = self.center

    def center_ship(self):
        """Move ship to the center of the screen"""
        self.center = self.screen_rect.centerx
