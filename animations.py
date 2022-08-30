"""Module designed to handle animations"""

import pygame


class Animation:
    """Class to handle all animation-related tasks"""

    def load_images(self, name, animation, frames, container):
        """Load all required images from source files"""
        container[animation] = []
        for i in range(frames):
            container[animation].append(
                pygame.image.load(f"images/{name}/{animation}/sprite_{i}.png")
            )
