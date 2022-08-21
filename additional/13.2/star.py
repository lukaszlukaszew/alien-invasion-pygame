"""Module for star features"""

import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Class representing ship and it's functionalities"""

    def __init__(self, ai_settings, screen, star_size, star_x, star_y, angle):
        """Create star object"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("images/star.png")
        self.image = pygame.transform.scale(self.image, (star_size * 5, star_size * 5))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = star_x
        self.rect.centery = star_y

    def blitme(self):
        """Show star in its current position"""
        self.screen.blit(self.image, self.rect)
