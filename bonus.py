"""Module containing all obtainable bonuses"""


from random import randint

import pygame
from pygame.sprite import Sprite


class Bonus(Sprite):
    """Class representing bonus dropout"""

    def __init__(self, settings, screen, stats, x, y, bonus_type):
        """Initialize attributes for general bonus type"""
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.bonus_type = bonus_type
        self.direction = 1
        self.load_image(bonus_type)
        self.rect.left = x
        self.rect.top = y

    def load_image(self, bonus_type):
        """Load proper imamage for the bonus"""
        self.image = pygame.image.load(f"images/bonus/{bonus_type}.png")
        self.rect = self.image.get_rect()

    def blitme(self):
        """Show Bonus image on the screen in its current position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move Bonus object"""
        self.direction *= -1
        self.rect.y += self.settings.bonus_drop_speed
        self.rect.x += self.direction * randint(1, 10)

    def apply_effect(self):
        """Change the game parameters"""

    def reverse_effect(self):
        """Reverse the change of the game parameters"""
