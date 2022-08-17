"""Main functions of the game"""

import sys

import pygame


def check_events():
    """Event loop"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def update_screen(ai_settings, screen, ship):
    """Actions required to screen refresh"""
    screen.fill(ai_settings.bg_color)
    ship.blitme()

    pygame.display.flip()
