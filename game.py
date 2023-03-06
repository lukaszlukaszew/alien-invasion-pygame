"""Main module of the game"""

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sounds import SoundMixer

import functions as gf


class Game:
    """Main class of the game combined with all required features"""

    def __init__(self):
        self.image = None
        self.image_rect = None

        pygame.init()

        self.clock = pygame.time.Clock()
        self.sounds = SoundMixer()

        self.settings = Settings()
        self.stats = GameStats(self.settings)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.scoreboard = Scoreboard(self.settings, self.screen, self.stats, self)

        # create containers
        self.bullets = Group()
        self.alien_bullets = Group()
        self.aliens = Group()
        self.bonuses = Group()
        self.explosions = Group()
        self.active_bonuses = {}

        self.ship = Ship(self)

        self.prepare_background_image("logo")
        self.play_button = Button(self, "Play")

        self.run_game()

    def run_game(self):
        """Start the main loop of the game"""
        pygame.display.set_caption("Alien Invasion")
        self.sounds.play_sound("menu_start", -1)

        while True:
            gf.check_events(self)

            if self.stats.game_not_paused:
                if self.stats.game_active:
                    self.ship.update()
                    gf.update_bullets(self)
                    gf.update_aliens(self)
                    gf.update_bonuses(self)

                gf.check_ship_movement(self)
                gf.update_explosions(self)

                gf.update_screen(self)

            self.clock.tick(60)

    def prepare_background_image(self, image):
        """Load proper imaage for the logo"""
        if image == "logo":
            self.image = pygame.image.load(f"images/Background/{image}.png")
        else:
            self.image = pygame.image.load(f"images/Background/{image}.jpg")

        self.image_rect = self.image.get_rect()
        self.image_rect.centery = self.settings.screen_height // 2
        self.image_rect.centerx = self.settings.screen_width // 2

    def background_image_blitme(self):
        """Show logo on the screen in its current position"""
        self.screen.blit(self.image, self.image_rect)
