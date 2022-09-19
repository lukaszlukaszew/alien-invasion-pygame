"""Module containing bullets features"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class representing basic bullets"""

    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.rect = None
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor
        self.direction = 0

    def update(self):
        """Move Bullet object"""
        self.y += self.speed_factor * self.direction
        self.rect.y = self.y

    def draw_bullet(self):
        """Make bullet visible on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class ShipBullet(Bullet, Sprite):
    """Class representing basic ship bullters"""

    def __init__(self, settings, screen, ship):
        """Create Bullet object at the top of the ship"""
        super().__init__(settings, screen)
        self.ship = ship
        self.direction = -1

        # ship bullet rect
        self.rect = pygame.Rect(
            ship.rect.centerx,
            ship.rect.top,
            settings.bullet_width,
            settings.bullet_height,
        )

        self.y = float(self.rect.y)


class AlienBullet(Bullet, Sprite):
    """Class representing basic alien bullets"""

    def __init__(self, settings, screen, x, y):
        """Create Bullet object at the top of the ship"""
        super().__init__(settings, screen)
        self.direction = 1

        # bullet rect
        self.rect = pygame.Rect(
            x,
            y,
            settings.bullet_width * 3,
            settings.bullet_width * 3,
        )

        self.y = float(self.rect.y)

    def draw_bullet(self):
        """Make bullet visible on the screen"""
        pygame.draw.circle(
            self.screen, self.color, self.rect.center, self.rect.width // 2
        )
