"""Main module of the game"""

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf


class Game:
    """Main class of the game"""

    def __init__(self):
        """Create game object with required: scoreboard, stats and settings, clock. Create ship and objects groups to
        handle elements of the screen. Prepare screen and refresh rate."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )

        self.stats = GameStats(self.settings)
        self.scoreboard = Scoreboard(self.settings, self.screen, self.stats)
        self.play_button = Button(self.screen, "Play")

        self.ship = Ship(self.settings, self.screen)

        self.bullets = Group()
        self.alien_bullets = Group()
        self.aliens = Group()

        self.clock = pygame.time.Clock()

        self.run_game()

    def run_game(self):
        """Start of the main loop of the game"""
        pygame.display.set_caption("Alien Invasion")
        gf.create_fleet(self)

        while True:
            gf.check_events(self)

            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self)
                gf.update_aliens(self)

            gf.update_screen(self)

            self.clock.tick(60)
