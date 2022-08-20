"""Module for bullets features"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class representing bullets and it's functionalities"""

    def __init__(self, ai_settings, screen, ship):
        """Create Bullet object at the position of the ship"""
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(
            ship.rect.centerx,
            ship.rect.top,
            ai_settings.bullet_width,
            ai_settings.bullet_height,
        )

        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move Bullet object"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Make bullet visible"""
        pygame.draw.rect(self.screen, self.color, self.rect)
