"""Module containing bullets features"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class representing basic bullets"""

    def __init__(self, settings, screen, ship):
        """Create Bullet object at the top of the ship"""
        super().__init__()
        self.screen = screen

        # bullet rect
        self.rect = pygame.Rect(
            ship.rect.centerx,
            ship.rect.top,
            settings.bullet_width,
            settings.bullet_height,
        )

        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """Move Bullet object"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Make bullet visible on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
