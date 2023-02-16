"""Module designed to track game score"""

import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """Class dedicated to represent current player score"""

    def __init__(self, settings, screen, stats):
        """Create score attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # font
        self.text_color = (30, 30, 30)
        self.text_full_health = (0, 255, 0)
        self.text_medium_health = (255, 255, 0)
        self.text_low_health = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

        self.prep_boss_health()

    def show_score(self):
        """Show additional information on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        if self.stats.level == self.settings.alien_changes[-1]:
            self.screen.blit(self.boss_health_image, self.boss_health_rect)
        self.ships.draw(self.screen)

    def prep_score(self):
        """Transform score into the on-screen image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"

        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()

        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 20

    def prep_high_score(self):
        """Transform high-score into the on-screen image"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = f"{rounded_high_score:,}"

        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()

        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Transform level info into the on-screen image"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color)
        self.level_rect = self.level_image.get_rect()

        self.level_rect.right = self.screen_rect.right - 10
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Prepare images representing remaining ships"""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_boss_health(self):
        """Transform boss health amount into the on-screen image"""
        color = ()
        if self.settings.alien_boss_life > 35:
            color = self.text_full_health
        elif self.settings.alien_boss_life > 20:
            color = self.text_medium_health
        else:
            color = self.text_low_health

        self.boss_health_image = self.font.render("BOSS: " + str(self.settings.alien_boss_life), True, color)
        self.boss_health_rect = self.boss_health_image.get_rect()

        self.boss_health_rect.left = 10
        self.boss_health_rect.top = self.score_rect.bottom + 10
