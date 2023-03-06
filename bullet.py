"""Module containing bullets features"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class representing basic bullets"""

    direction = None

    def __init__(self, game, x, y):
        super().__init__()
        self.rect = None
        self.pos_y = None
        self.screen = game.screen
        self.color = game.settings.bullet_color
        self.screen_height = game.settings.screen_height

        if type(self).__name__ == "ShipBullet":
            self.speed_factor = game.settings.bullet_speed_factor
        elif type(self).__name__ == "AlienBullet":
            self.speed_factor = game.settings.alien_bullet_speed_factor
        else:
            self.speed_factor = 0

        if type(self).__name__ != "AlienBossBeam":
            self.rect = pygame.Rect(
                x,
                y,
                game.settings.bullet_width,
                game.settings.bullet_height,
            )
        else:
            self.rect = pygame.Rect(
                x - 15,
                y,
                30,
                self.screen_height,
            )

        self.pos_y = float(self.rect.y)

    def update(self):
        """Move Bullet object"""
        self.pos_y += self.speed_factor * type(self).direction
        self.rect.y = self.pos_y

    def draw_bullet(self):
        """Make bullet visible on the screen"""
        if type(self).__name__ == "ShipBullet":
            pygame.draw.rect(self.screen, self.color, self.rect)
        elif type(self).__name__ == "AlienBullet":
            pygame.draw.circle(
                self.screen, self.color, self.rect.center, self.rect.height // 3
            )


class ShipBullet(Bullet):
    """Class representing basic ship bullters"""

    direction = -1


class AlienBullet(Bullet):
    """Class representing basic alien bullets"""

    direction = 1


class AlienBossBeam(Bullet):
    """Class representing boss beam"""

    direction = 0

    def __init__(self, game, x, y, frame):
        super().__init__(game, x, y)
        self.color_1 = game.settings.beam_color_1
        self.color_2 = game.settings.beam_color_2
        self.frame = frame

    def draw_bullet(self):
        """Make beam visible on the screen"""
        pygame.draw.rect(self.screen, self.color_1, self.rect)
        pygame.draw.rect(
            self.screen,
            self.color_2,
            (
                self.rect.left + 5 * (1 + int(self.frame % 2)),
                self.rect.top,
                int(5 * (3 + (self.frame + 1) % 2 - self.frame % 2)),
                self.screen_height,
            ),
        )
