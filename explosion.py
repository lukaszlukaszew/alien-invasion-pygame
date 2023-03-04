"""Module containing behaviour of the explosion effect"""

from pygame.sprite import Sprite

from animations import Animation


class Boom(Animation, Sprite):
    """Basic class of explosion effect"""

    animations = {"main": 11}
    animation_images = {}
    multiplier = 2
    starting_frame = 0

    def __init__(self, game, pos_x, pos_y):
        super().__init__("main")
        self.screen = game.screen
        self.animation = "main"

        self.rect.centerx = pos_x
        self.rect.centery = pos_y

        game.sounds.play_sound(type(self).__name__)

    def update(self):
        """Prepare next frame of animation for explosion effect"""
        self.next_frame()
