"""Module designed to track game score"""

import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """Class dedicated to represent current player score"""

    def __init__(self, settings, screen, stats, game):
        """Create score attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.game = game

        # font
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
        if (
            self.stats.level <= self.settings.alien_changes[-1]
            and self.stats.game_active
        ):
            self.screen.blit(self.score_image, self.score_rect)
            self.screen.blit(self.high_score_image, self.high_score_rect)
            self.screen.blit(self.level_image, self.level_rect)
            if self.stats.level == self.settings.alien_changes[-1]:
                self.screen.blit(self.boss_health_image, self.boss_health_rect)

            self.ships.draw(self.screen)
        else:
            self.screen.blit(self.title_image, self.title_rect)
            self.screen.blit(self.bullets_fired_txt_image, self.bullets_fired_txt_rect)
            self.screen.blit(self.bullets_fired_image, self.bullets_fired_rect)
            self.screen.blit(self.bullets_hit_txt_image, self.bullets_hit_txt_rect)
            self.screen.blit(self.bullets_hit_image, self.bullets_hit_rect)
            self.screen.blit(self.accuracy_txt_image, self.accuracy_txt_rect)
            self.screen.blit(self.accuracy_image, self.accuracy_rect)
            self.screen.blit(self.ships_left_txt_image, self.ships_left_txt_rect)
            self.screen.blit(self.ships_left_image, self.ships_left_rect)
            self.screen.blit(
                self.aliens_defeated_txt_image, self.aliens_defeated_txt_rect
            )
            self.screen.blit(self.aliens_defeated_image, self.aliens_defeated_rect)
            self.screen.blit(self.bonuses_used_txt_image, self.bonuses_used_txt_rect)
            self.screen.blit(self.bonuses_used_image, self.bonuses_used_rect)
            self.screen.blit(self.total_score_txt_image, self.total_score_txt_rect)
            self.screen.blit(self.total_score_image, self.total_score_rect)
            self.screen.blit(self.level_reached_txt_image, self.level_reached_txt_rect)
            self.screen.blit(self.level_reached_image, self.level_reached_rect)

    def prep_score(self):
        """Transform score into the on-screen image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"

        self.score_image = self.font.render(score_str, True, self.settings.text_color)
        self.score_rect = self.score_image.get_rect()

        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 20

    def prep_high_score(self):
        """Transform high-score into the on-screen image"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = f"{rounded_high_score:,}"

        self.high_score_image = self.font.render(
            high_score_str, True, self.settings.text_color
        )
        self.high_score_rect = self.high_score_image.get_rect()

        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Transform level info into the on-screen image"""
        self.level_image = self.font.render(
            str(self.stats.level), True, self.settings.text_color
        )
        self.level_rect = self.level_image.get_rect()

        self.level_rect.right = self.screen_rect.right - 10
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Prepare images representing remaining ships"""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_boss_health(self):
        """Transform boss health amount into the on-screen image"""

        if (
            self.settings.alien_boss_life
            > self.settings.starting_alien_boss_life // 3 * 2
        ):
            color = self.text_full_health
        elif (
            self.settings.alien_boss_life > self.settings.starting_alien_boss_life // 3
        ):
            color = self.text_medium_health
        else:
            color = self.text_low_health

        self.boss_health_image = self.font.render(
            "BOSS: " + str(self.settings.alien_boss_life), True, color
        )
        self.boss_health_rect = self.boss_health_image.get_rect()

        self.boss_health_rect.left = 10
        self.boss_health_rect.top = self.score_rect.bottom + 10

    def prep_end_screen(self):
        """Transform all end screen info into the on-screen images"""
        # victory or game over

        if self.stats.game_won:
            self.title_image = self.font.render(
                "VICTORY!", True, self.settings.text_color
            )
        else:
            self.title_image = self.font.render(
                "GAME OVER", True, self.settings.text_color
            )

        self.title_rect = self.title_image.get_rect()

        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = self.score_rect.top + 20

        # bullets fired - txt
        self.bullets_fired_txt_image = self.font.render(
            "Bullets fired", True, self.settings.text_color
        )
        self.bullets_fired_txt_rect = self.bullets_fired_txt_image.get_rect()

        self.bullets_fired_txt_rect.left = self.screen_rect.left + 20
        self.bullets_fired_txt_rect.top = self.title_rect.bottom + 20

        # bullets fired - value

        self.bullets_fired_image = self.font.render(
            str(self.stats.bullets_fired), True, self.settings.text_color
        )
        self.bullets_fired_rect = self.bullets_fired_image.get_rect()

        self.bullets_fired_rect.right = self.screen_rect.right - 20
        self.bullets_fired_rect.top = self.title_rect.bottom + 20

        # bullets hit - txt
        self.bullets_hit_txt_image = self.font.render(
            "Bullets hit", True, self.settings.text_color
        )
        self.bullets_hit_txt_rect = self.bullets_hit_txt_image.get_rect()

        self.bullets_hit_txt_rect.left = self.screen_rect.left + 20
        self.bullets_hit_txt_rect.top = self.bullets_fired_rect.bottom + 20

        # bullets hit - value

        self.bullets_hit_image = self.font.render(
            str(sum(self.stats.hits.values())), True, self.settings.text_color
        )
        self.bullets_hit_rect = self.bullets_hit_image.get_rect()

        self.bullets_hit_rect.right = self.screen_rect.right - 20
        self.bullets_hit_rect.top = self.bullets_fired_rect.bottom + 20

        # accuracy - txt
        self.accuracy_txt_image = self.font.render(
            "Accuracy", True, self.settings.text_color
        )
        self.accuracy_txt_rect = self.accuracy_txt_image.get_rect()

        self.accuracy_txt_rect.left = self.screen_rect.left + 20
        self.accuracy_txt_rect.top = self.bullets_hit_rect.bottom + 20

        # accuracy - value
        try:
            self.accuracy_image = self.font.render(
                f"{sum(self.stats.hits.values()) * 100 / self.stats.bullets_fired:.2f} %",
                True,
                self.settings.text_color,
            )
        except ZeroDivisionError:
            self.accuracy_image = self.font.render(
                "---", True, self.settings.text_color
            )

        self.accuracy_rect = self.accuracy_image.get_rect()

        self.accuracy_rect.right = self.screen_rect.right - 20
        self.accuracy_rect.top = self.bullets_hit_rect.bottom + 20

        # ships left - txt
        self.ships_left_txt_image = self.font.render(
            "Ships left", True, self.settings.text_color
        )
        self.ships_left_txt_rect = self.ships_left_txt_image.get_rect()

        self.ships_left_txt_rect.left = self.screen_rect.left + 20
        self.ships_left_txt_rect.top = self.accuracy_rect.bottom + 50

        # ships left - value

        self.ships_left_image = self.font.render(
            str(self.stats.ships_left), True, self.settings.text_color
        )
        self.ships_left_rect = self.ships_left_image.get_rect()

        self.ships_left_rect.right = self.screen_rect.right - 20
        self.ships_left_rect.top = self.accuracy_rect.bottom + 50

        # aliens defeated - txt
        self.aliens_defeated_txt_image = self.font.render(
            "Aliens defeated", True, self.settings.text_color
        )
        self.aliens_defeated_txt_rect = self.aliens_defeated_txt_image.get_rect()

        self.aliens_defeated_txt_rect.left = self.screen_rect.left + 20
        self.aliens_defeated_txt_rect.top = self.ships_left_rect.bottom + 20

        # aliens defeated - value

        self.aliens_defeated_image = self.font.render(
            str(
                sum(self.stats.hits.values())
                + int(
                    self.stats.hits[self.settings.alien_changes[-1]]
                    >= self.settings.starting_alien_boss_life
                )
                - self.stats.hits[self.settings.alien_changes[-1]]
            ),
            True,
            self.settings.text_color,
        )
        self.aliens_defeated_rect = self.aliens_defeated_image.get_rect()

        self.aliens_defeated_rect.right = self.screen_rect.right - 20
        self.aliens_defeated_rect.top = self.ships_left_rect.bottom + 20

        # bonuses used - txt
        self.bonuses_used_txt_image = self.font.render(
            "Bonuses used", True, self.settings.text_color
        )
        self.bonuses_used_txt_rect = self.bonuses_used_txt_image.get_rect()

        self.bonuses_used_txt_rect.left = self.screen_rect.left + 20
        self.bonuses_used_txt_rect.top = self.aliens_defeated_rect.bottom + 20

        # bonuses used - value

        self.bonuses_used_image = self.font.render(
            str(self.stats.bonuses_used), True, self.settings.text_color
        )
        self.bonuses_used_rect = self.bonuses_used_image.get_rect()

        self.bonuses_used_rect.right = self.screen_rect.right - 20
        self.bonuses_used_rect.top = self.aliens_defeated_rect.bottom + 20

        # total score - txt
        self.total_score_txt_image = self.font.render(
            "Total score", True, self.settings.text_color
        )
        self.total_score_txt_rect = self.total_score_txt_image.get_rect()

        self.total_score_txt_rect.left = self.screen_rect.left + 20
        self.total_score_txt_rect.top = self.bonuses_used_rect.bottom + 50

        # total score - value

        self.total_score_image = self.font.render(
            f"{round(self.stats.score, -1):,}", True, self.settings.text_color
        )
        self.total_score_rect = self.total_score_image.get_rect()

        self.total_score_rect.right = self.screen_rect.right - 20
        self.total_score_rect.top = self.bonuses_used_rect.bottom + 50

        # level reached - txt
        self.level_reached_txt_image = self.font.render(
            "Level reached", True, self.settings.text_color
        )
        self.level_reached_txt_rect = self.level_reached_txt_image.get_rect()

        self.level_reached_txt_rect.left = self.screen_rect.left + 20
        self.level_reached_txt_rect.top = self.total_score_rect.bottom + 20

        # level reached - value

        self.level_reached_image = self.font.render(
            str(self.stats.level), True, self.settings.text_color
        )
        self.level_reached_rect = self.level_reached_image.get_rect()

        self.level_reached_rect.right = self.screen_rect.right - 20
        self.level_reached_rect.top = self.total_score_rect.bottom + 20
