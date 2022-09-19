"""Module containing all aliens features and behaviours"""

from random import randint

from pygame.sprite import Sprite

from animations import Animation
from bullet import AlienBullet


class Alien(Sprite, Animation):
    """Super class for all alien types"""

    animations = {}

    def __init__(self, settings, screen, group):
        """Initialization of basic instance attributes"""
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = None
        self.frames = 1
        self.frame = 1
        self.multiplier = 1
        self.rect = None
        self.x = None
        self.bullet_group = group

    def check_edges(self):
        """Returns true if alien is at hhe edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True
        return False

    def blitme(self):
        """Show alien in its current position"""
        self.screen.blit(self.image, self.rect)

    def prepare_images(self):
        """Prepare all needed images for aliens"""
        self.load_images(str(self), type(self).__name__, self.frames, Alien.animations)

        self.frame = randint(
            0, len(Alien.animations[type(self).__name__]) * self.multiplier - 1
        )

        self.image = Alien.animations[type(self).__name__][
            self.frame // self.multiplier
        ]

        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

        self.place_alien_on_screen()

    def place_alien_on_screen(self):
        """Select starting position for image"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def __str__(self):
        return "alien"

    def update(self):
        """Animate and move alien to the left or to the right"""
        self.frame = int(
            (self.frame + 1)
            % len(Alien.animations[type(self).__name__] * self.multiplier)
        )
        self.image = Alien.animations[type(self).__name__][
            self.frame // self.multiplier
        ]

        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x


class AlienUFO(Alien):
    """Class representing UFO-type of alien and its functionalities"""

    def __init__(self, settings, screen, group):
        super().__init__(settings, screen, group)
        self.multiplier = 12
        self.frames = 9

        self.prepare_images()


class AlienTentacle(Alien):
    """Class representing alien with tentacles and its functionalities"""

    def __init__(self, settings, screen, group):
        super().__init__(settings, screen, group)
        self.multiplier = 18
        self.frames = 6

        self.prepare_images()

    def update(self):
        """Animate and move alien to the left or to the right"""
        self.frame = int(
            (self.frame + 1)
            % len(Alien.animations[type(self).__name__] * self.multiplier)
        )
        self.image = Alien.animations[type(self).__name__][
            self.frame // self.multiplier
        ]

        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x

        screen_rect = self.screen.get_rect()

        if self.rect.centerx >= screen_rect.centerx:
            self.rect.y -= self.settings.fleet_direction
        else:
            self.rect.y += self.settings.fleet_direction


class AlienShoot(Alien):
    """Class representing shooting alien and its functionalities"""

    def __init__(self, settings, screen, group):
        super().__init__(settings, screen, group)
        self.multiplier = 16
        self.frames = 4

        self.prepare_images()

    def update(self):
        """Animate and move alien pseudorandomly"""
        self.frame = int(
            (self.frame + 1)
            % len(Alien.animations[type(self).__name__] * self.multiplier)
        )
        self.image = Alien.animations[type(self).__name__][
            self.frame // self.multiplier
        ]
        self.rect.y = max(
            min(
                self.rect.y + randint(-1, 1) * randint(1, 3),
                self.settings.screen_height * 2 / 3,
            ),
            0,
        )
        self.rect.x = max(
            min(
                self.rect.x + randint(-1, 1) * randint(1, 3),
                self.settings.screen_width - self.rect.width,
            ),
            0,
        )
        self.shoot()

    def shoot(self):
        """Attack ship"""
        if randint(0, 1000) > 999:
            self.bullet_group.add(
                AlienBullet(
                    self.settings, self.screen, self.rect.centerx, self.rect.centery
                )
            )


class AlienTeleport(Alien):
    """Class representing teleporting alien and it's functionalities"""

    def __init__(self, settings, screen, group):
        super().__init__(settings, screen, group)
        self.multiplier = 8
        self.frames = 24

        self.prepare_images()

    def update(self):
        """Animate and move alien pseudorandonly"""
        self.frame = int(
            (self.frame + 1)
            % len(Alien.animations[type(self).__name__] * self.multiplier)
        )
        self.image = Alien.animations[type(self).__name__][
            self.frame // self.multiplier
        ]

        if not self.frame:
            self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
            self.rect.y = randint(0, self.settings.screen_height - 2 * self.rect.height)

        if 7 <= self.frame <= 11:
            self.shoot()

    def shoot(self):
        """Attack ship"""
        if randint(0, 1000) > 950:
            self.bullet_group.add(
                AlienBullet(
                    self.settings, self.screen, self.rect.centerx, self.rect.centery
                )
            )
