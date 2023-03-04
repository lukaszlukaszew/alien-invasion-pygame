"""Module containing all aliens features and behaviours"""

from random import randint

from pygame.sprite import Sprite

from animations import Animation
from bullet import AlienBullet, AlienBossBeam


class Alien(Animation, Sprite):
    """Super class for all alien types"""

    animations = {}
    animation_images = {}
    multiplier = 1

    def __init__(self, game):
        super().__init__("main")
        self.game = game
        self.screen = game.screen
        self.animation = "main"
        self.frame = randint(
            0, type(self).animations[self.animation] * self.multiplier - 1
        )

    def check_edges(self):
        """Returns true if alien is at the edge of the screen"""
        if self.rect.right >= self.game.settings.screen_width or self.rect.left <= 0:
            return True
        return False

    def shoot(self):
        """Attack ship - create round bullet moving downwards"""
        if randint(0, 1000) > self.game.settings.alien_shooting_range:
            self.game.alien_bullets.add(
                AlienBullet(
                    self.game.settings,
                    self.game.screen,
                    self.rect.centerx,
                    self.rect.centery,
                )
            )
            self.game.sounds.play_sound("alien_shoot")


class AlienUFO(Alien):
    """Class representing UFO-shaped alien and its functionalities"""

    animations = {"main": 9}
    animation_images = {}
    multiplier = 12

    def __init__(self, game):
        super().__init__(game)
        self.pos_x = 0

    def update(self):
        """Prepare next frame of the animation for AlienUFO object and adjust its position"""
        self.next_frame()

        self.pos_x += (
            self.game.settings.alien_horizontal_speed_factor
            * self.game.settings.fleet_direction
        )
        self.rect.x = self.pos_x


class AlienTentacle(Alien):
    """Class representing alien with tentacles and its functionalities"""

    animations = {"main": 6}
    animation_images = {}
    multiplier = 18

    def __init__(self, game):
        super().__init__(game)
        self.pos_x = 0

    def update(self):
        """Prepare next frame of the animation for AlienTentacle object and adjust its position"""
        self.next_frame()

        self.pos_x += (
            self.game.settings.alien_horizontal_speed_factor
            * self.game.settings.fleet_direction
        )
        self.rect.x = self.pos_x

        if self.rect.centerx >= self.game.settings.screen_width // 2:
            self.rect.y = max(
                self.rect.y
                - self.game.settings.fleet_direction
                * self.game.settings.alien_vertical_speed_factor,
                0,
            )
        else:
            self.rect.y += (
                self.game.settings.fleet_direction
                * self.game.settings.alien_vertical_speed_factor
            )


class AlienTeleport(Alien):
    """Class representing teleporting alien and it's functionalities"""

    animations = {"main": 24}
    animation_images = {}
    multiplier = 8

    def update(self):
        """Animate and move alien pseudorandonly"""
        self.next_frame()

        if not self.frame:
            self.rect.x = randint(0, self.game.settings.screen_width - self.rect.width)
            self.rect.y = randint(
                0, self.game.settings.screen_height - 2 * self.rect.height
            )

        if 7 <= self.frame // self.multiplier <= 11:
            self.shoot()


class AlienShoot(Alien):
    """Class representing shooting alien and its functionalities"""

    animations = {"main": 4}
    animation_images = {}
    multiplier = 16

    def update(self):
        """Prepare next frame of the animation for AlienShoot object, its position and shoot"""
        self.next_frame()

        self.rect.y = max(
            min(
                self.rect.y
                + randint(-1, 1)
                * randint(0, self.game.settings.alien_vertical_speed_factor),
                self.game.settings.screen_height * 2 / 3,
            ),
            0,
        )
        self.rect.x = max(
            min(
                self.rect.x
                + randint(-1, 1)
                * randint(0, int(self.game.settings.alien_horizontal_speed_factor)),
                self.game.settings.screen_width - self.rect.width,
            ),
            0,
        )

        if self.frame // self.multiplier >= 3:
            self.shoot()


class AlienBoss(Alien):
    """Class representing main boss of the game"""

    animations = {
        "main": 6,
        "left_up": 1,
        "left_down": 1,
        "right_up": 1,
        "right_down": 1,
        "shoot": 16,
    }
    animation_images = {}
    multiplier = 8

    def update(self):
        """Prepare next frame of the animation for AlienBoss object and adjust its position"""
        if not self.frame:
            self.choose_animation()

        getattr(self, self.animation)()

        self.next_frame()

    def choose_animation(self):
        """Select next move to execute"""
        self.animation = list(type(self).animations.keys())[
            randint(0, len(type(self).animations) - 1)
        ]

    def main(self):
        """Method without any action for the main animation"""

    def left_up(self):
        """Calculate and move alien towards left upper corner of the screen"""
        current_move = randint(
            0,
            min(
                self.rect.centerx, self.rect.centery, self.game.settings.alien_boss_area
            ),
        )
        self.rect.centerx = max(0, self.rect.centerx - current_move)
        self.rect.centery = max(0, self.rect.centery - current_move)

    def left_down(self):
        """Calculate and move alien towards left lower corner of the screen"""
        current_move = randint(
            0,
            min(
                self.game.settings.screen_width // 4 * 3 - self.rect.centery,
                self.game.settings.alien_boss_area,
            ),
        )
        self.rect.centerx = max(0, self.rect.centerx - current_move)
        self.rect.centery += current_move

    def right_up(self):
        """Calculate and move alien towards right upper corner of the screen"""
        current_move = randint(
            0,
            min(
                self.game.settings.screen_width - self.rect.centerx,
                self.rect.centery,
                self.game.settings.alien_boss_area,
            ),
        )
        self.rect.centerx = max(0, self.rect.centerx + current_move)
        self.rect.centery = max(0, self.rect.centery - current_move)

    def right_down(self):
        """Calculate and move alien towards right lower corner of the screen"""
        current_move = randint(
            0,
            min(
                self.game.settings.screen_width - self.rect.centerx,
                self.game.settings.screen_height // 4 * 3 - self.rect.centery,
                self.game.settings.alien_boss_area,
            ),
        )
        self.rect.centerx = self.rect.centerx + current_move
        self.rect.centery = self.rect.centery + current_move

    def shoot(self):
        """Attack ship"""
        if 5 <= self.frame // self.multiplier <= 9:
            self.game.alien_bullets.add(
                AlienBossBeam(
                    self.game.settings,
                    self.game.screen,
                    self.rect.centerx,
                    self.rect.centery,
                    self.frame // self.multiplier,
                )
            )
            self.game.sounds.play_sound("alien_beam")
        elif self.frame // self.multiplier == 10:
            self.game.alien_bullets.empty()
