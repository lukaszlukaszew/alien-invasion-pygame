"""Main functions of the game"""

import sys

from random import randint

import pygame
from pygame.sprite import Group
from star import Star


def check_events(ai_settings, screen):
    """Event loop"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                stars = Group()
                create_sky(ai_settings, screen, stars)
                update_screen(ai_settings, screen, stars)


def update_screen(ai_settings, screen, stars):
    """Actions required to screen refresh"""
    screen.fill(ai_settings.bg_color)
    stars.draw(screen)
    pygame.display.flip()


def create_sky(ai_settings, screen, stars):
    """Create full sky of stars"""
    for _ in range(randint(10, 150)):
        create_star(ai_settings, screen, stars)


def create_star(ai_settings, screen, stars):
    """Create star and add it to the sky"""
    star_size = randint(1, 4)
    star_x = randint(0, ai_settings.screen_width)
    star_y = randint(0, ai_settings.screen_height)
    angle = randint(0, 360)
    star = Star(ai_settings, screen, star_size, star_x, star_y, angle)
    stars.add(star)
