"""Module containing all obtainable bonuses"""


from random import randint

from pygame.sprite import Sprite

from explosion import Boom
from animations import Animation


class Bonus(Animation, Sprite):
    """Class representing basic bonus dropout"""

    animations = {"bonus_add": 1, "bonus_weapon": 1, "bonus_alien": 1}
    animation_images = {}
    multiplier = 1
    starting_frame = 0

    def __init__(self, game, pos_x, pos_y, bonus_type):
        super().__init__(bonus_type)

        self.game = game
        self.screen = self.game.screen
        self.direction = 1

        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        """Adjust position of the bonus image"""
        self.direction *= -1
        self.rect.y += self.game.settings.bonus_drop_speed
        self.rect.x += self.direction * randint(1, 10)

    def apply_effect(self):
        """Change the game parameters"""

    def reverse_effect(self):
        """Reverse previous change of the game parameters"""


class Bonus00(Bonus):
    """Add extra ship"""

    def apply_effect(self):
        """Change the game parameters - add extra ship"""
        self.game.stats.ships_left += 1
        self.game.scoreboard.prep_ships()


class Bonus01(Bonus):
    """Continuous fire"""

    def __init__(self, game, x, y, bonus_type):
        """Extend basic bonus parameters"""
        super().__init__(game, x, y, bonus_type)
        self.bullets_allowed = 0

    def apply_effect(self):
        """Change the game parameters - bullets allowed"""
        if self.bullets_allowed != self.game.settings.bullets_allowed:
            self.bullets_allowed = self.game.settings.bullets_allowed
            self.game.settings.bullets_allowed = 1000

    def reverse_effect(self):
        """Reverse the change of the game parameters - bullets allowed"""
        if self.bullets_allowed:
            self.game.settings.bullets_allowed = self.bullets_allowed


class Bonus02(Bonus):
    """All kill"""

    def apply_effect(self):
        """Change the game parameters - destroy all visible aliens one by one"""
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

            for alien in self.game.aliens.copy():
                self.game.explosions.add(
                    Boom(self.game, alien.rect.centerx, alien.rect.centery)
                )
                self.game.aliens.remove(alien)


class Bonus03(Bonus):
    """Additional points"""

    def apply_effect(self):
        """Change the game parameters - add 100000 points for every level achieved"""
        self.game.stats.score += self.game.stats.level * 1000000
        self.game.scoreboard.prep_score()


class Bonus04(Bonus):
    """Alien movement freeze"""

    def __init__(self, game, x, y, bonus_type):
        """Extend basic bonus parameters"""
        super().__init__(game, x, y, bonus_type)
        self.alien_speed = 0
        self.level = 0
        self.shooting_range = 0

    def apply_effect(self):
        """Change the game parameters - stop all alien movement and shooting"""
        if self.game.settings.alien_horizontal_speed_factor:
            self.alien_speed = self.game.settings.alien_horizontal_speed_factor
            self.level = self.game.stats.level
            self.game.settings.alien_horizontal_speed_factor = 0

            self.shooting_range = self.game.settings.alien_shooting_range
            self.game.settings.alien_shooting_range = 1000

    def reverse_effect(self):
        """Reverse the change of the game parameters - stop all alien movement and shooting"""
        if self.level + self.alien_speed + self.shooting_range:
            self.game.settings.alien_horizontal_speed_factor = self.alien_speed
            for _ in range(self.game.stats.level - self.level):
                self.game.settings.alien_horizontal_speed_factor *= (
                    self.game.settings.speedup_scale
                )

            self.game.settings.alien_shooting_range = self.shooting_range


class Bonus05(Bonus):
    """Alien speed decrease"""

    def __init__(self, game, x, y, bonus_type):
        """Extend basic bonus parameters"""
        super().__init__(game, x, y, bonus_type)
        self.alien_horizontal_speed = 0
        self.alien_vertical_speed = 0
        self.level = 0
        self.alien_bullet_speed = 0

    def apply_effect(self):
        """Change the game parameters - divide alien speed and alien bullet speed parameters by 2"""
        if (
            self.game.settings.alien_horizontal_speed_factor
            + self.game.settings.alien_vertical_speed_factor
            + self.game.settings.alien_bullet_speed_factor
        ):

            self.level = self.game.stats.level

            self.alien_horizontal_speed = (
                self.game.settings.alien_horizontal_speed_factor
            )
            self.game.settings.alien_horizontal_speed_factor //= 2

            self.alien_vertical_speed = self.game.settings.alien_vertical_speed_factor
            self.game.settings.alien_vertical_speed_factor //= 2

            self.alien_bullet_speed = self.game.settings.alien_bullet_speed_factor
            self.game.settings.alien_bullet_speed_factor //= 2

    def reverse_effect(self):
        """Reverse the change of the game parameters - divide alien speed and alien bullet spe..."""
        if (
            self.alien_horizontal_speed
            + self.alien_vertical_speed
            + self.level
            + self.alien_bullet_speed
        ):
            self.game.settings.alien_horizontal_speed_factor = (
                self.alien_horizontal_speed
            )
            self.game.settings.alien_vertical_speed_factor = self.alien_vertical_speed
            self.game.settings.alien_bullet_speed_factor = self.alien_bullet_speed

            for _ in range(self.game.stats.level - self.level):
                self.game.settings.alien_horizontal_speed_factor *= (
                    self.game.settings.speedup_scale
                )
                self.game.settings.alien_bullet_speed_factor *= (
                    self.game.settings.speedup_scale
                )
