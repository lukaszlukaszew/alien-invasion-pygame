"""Module designed to track game score"""

import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """Class dedicated to represent current player score"""

    def __init__(self, settings, screen, stats, game):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.game = game
        self.ships = None

        # font
        self.text_full_health = (0, 255, 0)
        self.text_medium_health = (255, 255, 0)
        self.text_low_health = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.standard_screen = ["score", "high_score", "level"]
        self.end_screen = [
            "title",
            "fired_t",
            "fired_v",
            "hit_t",
            "hit_v",
            "acc_t",
            "acc_v",
            "ships_t",
            "ships_v",
            "kill_t",
            "kill_v",
            "bonus_t",
            "bonus_v",
            "tot_t",
            "tot_v",
            "level_t",
            "level_v",
        ]

        self.rects = {"screen": self.screen.get_rect()}
        self.images = {}

        self.rect_pos = {
            "score": ("right", "screen", "right", -10, "top", "screen", "top", 20),
            "high_score": ("centerx", "screen", "centerx", 0, "top", "score", "top", 0),
            "level": ("right", "screen", "right", -10, "top", "score", "bottom", 10),
            "boss_health": ("left", "screen", "left", 10, "top", "score", "bottom", 10),
            "title": ("centerx", "screen", "centerx", 0, "top", "score", "top", 20),
            "fired_t": ("left", "screen", "left", 20, "top", "title", "bottom", 20),
            "fired_v": ("right", "screen", "right", -20, "top", "title", "bottom", 20),
            "hit_t": ("left", "screen", "left", 20, "top", "fired_t", "bottom", 20),
            "hit_v": ("right", "screen", "right", -20, "top", "fired_t", "bottom", 20),
            "acc_t": ("left", "screen", "left", 20, "top", "hit_t", "bottom", 20),
            "acc_v": ("right", "screen", "right", -20, "top", "hit_t", "bottom", 20),
            "ships_t": ("left", "screen", "left", 20, "top", "acc_t", "bottom", 50),
            "ships_v": ("right", "screen", "right", -20, "top", "acc_t", "bottom", 50),
            "kill_t": ("left", "screen", "left", 20, "top", "ships_t", "bottom", 20),
            "kill_v": ("right", "screen", "right", -20, "top", "ships_t", "bottom", 20),
            "bonus_t": ("left", "screen", "left", 20, "top", "kill_t", "bottom", 20),
            "bonus_v": ("right", "screen", "right", -20, "top", "kill_t", "bottom", 20),
            "tot_t": ("left", "screen", "left", 20, "top", "bonus_t", "bottom", 50),
            "tot_v": ("right", "screen", "right", -20, "top", "bonus_t", "bottom", 50),
            "level_t": ("left", "screen", "left", 20, "top", "tot_t", "bottom", 20),
            "level_v": ("right", "screen", "right", -20, "top", "tot_t", "bottom", 20),
        }

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_boss_health()

    def prepare_rects(self, key):
        """Prepare rect object in correct position based on an image"""
        self.rects[key] = self.images[key].get_rect()

        for i in range(2):
            setattr(
                self.rects[key],
                self.rect_pos[key][4 * i],
                getattr(
                    self.rects[self.rect_pos[key][4 * i + 1]],
                    self.rect_pos[key][4 * i + 2],
                )
                + self.rect_pos[key][4 * i + 3],
            )

    def show_score(self):
        """Show additional information on the screen"""
        if (
                self.stats.level <= self.settings.alien_changes[-1]
                and self.stats.game_active
        ):
            self.standard_screen = ["score", "high_score", "level"]
            if self.stats.level == self.settings.alien_changes[-1]:
                self.standard_screen.append("boss_health")

            for key in self.standard_screen:
                self.screen.blit(self.images[key], self.rects[key])

            self.ships.draw(self.screen)
        else:
            for key in self.end_screen:
                self.screen.blit(self.images[key], self.rects[key])

    def prep_end_screen(self):
        """Transform all end screen info into the on-screen images"""
        # victory or game over
        if self.stats.game_won:
            self.images["title"] = self.font.render(
                "VICTORY!", True, self.settings.text_color
            )
        else:
            self.images["title"] = self.font.render(
                "GAME OVER", True, self.settings.text_color
            )

        # bullets fired
        self.images["fired_t"] = self.font.render(
            "Bullets fired", True, self.settings.text_color
        )
        self.images["fired_v"] = self.font.render(
            str(self.stats.bullets_fired), True, self.settings.text_color
        )

        # bullets hit
        self.images["hit_t"] = self.font.render(
            "Bullets hit", True, self.settings.text_color
        )
        self.images["hit_v"] = self.font.render(
            str(sum(self.stats.hits.values())), True, self.settings.text_color
        )

        # accuracy
        self.images["acc_t"] = self.font.render(
            "Accuracy", True, self.settings.text_color
        )

        try:
            self.images["acc_v"] = self.font.render(
                f"{sum(self.stats.hits.values()) * 100 / self.stats.bullets_fired:.2f} %",
                True,
                self.settings.text_color,
            )
        except ZeroDivisionError:
            self.images["acc_v"] = self.font.render(
                "---", True, self.settings.text_color
            )

        # ships left
        self.images["ships_t"] = self.font.render(
            "Ships left", True, self.settings.text_color
        )
        self.images["ships_v"] = self.font.render(
            str(self.stats.ships_left), True, self.settings.text_color
        )

        # aliens defeated
        self.images["kill_t"] = self.font.render(
            "Aliens defeated", True, self.settings.text_color
        )
        self.images["kill_v"] = self.font.render(
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

        # bonuses used
        self.images["bonus_t"] = self.font.render(
            "Bonuses used", True, self.settings.text_color
        )
        self.images["bonus_v"] = self.font.render(
            str(self.stats.bonuses_used), True, self.settings.text_color
        )

        # total score
        self.images["tot_t"] = self.font.render(
            "Total score", True, self.settings.text_color
        )
        self.images["tot_v"] = self.font.render(
            f"{round(self.stats.score, -1):,}", True, self.settings.text_color
        )

        # level reached
        self.images["level_t"] = self.font.render(
            "Level reached", True, self.settings.text_color
        )
        self.images["level_v"] = self.font.render(
            str(self.stats.level), True, self.settings.text_color
        )
        for key in self.end_screen:
            self.prepare_rects(key)

    def prep_score(self):
        """Transform score into the on-screen image"""
        score_str = f"{int(self.stats.score):,}"

        self.images["score"] = self.font.render(score_str, True, self.settings.text_color)
        self.prepare_rects("score")

    def prep_high_score(self):
        """Transform high-score into the on-screen image"""
        high_score_str = f"{int(self.stats.high_score):,}"

        self.images["high_score"] = self.font.render(
            high_score_str, True, self.settings.text_color
        )
        self.prepare_rects("high_score")

    def prep_level(self):
        """Transform level info into the on-screen image"""
        self.images["level"] = self.font.render(
            str(self.stats.level), True, self.settings.text_color
        )

        self.prepare_rects("level")

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

        self.images["boss_health"] = self.font.render(
            "BOSS: " + str(self.settings.alien_boss_life), True, color
        )
        self.prepare_rects("boss_health")

    def prep_ships(self):
        """Prepare images representing remaining ships"""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
