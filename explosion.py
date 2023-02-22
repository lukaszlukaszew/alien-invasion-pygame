"""Module containing explosion effect"""

import pygame
from pygame.sprite import Sprite


class Boom(Sprite):
    """Basic class of explosion effect"""

    animation = []
    frames = 11

    for i in range(frames):
        animation.append(pygame.image.load(f"images/explosion/sprite_{i}.png"))

    def __init__(self, screen, x, y):
        """Initialization of basic instance attributes"""
        super().__init__()
        self.screen = screen
        self.frame = 1
        self.multiplier = 1
        self.prepare_images(x, y)

    def blitme(self):
        """Show explosion in its current position"""
        self.screen.blit(self.image, self.rect)

    def prepare_images(self, x, y):
        """Prepare all needed images for explosion"""
        self.image = Boom.animation[self.frame // self.multiplier]
        self.rect = self.image.get_rect()
        self.place_explosion_on_screen(x, y)

    def place_explosion_on_screen(self, x, y):
        """Select starting position for image"""
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        """Animate and move alien to the left or to the right"""
        self.frame = int((self.frame + 1) % (self.frames * self.multiplier))
        self.image = Boom.animation[self.frame // self.multiplier]
