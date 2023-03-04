"""Module designed to handle animations"""

import pygame


class Animation:
    """Class to handle all animation-related tasks"""

    animations = {}
    animation_images = {}
    multiplier = 1
    starting_frame = 1

    def __init__(self, animation):
        super().__init__()
        self.frame = type(self).starting_frame
        self.multiplier = type(self).multiplier
        self.animation = animation
        self.image = None
        self.rect = None
        self.screen = None

        self.load_images()
        self.set_image()

    def load_images(self):
        """Load all required images from source files"""
        main_folder = type(self).__name__.rstrip("0123456789")
        for animation, frames in type(self).animations.items():
            if not type(self).animation_images.get(animation):
                type(self).animation_images[animation] = []
                for i in range(frames):
                    type(self).animation_images[animation].append(
                        pygame.image.load(
                            f"images/{main_folder}/{animation}/sprite_{i}.png"
                        )
                    )

    def set_image(self):
        """Set begining image for an object"""
        self.image = type(self).animation_images[self.animation][
            self.frame // self.multiplier
        ]
        self.rect = self.image.get_rect()

    def blitme(self):
        """Show image in its current position"""
        self.screen.blit(self.image, self.rect)

    def next_frame(self):
        """Prepare image for next frame"""
        self.frame = int(
            (self.frame + 1) % (type(self).animations[self.animation] * self.multiplier)
        )
        self.image = type(self).animation_images[self.animation][
            self.frame // self.multiplier
        ]
