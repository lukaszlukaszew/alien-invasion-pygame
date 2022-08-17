"""Main module of the game"""

import sys
import pygame


def run_game():
    """Game initialization and creating window object"""
    pygame.init()
    pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Keyboard check")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()


run_game()

# nice it returns ascii/utf code point every time the key is pressed
