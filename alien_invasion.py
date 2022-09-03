"""Main module of the game"""

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf


def run_game():
    """Game initialization and creating window object"""
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    play_button = Button(screen, "Play")

    ship = Ship(settings, screen)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    stats = GameStats(settings)
    scoreboard = Scoreboard(settings, screen, stats)

    gf.create_fleet(settings, screen, stats, ship, aliens, alien_bullets)

    clock = pygame.time.Clock()

    while True:
        gf.check_events(
            settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, alien_bullets
        )

        if stats.game_active:
            ship.update()
            gf.update_bullets(
                settings, screen, stats, scoreboard, ship, aliens, bullets, alien_bullets
            )
            gf.update_aliens(
                settings, stats, scoreboard, screen, ship, aliens, bullets, alien_bullets
            )

        gf.update_screen(
            settings, screen, stats, scoreboard, ship, aliens, bullets, play_button, alien_bullets
        )

        clock.tick(60)


run_game()
