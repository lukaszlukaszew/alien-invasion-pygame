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


class Bonus02(Bonus):
    """All kill"""

    def apply_effect(self):
        """Change the game parameters"""
        if self.game.stats.level >= self.game.settings.alien_changes[-1]:
            self.game.stats.score += (
                self.game.settings.alien_boss_points
                * self.game.settings.alien_boss_life
            )
            self.game.settings.alien_boss_life = 0
        else:
            self.game.stats.score += self.game.settings.alien_points * len(
                self.game.aliens
            )

            self.game.aliens.empty()


class Bonus03(Bonus):
    """Additional points"""

    def apply_effect(self):
        """Change the game parameters"""
        self.game.stats.score += self.game.stats.level * 1000000
        self.game.scoreboard.prep_score()


class Bonus04(Bonus):
    """Alien movement freeze"""

    def apply_effect(self):
        """Change the game parameters"""
        self.alien_speed = self.game.settings.alien_horizontal_speed_factor
        self.level = self.game.stats.level
        self.game.settings.alien_horizontal_speed_factor = 0

        self.shooting_range = self.game.settings.alien_shooting_range
        self.game.settings.alien_shooting_range = 1000

    def reverse_effect(self):
        """Reverse the change of the game parameters"""
        self.game.settings.alien_horizontal_speed_factor = self.alien_speed
        for _ in range(self.game.stats.level - self.level):
            self.game.settings.alien_horizontal_speed_factor *= (
                self.game.settings.speedup_scale
            )

        self.game.settings.alien_shooting_range = self.shooting_range


class Bonus05(Bonus):
    """Alien speed decrease"""

    def apply_effect(self):
        """Change the game parameters"""
        self.level = self.game.stats.level

        self.alien_horizontal_speed = self.game.settings.alien_horizontal_speed_factor
        self.game.settings.alien_horizontal_speed_factor //= 2

        self.alien_vertical_speed = self.game.settings.alien_vertical_speed_factor
        self.game.settings.alien_vertical_speed_factor //= 2

        self.alien_bullet_speed = self.game.settings.alien_bullet_speed_factor
        self.game.settings.alien_bullet_speed_factor //= 2

    def reverse_effect(self):
        """Reverse the change of the game parameters"""
        self.game.settings.alien_horizontal_speed_factor = self.alien_horizontal_speed
        self.game.settings.alien_vertical_speed_factor = self.alien_vertical_speed
        self.game.settings.alien_bullet_speed_factor = self.alien_bullet_speed

        for _ in range(self.game.stats.level - self.level):
            self.game.settings.alien_horizontal_speed_factor *= (
                self.game.settings.speedup_scale
            )
            self.game.settings.alien_bullet_speed_factor *= (
                self.game.settings.speedup_scale
            )
