"""Module for ship features"""

import pygame

class Ship():
    """Class representing ship and it's functionalities"""
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        """Showing ship in it's current position"""
        self.screen.blit(self.image, self.rect)
