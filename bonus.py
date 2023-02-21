"""Module containing all obtainable bonuses"""


from random import randint

import pygame
from pygame.sprite import Sprite


class Bonus(Sprite):
    """Class representing bonus dropout"""

    def __init__(self, game, x, y, bonus_type):
        """Initialize attributes for general bonus type"""
        super().__init__()
        self.game = game
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
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        """Move Bonus object"""
        self.direction *= -1
        self.rect.y += self.game.settings.bonus_drop_speed
        self.rect.x += self.direction * randint(1, 10)

    def apply_effect(self):
        """Change the game parameters"""

    def reverse_effect(self):
        """Reverse the change of the game parameters"""


class Bonus00(Bonus):
    """Add extra ship"""

    def apply_effect(self):
        """Change the game parameters"""
        self.game.stats.ships_left += 1
        self.game.scoreboard.prep_ships()


class Bonus01(Bonus):
    """Continuous fire"""

    def apply_effect(self):
        """Change the game parameters"""
        self.game.settings.bullets_allowed = 1000

    def reverse_effect(self):
        """Reverse the change of the game parameters"""
        self.game.settings.bullets_allowed = 3
