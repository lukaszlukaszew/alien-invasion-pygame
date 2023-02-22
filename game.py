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
        """Create game object with required: scoreboard, stats and settings, clock. Create ship and
        objects groups to handle elements of the screen. Prepare screen and refresh rate."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.load_logo_image()
        self.logo_rect.centery = self.settings.screen_height // 2
        self.logo_rect.centerx = self.settings.screen_width // 2

        self.load_background_image()
        self.background_rect.centery = self.settings.screen_height // 2
        self.background_rect.centerx = self.settings.screen_width // 2

        self.stats = GameStats(self.settings)
        self.scoreboard = Scoreboard(self.settings, self.screen, self.stats)
        self.play_button = Button(self.screen, "Play")

        self.ship = Ship(self.settings, self.screen, self.background_rect.centerx)

        self.bullets = Group()
        self.alien_bullets = Group()
        self.aliens = Group()
        self.bonuses = Group()
        self.explosions = Group()
        self.active_bonuses = {}

        self.clock = pygame.time.Clock()

        self.run_game()

    def run_game(self):
        """Start of the main loop of the game"""
        pygame.display.set_caption("Alien Invasion")
        gf.create_fleet(self)

        while True:
            gf.check_events(self)

            if self.stats.game_not_paused:
                if self.stats.game_active:
                    self.background_rect.centerx = self.ship.update()
                    gf.update_bullets(self)
                    gf.update_aliens(self)
                    gf.update_bonuses(self)

            gf.update_explosions(self)
            gf.update_screen(self)

            self.clock.tick(60)

    def load_logo_image(self):
        """Load proper imaage for the logo"""
        self.logo_image = pygame.image.load("images/logo/logo.png")
        self.logo_rect = self.logo_image.get_rect()

    def logo_blitme(self):
        """Show logo on the screen in its current position"""
        self.screen.blit(self.logo_image, self.logo_rect)

    def load_background_image(self):
        """Load proper imaage for the background"""
        self.background_image = pygame.image.load("images/background/background.jpg")
        self.background_rect = self.background_image.get_rect()

    def background_blitme(self):
        """Show bakground on the screen in its current position"""
        self.screen.blit(self.background_image, self.background_rect)
