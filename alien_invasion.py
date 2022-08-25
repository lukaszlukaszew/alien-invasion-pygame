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
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")

    play_button = Button(screen, "Play")

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stats = GameStats(ai_settings)
    score_board = Scoreboard(ai_settings, screen, stats)

    gf.create_fleet(ai_settings, screen, ship, aliens)

    clock = pygame.time.Clock()

    while True:
        gf.check_events(
            ai_settings, screen, stats, score_board, play_button, ship, aliens, bullets
        )

        if stats.game_active:
            ship.update()
            gf.update_bullets(
                ai_settings, screen, stats, score_board, ship, aliens, bullets
            )
            gf.update_aliens(
                ai_settings, stats, score_board, screen, ship, aliens, bullets
            )

        gf.update_screen(
            ai_settings, screen, stats, score_board, ship, aliens, bullets, play_button
        )

        clock.tick(60)

run_game()
