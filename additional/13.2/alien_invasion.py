"""Main module of the game"""

# press space to see the sky

import pygame

from settings import Settings

import game_functions as gf


def run_game():
    """Game initialization and creating window object"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    screen.fill(ai_settings.bg_color)
    pygame.display.set_caption("Stars")

    while True:
        gf.check_events(ai_settings, screen)

run_game()
