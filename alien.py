"""Module containing all aliens features and behaviours"""

from random import randint

from pygame.sprite import Sprite

from animations import Animation


class Alien(Sprite, Animation):
    """Super class for all alien types"""

    animations = {}

    def __init__(self, settings, screen):
        """Initialization of basic instance attributes"""
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = None
        self.frames = 1
        self.frame = 1
        self.multiplier = 1
        self.rect = None

    def check_edges(self):
        """Returns true if alien is at hhe edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= 0:
            return True

    def blitme(self):
        """Show alien in its current position"""
        self.screen.blit(self.image, self.rect)

    def prepare_images(self):
        """Prepare all needed images for aliens"""
        self.load_images(str(self), type(self).__name__, self.frames, Alien.animations)

        self.frame = randint(
            0, (len(Alien.animations[type(self).__name__]) - 1) * self.multiplier
        )

        self.image = Alien.animations[type(self).__name__][
            self.frame // self.multiplier
        ]

        self.rect = self.image.get_rect()
        self.place_alien_on_screen()

    def place_alien_on_screen(self):
        """Select starting position for image"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def __str__(self):
        return "alien"

    def update(self):
        """Animate and move alien to the left or to the right"""
        if (
            self.frame
            >= (len(Alien.animations[type(self).__name__]) - 1) * self.multiplier
        ):
            self.frame = 0
        self.frame += 1
        self.image = Alien.animations[type(self).__name__][
            self.frame // self.multiplier
        ]
        self.rect.x += self.settings.alien_speed_factor * self.settings.fleet_direction


class AlienUFO(Alien):
    """Class representing UFO-type of alien and it's functionalities"""

    def __init__(self, settings, screen):
        super().__init__(settings, screen)
        self.multiplier = 12
        self.frames = 9

        self.prepare_images()


class AlienTentacle(Alien):
    """Class representing alien with tentacles and it's functionalities"""

    def __init__(self, settings, screen):
        super().__init__(settings, screen)
        self.multiplier = 18
        self.frames = 6

        self.prepare_images()
